"""Тесты ротации meta trendshift-repos в update_stars.

Корень бага: PR #20 добавил skip `if url in cache`, где cache — персистентный
stars.json из прошлого прогона. Условие слишком широкое: после первого fetch'а
trendshift-repo НИКОГДА больше не обновляется → meta замерзает (687/791 stale).

ЧАСТЬ 1: skip должен быть по `fetched_this_run` (множество этого прогона), а не
по `cache` (прошлого прогона). Тогда url, который однажды получил звёзды, всё
равно рефетчится — но дубль url из tools.yml (fetched в этом же прогоне) skip'ится.
ЧАСТЬ 3: бюджет-aware ротация (refresh_trendshift_meta).
"""
import datetime
import json

import responses

from common import GITHUB_REPO_API
from update_stars import main as update_main, refresh_trendshift_meta

TODAY = datetime.date(2026, 7, 5)


def _rec(url):
    """Минимальная запись trendshift-repos: только githubUrl."""
    return {"githubUrl": url}


def _meta(stars=100, archived=False, checked_at="", **kw):
    """meta-запись repos-meta.json (checked_at="" = «никогда не проверяли»)."""
    m = {"stars": stars, "archived": archived, "checkedAt": checked_at}
    m.update(kw)
    return m


def _fetcher_ok(stars=100, archived=False):
    """fetcher, всегда отдающий живой meta."""
    return lambda slug, headers, **_: {
        "stars": stars, "archived": archived, "checkedAt": TODAY.isoformat()}


def _alive(status):
    """alive_checker, всегда отдающий status."""
    return lambda slug, headers: (status, None)


def _api(owner, repo):
    return GITHUB_REPO_API.format(owner=owner, repo=repo)


# ---- ЧАСТЬ 1: skip-фикс fetched_this_run ----


@responses.activate
def test_trendshift_url_in_stars_cache_still_refetched(tmp_path, monkeypatch):
    """url ЕСТЬ в stars.json (прежний кэш) → всё равно фетчится и meta обновляется.

    Это регрессия на корень бага: раньше `url in cache` skip'ил бы этот url, и
    meta оставался прежним (замороженным). Теперь skip'ятся только url, уже
    fetched в этом же прогоне (т.е. дубль tools.yml), а не любой url из прошлого.
    Берём ЖИВОЕ репо (archived=False) — archived prune'ится отдельно (ЧАСТЬ 3),
    здесь проверяем именно снятие заморозки meta.
    """
    monkeypatch.setattr("update_stars.time.sleep", lambda s: None)
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

    # Свежий fetch: звёзды изменились (10 → 42), репо живое.
    responses.add(responses.GET, _api("ts", "repo"),
                  json={"stargazers_count": 42, "archived": False}, status=200)

    update_main(tools_yml, stars_file, regenerate=False, out_dir=tmp_path,
                history_file=history_file, meta_file=meta_file,
                trendshift_repos_file=trendshift_repos_file)

    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    # Ключевой assert: meta обновился, а НЕ остался прежним {stars:10}.
    assert meta[ts_url]["stars"] == 42


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


# ---- ЧАСТЬ 3: refresh_trendshift_meta (budget-aware ротация + pruning) ----
# Паттерн categorize_repos.enrich_repos_with_category: инкрементально, max_per_run,
# fetcher→None → alive_checker (404-pass), archived/low-stars → prune. Сортировка
# по checkedAt ASC — старейшие/непроверенные первыми (backfill за ~8 дней).


