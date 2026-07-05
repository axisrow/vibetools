#!/usr/bin/env python3
"""
Генератор статического сайта docs/index.html из data/tools.yml.

Сайт — user-friendly альтернатива плоскому README: полнотекстовый поиск,
фильтр по категориям/new, сортировка, i18n (EN/RU/ZH).

Данные живут отдельным файлом docs/data.json (раньше вшивались inline как
window.__DATA__ внутрь index.html). Фронтенд грузит их через fetch('data.json')
— тот же origin на GitHub Pages, без CORS. Так HTML-шаблон отделён от данных
и кешируется браузером отдельно (~100КБ HTML + ~1.2МБ JSON вместо монолита
1.5МБ). Переиспользует парсинг из generate_readme (load_tools, load_stars,
load_history, CATEGORIES, is_new) и github_slug из common — нулевое
дублирование логики.

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
# Trendshift-discovered репо, которых нет в tools.yml (autogen, растёт со stage 2/3).
# Подмешиваются на сайт (НЕ в README — золотое правило: tools.yml = единственный
# источник README). Category/name/description/language/topics кэшируются в этой
# же записи (scripts/categorize_repos.py), звёзды/meta — в stars.json/repos-meta.json.
TREND_SHIFT_REPOS_FILE = ROOT / "data" / "trendshift-repos.json"
OUT_FILE = ROOT / "docs" / "index.html"
# Данные сайта отдельным файлом рядом с index.html (тот же origin на Pages →
# fetch('data.json') без CORS). Раньше payload вшивался inline в index.html.
DATA_FILE = ROOT / "docs" / "data.json"
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
    trendshift_repos_file: Path = TREND_SHIFT_REPOS_FILE,
) -> dict:
    """Собирает единый объект данных для записи в docs/data.json.

    Все метрики автоматические (из stars.json/repos-meta.json/stars-history.json):
    stars, forks, openIssues, createdAt, archived, topics, language (primary),
    rank (по звёздам), starsPerWeek (рост за 7д), isNew (createdAt ≤14д).
    Ручных меток нет.
    search: lowercase name+en+ru+topics+language — для мгновенного client-side
    includes(). Сверху catalog languages (unique, sorted) для фильтра шаблона.

    trendshift-repos.json: обнаруженные trendshift-репо, которых нет в tools.yml
    (stage 2/3), подмешиваются в ``tools`` тем же payload-шейпом. Звёзды/meta —
    из stars.json/repos-meta.json (собирает update_stars для trendshift-репо);
    category/name/description/language/topics — из самой записи кэша. Флаг
    ``trendshiftDiscovered`` отличает их от кураторских (UI может пометить).
    """
    tools = load_tools(tools_yml)
    stars = load_stars(stars_file)
    meta = load_json_or_default(meta_file, {}) or {}
    history = load_history(history_file)
    trendshift = load_json_or_default(trendshift_file, {}) or {}
    today = datetime.date.today()

    out_tools = []
    tools_urls = {t["url"] for t in tools}
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
        # zh — опциональное поле в tools.yml; если нет, fallback на en.
        desc_zh = t["description"].get("zh", "") or desc_en
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
            "desc": {"en": desc_en, "ru": desc_ru, "zh": desc_zh},
            # lowercase haystack (Unicode/CJK-aware): name + desc (3 языка) + topics + language.
            "search": f"{t['name']} {desc_en} {desc_ru} {desc_zh} {' '.join(topics)} {language or ''}".lower(),
        }
        trendshift_entry = _trendshift_payload(trendshift.get(url))
        if trendshift_entry:
            tool_payload["trendshift"] = trendshift_entry
        out_tools.append(tool_payload)

    # Trendshift-discovered репо подмешиваются после кураторских. Дедуп против
    # tools_urls (на случай, если репо уже перенесли в tools.yml). Категория из
    # кэша (fallback 'needs-review'); isNew=False (discovery ≠ tool-new, которое
    # считается по createdAt). desc ru→en fallback (trendshift-репо без ru).
    trendshift_repos = []
    if trendshift_repos_file != TREND_SHIFT_REPOS_FILE or tools_yml == TOOLS_YML:
        trendshift_repos = load_json_or_default(trendshift_repos_file, []) or []
    for rec in trendshift_repos:
        if not isinstance(rec, dict):
            continue
        # irrelevant — ручная метка «не релевантен awesome-списку» (VPN, игры, OS-утилиты
        # и т.п.): не показываем на сайте. Ставится куратором в trendshift-repos.json.
        if rec.get("category") == "irrelevant":
            continue
        url = rec.get("githubUrl")
        if not isinstance(url, str) or url in tools_urls:
            continue
        tools_urls.add(url)
        m = meta.get(url) if isinstance(meta.get(url), dict) else {}
        slug = github_slug(url)
        stars_url = ""
        if slug:
            owner, repo = slug
            stars_url = SHIELDS_STARS.format(owner=owner, repo=repo)
        star_count = stars.get(url) if isinstance(stars.get(url), int) else None
        topics = rec.get("topics") or m.get("topics", []) or []
        language = rec.get("language") or m.get("language")
        desc_en = rec.get("description") or ""
        # ru/zh из кэша категоризации (descriptionRu/descriptionZh), fallback → en.
        desc_ru = rec.get("descriptionRu") or desc_en
        desc_zh = rec.get("descriptionZh") or desc_en
        name = rec.get("name") or (slug[1] if slug else url)
        tool_payload = {
            "name": name,
            "url": url,
            "category": rec.get("category") or "needs-review",
            "isNew": False,
            "trendshiftDiscovered": True,
            "stars": star_count,
            "starsPerWeek": _stars_per_week(url, history, stars),
            "starsUrl": stars_url,
            "forks": m.get("forks"),
            "openIssues": m.get("openIssues"),
            "createdAt": m.get("createdAt"),
            "archived": bool(m.get("archived")),
            "topics": topics,
            "language": language,
            "desc": {"en": desc_en, "ru": desc_ru, "zh": desc_zh},
            # haystack включает все 3 языка — поиск работает на любом языке UI.
            "search": f"{name} {desc_en} {desc_ru} {desc_zh} {' '.join(topics)} {language or ''}".lower(),
        }
        trendshift_entry = _trendshift_payload(rec)
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


def render_index_html(template: Path = INDEX_TEMPLATE) -> str:
    """Отдаёт HTML-шаблон как есть (данные больше не инлайнятся).

    Раньше сюда подставлялся window.__DATA__ payload с экранированием «</»
    (описания из GitHub API могли содержать «</script>» и порвать <script>).
    Теперь данные лежат отдельным docs/data.json и грузятся через fetch —
    шаблон не зависит от payload, экранирование не нужно.

    Регрессионный guard: placeholder-маркер ``/*__DATA__*/`` больше не нужен
    (generate_site его ничем не заменяет). Если кто-то вернёт его в шаблон
    (например, ``window.__DATA__ = /*__DATA__*/{}``), raise'им — иначе шаблон
    будет искать inline-данные, которых generate_site не подставляет, и
    деплой ляжет пустым сайтом при зелёном CI.
    """
    tpl = template.read_text(encoding="utf-8")
    if "/*__DATA__*/" in tpl:
        raise ValueError(
            f"шаблон {template} содержит inline-маркер данных /*__DATA__*/; "
            "данные вынесены в docs/data.json — уберите маркер из шаблона и "
            "грузите данные через fetch('data.json')")
    return tpl


def write_data_json(data: dict, data_file: Path = DATA_FILE) -> None:
    """Записывает payload в data.json (рядом с index.html, тот же origin).

    ensure_ascii=False — китайский текст читаемо и меньше байт. Данные лежат
    в отдельном .json (Content-Type: application/json), а не внутри <script> —
    поэтому ``</``-экранирование не нужно: парсер HTML сюда не смотрит.
    """
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    data_file.parent.mkdir(parents=True, exist_ok=True)
    data_file.write_text(payload, encoding="utf-8")


def main(
    tools_yml: Path = TOOLS_YML,
    stars_file: Path = STARS_FILE,
    out_file: Path = OUT_FILE,
    template: Path = INDEX_TEMPLATE,
    meta_file: Path = META_FILE,
    history_file: Path = HISTORY_FILE,
    trendshift_file: Path = TREND_SHIFT_FILE,
    trendshift_repos_file: Path = TREND_SHIFT_REPOS_FILE,
    data_file: Path | None = None,
) -> None:
    data = build_data_json(tools_yml, stars_file, meta_file, history_file,
                           trendshift_file, trendshift_repos_file)
    html = render_index_html(template)
    # data_file по умолчанию — рядом с out_file (data.json sibling index.html),
    # чтобы при инъекции out_file в тестах data_file тоже ложился в tmp.
    if data_file is None:
        data_file = out_file.parent / "data.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(html, encoding="utf-8")
    write_data_json(data, data_file)
    n = len(data["tools"])
    discovered = sum(1 for t in data["tools"] if t.get("trendshiftDiscovered"))
    print(f"✓ {out_file} + {data_file}: {n} утилит ({discovered} "
          f"trendshift-discovered), {len(data['categories'])} категорий, "
          f"языки en/ru/zh")


if __name__ == "__main__":
    main()
