"""Тесты fetch_repo — захват основного языка репо из GitHub API.

Язык берётся из поля `language` ответа /repos (без доп. запросов); None, если
GitHub его не определил. Контракт возврата None при rate-limit/ошибке сохраняется.
"""
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