def test_rotation_picks_oldest_by_checked_at():
    """При max_per_run < len(repos) фетчатся старейшие по checkedAt."""
    repos = [_rec(f"https://github.com/x/r{i}") for i in range(3)]
    meta = {
        "https://github.com/x/r0": _meta(checked_at="2026-07-01"),  # старейший
        "https://github.com/x/r1": _meta(checked_at="2026-07-04"),
        "https://github.com/x/r2": _meta(checked_at="2026-07-03"),
    }
    fetched_slugs = []

    def fetcher(slug, headers, **_):
        fetched_slugs.append(slug)
        return {"stars": 50, "archived": False, "checkedAt": TODAY.isoformat()}

    updated, missing, pruned = refresh_trendshift_meta(
        repos, meta, {}, set(), {}, fetcher=fetcher, max_per_run=2,
        alive_checker=_alive("alive"), now=TODAY)
    # Ротация взяла r0 (2026-07-01) и r2 (2026-07-03) — два старейших.
    fetched_repos = {slug[1] for slug in fetched_slugs}
    assert fetched_repos == {"r0", "r2"}
    assert updated == 2 and missing == 0 and pruned == []


def test_rotation_skips_fresh_checked_today():
    """checkedAt == today (уже проверяли сегодня) → skip (идемпотентность)."""
    repos = [_rec("https://github.com/x/fresh")]
    meta = {"https://github.com/x/fresh": _meta(checked_at=TODAY.isoformat())}
    calls = []
    refresh_trendshift_meta(
        repos, meta, {}, set(), {}, fetcher=lambda *a, **k: calls.append(a) or _meta(),
        max_per_run=10, alive_checker=_alive("alive"), now=TODAY)
    assert calls == []  # свежий не фетчится повторно


def test_rotation_no_checked_at_treated_as_oldest():
    """Без checkedAt ("" или отсутствие) → самый старый, фетчится первым."""
    repos = [_rec("https://github.com/x/none"), _rec("https://github.com/x/seen")]
    meta = {
        "https://github.com/x/none": _meta(checked_at=""),          # никогда
        "https://github.com/x/seen": _meta(checked_at="2026-07-04"),
    }
    fetched = []

    def fetcher(slug, headers, **_):
        fetched.append(slug[1])
        return {"stars": 50, "archived": False, "checkedAt": TODAY.isoformat()}

    refresh_trendshift_meta(
        repos, meta, {}, set(), {}, fetcher=fetcher, max_per_run=1,
        alive_checker=_alive("alive"), now=TODAY)
    assert fetched == ["none"]  # без checkedAt — первый кандидат


def test_rotation_respects_max_per_run():
    """fetcher зовётся не более max_per_run раз."""
    repos = [_rec(f"https://github.com/x/r{i}") for i in range(5)]
    meta = {f"https://github.com/x/r{i}": _meta(checked_at="") for i in range(5)}
    calls = []

    def fetcher(slug, headers, **_):
        calls.append(slug)
        return {"stars": 50, "archived": False, "checkedAt": TODAY.isoformat()}

    refresh_trendshift_meta(
        repos, meta, {}, set(), {}, fetcher=fetcher, max_per_run=3,
        alive_checker=_alive("alive"), now=TODAY)
    assert len(calls) == 3


def test_rotation_budget_check_stops_when_low():
    """budget_remaining < budget_floor → остановка ДО исчерпания max_per_run."""
    repos = [_rec(f"https://github.com/x/r{i}") for i in range(5)]
    meta = {f"https://github.com/x/r{i}": _meta(checked_at="") for i in range(5)}
    calls = []

    def fetcher(slug, headers, budget=None, **_):
        calls.append(slug)
        # Симулируем, что GitHub сообщает об исчерпании после 2-го запроса.
        if budget is not None and len(calls) >= 2:
            budget["remaining"] = 50  # ниже floor=100
        return {"stars": 50, "archived": False, "checkedAt": TODAY.isoformat()}

    refresh_trendshift_meta(
        repos, meta, {}, set(), {}, fetcher=fetcher, max_per_run=10,
        budget={"remaining": None}, budget_floor=100,
        alive_checker=_alive("alive"), now=TODAY)
    # 2 fetch'а прошло, на 3-м budget уже низкий → остановились. Не все 5.
    assert len(calls) <= 3


