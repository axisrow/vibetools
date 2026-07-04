"""Tests for Trendshift README badge extraction and generated cache behavior."""
import datetime
import json

import yaml

from update_trendshift import (
    _decorate_ranking_entry,
    enrich_from_rankings,
    extract_badge_rank,
    extract_ranking_entries,
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
                "source": "readme",
            },
            {
                "kind": "week",
                "badgeUrl": "https://trendshift.io/api/badge/trendshift/repositories/50668/weekly",
                "source": "readme",
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
            "source": "readme",
        }
    ]


def test_extract_badge_rank_from_svg_aria_label():
    svg = '<svg aria-label="Trendshift: number 5 repository of the week"></svg>'

    assert extract_badge_rank(svg) == 5


def test_extract_ranking_entries_from_json_ld_item_list():
    html = """
    <script type="application/ld+json">
    {
      "@type": "ItemList",
      "itemListElement": [{
        "@type": "ListItem",
        "position": 5,
        "url": "https://trendshift.io/repositories/25391",
        "item": {
          "@type": "SoftwareSourceCode",
          "name": "JuliusBrussee/caveman",
          "codeRepository": "https://github.com/JuliusBrussee/caveman"
        }
      }]
    }
    </script>
    """

    assert extract_ranking_entries(html, "week", "2026-07-04") == [{
        "githubUrl": "https://github.com/JuliusBrussee/caveman",
        "trendshiftId": "25391",
        "pageUrl": "https://trendshift.io/repositories/25391",
        "badges": [{
            "kind": "week",
            "currentRank": 5,
            "source": "ranking",
        }],
        "updatedAt": "2026-07-04",
    }]


def test_enrich_from_rankings_adds_ranked_badge_for_matching_tool():
    tools = [{"name": "caveman", "url": "https://github.com/JuliusBrussee/caveman"}]
    weekly_html = """
    <script type="application/ld+json">
    {"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":5,
    "url":"https://trendshift.io/repositories/25391","item":{"@type":"SoftwareSourceCode",
    "name":"JuliusBrussee/caveman","codeRepository":"https://github.com/JuliusBrussee/caveman"}}]}
    </script>
    """

    def page_fetcher(url, headers):
        return weekly_html if url.endswith("/weekly") else "<script type=\"application/ld+json\">{\"@type\":\"ItemList\",\"itemListElement\":[]}</script>"

    def badge_fetcher(url, headers):
        return '<svg aria-label="Trendshift: number 5 repository of the week"></svg>'

    cache = enrich_from_rankings(tools, {}, "2026-07-04", page_fetcher, badge_fetcher)

    assert cache == {
        "https://github.com/JuliusBrussee/caveman": {
            "trendshiftId": "25391",
            "pageUrl": "https://trendshift.io/repositories/25391",
            "badges": [{
                "kind": "week",
                "currentRank": 5,
                "source": "ranking",
                "badgeUrl": "https://trendshift.io/api/badge/trendshift/repositories/25391/weekly",
                "rank": 5,
            }],
            "updatedAt": "2026-07-04",
        }
    }


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
        page_fetcher=lambda url, headers: None,
        badge_fetcher=lambda url, headers: None,
    )

    assert cache == previous


def test_main_writes_cache_without_changing_tools_yml(tmp_path):
    tools_yml = tmp_path / "tools.yml"
    trendshift_file = tmp_path / "trendshift.json"
    trendshift_repos_file = tmp_path / "trendshift-repos.json"
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
        trendshift_repos_file=trendshift_repos_file,
        fetcher=lambda slug, headers: README_WITH_TRENDSHIFT,
        page_fetcher=lambda url, headers: None,
        badge_fetcher=lambda url, headers: None,
    )

    assert tools_yml.read_text(encoding="utf-8") == before
    cache = json.loads(trendshift_file.read_text(encoding="utf-8"))
    assert list(cache) == ["https://github.com/DietrichGebert/ponytail"]
    assert cache["https://github.com/DietrichGebert/ponytail"]["trendshiftId"] == "50668"
    # Новый кэш пишется всегда (даже пустой) и живёт в tmp — не в source tree.
    assert json.loads(trendshift_repos_file.read_text(encoding="utf-8")) == []


# ---- trendshift-repos cache: collect ALL ranking repos (этап 1) ----

def _ranking_html(entries):
    """Сборка JSON-LD ItemList страницы trendshift для нескольких репо."""
    items = ",".join(
        '{"@type":"ListItem","position":%d,"url":"https://trendshift.io/repositories/%s",'
        '"item":{"@type":"SoftwareSourceCode","name":"%s","codeRepository":"%s"}}'
        % (pos, tid, name, url)
        for pos, (tid, name, url) in enumerate(entries, 1)
    )
    return (
        '<script type="application/ld+json">'
        + '{"@type":"ItemList","itemListElement":[' + items + "]}"
        + "</script>"
    )


RANK_SVG = '<svg aria-label="Trendshift: number 5 repository of the week"></svg>'


def test_decorate_ranking_entry_returns_none_when_unranked():
    entry = {
        "githubUrl": "https://github.com/foo/bar",
        "trendshiftId": "25391",
        "pageUrl": "https://trendshift.io/repositories/25391",
        "badges": [{"kind": "week", "currentRank": 5, "source": "ranking"}],
        "updatedAt": "2026-07-04",
    }

    # badge_fetcher вернул None (сеть/404) → ранг не извлечь → None.
    assert _decorate_ranking_entry(entry, "weekly", lambda url, h: None) is None


