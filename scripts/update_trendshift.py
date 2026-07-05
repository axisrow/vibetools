#!/usr/bin/env python3
"""
Find Trendshift achievements published by tool authors in upstream READMEs.

This is an enrichment cache, not a human-curated source. data/tools.yml stays
limited to name/url/category/description, while Trendshift metadata lives in
data/trendshift.json and can disappear without breaking the site.

data/trendshift-repos.json — автогенерируемый кэш (list) репозиториев с
ranking-страниц trendshift.io, отсутствующих в tools.yml. Отдельный от
trendshift.json, чтобы не смешивать enrichment-only метаданные кураторских
тулзов и «сырые» trendshift-репо.
"""
from __future__ import annotations

import datetime
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape
from pathlib import Path
from typing import Callable

import requests

ROOT = Path(__file__).resolve().parent.parent
TOOLS_YML = ROOT / "data" / "tools.yml"
TREND_SHIFT_FILE = ROOT / "data" / "trendshift.json"
# Репозитории с trendshift.io, которых нет в tools.yml. List (отсортированный
# по url для детерминированного git-diff), отдельный от trendshift.json.
TREND_SHIFT_REPOS_FILE = ROOT / "data" / "trendshift-repos.json"
# repos-meta.json: update_stars уже обошёл все репо (tools.yml + trendshift-repos)
# и положил {stars, archived, ...} сюда ДО этого скрипта в daily-джобе. _prune
# переиспользует эти данные (0 API), дёргая alive-check только для отсутствующих.
META_FILE = ROOT / "data" / "repos-meta.json"
RAW_README = "https://raw.githubusercontent.com/{owner}/{repo}/HEAD/README.md"
TREND_SHIFT_PAGE = "https://trendshift.io/repositories/{id}"
TREND_SHIFT_BADGE = "https://trendshift.io/api/badge/trendshift/repositories/{id}/{window}"
RANKING_WINDOWS = {
    "day": ("https://trendshift.io/", "daily"),
    "week": ("https://trendshift.io/weekly", "weekly"),
    "month": ("https://trendshift.io/monthly", "monthly"),
    "year": ("https://trendshift.io/yearly", "yearly"),
}

# Языки, подлежащие per-language сбору (значения совпадают с label-ами в
# trendshift-селекторе, см. _LANGUAGE_URL_SEGMENT для URL-кодирования).
# Список добыт из JS-бандла trendshift (dropdown рендерится на клиенте, в
# server-side HTML ?language= ссылок нет). Порядок стабилен для детерминизма.
TREND_LANGUAGES = (
    "Python", "TypeScript", "JavaScript", "Rust", "Go", "Java",
    "C#", "C++", "C", "Ruby", "PHP", "Dart", "Swift", "Kotlin", "Zig",
)
# trendshift кодирует язык в query-параметре ?language= нестандартно для
# спецсимволов ('#' как %23, '+' как %2B). Таблица делает это явным и
# тестируемым; языки без спецсимволов идут как есть (идентичный сегмент).
_LANGUAGE_URL_SEGMENT = {
    "C#": "C%23",
    "C++": "C%2B%2B",
}

# trendshift.io отдаёт 403 на запросы без User-Agent. Дефолт подставляется в
# fetch_url, когда вызывающая сторона не передала свой headers — production
# безопасен без правок вызовов, а тесты могут явно прокинуть headers=None/dict.
_USER_AGENT = "vibetools-bot/1.0 (+https://github.com/axisrow/vibetools)"
_DEFAULT_HEADERS = {"User-Agent": _USER_AGENT}

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    check_repo_alive,
    github_headers,
    github_slug,
    load_json_or_default,
)
from generate_readme import load_tools  # noqa: E402

PAGE_RE = re.compile(r"https://trendshift\.io/repositories/(?P<id>\d+)")
BADGE_RE = re.compile(
    r"https://trendshift\.io/api/badge/trendshift/repositories/"
    r"(?P<id>\d+)/(?P<window>daily|weekly|monthly|yearly)(?:\?[^\s\"'<>)]*)?"
)
BADGE_LABEL_RE = re.compile(r"Trendshift: number (?P<rank>\d+) repository of the (?P<period>day|week|month|year)")
KIND_BY_WINDOW = {
    "daily": "day",
    "weekly": "week",
    "monthly": "month",
    "yearly": "year",
}
KIND_ORDER = {"day": 0, "week": 1, "month": 2, "year": 3}