def test_rotation_no_budget_uses_max_per_run_only():
    """budget=None → throttle только по max_per_run (header отсутствует)."""
    repos = [_rec(f"https://github.com/x/r{i}") for i in range(4)]
    meta = {f"https://github.com/x/r{i}": _meta(checked_at="") for i in range(4)}
    calls = []

    def fetcher(slug, headers, **_):
        calls.append(slug)
        return {"stars": 50, "archived": False, "checkedAt": TODAY.isoformat()}

    refresh_trendshift_meta(
        repos, meta, {}, set(), {}, fetcher=fetcher, max_per_run=4,
        budget=None, budget_floor=100,
        alive_checker=_alive("alive"), now=TODAY)
    assert len(calls) == 4  # без budget floor не сработал → все 4


def test_rotation_fetcher_none_alive_checker_dead_prunes():
    """fetcher→None (404 в fetch_repo) + alive dead → репо выкидывается (prune)."""
    repos = [_rec("https://github.com/x/gone"), _rec("https://github.com/x/ok")]
    meta = {
        "https://github.com/x/gone": _meta(checked_at=""),
        "https://github.com/x/ok": _meta(checked_at=""),
    }
    alive_calls = []

    def alive_checker(slug, headers):
        alive_calls.append(slug)
        return ("dead", None) if slug[1] == "gone" else ("alive", {"stars": 5})

    def fetcher(slug, headers, **_):
        # gone → fetch_repo вернул None (404); ok → живой.
        if slug[1] == "gone":
            return None
        return {"stars": 30, "archived": False, "checkedAt": TODAY.isoformat()}

    updated, missing, pruned = refresh_trendshift_meta(
        repos, meta, {}, set(), {}, fetcher=fetcher, max_per_run=10,
        alive_checker=alive_checker, now=TODAY)
    assert pruned == ["https://github.com/x/gone"]
    assert {r["githubUrl"] for r in repos} == {"https://github.com/x/ok"}
    # alive_checker дёргался ТОЛЬКО для gone (None-случай), не для ok.
    assert {s[1] for s in alive_calls} == {"gone"}
    assert updated == 1  # ok обновлён


def test_rotation_fetcher_none_unknown_keeps():
    """fetcher→None + alive unknown (rate-limit) → репо сохраняем, missing++."""
    repos = [_rec("https://github.com/x/net")]
    meta = {"https://github.com/x/net": _meta(checked_at="")}
    updated, missing, pruned = refresh_trendshift_meta(
        repos, meta, {}, set(), {}, fetcher=lambda *a, **k: None,
        max_per_run=10, alive_checker=_alive("unknown"), now=TODAY)
    assert missing == 1 and updated == 0 and pruned == []
    # репо сохранён (не выкинут), meta не тронут (прежний кэш остаётся).
    assert {r["githubUrl"] for r in repos} == {"https://github.com/x/net"}
    assert repos == [_rec("https://github.com/x/net")]


def test_rotation_archived_pruned():
    """archived=True → prune (заброшенные репо не мусорят в каталоге)."""
    repos = [_rec("https://github.com/x/old")]
    meta = {"https://github.com/x/old": _meta(checked_at="")}
    updated, missing, pruned = refresh_trendshift_meta(
        repos, meta, {}, set(), {}, fetcher=_fetcher_ok(archived=True),
        max_per_run=10, alive_checker=_alive("alive"), now=TODAY)
    assert pruned == ["https://github.com/x/old"]
    assert repos == []


def test_rotation_low_stars_pruned():
    """stars < min_stars → prune (пустой шум отсекается)."""
    repos = [_rec("https://github.com/x/small")]
    meta = {"https://github.com/x/small": _meta(checked_at="")}
    updated, missing, pruned = refresh_trendshift_meta(
        repos, meta, {}, set(), {}, fetcher=_fetcher_ok(stars=3),
        max_per_run=10, min_stars=10, alive_checker=_alive("alive"), now=TODAY)
    assert pruned == ["https://github.com/x/small"]
    assert repos == []


