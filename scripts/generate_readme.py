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
    ("cloud-coding-agents", {
        "title_en": "Cloud Coding Agents",
        "title_ru": "Облачные coding-агенты",
        "title_zh": "云端编程代理",
    }),
    ("editor-integrations", {
        "title_en": "Editor Integrations",
        "title_ru": "Интеграции в редакторы",
        "title_zh": "编辑器集成",
    }),
    ("code-review-testing", {
        "title_en": "Code Review, Testing and Quality",
        "title_ru": "Ревью, тестирование и качество кода",
        "title_zh": "代码审查、测试与质量",
    }),
    ("devops-cloud", {
        "title_en": "DevOps and Cloud Automation",
        "title_ru": "DevOps и облачная автоматизация",
        "title_zh": "DevOps 与云自动化",
    }),
    ("security-agents", {
        "title_en": "Security and Pentest Agents",
        "title_ru": "Security и pentest-агенты",
        "title_zh": "安全与渗透测试代理",
    }),
    ("browser-automation", {
        "title_en": "Browser and Web Automation",
        "title_ru": "Браузерная и web-автоматизация",
        "title_zh": "浏览器与网页自动化",
    }),
    ("design-frontend", {
        "title_en": "Design to Code and Frontend",
        "title_ru": "Design-to-code и фронтенд",
        "title_zh": "设计转代码与前端",
    }),
    ("app-builders-low-code", {
        "title_en": "App Builders and Low-Code",
        "title_ru": "App builders и low-code",
        "title_zh": "应用构建器与低代码",
    }),
    ("game-dev", {
        "title_en": "Game Development",
        "title_ru": "Разработка игр",
        "title_zh": "游戏开发",
    }),
    ("context-memory", {
        "title_en": "Context, Memory and Codebase Indexing",
        "title_ru": "Контекст, память и индексирование кода",
        "title_zh": "上下文、记忆与代码库索引",
    }),
    ("mcp", {
        "title_en": "MCP Servers and Clients",
        "title_ru": "MCP-серверы и клиенты",
        "title_zh": "MCP 服务器与客户端",
    }),
    ("agent-skills-prompts", {
        "title_en": "Agent Skills, Prompts and Rules",
        "title_ru": "Skills, промпты и правила агентов",
        "title_zh": "代理技能、提示词与规则",
    }),
    ("ai-assistants", {
        "title_en": "AI Assistants",
        "title_ru": "AI-ассистенты",
        "title_zh": "AI 助手",
    }),
    ("observability-eval", {
        "title_en": "Observability and Eval",
        "title_ru": "Наблюдаемость и eval",
        "title_zh": "可观测性与评估",
    }),
    ("docs-research", {
        "title_en": "Docs, Research and Knowledge Work",
        "title_ru": "Документация, research и knowledge work",
        "title_zh": "文档、研究与知识工作",
    }),
    ("learning-resources", {
        "title_en": "Learning and Resources",
        "title_ru": "Обучение и ресурсы",
        "title_zh": "学习与资源",
    }),
    ("ai-infra", {
        "title_en": "AI Infra and Model Platforms",
        "title_ru": "AI-инфра и модельные платформы",
        "title_zh": "AI 基础设施与模型平台",
    }),
    ("domain-agents", {
        "title_en": "Domain-Specific Agents",
        "title_ru": "Доменные AI-агенты",
        "title_zh": "垂直领域代理",
    }),
    ("needs-review", {
        "title_en": "Needs Review",
        "title_ru": "Требует ревью",
        "title_zh": "待复核",
    }),
]
CATEGORY_MAP = {key: meta for key, meta in CATEGORIES}
# Категории старой таксономии, выведенные из оборота (catch-all 'other' и др.).
# Единый источник для тестов, проверяющих, что в tools.yml не осталось легаси.
LEGACY_CATEGORIES = {"other", "prompt-mcp", "workflow-automation", "learning"}

OWNER_REPO_TEMPLATE = "https://github.com/{owner}/{repo}"
SHIELDS_STARS = "https://img.shields.io/github/stars/{owner}/{repo}?style=flat&color=yellow"

