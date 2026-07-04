#!/usr/bin/env python3
"""
Генератор README из data/tools.yml.

Читает единый источник правды (data/tools.yml), группирует утилиты по категориям
и рендерит двуязычные README.md (EN) и README.ru.md (RU). Бейджи числа звёзд —
через shields.io, обновляемые отдельным GitHub Action (см. .github/workflows/update-stars.yml).

Использование:
    python scripts/generate_readme.py

PR от сообщества сводится к правке одной записи в tools.yml и перегенерации.
"""
from __future__ import annotations

import datetime
import re
import sys
import unicodedata
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML не найден. Установите: pip install pyyaml")

# Импортируем общие функции. Скрипты лежат в той же директории (scripts/),
# поэтому добавляем её в sys.path при запуске как `python scripts/generate_readme.py`.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import github_slug, load_json_or_default  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TOOLS_YML = ROOT / "data" / "tools.yml"
STARS_FILE = ROOT / "data" / "stars.json"  # кэш звёзд от update-stars.py (опционален)
HISTORY_FILE = ROOT / "data" / "stars-history.json"  # срезы 1d/7d для дельт
META_FILE = ROOT / "data" / "repos-meta.json"  # метаданные (createdAt и т.п.) от update-stars

# Порядок и подписи категорий. Каждый ключ должен совпадать со значениями
# поля `category` в tools.yml.
CATEGORIES = [
    ("cli-agents", {
        "title_en": "AI Coding Agents and CLI",
        "title_ru": "AI-агенты кодинга и CLI",
        "title_zh": "AI 编程代理与 CLI",
    }),
    ("editor-integrations", {
        "title_en": "Editor Integrations",
        "title_ru": "Интеграции в редакторы",
        "title_zh": "编辑器集成",
    }),
    ("context-memory", {
        "title_en": "Context and Memory",
        "title_ru": "Контекст и память",
        "title_zh": "上下文与记忆",
    }),
    ("prompt-mcp", {
        "title_en": "Prompts and MCP",
        "title_ru": "Промпты и MCP",
        "title_zh": "提示词与 MCP",
    }),
    ("observability-eval", {
        "title_en": "Observability and Eval",
        "title_ru": "Наблюдаемость и оценка",
        "title_zh": "可观测性与评估",
    }),
    ("workflow-automation", {
        "title_en": "Workflow and Automation",
        "title_ru": "Воркфлоу и автоматизация",
        "title_zh": "工作流与自动化",
    }),
    ("learning", {
        "title_en": "Learning and Resources",
        "title_ru": "Обучение и ресурсы",
        "title_zh": "学习与资源",
    }),
    ("other", {
        "title_en": "Other and Adjacent",
        "title_ru": "Прочее и смежное",
        "title_zh": "其他及相关",
    }),
]
CATEGORY_MAP = {key: meta for key, meta in CATEGORIES}

OWNER_REPO_TEMPLATE = "https://github.com/{owner}/{repo}"
SHIELDS_STARS = "https://img.shields.io/github/stars/{owner}/{repo}?style=flat&color=yellow"

NEW_DAYS = 14  # [new] если добавлено ≤ N дней назад (поле added)

# Окна выбора «репо дня/недели» (ключ → дней назад). Единый контракт:
# update_stars.HISTORY_DAYS должен покрывать max(FEATURED_WINDOWS.values())+1.
FEATURED_WINDOWS = {"day": 1, "week": 7}


def load_tools(tools_yml: Path = TOOLS_YML) -> list[dict]:
    """Загружает и валидирует утилиты из YAML."""
    with tools_yml.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    tools = data.get("tools", []) if isinstance(data, dict) else (data or [])
    for t in tools:
        if not all(t.get(k) for k in ("name", "url", "category", "description")):
            raise ValueError(f"Неполная запись: {t}")
        if t["category"] not in CATEGORY_MAP:
            raise ValueError(f"Неизвестная категория '{t['category']}' у {t['name']}")
        for lang in ("en", "ru"):
            if lang not in t["description"]:
                raise ValueError(f"Нет описания '{lang}' у {t['name']}")
    return tools