# Порог звёзд для включения автособранного репо в trendshift-repos.json.
# 0 = «принимаем любые живые» (текущий консервативный дефолт); повысить до N,
# чтобы отсеивать шум. На курируемый tools.yml НЕ влияет — только на фильтр
# мёртвых/пустых автособранных репо (см. _prune_dead_new_repos).
MIN_STARS = 0


def fetch_readme(slug: tuple[str, str], headers: dict) -> str | None:
    """Fetch README.md from GitHub raw content using default-branch HEAD."""
    owner, repo = slug
    url = RAW_README.format(owner=owner, repo=repo)
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as exc:
        print(f"  ! {owner}/{repo}: README fetch failed: {exc}", file=sys.stderr)
        return None
    if response.status_code == 200:
        return response.text
    print(f"  ! {owner}/{repo}: README HTTP {response.status_code}", file=sys.stderr)
    return None


def fetch_url(url: str, headers: dict | None = None) -> str | None:
    """Fetch an arbitrary Trendshift/GitHub text URL.

    headers=None (по умолчанию у вызывающих) подставляет _DEFAULT_HEADERS с
    User-Agent: trendshift.io отдаёт 403 на bare urllib/requests без UA.
    Явный headers (для README-фетча через github_headers()) имеет приоритет.
    """
    try:
        response = requests.get(url, headers=headers or _DEFAULT_HEADERS, timeout=10)
    except requests.RequestException as exc:
        print(f"  ! {url}: fetch failed: {exc}", file=sys.stderr)
        return None
    if response.status_code == 200:
        return response.text
    return None


def extract_trendshift_entry(readme: str, updated_at: str) -> dict | None:
    """Extract the first repository-level daily/weekly Trendshift badge set."""
    page_ids = [match.group("id") for match in PAGE_RE.finditer(readme)]
    badge_matches = list(BADGE_RE.finditer(readme))
    if not badge_matches:
        return None

    trendshift_id = page_ids[0] if page_ids else badge_matches[0].group("id")
    badges_by_kind: dict[str, dict] = {}
    for match in badge_matches:
        if match.group("id") != trendshift_id:
            continue
        kind = KIND_BY_WINDOW[match.group("window")]
        badge_url = match.group(0)
        current = badges_by_kind.get(kind)
        if current is None or ("?" in current["badgeUrl"] and "?" not in badge_url):
            badges_by_kind[kind] = {
                "kind": kind,
                "badgeUrl": badge_url,
                "source": "readme",
            }

    badges = sorted(badges_by_kind.values(), key=lambda b: KIND_ORDER[b["kind"]])
    if not badges:
        return None

    return {
        "trendshiftId": trendshift_id,
        "pageUrl": TREND_SHIFT_PAGE.format(id=trendshift_id),
        "badges": badges,
        "updatedAt": updated_at,
    }


def extract_badge_rank(svg: str) -> int | None:
    """Extract the numeric rank Trendshift exposes in badge aria-label."""
    match = BADGE_LABEL_RE.search(svg)
    if not match:
        return None
    return int(match.group("rank"))


def extract_ranking_entries(html: str, kind: str, updated_at: str) -> list[dict]:
    """Extract repository candidates from Trendshift JSON-LD ItemList."""
    entries: list[dict] = []
    scripts = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>',
        html,
        flags=re.S,
    )
    for raw_script in scripts:
        try:
            obj = json.loads(unescape(raw_script))
        except (json.JSONDecodeError, TypeError):
            continue
        if obj.get("@type") != "ItemList":
            continue
        for item in obj.get("itemListElement", []) or []:
            software = item.get("item", {}) if isinstance(item, dict) else {}
            github_url = software.get("codeRepository") or software.get("url")
            page_url = item.get("url")
            if not isinstance(github_url, str) or "github.com/" not in github_url:
                continue
            if not isinstance(page_url, str):
                continue
            trendshift_id = page_url.rstrip("/").rsplit("/", 1)[-1]
            if not trendshift_id.isdigit():
                continue
            position = item.get("position")
            entry = {
                "githubUrl": github_url,
                "trendshiftId": trendshift_id,
                "pageUrl": TREND_SHIFT_PAGE.format(id=trendshift_id),
                "badges": [{
                    "kind": kind,
                    "currentRank": position if isinstance(position, int) else None,
                    "source": "ranking",
                }],
                "updatedAt": updated_at,
            }
            entries.append(entry)
        break
    return entries


