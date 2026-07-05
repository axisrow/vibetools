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


def _alive_ok(slug, headers):
    """alive_checker-заглушка: все репо живые, 100 звёзд — фильтр не выкидывает."""
    return "alive", {"stars": 100, "archived": False}


def test_main_writes_cache_without_changing_tools_yml(tmp_path):
    tools_yml = tmp_path / "tools.yml"
    trendshift_file = tmp_path / "trendshift.json"
    trendshift_repos_file = tmp_path / "trendshift-repos.json"
    tool = {
        "name": "ponytail",
        "url": "https://github.com/DietrichGebert/ponytail",
        "category": "agent-skills-prompts",
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
        alive_checker=_alive_ok,
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
        "category": "agent-skills-prompts",
        "description": {"en": "Tool", "ru": "Утилита"},
    }
    tools_yml.write_text(
        yaml.safe_dump({"tools": [tool]}, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    # weekly-страница содержит И tools.yml-репо (ponytail), И новое (foo/bar).
    html = _ranking_html([
        ("50668", "ponytail", "https://github.com/DietrichGebert/ponytail"),
        ("25391", "foo/bar", "https://github.com/foo/bar"),
    ])

    main(
        tools_yml=tools_yml,
        trendshift_file=trendshift_file,
        trendshift_repos_file=trendshift_repos_file,
        fetcher=lambda slug, headers: None,  # README не нужен — rankings всё дают
        page_fetcher=lambda url, h: html,
        badge_fetcher=lambda url, h: RANK_SVG,
        alive_checker=_alive_ok,
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


# ---- stage 2: per-language × 4 windows harvest ----

def test_enrich_from_rankings_iterates_languages_when_given():
    """languages=("Python",) → page_fetcher зовётся с ?language=Python на каждом окне."""
    tools = []
    fetched_urls = []

    def page_fetcher(url, headers):
        fetched_urls.append(url)
        # Отдаём одну и ту же запись на каждой странице — достаточно проверить URL.
        return _ranking_html([("1", "foo/bar", "https://github.com/foo/bar")])

    enrich_from_rankings(
        tools, {}, "2026-07-05",
        page_fetcher=page_fetcher,
        badge_fetcher=lambda url, h: None,  # без ранга → не декорируется
        new_repos={},
        languages=("Python",),
    )

    # 4 глобальных + 4 per-language (Python × 4 окна).
    assert len(fetched_urls) == 8
    lang_urls = [u for u in fetched_urls if "?language=Python" in u]
    assert len(lang_urls) == 4
    # Все 4 окна покрыты per-language.
    assert any(u == "https://trendshift.io/?language=Python" for u in lang_urls)
    assert any(u == "https://trendshift.io/weekly?language=Python" for u in lang_urls)
    assert any(u == "https://trendshift.io/monthly?language=Python" for u in lang_urls)
    assert any(u == "https://trendshift.io/yearly?language=Python" for u in lang_urls)


def test_enrich_from_rankings_no_languages_is_legacy():
    """languages=None → только 4 глобальные страницы, без ?language= (backward compat)."""
    tools = []
    fetched_urls = []

    enrich_from_rankings(
        tools, {}, "2026-07-05",
        page_fetcher=lambda url, h: fetched_urls.append(url) or "<script></script>",
        badge_fetcher=lambda url, h: None,
        new_repos={},
        languages=None,
    )

    assert len(fetched_urls) == 4
    assert not any("?language=" in u for u in fetched_urls)


def test_enrich_from_rankings_passes_headers_to_fetchers():
    """headers прокидывается в page_fetcher и badge_fetcher (не None)."""
    seen_page_headers = []
    seen_badge_headers = []
    headers = {"User-Agent": "test-ua/1.0"}

    def page_fetcher(url, h):
        seen_page_headers.append(h)
        return _ranking_html([("1", "foo/bar", "https://github.com/foo/bar")])

    def badge_fetcher(url, h):
        seen_badge_headers.append(h)
        return RANK_SVG

    enrich_from_rankings(
        [], {}, "2026-07-05",
        page_fetcher=page_fetcher, badge_fetcher=badge_fetcher,
        new_repos={}, languages=None, headers=headers,
    )

    assert seen_page_headers and all(h is headers for h in seen_page_headers)
    assert seen_badge_headers and all(h is headers for h in seen_badge_headers)


def test_enrich_from_rankings_dedup_across_language_windows():
    """Один url на двух языках × два окна → одна запись, badges слиты."""
    tools = []
    repo_url = "https://github.com/foo/bar"
    week_html = _ranking_html([("25391", "foo/bar", repo_url)])

    pages = {
        "https://trendshift.io/weekly?language=Python": week_html,
        "https://trendshift.io/weekly?language=TypeScript": week_html,
    }

    new_repos = {}
    enrich_from_rankings(
        tools, {}, "2026-07-05",
        page_fetcher=lambda url, h: pages.get(url, "<script></script>"),
        badge_fetcher=lambda url, h: RANK_SVG,
        new_repos=new_repos, languages=("Python", "TypeScript"),
    )

    # Один url → одна запись (дедуп по githubUrl через merge_trendshift_entry).
    assert list(new_repos) == [repo_url]
    # kind=week один (оба окна weekly), merge сохранил сильнейший ранг.
    badges = new_repos[repo_url]["badges"]
    assert len(badges) == 1
    assert badges[0]["kind"] == "week"


def test_main_seeds_new_repos_preserving_category(tmp_path):
    """При outage (все fetcher→None) категория на сиде выживает (фикс #16 + stage 3)."""
    tools_yml = tmp_path / "tools.yml"
    trendshift_file = tmp_path / "trendshift.json"
    trendshift_repos_file = tmp_path / "trendshift-repos.json"
    tools_yml.write_text(
        yaml.safe_dump({"tools": []}, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    # Сид: одна запись с уже проставленной категорией (из stage 3).
    trendshift_repos_file.write_text(
        json.dumps([{
            "githubUrl": "https://github.com/foo/bar",
            "trendshiftId": "25391",
            "pageUrl": "https://trendshift.io/repositories/25391",
            "badges": [{"kind": "week", "rank": 5, "source": "ranking"}],
            "updatedAt": "2026-07-04",
            "category": "cli-agents",
            "categoryReason": "topic:ai-agent",
        }]),
        encoding="utf-8",
    )

    main(
        tools_yml=tools_yml,
        trendshift_file=trendshift_file,
        trendshift_repos_file=trendshift_repos_file,
        fetcher=lambda slug, headers: None,       # outage README
        page_fetcher=lambda url, headers: None,   # outage trendshift pages
        badge_fetcher=lambda url, headers: None,  # outage badges
        languages=("Python",),
        alive_checker=lambda slug, h: ("unknown", None),  # outage alive-check → сохранить
    )

    repos = json.loads(trendshift_repos_file.read_text(encoding="utf-8"))
    # Запись сохранилась (не выкинута при outage)...
    assert [r["githubUrl"] for r in repos] == ["https://github.com/foo/bar"]
    # ...и category/categoryReason пережили перезапись (merge их не трогает).
    rec = repos[0]
    assert rec["category"] == "cli-agents"
    assert rec["categoryReason"] == "topic:ai-agent"


def test_language_url_segment_for_csharp_and_cpp():
    """C#→C%23, C++→C%2B%2B в URL; обычные языки — identity."""
    from update_trendshift import _LANGUAGE_URL_SEGMENT, _ranking_pages

    pages = {(kind, url) for kind, url, _ in _ranking_pages(("C#", "C++", "Python"))}
    # C# кодируется как %23, C++ как %2B%2B, Python — как есть.
    assert any("?language=C%23" in url for _, url in pages), \
        f"C# segment not URL-encoded: {_LANGUAGE_URL_SEGMENT.get('C#')}"
    assert any("?language=C%2B%2B" in url for _, url in pages), \
        f"C++ segment not URL-encoded: {_LANGUAGE_URL_SEGMENT.get('C++')}"
    assert any("?language=Python" in url for _, url in pages)


def test_enrich_from_rankings_keeps_repo_when_badge_unavailable():
    """badge_fetcher→None (outage / отключен) → репо всё равно собирается с currentRank.

    Без badge SVG нельзя вытащить точный ранг, но ItemList уже даёт currentRank
    (позиция в рейтинге). Репо не должно теряться — иначе harvest без медленных
    badge-фетчей терял бы все записи, а частичный outage trendshift-badge выкашивал бы каталог.
    """
    tools = []
    html = _ranking_html([("25391", "foo/bar", "https://github.com/foo/bar")])
    new_repos = {}
    enrich_from_rankings(
        tools, {}, "2026-07-05",
        page_fetcher=lambda url, h: html,
        badge_fetcher=lambda url, h: None,  # badge недоступен
        new_repos=new_repos, languages=None,
    )
    # Репо собрано (не выкинуто), currentRank пришёл из ItemList.
    assert list(new_repos) == ["https://github.com/foo/bar"]
    badge = new_repos["https://github.com/foo/bar"]["badges"][0]
    assert badge.get("currentRank") == 1  # из ItemList position
    assert "rank" not in badge  # точного ранга из SVG нет
    assert "badgeUrl" not in badge  # badgeUrl не приделан (SVG не получен)


# ---- 404-валидатор: _prune_dead_new_repos (фильтр мёртвых/пустых репо) ----

from update_trendshift import _prune_dead_new_repos, MIN_STARS  # noqa: E402


def _alive_map(by_repo: dict):
    """Создаёт alive_checker по таблице {repo: (status, meta)}.
    slug → lookup по имени репо; неизвестные → alive(10 звёзд)."""
    def checker(slug, headers):
        _, repo = slug
        return by_repo.get(repo, ("alive", {"stars": 10, "archived": False}))
    return checker


def test_prune_removes_dead_repos():
    """dead (404) → выкидывается из new_repos."""
    new_repos = {
        "https://github.com/foo/alive": {"trendshiftId": "1"},
        "https://github.com/foo/dead": {"trendshiftId": "2"},
    }
    checker = _alive_map({"dead": ("dead", None)})
    _prune_dead_new_repos(new_repos, {}, checker, workers=1)
    assert list(new_repos) == ["https://github.com/foo/alive"]


def test_prune_removes_archived_repos():
    """alive + archived=True → выкидывается (заброшенные)."""
    new_repos = {
        "https://github.com/foo/ok": {},
        "https://github.com/foo/old": {},
    }
    checker = _alive_map({"old": ("alive", {"stars": 50, "archived": True})})
    _prune_dead_new_repos(new_repos, {}, checker, workers=1)
    assert list(new_repos) == ["https://github.com/foo/ok"]


def test_prune_removes_low_stars_via_min_stars():
    """alive + stars < min_stars → выкидывается (пустой шум)."""
    new_repos = {
        "https://github.com/foo/big": {},
        "https://github.com/foo/small": {},
    }
    checker = _alive_map({
        "big": ("alive", {"stars": 100, "archived": False}),
        "small": ("alive", {"stars": 5, "archived": False}),
    })
    _prune_dead_new_repos(new_repos, {}, checker, workers=1, min_stars=10)
    assert list(new_repos) == ["https://github.com/foo/big"]


def test_prune_keeps_unknown_repos():
    """unknown (rate-limit/timeout) → НЕ выкидывается (обрыв ≠ мёртвый)."""
    new_repos = {
        "https://github.com/foo/ok": {},
        "https://github.com/foo/net": {},
    }
    checker = _alive_map({"net": ("unknown", None)})
    _prune_dead_new_repos(new_repos, {}, checker, workers=1)
    assert set(new_repos) == {"https://github.com/foo/ok", "https://github.com/foo/net"}


def test_prune_noop_on_empty():
    """Пустой new_repos → никаких запросов, остаётся пустым."""
    calls = []

    def checker(slug, headers):
        calls.append(slug)
        return "alive", {"stars": 1, "archived": False}

    new_repos = {}
    _prune_dead_new_repos(new_repos, {}, checker, workers=1)
    assert new_repos == {}
    assert calls == []


def test_prune_skips_non_github_urls():
    """url без github.com (slug → None) не доходит до alive_checker."""
    seen = []

    def checker(slug, headers):
        seen.append(slug)
        return "alive", {"stars": 1, "archived": False}

    new_repos = {"https://example.com/notgithub": {}}
    _prune_dead_new_repos(new_repos, {}, checker, workers=1)
    assert list(new_repos) == ["https://example.com/notgithub"]  # сохранён без проверки
    assert seen == []


def test_prune_min_stars_default_is_module_constant():
    """min_stars по умолчанию = MIN_STARS (0 = принимать любые живые)."""
    new_repos = {"https://github.com/foo/zero": {}}
    checker = _alive_map({"zero": ("alive", {"stars": 0, "archived": False})})
    _prune_dead_new_repos(new_repos, {}, checker, workers=1)  # без min_stars
    assert list(new_repos) == ["https://github.com/foo/zero"]  # 0 < 0 → False, остаётся
    assert MIN_STARS == 0


def test_update_trendshift_cache_prunes_via_injected_alive_checker():
    """update_trendshift_cache(alive_checker=...) выкидывает dead из new_repos."""
    tools = []
    html = _ranking_html([
        ("1", "foo/alive", "https://github.com/foo/alive"),
        ("2", "foo/dead", "https://github.com/foo/dead"),
    ])
    new_repos = {}
    update_trendshift_cache(
        tools, {}, "2026-07-05", {},
        fetcher=lambda slug, h: None,
        page_fetcher=lambda url, h: html,
        badge_fetcher=lambda url, h: None,
        new_repos=new_repos,
        alive_checker=_alive_map({"dead": ("dead", None)}),
    )
    assert list(new_repos) == ["https://github.com/foo/alive"]


def test_update_trendshift_cache_no_alive_checker_is_legacy():
    """Без alive_checker фильтр не запускается — dead репо остаётся (legacy)."""
    tools = []
    html = _ranking_html([("1", "foo/dead", "https://github.com/foo/dead")])
    new_repos = {}
    update_trendshift_cache(
        tools, {}, "2026-07-05", {},
        fetcher=lambda slug, h: None,
        page_fetcher=lambda url, h: html,
        badge_fetcher=lambda url, h: None,
        new_repos=new_repos,
        # alive_checker не передаётся → фильтр отключен
    )
    assert list(new_repos) == ["https://github.com/foo/dead"]

