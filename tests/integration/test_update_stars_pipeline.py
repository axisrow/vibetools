"""Integration: связка update_stars + generate_readme на tmp-данных.

КРИТИЧНО: прежний кэш должен сохраняться при разовых сбоях (404/429/сеть),
чтобы не терять звёзды из-за мимолётного сбоя GitHub.
"""
import json

import responses

from update_stars import API, main as update_main

HI_URL = "https://github.com/a/hi"
LO_URL = "https://github.com/a/lo"
EDITOR_URL = "https://github.com/b/editor"
NOGIT_URL = "https://example.com/tool"

HI_API = API.format(owner="a", repo="hi")
LO_API = API.format(owner="a", repo="lo")
EDITOR_API = API.format(owner="b", repo="editor")


def _read_cache(tmp_repo):
    return json.loads(tmp_repo["stars_file"].read_text(encoding="utf-8"))


@responses.activate
def test_update_stars_writes_stars_cache(tmp_repo):
    responses.add(responses.GET, HI_API, json={"stargazers_count": 100}, status=200)
    responses.add(responses.GET, LO_API, json={"stargazers_count": 5}, status=200)
    responses.add(responses.GET, EDITOR_API, json={"stargazers_count": 50}, status=200)

    rc = update_main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"], history_file=tmp_repo["history_file"], meta_file=tmp_repo["meta_file"])
    cache = _read_cache(tmp_repo)
    assert rc == 0
    assert cache[HI_URL] == 100
    assert cache[LO_URL] == 5
    assert cache[EDITOR_URL] == 50


@responses.activate
def test_update_stars_preserves_old_cache_on_404(tmp_repo):
    """404 на один репо не должен затирать прежнее значение в кэше."""
    # Прежний кэш с заведомо известным значением для HI.
    tmp_repo["stars_file"].write_text(json.dumps({HI_URL: 999}), encoding="utf-8")
    responses.add(responses.GET, HI_API, json={"message": "Not Found"}, status=404)
    responses.add(responses.GET, LO_API, json={"stargazers_count": 5}, status=200)
    responses.add(responses.GET, EDITOR_API, json={"stargazers_count": 50}, status=200)

    update_main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"], history_file=tmp_repo["history_file"], meta_file=tmp_repo["meta_file"])
    cache = _read_cache(tmp_repo)
    assert cache[HI_URL] == 999  # прежнее значение сохранено
    assert cache[LO_URL] == 5


@responses.activate
def test_update_stars_skips_non_github(tmp_repo):
    responses.add(responses.GET, HI_API, json={"stargazers_count": 100}, status=200)
    responses.add(responses.GET, LO_API, json={"stargazers_count": 5}, status=200)
    responses.add(responses.GET, EDITOR_API, json={"stargazers_count": 50}, status=200)

    update_main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"], history_file=tmp_repo["history_file"], meta_file=tmp_repo["meta_file"])
    cache = _read_cache(tmp_repo)
    assert NOGIT_URL not in cache


@responses.activate
def test_update_stars_regenerates_readme(tmp_repo):
    responses.add(responses.GET, HI_API, json={"stargazers_count": 100}, status=200)
    responses.add(responses.GET, LO_API, json={"stargazers_count": 5}, status=200)
    responses.add(responses.GET, EDITOR_API, json={"stargazers_count": 50}, status=200)

    update_main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"], history_file=tmp_repo["history_file"], meta_file=tmp_repo["meta_file"])
    readme = (tmp_repo["root"] / "README.md").read_text(encoding="utf-8")
    # README перегенерирован: бейджи owner/repo на месте.
    assert "img.shields.io/github/stars/a/hi" in readme
    assert "img.shields.io/github/stars/b/editor" in readme


@responses.activate
def test_update_stars_all_fail_still_writes(tmp_repo):
    """Все запросы упали (403) → кэш сохранён, README регенерирован, return 0."""
    tmp_repo["stars_file"].write_text(json.dumps({HI_URL: 7}), encoding="utf-8")
    for api in (HI_API, LO_API, EDITOR_API):
        responses.add(responses.GET, api, json={"message": "rate"}, status=403)

    rc = update_main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"], history_file=tmp_repo["history_file"], meta_file=tmp_repo["meta_file"])
    cache = _read_cache(tmp_repo)
    assert rc == 0
    assert cache[HI_URL] == 7  # прежний кэш уцелел
    assert (tmp_repo["root"] / "README.md").exists()


@responses.activate
def test_update_stars_rate_limit_partial(tmp_repo):
    """3 репо: 200, 429, 200 — обновлены 2, третье сохраняет прежнее значение."""
    tmp_repo["stars_file"].write_text(json.dumps({LO_URL: 3}), encoding="utf-8")
    responses.add(responses.GET, HI_API, json={"stargazers_count": 100}, status=200)
    responses.add(responses.GET, LO_API, json={"message": "rate"}, status=429)
    responses.add(responses.GET, EDITOR_API, json={"stargazers_count": 50}, status=200)

    update_main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"], history_file=tmp_repo["history_file"], meta_file=tmp_repo["meta_file"])
    cache = _read_cache(tmp_repo)
    assert cache[HI_URL] == 100
    assert cache[LO_URL] == 3   # прежнее значение сохранено при 429
    assert cache[EDITOR_URL] == 50
