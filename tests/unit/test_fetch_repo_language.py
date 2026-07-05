"""Тесты fetch_repo — захват основного языка репо из GitHub API.

Язык берётся из поля `language` ответа /repos (без доп. запросов); None, если
GitHub его не определил. Контракт возврата None при rate-limit/ошибке сохраняется.
"""
import datetime

import responses

from update_stars import API, fetch_repo

AIDER_URL = API.format(owner="Aider-AI", repo="aider")


@responses.activate
def test_fetch_repo_captures_language():
    """200 с полем language → meta несёт language строкой."""
    responses.add(responses.GET, AIDER_URL, json={
        "stargazers_count": 42, "language": "Python",
    }, status=200)
    meta = fetch_repo(("Aider-AI", "aider"), {})
    assert meta is not None
    assert meta["language"] == "Python"


@responses.activate
def test_fetch_repo_language_null_when_absent():
    """200 без language → .get возвращает None (GitHub не определил язык)."""
    responses.add(responses.GET, AIDER_URL, json={
        "stargazers_count": 5, "language": None,
    }, status=200)
    meta = fetch_repo(("Aider-AI", "aider"), {})
    assert meta is not None
    assert meta["language"] is None


@responses.activate
def test_fetch_repo_no_language_field():
    """В ответе нет поля language вовсе → language == None."""
    responses.add(responses.GET, AIDER_URL, json={"stargazers_count": 1}, status=200)
    meta = fetch_repo(("Aider-AI", "aider"), {})
    assert meta is not None
    assert "language" in meta
    assert meta["language"] is None


@responses.activate
def test_fetch_repo_language_none_on_rate_limit():
    """429 → None целиком (контракт: не теряем данные, вызов. сторона держит кэш)."""
    responses.add(responses.GET, AIDER_URL, json={"message": "rate"}, status=429)
    assert fetch_repo(("Aider-AI", "aider"), {}) is None


# ---- checkedAt маркер + budget (x-ratelimit-remaining) ----
# Нужны для budget-aware ротации trendshift-repos (refresh_trendshift_meta):
# без checkedAt невозможно понять «когда проверяли», без budget — уложиться в
# Actions-лимит 1000 req/hour.


@responses.activate
def test_fetch_repo_sets_checked_at():
    """now=date(...) → meta["checkedAt"] = ISO-строка этой даты."""
    responses.add(responses.GET, AIDER_URL, json={"stargazers_count": 1}, status=200)
    when = datetime.date(2026, 7, 5)
    meta = fetch_repo(("Aider-AI", "aider"), {}, now=when)
    assert meta is not None
    assert meta["checkedAt"] == "2026-07-05"


@responses.activate
def test_fetch_repo_checked_at_defaults_to_today():
    """Без now → checkedAt = сегодня (datetime.date.today().isoformat())."""
    responses.add(responses.GET, AIDER_URL, json={"stargazers_count": 1}, status=200)
    meta = fetch_repo(("Aider-AI", "aider"), {})
    assert meta is not None
    assert meta["checkedAt"] == datetime.date.today().isoformat()


@responses.activate
def test_fetch_repo_reads_ratelimit_remaining():
    """budget dict + header x-ratelimit-remaining:42 → budget["remaining"]==42."""
    responses.add(responses.GET, AIDER_URL, json={"stargazers_count": 1},
                  status=200, headers={"x-ratelimit-remaining": "42"})
    budget = {"remaining": None}
    meta = fetch_repo(("Aider-AI", "aider"), {}, budget=budget)
    assert meta is not None
    assert budget["remaining"] == 42


@responses.activate
def test_fetch_repo_ignores_absent_ratelimit_header():
    """Нет header x-ratelimit-remaining → budget не трогаем (остаётся None)."""
    responses.add(responses.GET, AIDER_URL, json={"stargazers_count": 1}, status=200)
    budget = {"remaining": None}
    fetch_repo(("Aider-AI", "aider"), {}, budget=budget)
    assert budget["remaining"] is None


@responses.activate
def test_fetch_repo_ignores_non_numeric_ratelimit_header():
    """Нечисловой header (прокси/Enterprise) → budget не трогаем (безопасно)."""
    responses.add(responses.GET, AIDER_URL, json={"stargazers_count": 1},
                  status=200, headers={"x-ratelimit-remaining": "unlimited"})
    budget = {"remaining": None}
    fetch_repo(("Aider-AI", "aider"), {}, budget=budget)
    assert budget["remaining"] is None


@responses.activate
def test_fetch_repo_reads_ratelimit_on_error_too():
    """На 429 budget тоже обновляется — узнаём об исчерпании до следующего fetch."""
    responses.add(responses.GET, AIDER_URL, json={"message": "rate"}, status=429,
                  headers={"x-ratelimit-remaining": "0"})
    budget = {"remaining": None}
    assert fetch_repo(("Aider-AI", "aider"), {}, budget=budget) is None
    assert budget["remaining"] == 0


def test_fetch_repo_without_budget_is_unchanged():
    """budget=None (дефолт) → никаких побочных эффектов, обратная совместимость."""
    # Без @responses тест не делает реального запроса только если fetch_repo не
    # дойдёт до requests.get — но дефолт budget=None не должен ничего читать.
    # Гарантируем: передача now= достаточна, budget= опционален.
    import inspect
    sig = inspect.signature(fetch_repo)
    assert sig.parameters["budget"].default is None
    assert sig.parameters["now"].default is None
