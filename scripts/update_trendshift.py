#!/usr/bin/env python3
"""
Find Trendshift achievements published by tool authors in upstream READMEs.

This is an enrichment cache, not a human-curated source. data/tools.yml stays
limited to name/url/category/description, while Trendshift metadata lives in
data/trendshift.json and can disappear without breaking the site.
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
RAW_README = "https://raw.githubusercontent.com/{owner}/{repo}/HEAD/README.md"
TREND_SHIFT_PAGE = "https://trendshift.io/repositories/{id}"
TREND_SHIFT_BADGE = "https://trendshift.io/api/badge/trendshift/repositories/{id}/{window}"
RANKING_WINDOWS = {
    "day": ("https://trendshift.io/", "daily"),
    "week": ("https://trendshift.io/weekly", "weekly"),
    "month": ("https://trendshift.io/monthly", "monthly"),
    "year": ("https://trendshift.io/yearly", "yearly"),
}

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import github_headers, github_slug, load_json_or_default  # noqa: E402
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
    """Fetch an arbitrary Trendshift/GitHub text URL."""
    try:
        response = requests.get(url, headers=headers or {}, timeout=10)
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


def enrich_from_rankings(
    tools: list[dict],
    cache: dict,
    updated_at: str,
    page_fetcher: Callable[[str, dict | None], str | None] = fetch_url,
    badge_fetcher: Callable[[str, dict | None], str | None] = fetch_url,
) -> dict:
    """Add matching repos discovered from Trendshift ranking pages."""
    by_url = {tool.get("url"): tool for tool in tools}
    for kind, (page_url, badge_window) in RANKING_WINDOWS.items():
        html = page_fetcher(page_url, None)
        if html is None:
            continue
        for entry in extract_ranking_entries(html, kind, updated_at):
            github_url = entry["githubUrl"]
            if github_url not in by_url:
                continue
            trendshift_id = entry["trendshiftId"]
            badge_url = TREND_SHIFT_BADGE.format(id=trendshift_id, window=badge_window)
            svg = badge_fetcher(badge_url, None)
            rank = extract_badge_rank(svg or "")
            if rank is None:
                continue
            badge = entry["badges"][0]
            badge["badgeUrl"] = badge_url
            badge["rank"] = rank
            cache[github_url] = merge_trendshift_entry(cache.get(github_url), entry)
    return cache


def update_trendshift_cache(
    tools: list[dict],
    previous_cache: dict,
    updated_at: str,
    headers: dict,
    fetcher: Callable[[tuple[str, str], dict], str | None] = fetch_readme,
    page_fetcher: Callable[[str, dict | None], str | None] = fetch_url,
    badge_fetcher: Callable[[str, dict | None], str | None] = fetch_url,
    workers: int = 16,
) -> dict:
    """Build a fresh cache and preserve previous entries on fetch failures."""
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
    return enrich_from_rankings(tools, next_cache, updated_at, page_fetcher, badge_fetcher)


def main(
    tools_yml: Path = TOOLS_YML,
    trendshift_file: Path = TREND_SHIFT_FILE,
    fetcher: Callable[[tuple[str, str], dict], str | None] = fetch_readme,
    page_fetcher: Callable[[str, dict | None], str | None] = fetch_url,
    badge_fetcher: Callable[[str, dict | None], str | None] = fetch_url,
) -> int:
    tools = load_tools(tools_yml)
    previous_cache = load_json_or_default(trendshift_file, {}) or {}
    updated_at = datetime.date.today().isoformat()
    cache = update_trendshift_cache(
        tools, previous_cache, updated_at, github_headers(), fetcher,
        page_fetcher, badge_fetcher
    )
    trendshift_file.parent.mkdir(parents=True, exist_ok=True)
    trendshift_file.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Trendshift badges: {len(cache)} repos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