def test_rotation_skips_fetched_this_run():
    """url в fetched_this_run (дубль tools.yml) → не фетчится."""
    repos = [_rec("https://github.com/x/dup")]
    meta = {}
    calls = []
    refresh_trendshift_meta(
        repos, meta, {}, {"https://github.com/x/dup"}, {},
        fetcher=lambda *a, **k: calls.append(1) or _meta(),
        max_per_run=10, alive_checker=_alive("alive"), now=TODAY)
    assert calls == []


def test_rotation_skips_non_github_url():
    """url без github.com (slug → None) → пропускается без fetch."""
    repos = [{"githubUrl": "https://example.com/x"}]
    calls = []
    refresh_trendshift_meta(
        repos, {}, {}, set(), {}, fetcher=lambda *a, **k: calls.append(1) or _meta(),
        max_per_run=10, alive_checker=_alive("alive"), now=TODAY)
    assert calls == []


def test_rotation_sleeps_between_requests(monkeypatch):
    """time.sleep зовётся между fetch'ами (уважение к rate-limit), не после последнего."""
    repos = [_rec(f"https://github.com/x/r{i}") for i in range(3)]
    meta = {f"https://github.com/x/r{i}": _meta(checked_at="") for i in range(3)}
    sleeps = []
    monkeypatch.setattr("update_stars.time.sleep", lambda s: sleeps.append(s))
    refresh_trendshift_meta(
        repos, meta, {}, set(), {}, fetcher=_fetcher_ok(),
        max_per_run=10, sleep_between=0.5, alive_checker=_alive("alive"), now=TODAY)
    # 3 запроса → 2 sleep между ними (не после последнего).
    assert sleeps == [0.5, 0.5]


def test_rotation_writes_cache_and_meta():
    """Успешный fetch обновляет и cache (stars), и meta (полный словарь)."""
    repos = [_rec("https://github.com/x/new")]
    meta = {}
    cache = {}
    refresh_trendshift_meta(
        repos, meta, cache, set(), {}, fetcher=_fetcher_ok(stars=77),
        max_per_run=10, alive_checker=_alive("alive"), now=TODAY)
    assert cache["https://github.com/x/new"] == 77
    assert meta["https://github.com/x/new"]["stars"] == 77
    assert meta["https://github.com/x/new"]["checkedAt"] == TODAY.isoformat()


# ---- Доказательство экономии API-бюджета (ЧАСТЬ 3, core claim) ----
# Наивный «рефетчить всё» (после skip-фикса ЧАСТЬ 1) даёт 383 + 791 = 1174
# запроса/день > Actions-лимита 1000/час. Budget-aware ротация режет trendshift
# до max_per_run=100/день + ~5 None-pass → ~488/день, в 2× запасом под лимит.
# Backfill 791 репо растягивается на ~8 дней (по 100/день), потом steady-state.


def test_rotation_budget_proof_488_not_1174(monkeypatch):
    """791 trendshift-repo с max_per_run=100 → ~100 fetch'ей, а не 791.

    Симулируем production-масштаб: ни один репо не проверялся (checkedAt="").
    Доказываем: ротация делает ровно max_per_run запросов (+0 None-pass, т.к.
    все живые), а не все 791. Вместе с tools.yml-циклом (383) это ~483 < 1000.
    """
    monkeypatch.setattr("update_stars.time.sleep", lambda s: None)
    repos = [_rec(f"https://github.com/ts/r{i:04d}") for i in range(791)]
    meta = {r["githubUrl"]: _meta(checked_at="") for r in repos}
    calls = {"fetch": 0, "alive": 0}

    def fetcher(slug, headers, **_):
        calls["fetch"] += 1
        return {"stars": 50, "archived": False, "checkedAt": TODAY.isoformat()}

    def alive_checker(slug, headers):
        calls["alive"] += 1
        return "alive", None

    updated, missing, pruned = refresh_trendshift_meta(
        repos, meta, {}, set(), {}, fetcher=fetcher, max_per_run=100,
        alive_checker=alive_checker, now=TODAY)
    # Ровно 100 fetch'ей (max_per_run), 0 alive-check (все живые, fetcher не None).
    assert calls["fetch"] == 100
    assert calls["alive"] == 0
    assert updated == 100 and missing == 0 and pruned == []
    # 691 репо остались непроверенными — ждут след. прогонов (self-healing за ~8 дней).
    assert len(repos) == 791


