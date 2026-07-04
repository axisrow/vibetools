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
from pathlib import Path
from typing import Callable

import requests

ROOT = Path(__file__).resolve().parent.parent
TOOLS_YML = ROOT / "data" / "tools.yml"
TREND_SHIFT_FILE = ROOT / "data" / "trendshift.json"
RAW_README = "https://raw.githubusercontent.com/{owner}/{repo}/HEAD/README.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import github_headers, github_slug, load_json_or_default  # noqa: E402
from generate_readme import load_tools  # noqa: E402

PAGE_RE = re.compile(r"https://trendshift\.io/repositories/(?P<id>\d+)")
BADGE_RE = re.compile(
    r"https://trendshift\.io/api/badge/trendshift/repositories/"
    r"(?P<id>\d+)/(?P<window>daily|weekly)(?:\?[^\s\"'<>)]*)?"
)
KIND_BY_WINDOW = {"daily": "day", "weekly": "week"}
KIND_ORDER = {"day": 0, "week": 1}


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
            badges_by_kind[kind] = {"kind": kind, "badgeUrl": badge_url}

    badges = sorted(badges_by_kind.values(), key=lambda b: KIND_ORDER[b["kind"]])
    if not badges:
        return None

    return {
        "trendshiftId": trendshift_id,
        "pageUrl": f"https://trendshift.io/repositories/{trendshift_id}",
        "badges": badges,
        "updatedAt": updated_at,
    }


def update_trendshift_cache(
    tools: list[dict],
    previous_cache: dict,
    updated_at: str,
    headers: dict,
    fetcher: Callable[[tuple[str, str], dict], str | None] = fetch_readme,
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
            next_cache[url] = entry
    return next_cache


def main(
    tools_yml: Path = TOOLS_YML,
    trendshift_file: Path = TREND_SHIFT_FILE,
    fetcher: Callable[[tuple[str, str], dict], str | None] = fetch_readme,
) -> int:
    tools = load_tools(tools_yml)
    previous_cache = load_json_or_default(trendshift_file, {}) or {}
    updated_at = datetime.date.today().isoformat()
    cache = update_trendshift_cache(
        tools, previous_cache, updated_at, github_headers(), fetcher
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
