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

# Порядок и подписи категорий. Каждый ключ должен совпадать со значениями
# поля `category` в tools.yml.
CATEGORIES = [
    ("cli-agents", {
        "emoji": "🤖",
        "title_en": "AI Coding Agents / CLI",
        "title_ru": "AI-агенты кодинга / CLI",
    }),
    ("editor-integrations", {
        "emoji": "⚡",
        "title_en": "Editor Integrations",
        "title_ru": "Интеграции в редакторы",
    }),
    ("context-memory", {
        "emoji": "🧠",
        "title_en": "Context / Memory",
        "title_ru": "Контекст / Память",
    }),
    ("prompt-mcp", {
        "emoji": "🔧",
        "title_en": "Prompts / MCP",
        "title_ru": "Промпты / MCP",
    }),
    ("observability-eval", {
        "emoji": "📊",
        "title_en": "Observability / Eval",
        "title_ru": "Наблюдаемость / Оценка",
    }),
    ("workflow-automation", {
        "emoji": "🛠️",
        "title_en": "Workflow / Automation",
        "title_ru": "Воркфлоу / Автоматизация",
    }),
    ("learning", {
        "emoji": "📚",
        "title_en": "Learning / Resources",
        "title_ru": "Обучение / Ресурсы",
    }),
    ("other", {
        "emoji": "📦",
        "title_en": "Other / Adjacent",
        "title_ru": "Прочее / Смежное",
    }),
]
CATEGORY_MAP = {key: meta for key, meta in CATEGORIES}

OWNER_REPO_TEMPLATE = "https://github.com/{owner}/{repo}"
SHIELDS_STARS = "https://img.shields.io/github/stars/{owner}/{repo}?style=flat&color=yellow"

# Пороги бейджей (эмодзи-префиксы перед shields-бейджем). Сортировка по убыванию.
STAR_TIERS = [
    (50000, "⭐"),
    (10000, "🌟"),
    (1000, "✨"),
]
NEW_DAYS = 14  # 🆕 если добавлено ≤ N дней назад (поле added)

# Окна выбора «репо дня/недели» (ключ → дней назад). Единый контракт:
# update_stars.HISTORY_DAYS должен покрывать max(FEATURED_WINDOWS.values())+1.
# Ключи — те же, что в MARK_EMOJI (_marks и render_featured читают их).
FEATURED_WINDOWS = {"day": 1, "week": 7}

# Эмодзи меток и порядок их вывода в строке. Единый источник: render_line
# (инлайн-метки) и render_featured (блок вверху) читают отсюда.
MARK_EMOJI = {"day": "🏆", "week": "📅", "verified": "🏅", "new": "🆕"}


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
    """Рендерит блок «🏆 Repo of the day / 📅 of the week» вверху README.

    Пустая строка, если нет ни дня, ни недели. Идёт по FEATURED_WINDOWS,
    чтобы порядок и состав меток были единым источником.
    """
    # URL для каждой метки из featured (если есть).
    urls = {kind: next((u for u, m in featured.items() if kind in m), None)
            for kind in FEATURED_WINDOWS}
    if not any(urls.values()):
        return ""
    labels = {
        ("en", "day"): "🏆 Repo of the day",
        ("en", "week"): "📅 Repo of the week",
        ("ru", "day"): "🏆 Репозиторий дня",
        ("ru", "week"): "📅 Репозиторий недели",
    }
    lines = []
    for kind, url in urls.items():
        if not url:
            continue
        t = tools_by_url.get(url)
        if not t:
            continue
        lines.append(f"{labels[(lang, kind)]}: [{t['name']}]({url}) — {t['description'][lang]}")
    if not lines:
        return ""
    return "## Featured\n\n" + "\n".join(lines) + "\n\n"


def tier_emoji(stars: int) -> str:
    """Эмодзи-префикс порога звёзд (⭐≥50k / 🌟≥10k / ✨≥1k), пусто если ниже."""
    for threshold, emoji in STAR_TIERS:
        if stars >= threshold:
            return emoji
    return ""


def is_new(tool: dict, today=None) -> bool:
    """🆕 если поле added есть и дата в пределах NEW_DAYS дней от today.

    today передаётся для детерминированности в тестах; по умолчанию —
    datetime.date.today(). Толерантна к отсутствию/битому полю added.
    """
    added = tool.get("added")
    if not added:
        return False
    today = today or datetime.date.today()
    try:
        d = datetime.date.fromisoformat(str(added))
    except ValueError:
        return False
    return 0 <= (today - d).days <= NEW_DAYS