def load_stars(stars_file: Path = STARS_FILE) -> dict[str, int]:
    """Загружает кэш звёзд (url -> stars), если он есть."""
    return load_json_or_default(stars_file, {}) or {}


def load_history(history_file: Path = HISTORY_FILE) -> dict[str, dict]:
    """Загружает dated-срезы звёзд {url: {"YYYY-MM-DD": stars}}, если есть."""
    return load_json_or_default(history_file, {}) or {}


def _delta(cur, history: dict, days_ago: int) -> int | None:
    """Дельта cur vs среза за days_ago дней назад. None если среза нет."""
    target = (datetime.date.today() - datetime.timedelta(days=days_ago)).isoformat()
    snap = history.get(target)
    if not isinstance(snap, int):
        return None
    return cur - snap


def pick_featured(tools: list[dict], stars: dict[str, int],
                  history: dict[str, dict]) -> dict[str, set[str]]:
    """Выбирает репо дня (макс. дельта за 1д) и недели (за 7д).

    history: {url: {"YYYY-MM-DD": stars}}. Возвращает {url: {"day"} | {"week"}}.
    Если истории нет или все дельты ≤ 0 — пустой dict (блок не рендерится).
    """
    featured: dict[str, set[str]] = {}
    for kind, days_ago in FEATURED_WINDOWS.items():
        # Максимум (дельта, url) среди репо с положительной дельтой за окно.
        best = None
        for t in tools:
            cur = stars.get(t["url"])
            if cur is None:
                continue
            d = _delta(cur, history.get(t["url"], {}), days_ago)
            if d is not None and d > 0 and (best is None or d > best[0]):
                best = (d, t["url"])
        if best:
            featured.setdefault(best[1], set()).add(kind)
    return featured


def render_featured(featured: dict[str, set[str]], tools_by_url: dict[str, dict], lang: str) -> str:
    """Рендерит блок «Repo of the day / Repo of the week» вверху README.

    Пустая строка, если нет ни дня, ни недели. Идёт по FEATURED_WINDOWS,
    чтобы порядок и состав меток были единым источником.
    """
    # URL для каждой метки из featured (если есть).
    urls = {kind: next((u for u, m in featured.items() if kind in m), None)
            for kind in FEATURED_WINDOWS}
    if not any(urls.values()):
        return ""
    labels = {
        ("en", "day"): "Repo of the day",
        ("en", "week"): "Repo of the week",
        ("ru", "day"): "Репозиторий дня",
        ("ru", "week"): "Репозиторий недели",
    }
    lines = []
    for kind, url in urls.items():
        if not url:
            continue
        t = tools_by_url.get(url)
        if not t:
            continue
        # Anchor #featured отличает ссылку от её вхождения в категории:
        # тот же репо легитимно показан дважды (блок Featured + своя категория),
        # и без различия remark-lint:double-link считает это дублем.
        # stripHash:false правила → URL'ы с разным hash формально различны.
        featured_url = f"{url}#featured"
        lines.append(f"{labels[(lang, kind)]}: [{t['name']}]({featured_url}) — {t['description'][lang]}")
    if not lines:
        return ""
    heading = "## Featured" if lang == "en" else "## Избранное"
    return heading + "\n\n" + "\n".join(lines) + "\n\n"


def _is_emoji(c: str) -> bool:
    """True, если символ — эмодзи/символ (ломают awesome-list-item формат).

    Учитываем Unicode-категории So (символы), Sk (модификаторы), а также
    variation-selector U+FE0F и private-use/суррогаты в верхних плоскостях.
    """
    if c == "️":  # emoji variation selector
        return True
    cat = unicodedata.category(c)
    if cat.startswith(("So", "Sk")):
        return True
    return cat in ("Co", "Cn") and ord(c) > 0x2000


