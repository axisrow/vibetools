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

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML не найден. Установите: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
TOOLS_YML = ROOT / "data" / "tools.yml"
STARS_FILE = ROOT / "data" / "stars.json"  # кэш звёзд от update-stars.py (опционален)

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
]
CATEGORY_MAP = {key: meta for key, meta in CATEGORIES}

OWNER_REPO_TEMPLATE = "https://github.com/{owner}/{repo}"
SHIELDS_STARS = "https://img.shields.io/github/stars/{owner}/{repo}?style=flat&color=yellow"


def load_tools() -> list[dict]:
    """Загружает и валидирует утилиты из YAML."""
    with TOOLS_YML.open(encoding="utf-8") as fh:
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


def load_stars() -> dict[str, int]:
    """Загружает кэш звёзд (url -> stars), если он есть."""
    if not STARS_FILE.exists():
        return {}
    try:
        with STARS_FILE.open(encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return {}


def github_slug(url: str) -> tuple[str, str] | None:
    """Достаёт (owner, repo) из GitHub URL, иначе None (бейдж не рисуем)."""
    if "github.com/" not in url:
        return None
    parts = url.split("github.com/", 1)[1].split("/")
    if len(parts) < 2:
        return None
    owner, repo = parts[0], parts[1].removesuffix(".git")
    return owner, repo


def render_line(tool: dict, lang: str) -> str:
    """Рендерит одну строку списка утилиты для нужного языка."""
    name = tool["name"]
    url = tool["url"]
    desc = tool["description"][lang]
    slug = github_slug(url)
    badge = ""
    if slug:
        owner, repo = slug
        badge = f" ![]({SHIELDS_STARS.format(owner=owner, repo=repo)})"
    return f"- [{name}]({url}){badge} — {desc}"


def group_by_category(tools: list[dict], stars: dict[str, int]) -> dict[str, list[dict]]:
    """Группирует по категориям и сортирует внутри по убыванию звёзд."""
    groups: dict[str, list[dict]] = {key: [] for key, _ in CATEGORIES}
    for t in tools:
        groups[t["category"]].append(t)
    for items in groups.values():
        items.sort(key=lambda t: stars.get(t["url"], 0), reverse=True)
    return groups


def render_section(groups, lang):
    title_key = f"title_{lang}"
    lines = []
    for cat_key, meta in CATEGORIES:
        items = groups.get(cat_key, [])
        if not items:
            continue
        lines.append(f"## {meta['emoji']} {meta[title_key]}\n")
        for tool in items:
            lines.append(render_line(tool, lang))
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


def main() -> None:
    tools = load_tools()
    stars = load_stars()
    groups = group_by_category(tools, stars)

    for lang, header, footer, out_name in (
        ("en", HEADER_EN, FOOTER_EN, "README.md"),
        ("ru", HEADER_RU, FOOTER_RU, "README.ru.md"),
    ):
        toc = build_toc(groups, lang)
        body = render_section(groups, lang)
        content = header.format(toc=toc) + "\n" + body + footer
        out_path = ROOT / out_name
        out_path.write_text(content, encoding="utf-8")
        print(f"✓ {out_name}: {len(tools)} утилит, {len([c for c in CATEGORIES if groups[c[0]]])} категорий")


if __name__ == "__main__":
    main()
