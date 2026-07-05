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
    """Тотальный сбой (все 403) → кэш сохранён, но history НЕ портится, rc != 0.

    Контракт #14: прежние звёзды в stars.json уцелели (не теряем данные при
    разовом сбое), README регенерирован, но dated-срез за сегодня НЕ пишется из
    устаревшего кэша (иначе дельты обнулятся), а main() возвращает nonzero,
    чтобы CI покраснел при тотальном сбое (например, истёкший токен).
    """
    tmp_repo["stars_file"].write_text(json.dumps({HI_URL: 7}), encoding="utf-8")
    for api in (HI_API, LO_API, EDITOR_API):
        responses.add(responses.GET, api, json={"message": "rate"}, status=403)

    rc = update_main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"], history_file=tmp_repo["history_file"], meta_file=tmp_repo["meta_file"])
    cache = _read_cache(tmp_repo)
    assert rc == 1  # тотальный сбой → nonzero, чтобы CI заметил
    assert cache[HI_URL] == 7  # прежний кэш уцелел
    assert (tmp_repo["root"] / "README.md").exists()
    # History-файл не создан / не обновлён — свежий срез из устаревшего кэша
    # не штампуем (иначе окно сузится до копий одного снимка).
    assert not tmp_repo["history_file"].exists()


@responses.activate
def test_update_stars_regenerates_with_meta_history_trendshift(tmp_repo):
    """#17: регенерация README/site после fetch несёт meta/history/trendshift.

    Раньше update_stars.main не пробрасывал meta_file/history_file/trendshift_file
    в генераторы — committed index.html терял Featured (нужен history), README
    терял [new] (нужен meta createdAt), сайт терял trendshift-бейджи. Здесь все
    три инъектируемых пути доходят до генераторов на tmp-данных.
    """
    import datetime
    hi_created = (datetime.date.today() - datetime.timedelta(days=2)).isoformat()
    responses.add(responses.GET, HI_API, json={
        "stargazers_count": 1100, "forks": 9, "created_at": f"{hi_created}T00:00:00Z",
        "language": "Rust", "topics": ["ai"]}, status=200)
    responses.add(responses.GET, LO_API, json={"stargazers_count": 5}, status=200)
    responses.add(responses.GET, EDITOR_API, json={"stargazers_count": 50}, status=200)

    # history даёт положительную недельную дельту для HI → Featured(week).
    today = datetime.date.today()
    tmp_repo["history_file"].write_text(json.dumps({
        HI_URL: {(today - datetime.timedelta(days=7)).isoformat(): 1000}}), encoding="utf-8")
    # trendshift-кэш для HI → сайт должен нести trendshift-бейдж.
    tmp_repo["trendshift_file"].write_text(json.dumps({
        HI_URL: {"trendshiftId": "1", "pageUrl": "https://trendshift.io/repositories/1",
                 "badges": [{"kind": "week", "badgeUrl": "https://trendshift.io/api/badge/trendshift/repositories/1/weekly"}],
                 "updatedAt": today.isoformat()}}), encoding="utf-8")

    rc = update_main(tmp_repo["tools_yml"], tmp_repo["stars_file"],
                     out_dir=tmp_repo["root"], history_file=tmp_repo["history_file"],
                     meta_file=tmp_repo["meta_file"],
                     trendshift_file=tmp_repo["trendshift_file"])
    assert rc == 0

    # README обогащён created_at из meta → HiStars свежий (2 дня) → [new].
    readme = (tmp_repo["root"] / "README.md").read_text(encoding="utf-8")
    # is_new рендерится только блоком Featured в README, но не инлайн-меткой;
    # Featured(week) присутствует благодаря проброшенному history_file.
    assert "## Featured" in readme
    assert "caveman" not in readme  # sanity: данные из tmp, не реальные

    # Сайт несёт Featured (history) и trendshift (trendshift_file).
    import re
    html = (tmp_repo["root"] / "docs" / "index.html").read_text(encoding="utf-8")
    payload = json.loads(re.search(r"window\.__DATA__ = (\{.*?\});\n", html, re.S).group(1))
    featured_urls = {e["url"] for e in payload["featured"]}
    assert HI_URL in featured_urls  # history добрался до site
    hi = next(t for t in payload["tools"] if t["name"] == "HiStars")
    assert hi["isNew"] is True  # meta createdAt добрался → isNew вычислен верно
    assert hi["trendshift"]["badges"][0]["kind"] == "week"  # trendshift добрался


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