def is_new(tool: dict, today=None) -> bool:
    """[new] если репо создано за последние NEW_DAYS дней.

    Дата берётся из created_at (ISO-datetime из repos-meta, поле GitHub API);
    для совместимости принимает и устаревшее поле added. Толерантна к
    отсутствию/битому значению. today — для детерминированности в тестах.
    """
    raw = tool.get("created_at") or tool.get("added")
    if not raw:
        return False
    today = today or datetime.date.today()
    # created_at — ISO datetime ('2024-01-15T...'); берём дату до 'T'.
    date_part = str(raw)[:10]
    try:
        d = datetime.date.fromisoformat(date_part)
    except ValueError:
        return False
    age = (today - d).days
    return 0 <= age <= NEW_DAYS


def render_line(tool: dict, lang: str, stars: int = 0, marks: set[str] | None = None) -> str:
    """Рендит одну строку списка в каноническом формате awesome-lint:

        - [Name](url) <badge> - Description.

    stars/marks не выводятся в строке (awesome-lint диктует строгий формат);
    stars влияют только на сортировку (group_by_category), new/day/week
    вычисляются и используются блоком Featured, но не инлайн-метками.
    """
    del stars, marks  # не используются в выводе; в сигнатуре для совместимости
    name = tool["name"]
    url = tool["url"]
    # Очищаем описание: убираем эмодзи (ломают awesome-list-item), экранируем '['
    # (иначе markdown воспринимает как ссылку-определение), убираем ведущий '#',
    # тримим точку/пробелы, капитализируем первое слово (требование awesome-lint).
    raw = tool["description"][lang]
    desc = "".join(c for c in raw if not _is_emoji(c))
    desc = desc.replace("[", "\\[").strip().lstrip("#").strip()
    desc = desc.strip("—-").strip().rstrip(". ")
    if desc:
        desc = desc[0].upper() + desc[1:]

    # shields.io бейдж актуального числа звёзд.
    slug = github_slug(url)
    badge = ""
    if slug:
        owner, repo = slug
        badge = f" ![]({SHIELDS_STARS.format(owner=owner, repo=repo)}) "

    # Пробел перед '- desc' гарантирован: badge оканчивается пробелом, а при
    # отсутствии бейджа (non-github) ставим его явно.
    sep = badge if badge else " "
    return f"- [{name}]({url}){sep}- {desc}."


def group_by_category(tools: list[dict], stars: dict[str, int]) -> dict[str, list[dict]]:
    """Группирует по категориям и сортирует внутри по убыванию звёзд."""
    groups: dict[str, list[dict]] = {key: [] for key, _ in CATEGORIES}
    for t in tools:
        groups[t["category"]].append(t)
    for items in groups.values():
        items.sort(key=lambda t: stars.get(t["url"], 0), reverse=True)
    return groups


def render_section(groups, lang, stars=None, featured=None):
    """Рендерит тело списка по категориям.

    stars — dict url→int (для порогов звёзд).
    featured — dict url→set[day|week] (отметки репо дня/недели).
    """
    stars = stars or {}
    featured = featured or {}
    title_key = f"title_{lang}"
    lines = []
    for cat_key, meta in CATEGORIES:
        items = groups.get(cat_key, [])
        if not items:
            continue
        lines.append(f"## {meta[title_key]}\n")
        for tool in items:
            url = tool["url"]
            marks = set(featured.get(url, ()))
            if is_new(tool):
                marks.add("new")
            lines.append(render_line(tool, lang, stars.get(url, 0), marks))
        lines.append("")  # пустая строка между категориями
    return "\n".join(lines).rstrip() + "\n"


HEADER_EN = """# Awesome Vibe Coding Tools [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of tools for **vibe coders** — developers building software with AI assistants (Claude Code, Cursor, Copilot and friends). Star counts are auto-updated daily. **[Browse the searchable site →](https://axisrow.github.io/vibetools/)** · Built with GLM-5.2.

A list should be a **curation, not a collection**: every entry is hand-picked, has a live repository, and is relevant to AI-assisted development. See CONTRIBUTING.md to add a tool. Русская версия: README.ru.md.

## Contents

{toc}

"""