NEW_DAYS = 14  # [new] если добавлено ≤ N дней назад (поле added)

# Окна выбора «репо дня/недели» (ключ → дней назад). Единый контракт:
# update_stars.HISTORY_DAYS должен покрывать max(FEATURED_WINDOWS.values())+1.
FEATURED_WINDOWS = {"day": 1, "week": 7}

# Название секции Featured по языку — единый источник, чтобы заголовок секции
# (## Featured) и пункт оглавления (#featured) всегда совпадали (иначе
# remark-lint:awesome-toc ловит рассинхрон). Текст без «## » — префикс добавляет
# вызывающая сторона (заголовок) либо использует как есть (текст ссылки/якорь).
FEATURED_TITLES = {"en": "Featured", "ru": "Избранное"}


def featured_heading(lang: str, prefix: str = "") -> str:
    """Заголовок секции Featured: «## Featured» / «Избранное» и т. п."""
    return f"{prefix}{FEATURED_TITLES[lang]}"


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
    """Дельта cur vs точного среза за days_ago дней назад."""
    delta = _window_delta(cur, history, "day" if days_ago == 1 else "week",
                          days_ago)
    return delta["delta"] if delta else None


def _window_delta(cur: int, history: dict, kind: str, days_ago: int,
                  today=None) -> dict | None:
    """Дельта для featured-окна.

    day требует точный вчерашний срез. week использует самый старый доступный
    срез в пределах 7 дней, чтобы ранние daily cache не скрывали неделю.
    """
    today = today or datetime.date.today()
    target = today - datetime.timedelta(days=days_ago)

    if kind == "day":
        snap = history.get(target.isoformat())
        if not isinstance(snap, int):
            return None
        return {"delta": cur - snap, "days": days_ago,
                "windowComplete": True}

    candidates = []
    for raw_date, snap in history.items():
        if not isinstance(snap, int):
            continue
        try:
            snap_date = datetime.date.fromisoformat(str(raw_date)[:10])
        except ValueError:
            continue
        if target <= snap_date < today:
            candidates.append((snap_date, snap))
    if not candidates:
        return None
    snap_date, snap = min(candidates, key=lambda item: item[0])
    days = (today - snap_date).days
    return {"delta": cur - snap, "days": days,
            "windowComplete": days == days_ago}


def pick_featured_entries(tools: list[dict], stars: dict[str, int],
                          history: dict[str, dict]) -> list[dict]:
    """Выбирает featured entries с метаданными окна и дельты.

    Возвращает список в порядке FEATURED_WINDOWS:
    {"kind": "day"|"week", "url": str, "delta": int, "days": int,
     "windowComplete": bool}.
    """
    entries: list[dict] = []
    for kind, days_ago in FEATURED_WINDOWS.items():
        best = None
        for t in tools:
            cur = stars.get(t["url"])
            if cur is None:
                continue
            delta = _window_delta(cur, history.get(t["url"], {}), kind,
                                  days_ago)
            if not delta or delta["delta"] <= 0:
                continue
            if best is None or delta["delta"] > best["delta"]:
                best = {"kind": kind, "url": t["url"], **delta}
        if best:
            entries.append(best)
    return entries


def pick_featured(tools: list[dict], stars: dict[str, int],
                  history: dict[str, dict]) -> dict[str, set[str]]:
    """Выбирает репо дня и недели.

    history: {url: {"YYYY-MM-DD": stars}}. Возвращает {url: {"day"} | {"week"}}.
    Если истории нет или все дельты ≤ 0 — пустой dict (блок не рендерится).
    """
    featured: dict[str, set[str]] = {}
    for entry in pick_featured_entries(tools, stars, history):
        featured.setdefault(entry["url"], set()).add(entry["kind"])
    return featured


def _featured_entries(featured) -> list[dict]:
    """Нормализует новый entries-формат и legacy url->marks dict."""
    if isinstance(featured, list):
        return featured
    entries = []
    for kind in FEATURED_WINDOWS:
        url = next((u for u, marks in featured.items() if kind in marks), None)
        if url:
            entries.append({"kind": kind, "url": url})
    return entries