def render_line(tool: dict, lang: str, stars: int = 0, marks: set[str] | None = None) -> str:
    """Рендерит одну строку списка утилиты для нужного языка.

    stars — для эмодзи-порога; marks — множество из {day, week, verified, new}
    (day/week приходят от выбора репо дня/недели; verified/new — из полей tool).
    """
    name = tool["name"]
    url = tool["url"]
    desc = tool["description"][lang]
    marks = marks or set()

    # Эмодзи-префикс: метки в фиксированном порядке (MARK_EMOJI) + порог звёзд.
    parts = [MARK_EMOJI[m] for m in MARK_EMOJI if m in marks]
    tier = tier_emoji(stars)
    if tier:
        parts.append(tier)
    prefix = " ".join(parts)

    # shields.io бейдж актуального числа звёзд.
    slug = github_slug(url)
    badge = ""
    if slug:
        owner, repo = slug
        badge = f" ![]({SHIELDS_STARS.format(owner=owner, repo=repo)})"

    lead = f"- {prefix} " if prefix else "- "
    return f"{lead}[{name}]({url}){badge} — {desc}"


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
        lines.append(f"## {meta['emoji']} {meta[title_key]}\n")
        for tool in items:
            url = tool["url"]
            marks = set(featured.get(url, ()))
            if tool.get("verified"):
                marks.add("verified")
            if is_new(tool):
                marks.add("new")
            lines.append(render_line(tool, lang, stars.get(url, 0), marks))
        lines.append("")  # пустая строка между категориями
    return "\n".join(lines).rstrip() + "\n"


HEADER_EN = """# Awesome Vibe Coding Tools

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re) [![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](LICENSE)

> A curated list of tools for **vibe coders** — developers building software with AI assistants (Claude Code, Cursor, Copilot and friends). Star counts are auto-updated daily.

A list should be a **curation, not a collection**: every entry is hand-picked, has a live repository, and is relevant to AI-assisted development.

**[Русская версия](README.ru.md)** · **[Contribute](CONTRIBUTING.md)** · **[Add a tool via PR →](CONTRIBUTING.md#how-to-add-a-tool)**

## Contents

{toc}

"""

HEADER_RU = """# Awesome Vibe Coding Tools

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re) [![Лицензия: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](LICENSE)

> Кураторский список инструментов для **вайбкодеров** — разработчиков, которые пишут код с AI-ассистентами (Claude Code, Cursor, Copilot и компания). Число звёзд обновляется автоматически раз в сутки.

Список должен быть **кураторским, а не коллекционным**: каждая запись отобрана вручную, репозиторий жив, и инструмент относится к AI-разработке.

**[English version](README.md)** · **[Контрибьютить](CONTRIBUTING.md)** · **[Добавить утилиту через PR →](CONTRIBUTING.md#как-добавить-утилиту)**

## Содержание

{toc}

"""

FOOTER_EN = """
## Contributing

Found a great tool or built one? Add it via a Pull Request — see [CONTRIBUTING.md](CONTRIBUTING.md) for the rules (one tool per PR, live repo, neutral description). Star counts are refreshed daily by a GitHub Action.

## License

[CC0-1.0](LICENSE) — public domain. To the extent possible under law, the contributors have waived all copyright.
"""

FOOTER_RU = """
## Контрибьютинг

Нашли классный инструмент или сделали свой? Добавьте через Pull Request — правила в [CONTRIBUTING.md](CONTRIBUTING.md) (одна утилита на PR, живой репозиторий, нейтральное описание). Число звёзд обновляется автоматически раз в сутки через GitHub Action.

## Лицензия

[CC0-1.0](LICENSE) — общественное достояние.
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


def build_toc(groups, lang) -> str:
    title_key = f"title_{lang}"
    items = []
    for cat_key, meta in CATEGORIES:
        if not groups.get(cat_key):
            continue
        anchor = gh_anchor(f"{meta['emoji']} {meta[title_key]}")
        items.append(f"- [{meta['emoji']} {meta[title_key]}](#{anchor})")
    return "\n".join(items)


def main(
    tools_yml: Path = TOOLS_YML,
    stars_file: Path = STARS_FILE,
    out_dir: Path = ROOT,
    history_file: Path = HISTORY_FILE,
) -> None:
    tools = load_tools(tools_yml)
    stars = load_stars(stars_file)
    history = load_history(history_file)
    groups = group_by_category(tools, stars)
    featured = pick_featured(tools, stars, history)
    tools_by_url = {t["url"]: t for t in tools}

    for lang, header, footer, out_name in (
        ("en", HEADER_EN, FOOTER_EN, "README.md"),
        ("ru", HEADER_RU, FOOTER_RU, "README.ru.md"),
    ):
        toc = build_toc(groups, lang)
        featured_block = render_featured(featured, tools_by_url, lang)
        body = render_section(groups, lang, stars, featured)
        content = header.format(toc=toc) + featured_block + body + footer
        out_path = out_dir / out_name
        out_path.write_text(content, encoding="utf-8")
        print(f"✓ {out_name}: {len(tools)} утилит, {len([c for c in CATEGORIES if groups[c[0]]])} категорий"
              + (f", featured: {sorted({m for s in featured.values() for m in s})}" if featured else ", featured: none"))


if __name__ == "__main__":
    main()
