#!/usr/bin/env python3
"""
Генератор статического сайта docs/index.html из data/tools.yml.

Сайт — user-friendly альтернатива плоскому README: полнотекстовый поиск,
фильтр по категориям/verified/new, сортировка, i18n (EN/RU/ZH).

Данные встраиваются inline как window.__DATA__ (без fetch/CORS — работает
на GitHub Pages как есть). Переиспует парсинг из generate_readme (load_tools,
load_stars, load_history, CATEGORIES, is_new) и github_slug из common —
нулевое дублирование логики.

Использование:
    python scripts/generate_site.py
"""
from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import github_slug  # noqa: E402
from generate_readme import (  # noqa: E402
    CATEGORIES, ROOT, SHIELDS_STARS, is_new, load_stars, load_tools,
)

TOOLS_YML = ROOT / "data" / "tools.yml"
STARS_FILE = ROOT / "data" / "stars.json"
OUT_FILE = ROOT / "docs" / "index.html"
INDEX_TEMPLATE = ROOT / "scripts" / "site_template.html"


def build_data_json(
    tools_yml: Path = TOOLS_YML,
    stars_file: Path = STARS_FILE,
) -> dict:
    """Собирает единый объект данных для встраивания в index.html.

    stars: int из stars.json (None, если файла нет/нет записи).
    isNew: precomputed через is_new (окно 14д от сегодня).
    search: lowercase name+en+ru — для мгновенного client-side includes().
    """
    tools = load_tools(tools_yml)
    stars = load_stars(stars_file)
    today = datetime.date.today()
    out_tools = []
    for t in tools:
        url = t["url"]
        slug = github_slug(url)
        stars_url = ""
        if slug:
            owner, repo = slug
            stars_url = SHIELDS_STARS.format(owner=owner, repo=repo)
        star_count = stars.get(url) if isinstance(stars.get(url), int) else None
        desc_en = t["description"].get("en", "")
        desc_ru = t["description"].get("ru", "")
        out_tools.append({
            "name": t["name"],
            "url": url,
            "category": t["category"],
            "verified": bool(t.get("verified")),
            "isNew": is_new(t, today),
            "added": t.get("added"),
            "stars": star_count,
            "starsUrl": stars_url,
            "desc": {"en": desc_en, "ru": desc_ru},
            # lowercase haystack для поиска (Unicode/CJK-aware через str.lower).
            "search": f"{t['name']} {desc_en} {desc_ru}".lower(),
        })
    return {
        "generatedAt": today.isoformat(),
        "categories": [{"key": k, **m} for k, m in CATEGORIES],
        "tools": out_tools,
    }


def render_index_html(data: dict, template: Path = INDEX_TEMPLATE) -> str:
    """Подставляет data.json в HTML-шаблон (window.__DATA__)."""
    tpl = template.read_text(encoding="utf-8")
    # json с ensure_ascii=False — китайский текст читаемо и меньше байт.
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return tpl.replace("/*__DATA__*/{}", payload)


def main(
    tools_yml: Path = TOOLS_YML,
    stars_file: Path = STARS_FILE,
    out_file: Path = OUT_FILE,
    template: Path = INDEX_TEMPLATE,
) -> None:
    data = build_data_json(tools_yml, stars_file)
    html = render_index_html(data, template)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    n = len(data["tools"])
    print(f"✓ {out_file}: {n} утилит, {len(data['categories'])} категорий, "
          f"языки en/ru/zh")


if __name__ == "__main__":
    main()