def test_enrich_from_rankings_collects_unknown_repos_into_new_repos():
    """Репо НЕ из tools.yml попадает в new_repos (а не дропается)."""
    tools = [{"name": "ponytail", "url": "https://github.com/DietrichGebert/ponytail"}]
    weekly_html = _ranking_html([("25391", "foo/bar", "https://github.com/foo/bar")])

    new_repos = {}
    cache = enrich_from_rankings(
        tools, {}, "2026-07-04",
        # html есть только на weekly-странице → badge получает kind="week".
        page_fetcher=lambda url, h: weekly_html if url.endswith("/weekly") else "<script></script>",
        badge_fetcher=lambda url, h: RANK_SVG,
        new_repos=new_repos,
    )

    assert cache == {}  # репо нет в tools → в cache ничего не попало
    assert list(new_repos) == ["https://github.com/foo/bar"]
    entry = new_repos["https://github.com/foo/bar"]
    assert entry["trendshiftId"] == "25391"
    badge = entry["badges"][0]
    assert badge["kind"] == "week"
    assert badge["rank"] == 5
    assert badge["badgeUrl"] == "https://trendshift.io/api/badge/trendshift/repositories/25391/weekly"


def test_enrich_from_rankings_backward_compat_no_new_repos_arg():
    """Без new_repos неизвестные репо по-прежнему дропаются (legacy behavior)."""
    tools = [{"name": "ponytail", "url": "https://github.com/DietrichGebert/ponytail"}]
    html = _ranking_html([("25391", "foo/bar", "https://github.com/foo/bar")])

    cache = enrich_from_rankings(
        tools, {}, "2026-07-04",
        page_fetcher=lambda url, h: html,
        badge_fetcher=lambda url, h: RANK_SVG,
        # new_repos не передаём
    )

    assert cache == {}


def test_enrich_from_rankings_merges_badges_across_windows():
    """Один url на двух окнах (week + month) → одна запись с двумя badges."""
    tools = []
    week_html = _ranking_html([("25391", "foo/bar", "https://github.com/foo/bar")])
    month_html = _ranking_html([("25391", "foo/bar", "https://github.com/foo/bar")])

    pages = {
        "https://trendshift.io/weekly": week_html,
        "https://trendshift.io/monthly": month_html,
    }

    new_repos = {}
    enrich_from_rankings(
        tools, {}, "2026-07-04",
        page_fetcher=lambda url, h: pages.get(url, "<script></script>"),
        badge_fetcher=lambda url, h: RANK_SVG,
        new_repos=new_repos,
    )

    assert list(new_repos) == ["https://github.com/foo/bar"]
    kinds = sorted(b["kind"] for b in new_repos["https://github.com/foo/bar"]["badges"])
    assert kinds == ["month", "week"]


def test_main_writes_trendshift_repos_file(tmp_path):
    """main() пишет trendshift-repos.json (list, отсортирован по url) и не
    пересекается по url с trendshift.json (инвариант: tools.yml-репо — только
    в trendshift.json)."""
    tools_yml = tmp_path / "tools.yml"
    trendshift_file = tmp_path / "trendshift.json"
    trendshift_repos_file = tmp_path / "trendshift-repos.json"
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

    # weekly-страница содержит И tools.yml-репо (ponytail), И новое (foo/bar).
    html = (
        '<script type="application/ld+json">'
        '{"@type":"ItemList","itemListElement":['
        '{"@type":"ListItem","position":1,"url":"https://trendshift.io/repositories/50668",'
        '"item":{"@type":"SoftwareSourceCode","name":"ponytail",'
        '"codeRepository":"https://github.com/DietrichGebert/ponytail"}},'
        '{"@type":"ListItem","position":5,"url":"https://trendshift.io/repositories/25391",'
        '"item":{"@type":"SoftwareSourceCode","name":"foo/bar",'
        '"codeRepository":"https://github.com/foo/bar"}}'
        "]}</script>"
    )

    main(
        tools_yml=tools_yml,
        trendshift_file=trendshift_file,
        trendshift_repos_file=trendshift_repos_file,
        fetcher=lambda slug, headers: None,  # README не нужен — rankings всё дают
        page_fetcher=lambda url, h: html,
        badge_fetcher=lambda url, h: RANK_SVG,
    )

    cache = json.loads(trendshift_file.read_text(encoding="utf-8"))
    repos = json.loads(trendshift_repos_file.read_text(encoding="utf-8"))

    # Инвариант: tools.yml-репо обогатилось в trendshift.json...
    assert "https://github.com/DietrichGebert/ponytail" in cache
    # ...а новое попало в trendshift-repos.json...
    assert [r["githubUrl"] for r in repos] == ["https://github.com/foo/bar"]
    # ...и множества url не пересекаются.
    cache_urls = set(cache)
    repos_urls = {r["githubUrl"] for r in repos}
    assert cache_urls.isdisjoint(repos_urls)
    # Запись несёт badges + идентификаторы.
    rec = repos[0]
    assert rec["trendshiftId"] == "25391"
    assert rec["pageUrl"] == "https://trendshift.io/repositories/25391"
    assert rec["badges"][0]["rank"] == 5
    assert rec["updatedAt"] == datetime.date.today().isoformat()
