"""Tests for Trendshift README badge extraction and generated cache behavior."""
import json

import yaml

from update_trendshift import (
    extract_trendshift_entry,
    main,
    update_trendshift_cache,
)


README_WITH_TRENDSHIFT = """
<a href="https://trendshift.io/repositories/50668">
  <img src="https://trendshift.io/api/badge/trendshift/repositories/50668/daily" />
</a>
<a href="https://trendshift.io/repositories/50668">
  <img src="https://trendshift.io/api/badge/trendshift/repositories/50668/weekly" />
</a>
"""


def test_extract_trendshift_entry_daily_and_weekly():
    entry = extract_trendshift_entry(README_WITH_TRENDSHIFT, "2026-07-04")

    assert entry == {
        "trendshiftId": "50668",
        "pageUrl": "https://trendshift.io/repositories/50668",
        "badges": [
            {
                "kind": "day",
                "badgeUrl": "https://trendshift.io/api/badge/trendshift/repositories/50668/daily",
            },
            {
                "kind": "week",
                "badgeUrl": "https://trendshift.io/api/badge/trendshift/repositories/50668/weekly",
            },
        ],
        "updatedAt": "2026-07-04",
    }


def test_extract_trendshift_entry_ignores_non_trendshift_badges():
    readme = """
    ![stars](https://img.shields.io/github/stars/DietrichGebert/ponytail)
    ![npm](https://img.shields.io/npm/v/@dietrichgebert/ponytail)
    """

    assert extract_trendshift_entry(readme, "2026-07-04") is None


def test_extract_trendshift_entry_prefers_plain_repository_badge():
    readme = """
    <a href="https://trendshift.io/repositories/50668">
      <img src="https://trendshift.io/api/badge/trendshift/repositories/50668/weekly?language=JavaScript" />
      <img src="https://trendshift.io/api/badge/trendshift/repositories/50668/weekly" />
    </a>
    """

    entry = extract_trendshift_entry(readme, "2026-07-04")

    assert entry["badges"] == [
        {
            "kind": "week",
            "badgeUrl": "https://trendshift.io/api/badge/trendshift/repositories/50668/weekly",
        }
    ]


def test_update_trendshift_cache_preserves_previous_entry_on_fetch_failure():
    url = "https://github.com/DietrichGebert/ponytail"
    previous = {
        url: {
            "trendshiftId": "50668",
            "pageUrl": "https://trendshift.io/repositories/50668",
            "badges": [{"kind": "week", "badgeUrl": "old"}],
            "updatedAt": "2026-07-03",
        }
    }
    tools = [{"name": "ponytail", "url": url}]

    cache = update_trendshift_cache(
        tools,
        previous,
        "2026-07-04",
        {},
        fetcher=lambda slug, headers: None,
    )

    assert cache == previous


def test_main_writes_cache_without_changing_tools_yml(tmp_path):
    tools_yml = tmp_path / "tools.yml"
    trendshift_file = tmp_path / "trendshift.json"
    tool = {
        "name": "ponytail",
        "url": "https://github.com/DietrichGebert/ponytail",
        "category": "workflow-automation",
        "description": {"en": "Tool", "ru": "Утилита"},
    }
    tools_yml.write_text(
        yaml.safe_dump({"tools": [tool]}, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    before = tools_yml.read_text(encoding="utf-8")

    main(
        tools_yml=tools_yml,
        trendshift_file=trendshift_file,
        fetcher=lambda slug, headers: README_WITH_TRENDSHIFT,
    )

    assert tools_yml.read_text(encoding="utf-8") == before
    cache = json.loads(trendshift_file.read_text(encoding="utf-8"))
    assert list(cache) == ["https://github.com/DietrichGebert/ponytail"]
    assert cache["https://github.com/DietrichGebert/ponytail"]["trendshiftId"] == "50668"
