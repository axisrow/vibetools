#!/usr/bin/env python3
"""
Генератор статического сайта docs/index.html из data/tools.yml.

Сайт — user-friendly альтернатива плоскому README: полнотекстовый поиск,
фильтр по категориям/new, сортировка, i18n (EN/RU/ZH).

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
from common import github_slug, load_json_or_default  # noqa: E402
from generate_readme import (  # noqa: E402
    CATEGORIES, ROOT, SHIELDS_STARS, _window_delta, is_new, load_history,
    load_stars, load_tools, pick_featured_entries,
)

TOOLS_YML = ROOT / "data" / "tools.yml"
STARS_FILE = ROOT / "data" / "stars.json"
META_FILE = ROOT / "data" / "repos-meta.json"
HISTORY_FILE = ROOT / "data" / "stars-history.json"
TREND_SHIFT_FILE = ROOT / "data" / "trendshift.json"
OUT_FILE = ROOT / "docs" / "index.html"
INDEX_TEMPLATE = ROOT / "scripts" / "site_template.html"


def _stars_per_week(url: str, history: dict, stars: dict) -> int | None:
    """Рост звёзд за последние 7 дней из stars-history (None если данных нет).

    Переиспользует _window_delta из generate_readme (единая 7-дневная логика)
    вместо собственного дубля с наивным today — устойчива к пропущенному
    daily-срезу (week-окно берёт самый старый доступный снимок в пределах 7
    дней, а не точную дату) и не обнуляется в не-UTC таймзоне.
    """
    cur = stars.get(url)
    if not isinstance(cur, int):
        return None
    snaps = history.get(url, {})
    if not snaps:
        return None
    delta = _window_delta(cur, snaps, "week", 7)
    if not delta:
        return None
    return max(0, delta["delta"])


def _trendshift_payload(entry) -> dict | None:
    """Normalize optional data/trendshift.json entry for the public site payload."""
    if not isinstance(entry, dict):
        return None
    badges = []
    for badge in entry.get("badges", []) or []:
        if not isinstance(badge, dict):
            continue
        kind = badge.get("kind")
        badge_url = badge.get("badgeUrl")
        if kind not in {"day", "week", "month", "year"} or not isinstance(badge_url, str):
            continue
        badge_payload = {"kind": kind, "badgeUrl": badge_url}
        if isinstance(badge.get("rank"), int):
            badge_payload["rank"] = badge["rank"]
        if isinstance(badge.get("currentRank"), int):
            badge_payload["currentRank"] = badge["currentRank"]
        if isinstance(badge.get("source"), str):
            badge_payload["source"] = badge["source"]
        badges.append(badge_payload)
    if not badges:
        return None
    page_url = entry.get("pageUrl")
    trendshift_id = entry.get("trendshiftId")
    payload = {"badges": badges}
    if isinstance(trendshift_id, (str, int)):
        payload["trendshiftId"] = str(trendshift_id)
    if isinstance(page_url, str):
        payload["pageUrl"] = page_url
    if isinstance(entry.get("updatedAt"), str):
        payload["updatedAt"] = entry["updatedAt"]
    return payload


def build_data_json(
    tools_yml: Path = TOOLS_YML,
    stars_file: Path = STARS_FILE,
    meta_file: Path = META_FILE,
    history_file: Path = HISTORY_FILE,
    trendshift_file: Path = TREND_SHIFT_FILE,
) -> dict:
    """Собирает единый объект данных для встраивания в index.html.

    Все метрики автоматические (из stars.json/repos-meta.json/stars-history.json):
    stars, forks, openIssues, createdAt, archived, topics, language (primary),
    rank (по звёздам), starsPerWeek (рост за 7д), isNew (createdAt ≤14д).
    Ручных меток нет.
    search: lowercase name+en+ru+topics+language — для мгновенного client-side
    includes(). Сверху catalog languages (unique, sorted) для фильтра шаблона.
    """
    tools = load_tools(tools_yml)
    stars = load_stars(stars_file)
    meta = load_json_or_default(meta_file, {}) or {}
    history = load_history(history_file)
    trendshift = load_json_or_default(trendshift_file, {}) or {}
    today = datetime.date.today()

    out_tools = []
    for t in tools:
        url = t["url"]
        m = meta.get(url) if isinstance(meta.get(url), dict) else {}
        slug = github_slug(url)
        stars_url = ""
        if slug:
            owner, repo = slug
            stars_url = SHIELDS_STARS.format(owner=owner, repo=repo)
        star_count = stars.get(url) if isinstance(stars.get(url), int) else None
        # Обогащаем tool-dict created_at для is_new (как в generate_readme.main).
        t["created_at"] = m.get("createdAt")
        desc_en = t["description"].get("en", "")
        desc_ru = t["description"].get("ru", "")
        topics = m.get("topics", []) or []
        language = m.get("language")
        tool_payload = {
            "name": t["name"],
            "url": url,
            "category": t["category"],
            "isNew": is_new(t, today),
            "stars": star_count,
            "starsPerWeek": _stars_per_week(url, history, stars),
            "starsUrl": stars_url,
            "forks": m.get("forks"),
            "openIssues": m.get("openIssues"),
            "createdAt": m.get("createdAt"),
            "archived": bool(m.get("archived")),
            "topics": topics,
            "language": language,
            "desc": {"en": desc_en, "ru": desc_ru},
            # lowercase haystack (Unicode/CJK-aware): name + desc + topics + language.
            "search": f"{t['name']} {desc_en} {desc_ru} {' '.join(topics)} {language or ''}".lower(),
        }
        trendshift_entry = _trendshift_payload(trendshift.get(url))
        if trendshift_entry:
            tool_payload["trendshift"] = trendshift_entry
        out_tools.append(tool_payload)

    # Global rank по звёздам (1 = топ базы); null-stars в конце.
    ranked = sorted(out_tools, key=lambda t: (t["stars"] or -1), reverse=True)
    for i, t in enumerate(ranked, 1):
        t["rank"] = i if t["stars"] is not None else None

    # Каталог языков (unique, sorted) — для фильтра в шаблоне без пересчёта.
    languages = sorted({t["language"] for t in out_tools if t["language"]})

    return {
        "generatedAt": today.isoformat(),
        "categories": [{"key": k, **m} for k, m in CATEGORIES],
        "languages": languages,
        "featured": pick_featured_entries(tools, stars, history),
        "tools": out_tools,
    }


DATA_MARKER = "/*__DATA__*/{}"


def render_index_html(data: dict, template: Path = INDEX_TEMPLATE) -> str:
    """Подставляет data.json в HTML-шаблон (window.__DATA__).

    Безопасность payload: json.dumps НЕ экранирует «</», а описания репо
    попадают из GitHub API дословно (в т.ч. через fetch_candidates → tools.yml).
    Любой «</script>» в описании закрыл бы <script>-элемент досрочно —
    window.__DATA__ остался бы undefined (пустой сайт), а крафтовый
    «</script><img onerror=…>» — stored-XSS. Поэтому экранируем последовательность
    «</» → «<\\/» (json-валидно, в JS читается обратно как «</», но парсер HTML
    его как закрывающий тег не видит). Дополнительно assert-им, что маркер
    шаблона найден — иначе косметическая правка шаблона заставила бы replace
    молча не сработать и деплоить пустой сайт при зелёном CI.
    """
    tpl = template.read_text(encoding="utf-8")
    if DATA_MARKER not in tpl:
        raise ValueError(
            f"маркер данных {DATA_MARKER!r} не найден в шаблоне {template}; "
            "generate_site не сможет встроить window.__DATA__")
    # json с ensure_ascii=False — китайский текст читаемо и меньше байт.
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # Экранируем «</» (в т.ч. «</script>»), чтобы payload не порвал <script>.
    payload = payload.replace("</", "<\\/")
    return tpl.replace(DATA_MARKER, payload)


def main(
    tools_yml: Path = TOOLS_YML,
    stars_file: Path = STARS_FILE,
    out_file: Path = OUT_FILE,
    template: Path = INDEX_TEMPLATE,
    meta_file: Path = META_FILE,
    history_file: Path = HISTORY_FILE,
    trendshift_file: Path = TREND_SHIFT_FILE,
) -> None:
    data = build_data_json(tools_yml, stars_file, meta_file, history_file,
                           trendshift_file)
    html = render_index_html(data, template)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    n = len(data["tools"])
    print(f"✓ {out_file}: {n} утилит, {len(data['categories'])} категорий, "
          f"языки en/ru/zh")


if __name__ == "__main__":
    main()