def test_rotation_budget_with_few_dead_adds_alive_pass(monkeypatch):
    """None-случаи (404/rate-limit) дают +1 alive-check каждый — но только для None.

    Worst case для budget: несколько fetcher→None. Каждый → 1 alive-check.
    100 ротации + 5 None = 105 запросов (всё ещё ≪ 791 наивных).
    """
    monkeypatch.setattr("update_stars.time.sleep", lambda s: None)
    repos = [_rec(f"https://github.com/ts/r{i}") for i in range(100)]
    meta = {r["githubUrl"]: _meta(checked_at="") for r in repos}
    calls = {"fetch": 0, "alive": 0}

    def fetcher(slug, headers, **_):
        calls["fetch"] += 1
        # первые 5 → None (симулируем 404/rate-limit в fetch_repo).
        if calls["fetch"] <= 5:
            return None
        return {"stars": 50, "archived": False, "checkedAt": TODAY.isoformat()}

    def alive_checker(slug, headers):
        calls["alive"] += 1
        return "unknown", None  # rate-limit → keep, не prune

    refresh_trendshift_meta(repos, meta, {}, set(), {}, fetcher=fetcher,
                            max_per_run=100, alive_checker=alive_checker, now=TODAY)
    assert calls["fetch"] == 100
    assert calls["alive"] == 5  # только None-случаи, не для живых


# ---- Интеграция refresh_trendshift_meta в main (end-to-end pruning) ----


@responses.activate
def test_main_prunes_archived_trendshift_repo_writes_file(tmp_path):
    """main() через ротацию выкидывает archived-репо и перезаписывает trendshift-repos.json.

    End-to-end: @responses эмулирует GitHub API (archived=True → prune), main
    интегрирует refresh_trendshift_meta и фиксирует урезанный список на диске.
    Доказывает, что liveness теперь живёт в update_stars, а не в отдельном скрипте.
    """
    data = tmp_path / "data"
    data.mkdir()
    tools_yml = data / "tools.yml"
    stars_file = data / "stars.json"
    meta_file = data / "repos-meta.json"
    history_file = data / "stars-history.json"
    trendshift_repos_file = data / "trendshift-repos.json"
    tools_yml.write_text("tools: []\n", encoding="utf-8")
    keep_url = "https://github.com/ts/keep"
    dead_url = "https://github.com/ts/archived"
    stars_file.write_text("{}", encoding="utf-8")
    trendshift_repos_file.write_text(json.dumps([
        {"githubUrl": keep_url}, {"githubUrl": dead_url}]), encoding="utf-8")

    responses.add(responses.GET, _api("ts", "keep"),
                  json={"stargazers_count": 50, "archived": False}, status=200)
    responses.add(responses.GET, _api("ts", "archived"),
                  json={"stargazers_count": 5, "archived": True}, status=200)

    update_main(tools_yml, stars_file, regenerate=False, out_dir=tmp_path,
                history_file=history_file, meta_file=meta_file,
                trendshift_repos_file=trendshift_repos_file, now=TODAY)

    repos = json.loads(trendshift_repos_file.read_text(encoding="utf-8"))
    urls = {r["githubUrl"] for r in repos}
    assert urls == {keep_url}, "archived выкинут из trendshift-repos.json"
    # meta живого обновлён (archived в meta НЕ пишем — он выкинут).
    meta = json.loads(meta_file.read_text(encoding="utf-8"))
    assert keep_url in meta and dead_url not in meta


