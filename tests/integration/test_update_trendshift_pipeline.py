"""Integration: update_trendshift.main() end-to-end через tmp_repo + mock fetchers.

Фильтр мёртвых/пустых репо (404-валидатор) применяется к автособранному
trendshift-repos.json, но НЕ к курируемому tools.yml → trendshift.json.
Все fetcher-ы и alive_checker инъецированы → 0 сетевых вызовов.
"""
import json

import responses

from common import GITHUB_REPO_API
from update_trendshift import main as ts_main

# tools.yml-репо из conftest.tmp_repo.
PONYTAIL_URL = "https://github.com/DietrichGebert/ponytail"  # для теста ниже нет;
# используем tmp_repo-репо напрямую через фикстуру.

RANK_SVG = '<svg aria-label="Trendshift: number 3 repository of the week"></svg>'


def _ranking_html(entries):
    """JSON-LD ItemList для нескольких репо: entries=[(trendshiftId, name, url), ...]."""
    items = ",".join(
        '{"@type":"ListItem","position":%d,"url":"https://trendshift.io/repositories/%s",'
        '"item":{"@type":"SoftwareSourceCode","name":"%s","codeRepository":"%s"}}'
        % (pos, tid, name, url)
        for pos, (tid, name, url) in enumerate(entries, 1)
    )
    return (
        '<script type="application/ld+json">'
        + '{"@type":"ItemList","itemListElement":[' + items + ']}'
        + "</script>"
    )


def _read_repos(tmp_repo):
    return json.loads(tmp_repo["trendshift_repos_file"].read_text(encoding="utf-8"))


def _read_cache(tmp_repo):
    return json.loads(tmp_repo["trendshift_file"].read_text(encoding="utf-8"))


def test_pipeline_prunes_dead_keeps_alive(tmp_repo):
    """main() выкидывает dead (404), сохраняет alive — через injected alive_checker."""
    alive_url = "https://github.com/foo/alive"
    dead_url = "https://github.com/foo/dead"
    # weekly-страница содержит оба репо (не из tools.yml → попадают в new_repos).
    html = _ranking_html([
        ("1", "foo/alive", alive_url),
        ("2", "foo/dead", dead_url),
    ])

    def alive_checker(slug, headers):
        _, repo = slug
        if repo == "dead":
            return "dead", None
        return "alive", {"stars": 50, "archived": False}

    ts_main(
        tools_yml=tmp_repo["tools_yml"],
        trendshift_file=tmp_repo["trendshift_file"],
        trendshift_repos_file=tmp_repo["trendshift_repos_file"],
        fetcher=lambda slug, h: None,
        page_fetcher=lambda url, h: html,
        badge_fetcher=lambda url, h: RANK_SVG,
        alive_checker=alive_checker,
    )

    repos = _read_repos(tmp_repo)
    urls = {r["githubUrl"] for r in repos}
    assert dead_url not in urls, "мёртвый репо должен быть отфильтрован"
    assert alive_url in urls, "живой репо должен сохраниться"


def test_pipeline_keeps_repos_on_unknown(tmp_repo):
    """unknown (rate-limit) → репо сохраняется (обрыв сети ≠ мёртвый)."""
    net_url = "https://github.com/foo/net"
    html = _ranking_html([("1", "foo/net", net_url)])

    ts_main(
        tools_yml=tmp_repo["tools_yml"],
        trendshift_file=tmp_repo["trendshift_file"],
        trendshift_repos_file=tmp_repo["trendshift_repos_file"],
        fetcher=lambda slug, h: None,
        page_fetcher=lambda url, h: html,
        badge_fetcher=lambda url, h: RANK_SVG,
        alive_checker=lambda slug, h: ("unknown", None),
    )

    repos = _read_repos(tmp_repo)
    assert {r["githubUrl"] for r in repos} == {net_url}


def test_pipeline_does_not_filter_tools_yml_repo(tmp_repo):
    """tools.yml-репо обогащает trendshift.json; alive_checker его не трогает.

    Инвариант: фильтр применяется только к автособранным new_repos, а не к
    кураторским tools.yml → trendshift.json. Здесь tools.yml-репо (a/hi) идёт
    в trendshift.json даже если alive_checker сказал бы 'dead'.
    """
    hi_url = "https://github.com/a/hi"  # есть в tmp_repo.tools_yml
    # README для a/hi содержит trendshift-бейдж → enrich в trendshift.json.
    readme_hi = (
        '<a href="https://trendshift.io/repositories/999">'
        '<img src="https://trendshift.io/api/badge/trendshift/repositories/999/daily" /></a>'
    )

    def fetcher(slug, headers):
        owner, repo = slug
        if (owner, repo) == ("a", "hi"):
            return readme_hi
        return None

    ts_main(
        tools_yml=tmp_repo["tools_yml"],
        trendshift_file=tmp_repo["trendshift_file"],
        trendshift_repos_file=tmp_repo["trendshift_repos_file"],
        fetcher=fetcher,
        page_fetcher=lambda url, h: "<script></script>",  # нет ranking-записей
        badge_fetcher=lambda url, h: None,
        # alive_checker ВСЕГДА dead — но tools.yml-репо не должно вылететь.
        alive_checker=lambda slug, h: ("dead", None),
    )

    cache = _read_cache(tmp_repo)
    assert hi_url in cache, "tools.yml-репо должно обогатить trendshift.json, фильтр его не касается"
    repos = _read_repos(tmp_repo)
    assert repos == [], "автособранных репо нет → trendshift-repos.json пуст"