def _featured_label(lang: str, entry: dict) -> str:
    labels = {
        ("en", "day"): "Repo of the day",
        ("en", "week"): "Repo of the week",
        ("ru", "day"): "Репозиторий дня",
        ("ru", "week"): "Репозиторий недели",
    }
    label = labels[(lang, entry["kind"])]
    if entry.get("kind") == "week" and entry.get("days") and not entry.get("windowComplete", True):
        days = entry["days"]
        if lang == "en":
            return f"{label} ({days}-day growth)"
        return f"{label} (рост за {days} дн.)"
    return label


def render_featured(featured, tools_by_url: dict[str, dict], lang: str) -> str:
    """Рендерит блок «Repo of the day / Repo of the week» вверху README.

    Пустая строка, если нет ни дня, ни недели. Идёт по FEATURED_WINDOWS,
    чтобы порядок и состав меток были единым источником.
    """
    entries = _featured_entries(featured)
    if not entries:
        return ""
    lines = []
    for entry in entries:
        url = entry["url"]
        t = tools_by_url.get(url)
        if not t:
            continue
        # Anchor #featured-{kind} отличает ссылку от её вхождения в категории:
        # тот же репо легитимно показан несколько раз (блок Featured + своя
        # категория, а внутри Featured — отдельно repo-of-day и repo-of-week).
        # Без различия remark-lint:double-link считает дубликатом. Привязка anchor
        # к типу (day/week) делает уникальными даже два featured-вхождения одного
        # репо; stripHash:false правила → URL'ы с разным hash формально различны.
        featured_url = f"{url}#featured-{entry['kind']}"
        lines.append(f"{_featured_label(lang, entry)}: [{t['name']}]({featured_url}) — {t['description'][lang]}")
    if not lines:
        return ""
    return featured_heading(lang, "## ") + "\n\n" + "\n".join(lines) + "\n\n"


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

    Дата берётся из created_at (ISO-datetime из repos-meta, поле GitHub API;
    обогащается в main перед вызовом). Толерантна к отсутствию/битому значению.
    today — для детерминированности в тестах.

    Золотое правило CLAUDE.md: tools.yml хранит только name/url/category/
    description — ручного поля «added» нет (оно вычисляется из createdAt).
    Поэтому legacy-fallback на «added» убран: единственный источник — created_at.
    """
    raw = tool.get("created_at")
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
    # тримим завершающую пунктуацию/пробелы (чтобы не получить «!.» / «?.» / «. »),
    # схлопываем множественные пробелы и капитализируем первое слово (требование
    # awesome-lint).
    raw = tool["description"][lang]
    desc = "".join(c for c in raw if not _is_emoji(c))
    desc = desc.replace("[", "\\[").strip().lstrip("#").strip()
    desc = desc.strip("—-").strip()
    # Убираем хвостовую пунктуацию/пробелы — точку добавим сами ниже.
    desc = desc.rstrip(".!? ").rstrip()
    # Схлопываем повторы пробелов (могут остаться после вырезания эмодзи).
    desc = re.sub(r"\s+", " ", desc).strip()
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
        title = FEATURED_TITLES[lang]
        items.append(f"- [{title}](#{gh_anchor(title)})")
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
    featured_entries = pick_featured_entries(tools, stars, history)
    featured = pick_featured(tools, stars, history)
    tools_by_url = {t["url"]: t for t in tools}

    for lang, header, footer, out_name in (
        ("en", HEADER_EN, FOOTER_EN, "README.md"),
        ("ru", HEADER_RU, FOOTER_RU, "README.ru.md"),
    ):
        featured_block = render_featured(featured_entries, tools_by_url, lang)
        toc = build_toc(groups, lang, with_featured=bool(featured_block))
        body = render_section(groups, lang, stars, featured)
        content = header.format(toc=toc) + featured_block + body + footer
        out_path = out_dir / out_name
        out_path.write_text(content, encoding="utf-8")
        print(f"✓ {out_name}: {len(tools)} утилит, {len([c for c in CATEGORIES if groups[c[0]]])} категорий"
              + (f", featured: {[e['kind'] for e in featured_entries]}" if featured_entries else ", featured: none"))


if __name__ == "__main__":
    main()
