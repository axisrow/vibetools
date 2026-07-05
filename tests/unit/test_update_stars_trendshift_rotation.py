"""Тесты ротации meta trendshift-repos в update_stars.

Корень бага: PR #20 добавил skip `if url in cache`, где cache — персистентный
stars.json из прошлого прогона. Условие слишком широкое: после первого fetch'а
trendshift-repo НИКОГДА больше не обновляется → meta замерзает (687/791 stale).

ЧАСТЬ 1: skip должен быть по `fetched_this_run` (множество этого прогона), а не
по `cache` (прошлого прогона). Тогда url, который однажды получил звёзды, всё
равно рефетчится — но дубль url из tools.yml (fetched в этом же прогоне) skip'ится.
ЧАСТЬ 3: бюджет-aware ротация (см. ниже, test_rotation_*).
"""
import datetime
import json

import responses

from common import GITHUB_REPO_API
from update_stars import main as update_main

TODAY = datetime.date(2026, 7, 5)


def _api(owner, repo):
    return GITHUB_REPO_API.format(owner=owner, repo=repo)


# ---- ЧАСТЬ 1: skip-фикс fetched_this_run ----


@responses.activate
def test_trendshift_url_in_stars_cache_still_refetched(tmp_path):
    """url ЕСТЬ в stars.json (прежний кэш) → всё равно фетчится и meta обновляется.

    Это регрессия на корень бага: раньше `url in cache` skip'ил бы этот url, и
    meta оставался прежним (замороженным). Теперь skip'ятся только url, уже
    fetched в этом же прогоне (т.е. дубль tools.yml), а не любой url из прошлого.
    """
    data = tmp_path / "data"
    data.mkdir()
    tools_yml = data / "tools.yml"
    stars_file = data / "stars.json"
    meta_file = data / "repos-meta.json"
    history_file = data / "stars-history.json"
    trendshift_repos_file = data / "trendshift-repos.json"
    # tools.yml пустой — trendshift-репо не дублирует кураторские.
    tools_yml.write_text("tools: []\n", encoding="utf-8")
    # url УЖЕ в stars.json (как раз условие старого багового skip'а).
    ts_url = "https://github.com/ts/repo"
    stars_file.write_text(json.dumps({ts_url: 10}), encoding="utf-8")
    meta_file.write_text(json.dumps({ts_url: {"stars": 10, "archived": False}}),
                         encoding="utf-8")
    trendshift_repos_file.write_text(json.dumps([{"githubUrl": ts_url}]),
                                     encoding="utf-8")

    # Свежий fetch: звёзды изменились + archived сменился.
    responses.add(responses.GET, _api("ts", "repo"),
                  json={"stargazers_count": 42, "archived": True}, status=200)

    update_main(tools_yml, stars_file, regenerate=False, out_dir=tmp_path,
                history_file=history_file, meta_file=meta_file,
                trendshift_repos_file=trendshift_repos_file)

    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    # Ключевой assert: meta обновился, а НЕ остался прежним {stars:10,archived:False}.
    assert meta[ts_url]["stars"] == 42
    assert meta[ts_url]["archived"] is True


@responses.activate
def test_trendshift_url_duplicate_of_tools_yml_skipped(tmp_path):
    """url есть и в tools.yml, и в trendshift-repos → fetcher зовётся 1 раз.

    Это то, что задумал PR #20: не фетчить дубликаты tools.yml. После skip-фикса
    дубль skip'ится по `fetched_this_run` (tools.yml-цикл уже фетчнул url), а не
    по персистентному cache. Доказываем счётчиком вызовов: ровно 1 запрос.
    """
    import yaml
    data = tmp_path / "data"
    data.mkdir()
    tools_yml = data / "tools.yml"
    stars_file = data / "stars.json"
    meta_file = data / "repos-meta.json"
    history_file = data / "stars-history.json"
    trendshift_repos_file = data / "trendshift-repos.json"
    dup_url = "https://github.com/a/hi"
    tools_yml.write_text(yaml.safe_dump({"tools": [
        {"name": "Hi", "url": dup_url, "category": "cli-agents",
         "description": {"en": "Hi", "ru": "Привет"}}]}, allow_unicode=True,
        sort_keys=False), encoding="utf-8")
    stars_file.write_text("{}", encoding="utf-8")
    trendshift_repos_file.write_text(json.dumps([{"githubUrl": dup_url}]),
                                     encoding="utf-8")

    responses.add(responses.GET, _api("a", "hi"),
                  json={"stargazers_count": 7, "archived": False}, status=200)

    update_main(tools_yml, stars_file, regenerate=False, out_dir=tmp_path,
                history_file=history_file, meta_file=meta_file,
                trendshift_repos_file=trendshift_repos_file)

    # Только один вызов к /repos/a/hi — дубль trendshift skip'нут.
    assert len(responses.calls) == 1