def merge_trendshift_entry(base: dict | None, incoming: dict) -> dict:
    """Merge badges for one repo, keeping the strongest known rank per kind."""
    if not isinstance(base, dict):
        base = {
            "trendshiftId": incoming.get("trendshiftId"),
            "pageUrl": incoming.get("pageUrl"),
            "badges": [],
            "updatedAt": incoming.get("updatedAt"),
        }
    base["trendshiftId"] = str(incoming.get("trendshiftId") or base.get("trendshiftId"))
    base["pageUrl"] = incoming.get("pageUrl") or base.get("pageUrl")
    base["updatedAt"] = incoming.get("updatedAt") or base.get("updatedAt")

    badges_by_kind = {
        badge.get("kind"): dict(badge)
        for badge in base.get("badges", []) or []
        if isinstance(badge, dict) and badge.get("kind") in KIND_ORDER
    }
    for badge in incoming.get("badges", []) or []:
        if not isinstance(badge, dict):
            continue
        kind = badge.get("kind")
        if kind not in KIND_ORDER:
            continue
        current = badges_by_kind.get(kind)
        if current is None:
            badges_by_kind[kind] = dict(badge)
            continue
        current_rank = current.get("rank")
        incoming_rank = badge.get("rank")
        if isinstance(incoming_rank, int) and (
            not isinstance(current_rank, int) or incoming_rank < current_rank
        ):
            badges_by_kind[kind] = dict(badge)
        elif current.get("badgeUrl") is None and badge.get("badgeUrl"):
            current["badgeUrl"] = badge["badgeUrl"]
        elif current.get("source") == "readme" and badge.get("source") == "ranking":
            current["source"] = "readme+ranking"

    base["badges"] = [
        badges_by_kind[kind]
        for kind in sorted(badges_by_kind, key=lambda k: KIND_ORDER[k])
    ]
    return base


def _decorate_ranking_entry(
    entry: dict,
    badge_window: str,
    badge_fetcher: Callable[[str, dict | None], str | None],
    headers: dict | None = None,
) -> dict | None:
    """Fetch the badge SVG for a ranking entry and attach rank/badgeUrl.

    Returns the entry with its first badge decorated (badgeUrl + rank), or
    None if the rank could not be extracted (unranked / fetch failed). Single
    source of truth for the badge→rank enrichment shared by both branches of
    enrich_from_rankings. ``headers`` пробрасывается в badge_fetcher (UA для
    trendshift.io; без него — 403).
    """
    trendshift_id = entry["trendshiftId"]
    badge_url = TREND_SHIFT_BADGE.format(id=trendshift_id, window=badge_window)
    svg = badge_fetcher(badge_url, headers)
    rank = extract_badge_rank(svg or "")
    if rank is None:
        return None
    badge = entry["badges"][0]
    badge["badgeUrl"] = badge_url
    badge["rank"] = rank
    return entry


def _ranking_pages(languages: tuple[str, ...] | None):
    """Yield (kind, page_url, badge_window) — глобальные страницы, затем
    per-language × 4 окна.

    Глобальные окна идут первыми (важно: репо из tools.yml должны попасть в
    trendshift.json через тот же путь, что и раньше). Per-language добавляются
    только когда передан непустой ``languages``. Дедуп по githubUrl делает
    enrich_from_rankings через merge_trendshift_entry — здесь только перечисляем
    страницы.
    """
    for kind, (page_url, badge_window) in RANKING_WINDOWS.items():
        yield kind, page_url, badge_window
    if not languages:
        return
    for lang in languages:
        segment = _LANGUAGE_URL_SEGMENT.get(lang, lang)
        for kind, (page_url, badge_window) in RANKING_WINDOWS.items():
            yield kind, f"{page_url}?language={segment}", badge_window