HEADER_RU = """# Awesome Vibe Coding Tools [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> Кураторский список инструментов для **вайбкодеров** — разработчиков, которые пишут код с AI-ассистентами (Claude Code, Cursor, Copilot и компания). Число звёзд обновляется автоматически раз в сутки. **[Открыть сайт с поиском →](https://axisrow.github.io/vibetools/)** · Создано на GLM-5.2.

Список должен быть **кураторским, а не коллекционным**: каждая запись отобрана вручную, репозиторий жив, и инструмент относится к AI-разработке. Как добавить утилиту — см. CONTRIBUTING.md. English version: README.md.

## Содержание

{toc}

"""

FOOTER_EN = """
## Contributing

Found a great tool or built one? Add it via a Pull Request — see CONTRIBUTING.md for the rules (one tool per PR, live repo, neutral description). Star counts are refreshed daily by a GitHub Action. Licensed under CC0-1.0.
"""

FOOTER_RU = """
## Контрибьютинг

Нашли классный инструмент или сделали свой? Добавьте через Pull Request — правила см. в CONTRIBUTING.md (одна утилита на PR, живой репозиторий, нейтральное описание). Число звёзд обновляется автоматически раз в сутки через GitHub Action. Лицензия CC0-1.0.
"""


def gh_anchor(text: str) -> str:
    """Эмулирует генерацию якоря заголовка GitHub README.

    Правила: lowercase, удалить пунктуацию (кроме дефиса и букв/цифр/пробелов),
    пробелы → дефис, схлопнуть повторы дефисов.
    """
    keep = "- "  # дефис и пробел оставляем для дальнейшей обработки
    cleaned = "".join(c if (c.isalnum() or c in keep) else " " for c in text.lower())
    collapsed = re.sub(r"\s+", "-", cleaned.strip())
    return re.sub(r"-+", "-", collapsed)


def build_toc(groups, lang, with_featured: bool = False) -> str:
    title_key = f"title_{lang}"
    items = []
    # Секция Featured идёт между Contents и категориями — ToC обязан её
    # перечислять, иначе remark-lint:awesome-toc ругается на первый пункт
    # (ожидает Featured, видит AI Coding Agents). Пункт добавляем только когда
    # featured-блок реально рендерится (есть day/week), иначе якорь будет битым.
    if with_featured:
        featured_title = "Featured" if lang == "en" else "Избранное"
        items.append(f"- [{featured_title}](#{gh_anchor(featured_title)})")
    for cat_key, meta in CATEGORIES:
        if not groups.get(cat_key):
            continue
        anchor = gh_anchor(meta[title_key])
        items.append(f"- [{meta[title_key]}](#{anchor})")
    return "\n".join(items)


def main(
    tools_yml: Path = TOOLS_YML,
    stars_file: Path = STARS_FILE,
    out_dir: Path = ROOT,
    history_file: Path = HISTORY_FILE,
    meta_file: Path = META_FILE,
) -> None:
    tools = load_tools(tools_yml)
    stars = load_stars(stars_file)
    history = load_history(history_file)
    meta = load_json_or_default(meta_file, {}) or {}
    # Обогащаем tool-dict созданием created_at из repos-meta (для is_new).
    for t in tools:
        m = meta.get(t["url"])
        if isinstance(m, dict) and m.get("createdAt"):
            t["created_at"] = m["createdAt"]
    groups = group_by_category(tools, stars)
    featured = pick_featured(tools, stars, history)
    tools_by_url = {t["url"]: t for t in tools}

    for lang, header, footer, out_name in (
        ("en", HEADER_EN, FOOTER_EN, "README.md"),
        ("ru", HEADER_RU, FOOTER_RU, "README.ru.md"),
    ):
        featured_block = render_featured(featured, tools_by_url, lang)
        toc = build_toc(groups, lang, with_featured=bool(featured_block))
        body = render_section(groups, lang, stars, featured)
        content = header.format(toc=toc) + featured_block + body + footer
        out_path = out_dir / out_name
        out_path.write_text(content, encoding="utf-8")
        print(f"✓ {out_name}: {len(tools)} утилит, {len([c for c in CATEGORIES if groups[c[0]]])} категорий"
              + (f", featured: {sorted({m for s in featured.values() for m in s})}" if featured else ", featured: none"))


if __name__ == "__main__":
    main()
