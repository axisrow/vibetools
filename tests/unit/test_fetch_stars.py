"""Тесты fetch_stars — мок requests через responses.

Покрывает все ветви: успех, rate-limit, 404, неожиданная ошибка, таймаут,
отсутствие поля stargazers_count, прокидывание Authorization-заголовка.
"""
import requests
import responses

from update_stars import API, fetch_stars

AIDER_URL = API.format(owner="Aider-AI", repo="aider")


@responses.activate
def test_fetch_stars_200():
    responses.add(responses.GET, AIDER_URL, json={"stargazers_count": 42}, status=200)
    assert fetch_stars(("Aider-AI", "aider"), {}) == 42


@responses.activate
def test_fetch_stars_403_rate_limit():
    responses.add(responses.GET, AIDER_URL, json={"message": "rate"}, status=403)
    assert fetch_stars(("Aider-AI", "aider"), {}) is None


@responses.activate
def test_fetch_stars_429_rate_limit():
    responses.add(responses.GET, AIDER_URL, json={"message": "rate"}, status=429)
    assert fetch_stars(("Aider-AI", "aider"), {}) is None


@responses.activate
def test_fetch_stars_404():
    responses.add(responses.GET, AIDER_URL, json={"message": "Not Found"}, status=404)
    assert fetch_stars(("Aider-AI", "aider"), {}) is None


@responses.activate
def test_fetch_stars_500_unexpected():
    responses.add(responses.GET, AIDER_URL, json={"message": "boom"}, status=500)
    assert fetch_stars(("Aider-AI", "aider"), {}) is None


@responses.activate
def test_fetch_stars_timeout():
    responses.add(responses.GET, AIDER_URL, body=requests.Timeout("timed out"))
    assert fetch_stars(("Aider-AI", "aider"), {}) is None


@responses.activate
def test_fetch_stars_missing_stargazers_field():
    """200, но в ответе нет stargazers_count → .get возвращает None."""
    responses.add(responses.GET, AIDER_URL, json={"other": "field"}, status=200)
    assert fetch_stars(("Aider-AI", "aider"), {}) is None


@responses.activate
def test_fetch_stars_passes_authorization_header():
    responses.add(responses.GET, AIDER_URL, json={"stargazers_count": 1}, status=200)
    headers = {"Authorization": "Bearer ghp_secret", "Accept": "application/vnd.github+json"}
    fetch_stars(("Aider-AI", "aider"), headers)
    sent = responses.calls[0].request
    assert sent.headers["Authorization"] == "Bearer ghp_secret"