def enrich_from_rankings(
    tools: list[dict],
    cache: dict,
    updated_at: str,
    page_fetcher: Callable[[str, dict | None], str | None] = fetch_url,
    badge_fetcher: Callable[[str, dict | None], str | None] = fetch_url,
    new_repos: dict | None = None,
    languages: tuple[str, ...] | None = None,
    headers: dict | None = None,
) -> dict:
    """Add repos discovered from Trendshift ranking pages.

    Repos whose githubUrl is in ``tools`` enrich ``cache`` (the trendshift.json
    enrichment cache keyed by url) — unchanged behavior. Repos NOT in tools.yml
    are collected into ``new_repos`` (keyed by url) when that accumulator is
    provided, so we no longer silently drop trendshift-only repos. When
    ``new_repos`` is None the legacy behavior is preserved (unknown repos are
    skipped) — this keeps existing callers/tests unchanged.

    ``languages`` — кортеж языков для per-language сбора (None/() → только 4
    глобальные страницы, legacy). ``headers`` пробрасывается в fetcher-ы (UA для
    trendshift.io); по умолчанию None, и тогда fetch_url подставит свой
    _DEFAULT_HEADERS.
    """
    by_url = {tool.get("url"): tool for tool in tools}
    for kind, page_url, badge_window in _ranking_pages(languages):
        html = page_fetcher(page_url, headers)
        if html is None:
            continue
        for entry in extract_ranking_entries(html, kind, updated_at):
            # decorate пытается вытащить точный ранг из badge SVG (+1 запрос на репо).
            # Если badge недоступен (outage / fetcher отключен) — не теряем репо:
            # берём исходный entry, у которого уже есть currentRank из ItemList
            # (позиция в рейтинге на момент парсинга страницы). Это позволяет
            # собирать каталог без медленных badge-фетчей и не терять репо при
            # частичном outage trendshift-badge.
            decorated = _decorate_ranking_entry(entry, badge_window, badge_fetcher, headers)
            if decorated is None:
                decorated = entry
            github_url = decorated["githubUrl"]
            if github_url in by_url:
                cache[github_url] = merge_trendshift_entry(cache.get(github_url), decorated)
            elif new_repos is not None:
                new_repos[github_url] = merge_trendshift_entry(new_repos.get(github_url), decorated)
    return cache


def _prune_dead_new_repos(
    new_repos: dict,
    headers: dict,
    alive_checker: Callable[[tuple[str, str], dict], tuple],
    workers: int = 16,
    min_stars: int = MIN_STARS,
    meta: dict | None = None,
) -> dict:
    """Фильтрует мёртвые/пустые репо из автособранного new_repos (in-place).

    Применяется ТОЛЬКО к trendshift-only репо (которых нет в tools.yml) — на
    курируемый tools.yml и обогащающий trendshift.json не влияет. Вызывается из
    update_trendshift_cache ПОСЛЕ enrich_from_rankings, когда new_repos уже
    наполнен и badge-merge сделан (фильтр ортогонален merge-логике).

    Два источника решения о репо, чтобы не сжечь GitHub API budget (Actions
    GITHUB_TOKEN = 1000 req/hour/repo, а update_stars уже тратит его на все
    репо — см. https://docs.github.com/en/rest/using-rest-api/rate-limits):

    1. ``meta`` (data/repos-meta.json, обновляется update_stars ДО этого
       скрипта в том же daily-джобе). Для url, которые есть в meta, archived/
       stars берутся оттуда — БЕЗ API-запроса. Этим покрывается подавляющее
       большинство репо (мёртвые 404 в meta просто не попадают — fetch_repo
       возвращает None при 404 и не пишет запись).
    2. ``alive_checker`` (default common.check_repo_alive) — ТОЛЬКО для url,
       отсутствующих в meta: это либо реально мёртвые, либо живые, не успевшие
       попасть в meta из-за rate-limit в прошлый прогон.

    Правила для каждого url в new_repos:
    - в ``meta`` + ``archived=True`` → удалить (заброшенные);
    - в ``meta`` + ``stars < min_stars`` → удалить (пустой шум);
    - в ``meta`` иначе → оставить (живое, проверено);
    - НЕ в meta + alive-check ``dead`` (404) → удалить;
    - НЕ в meta + alive-check ``unknown`` (403/429/5xx/timeout/...) → оставить
      («не смогли проверить» ≠ «мёртвый»: обрыв сети не должен выкашивать
      живые репо; в след. прогоне update_stars положит их в meta).

    url без github.com (github_slug → None) пропускаются без проверок.
    alive-check параллелится через ThreadPoolExecutor (паттерн README-fetch).
    """
    # Проход 1: фильтр по meta (0 API-запросов) — для url, которые update_stars
    # уже проверил и положил в repos-meta.json.
    if meta:
        for url in list(new_repos.keys()):
            m = meta.get(url)
            if not isinstance(m, dict):
                continue  # нет в meta → оставляем для alive-check (проход 2)
            if m.get("archived"):
                del new_repos[url]
                continue
            stars = m.get("stars")
            if isinstance(stars, int) and stars < min_stars:
                del new_repos[url]
                continue
            # есть в meta, не archived, stars >= min_stars → живое, оставляем.
            # В new_repos у него нет записи-маркера «проверено» — но оно просто
            # останется в словаре как есть, что и нужно.

    # Проход 2: alive-check только для того, чего нет в meta (или meta=None).
    candidates: list[tuple[str, tuple[str, str]]] = []
    for url in new_repos:
        if meta and isinstance(meta.get(url), dict):
            continue  # уже решено в проходе 1
        slug = github_slug(url)
        if slug is None:
            continue
        candidates.append((url, slug))
    if not candidates:
        return new_repos

    statuses: dict[str, str] = {}

    def check(url: str, slug: tuple[str, str]):
        try:
            status, _ = alive_checker(slug, headers)
        except Exception as exc:  # pragma: no cover - defensive for injected checker
            print(f"  ! {slug[0]}/{slug[1]}: alive-check упал {exc}", file=sys.stderr)
            status = "unknown"
        statuses[url] = status

    if workers <= 1:
        for url, slug in candidates:
            check(url, slug)
    else:
        max_workers = min(workers, len(candidates)) or 1
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(check, url, slug) for url, slug in candidates]
            for future in as_completed(futures):
                future.result()

    for url, status in statuses.items():
        if status == "dead":
            del new_repos[url]
            continue
        # alive (уже отфильтрован бы в проходе 1, раз попал сюда — только если
        # meta=None) → оставляем; unknown → оставляем.
    return new_repos


