"""Integration: update_trendshift.main() end-to-end через tmp_repo + mock fetchers.

Liveness/freshness автособранного trendshift-repos.json теперь НЕ здесь — её
делает update_stars.refresh_trendshift_meta (бюджет-aware ротация + pruning
404/archived/low-stars, см. tests/unit/test_update_stars_trendshift_rotation.py).
Этот скрипт только собирает ranking-данные и мёржит бейджи; фильтр мёртвых
переехал туда, где уже есть meta из /repos (0 лишних API, meta не замораживается).

Все fetcher-ы инъецированы → 0 сетевых вызовов.
"""
import json

from update_trendshift import main as ts_main

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


def test_pipeline_collects_ranking_repos(tmp_repo):
    """main() собирает trendshift-only репо из ranking-страниц в trendshift-repos.json.

    Liveness больше не задача этого скрипта — все собранные репо попадают в
    список как есть (pruning 404/archived делает update_stars след. шагом).
    """
    alive_url = "https://github.com/foo/alive"
    other_url = "https://github.com/foo/other"
    html = _ranking_html([
        ("1", "foo/alive", alive_url),
        ("2", "foo/other", other_url),
    ])

    ts_main(
        tools_yml=tmp_repo["tools_yml"],
        trendshift_file=tmp_repo["trendshift_file"],
        trendshift_repos_file=tmp_repo["trendshift_repos_file"],
        fetcher=lambda slug, h: None,
        page_fetcher=lambda url, h: html,
        badge_fetcher=lambda url, h: RANK_SVG,
    )

    repos = _read_repos(tmp_repo)
    urls = {r["githubUrl"] for r in repos}
    assert urls == {alive_url, other_url}, "оба ranking-репо собраны"


def test_pipeline_does_not_filter_tools_yml_repo(tmp_repo):
    """tools.yml-репо обогащает trendshift.json; рейтинг-сбор его не трогает.

    Инвариант: update_trendshift разделяет кураторские tools.yml (→ trendshift.json)
    и автособранные (→ trendshift-repos.json). tools.yml-репо (a/hi) идёт в
    trendshift.json и НЕ попадает в trendshift-repos.json (он не «новый»).
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
    )

    cache = _read_cache(tmp_repo)
    assert hi_url in cache, "tools.yml-репо обогащает trendshift.json"
    repos = _read_repos(tmp_repo)
    assert repos == [], "автособранных репо нет → trendshift-repos.json пуст"