@responses.activate
def test_pipeline_default_alive_checker_filters_dead(tmp_repo):
    """main() без явного alive_checker использует реальный check_repo_alive.

    wired-in дефолт (alive_checker=check_repo_alive в main) действительно
    фильтрует: 404-репо выкидывается, 200-репо сохраняется. @responses
    детерминированно эмулирует GitHub API без реальной сети.
    """
    alive_url = "https://github.com/foo/alive"
    dead_url = "https://github.com/foo/dead"
    html = _ranking_html([
        ("1", "foo/alive", alive_url),
        ("2", "foo/dead", dead_url),
    ])
    responses.add(responses.GET,
                  GITHUB_REPO_API.format(owner="foo", repo="alive"),
                  json={"stargazers_count": 42, "archived": False}, status=200)
    responses.add(responses.GET,
                  GITHUB_REPO_API.format(owner="foo", repo="dead"),
                  json={"message": "Not Found"}, status=404)

    ts_main(
        tools_yml=tmp_repo["tools_yml"],
        trendshift_file=tmp_repo["trendshift_file"],
        trendshift_repos_file=tmp_repo["trendshift_repos_file"],
        fetcher=lambda slug, h: None,
        page_fetcher=lambda url, h: html,
        badge_fetcher=lambda url, h: RANK_SVG,
        # alive_checker не передаём → дефолт check_repo_alive.
    )

    repos = _read_repos(tmp_repo)
    assert {r["githubUrl"] for r in repos} == {alive_url}


def test_pipeline_meta_driven_prune_skips_alive_check(tmp_repo):
    """meta_file→meta фильтрует archived/low-stars БЕЗ alive_checker (FIX rate-limit).

    Главная цель фикса Codex rate-limit budget: update_stars уже положил
    {stars, archived} в repos-meta.json. main(meta_file=...) читает его и
    фильтрует archived/low-stars оттуда, НЕ дёргая alive_checker для url в meta.
    alive_checker вызывается только для отсутствующих в meta. Это держит
    API-бюджет в рамках Actions-лимита 1000/час вместо ~791 лишних запросов.
    """
    ok_url = "https://github.com/foo/ok"
    archived_url = "https://github.com/foo/archived"
    # третий url отсутствует в meta → должен дойти до alive_checker (проход 2),
    # что доказывает: meta-фильтр и alive-фильтр работают вместе, не дублируя.
    missing_url = "https://github.com/foo/missing"
    html = _ranking_html([
        ("1", "foo/ok", ok_url),
        ("2", "foo/archived", archived_url),
        ("3", "foo/missing", missing_url),
    ])
    meta_file = tmp_repo["root"] / "data" / "repos-meta.json"
    meta_file.parent.mkdir(parents=True, exist_ok=True)
    # ok и archived есть в meta → решаются без alive_checker (0 API).
    # missing отсутствует → единственный, кто дёргает alive_checker.
    meta_file.write_text(json.dumps({
        ok_url: {"stars": 100, "archived": False},
        archived_url: {"stars": 100, "archived": True},
    }), encoding="utf-8")

    called = []

    def alive_checker(slug, headers):
        called.append(slug)
        return "alive", {"stars": 50, "archived": False}

    ts_main(
        tools_yml=tmp_repo["tools_yml"],
        trendshift_file=tmp_repo["trendshift_file"],
        trendshift_repos_file=tmp_repo["trendshift_repos_file"],
        fetcher=lambda slug, h: None,
        page_fetcher=lambda url, h: html,
        badge_fetcher=lambda url, h: RANK_SVG,
        alive_checker=alive_checker,
        meta_file=meta_file,
    )

    repos = _read_repos(tmp_repo)
    urls = {r["githubUrl"] for r in repos}
    # archived выкинут по meta; ok и missing (alive) сохранены.
    assert urls == {ok_url, missing_url}, "archived выкинут по meta; ok+missing живы"
    # alive_checker дёргался ТОЛЬКО для missing — ok/archived решены через meta.
    assert called == [("foo", "missing")], "только отсутствующий в meta url дошёл до alive_checker"