def update_trendshift_cache(
    tools: list[dict],
    previous_cache: dict,
    updated_at: str,
    headers: dict,
    fetcher: Callable[[tuple[str, str], dict], str | None] = fetch_readme,
    page_fetcher: Callable[[str, dict | None], str | None] = fetch_url,
    badge_fetcher: Callable[[str, dict | None], str | None] = fetch_url,
    workers: int = 16,
    new_repos: dict | None = None,
    languages: tuple[str, ...] | None = None,
    alive_checker: Callable[[tuple[str, str], dict], tuple] | None = None,
    meta: dict | None = None,
) -> dict:
    """Build a fresh cache and preserve previous entries on fetch failures.

    ``new_repos`` — опциональный mutable-аккумулятор (dict url→entry) для
    trendshift-репо, которых нет в tools.yml. Пробрасывается в
    enrich_from_rankings. Возвращается по-прежнему только cache (как и cache,
    new_repos мутируется по ссылке, вызывающая сторона читает его после вызова).

    ``languages`` — пробрасывается в enrich_from_rankings для per-language
    сбора (None/() → legacy, только 4 глобальные страницы).

    ``alive_checker`` — опциональный детектор живости репо (см.
    common.check_repo_alive). Если передан И new_repos не None — после
    enrich_from_rankings вызывается _prune_dead_new_repos, выкидывающий из
    new_repos 404/archived/low-stars. None → фильтр отключен (legacy-режим,
    старые тесты не ломаются).

    ``meta`` — data/repos-meta.json (обновляется update_stars ДО этого скрипта
    в daily-джобе). _prune_dead_new_repos берёт archived/stars из meta для url,
    которые там есть (0 API), а alive_checker дёргает только для отсутствующих
    в meta — это держит API-бюджет в рамках Actions-лимита 1000/час.
    """
    candidates = []
    for tool in tools:
        url = tool.get("url", "")
        slug = github_slug(url)
        if slug:
            candidates.append((url, slug))

    def process(candidate: tuple[str, tuple[str, str]]) -> tuple[str, dict | None]:
        url, slug = candidate
        try:
            readme = fetcher(slug, headers)
        except Exception as exc:  # pragma: no cover - defensive for injected fetchers
            print(f"  ! {slug[0]}/{slug[1]}: README fetch failed: {exc}", file=sys.stderr)
            readme = None
        if readme is None:
            old_entry = previous_cache.get(url)
            return url, old_entry if isinstance(old_entry, dict) else None
        return url, extract_trendshift_entry(readme, updated_at)

    next_cache: dict[str, dict] = {}
    if workers <= 1:
        results = [process(candidate) for candidate in candidates]
    else:
        max_workers = min(workers, len(candidates)) or 1
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process, candidate) for candidate in candidates]
            results = [future.result() for future in as_completed(futures)]
    for url, entry in results:
        if entry is not None:
            next_cache[url] = merge_trendshift_entry(next_cache.get(url), entry)
    cache = enrich_from_rankings(tools, next_cache, updated_at, page_fetcher,
                                 badge_fetcher, new_repos, languages, None)
    # Фильтр мёртвых/пустых автособранных репо — только когда аккумулятор
    # включён (new_repos is not None) и задан alive_checker. Иначе legacy-режим
    # без alive-проверки (старые тесты и outage-сида не затрагиваются).
    if new_repos is not None and alive_checker is not None:
        _prune_dead_new_repos(new_repos, headers, alive_checker, workers, meta=meta)
    return cache


def _serialize_repos_cache(new_repos: dict) -> list[dict]:
    """Dict url→entry → отсортированный по url list; каждой записи добавлен
    githubUrl (бывший ключ). Сортировка даёт детерминированный git-diff при
    ежедневных перезаписях (иначе порядок от ThreadPoolExecutor плавал бы).

    Поля entry не переописываются — spread ``**entry`` копирует всё, что
    extract_ranking_entries/merge_trendshift_entry туда положили, так что
    сериализатор не рассинхронится при эволюции схемы записи.
    """
    records = [
        {"githubUrl": url, **entry}
        for url, entry in new_repos.items()
        if isinstance(entry, dict)
    ]
    records.sort(key=lambda r: r["githubUrl"])
    return records


def main(
    tools_yml: Path = TOOLS_YML,
    trendshift_file: Path = TREND_SHIFT_FILE,
    trendshift_repos_file: Path = TREND_SHIFT_REPOS_FILE,
    fetcher: Callable[[tuple[str, str], dict], str | None] = fetch_readme,
    page_fetcher: Callable[[str, dict | None], str | None] = fetch_url,
    badge_fetcher: Callable[[str, dict | None], str | None] = fetch_url,
    languages: tuple[str, ...] | None = TREND_LANGUAGES,
    alive_checker: Callable[[tuple[str, str], dict], tuple] | None = check_repo_alive,
    meta_file: Path | None = META_FILE,
) -> int:
    tools = load_tools(tools_yml)
    previous_cache = load_json_or_default(trendshift_file, {}) or {}
    # repos-meta.json: update_stars уже положил сюда {stars, archived, ...} для
    # всех репо (tools.yml + trendshift-repos). _prune берёт archived/stars
    # отсюда (0 API), alive-check — только для отсутствующих (см. _prune_dead_new_repos).
    meta = load_json_or_default(meta_file, {}) if meta_file is not None else None
    updated_at = datetime.date.today().isoformat()
    # README-фетч (raw.githubusercontent.com) идёт через github_headers() — там
    # нужен Accept+GITHUB_TOKEN для повышенного rate-лимита. trendshift-страницы и
    # бейджи идут через тот же fetch_url, но с headers=None → _DEFAULT_HEADERS с
    # User-Agent (trendshift.io отдаёт 403 без UA). Проброс headers=None в
    # enrich_from_rankings гарантирует UA для trendshift, не затрагивая README.
    gh_headers = github_headers()
    # Сохраняем ранее собранные trendshift-only репо: при частичном/полном
    # outage trendshift.io свежий new_repos будет пустым, и без сида мы
    # перезаписали бы trendshift-repos.json на [] — потеряв всю коллекцию.
    # Сида по githubUrl позволяет merge_trendshift_entry обновить записи
    # на месте, а при сбое — сохранить прежние (симметрия с previous_cache).
    # Важно: категория/categoryReason/categoryAt и др. обогащающие поля на сиде
    # сохраняются — merge_trendshift_entry их не трогает (правит только badges).
    new_repos: dict[str, dict] = {}
    for rec in load_json_or_default(trendshift_repos_file, []) or []:
        if isinstance(rec, dict) and isinstance(rec.get("githubUrl"), str):
            url = rec["githubUrl"]
            entry = {k: v for k, v in rec.items() if k != "githubUrl"}
            new_repos[url] = entry
    cache = update_trendshift_cache(
        tools, previous_cache, updated_at, gh_headers, fetcher,
        page_fetcher, badge_fetcher, new_repos=new_repos,
        languages=languages, alive_checker=alive_checker, meta=meta,
    )
    trendshift_file.parent.mkdir(parents=True, exist_ok=True)
    trendshift_file.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    repos_records = _serialize_repos_cache(new_repos)
    trendshift_repos_file.parent.mkdir(parents=True, exist_ok=True)
    trendshift_repos_file.write_text(
        json.dumps(repos_records, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Trendshift badges: {len(cache)} repos (+ {len(repos_records)} "
          f"new trendshift-only repos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
