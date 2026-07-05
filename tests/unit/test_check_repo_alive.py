"""Тесты common.check_repo_alive — детектор живости репо через GitHub API.

Контракт: 200 → ("alive", meta); 404 → ("dead", None); 403/429/5xx/timeout/
ConnectionError → ("unknown", None). Симметрия с fetch_repo (любое сомнение
трактуется в пользу сохранения), но в отличие от fetch_repo различает dead
(удалять) и unknown (оставить). Паттерн @responses — как test_fetch_repo_language.
"""
from __future__ import annotations

import responses

from common import GITHUB_REPO_API, check_repo_alive

AIDER = ("Aider-AI", "aider")
AIDER_URL = GITHUB_REPO_API.format(owner="Aider-AI", repo="aider")


@responses.activate
def test_check_repo_alive_returns_alive_with_meta():
    """200 + полный ответ → ('alive', нормализованный meta-словарь)."""
    responses.add(responses.GET, AIDER_URL, json={
        "stargazers_count": 42,
        "forks_count": 7,
        "open_issues_count": 3,
        "pushed_at": "2026-07-01T00:00:00Z",
        "created_at": "2024-01-01T00:00:00Z",
        "topics": ["ai", "cli"],
        "archived": False,
        "language": "Python",
        "description": "AI pair programming",
    }, status=200)
    status, meta = check_repo_alive(AIDER, {})
    assert status == "alive"
    assert meta is not None
    assert meta["stars"] == 42
    assert meta["forks"] == 7
    assert meta["archived"] is False
    assert meta["language"] == "Python"
    assert meta["topics"] == ["ai", "cli"]
    assert meta["createdAt"] == "2024-01-01T00:00:00Z"


@responses.activate
def test_check_repo_alive_returns_dead_on_404():
    """404 → ('dead', None) — репозиторий удалён, безопасно выкинуть."""
    responses.add(responses.GET, AIDER_URL, json={"message": "Not Found"}, status=404)
    status, meta = check_repo_alive(AIDER, {})
    assert status == "dead"
    assert meta is None


@responses.activate
def test_check_repo_alive_returns_unknown_on_rate_limit_429():
    """429 (rate-limit) → ('unknown', None) — не выкидываем живое репо."""
    responses.add(responses.GET, AIDER_URL, json={"message": "rate"}, status=429)
    status, meta = check_repo_alive(AIDER, {})
    assert status == "unknown"
    assert meta is None


@responses.activate
def test_check_repo_alive_returns_unknown_on_403():
    """403 (запрет/rate-limit) → ('unknown', None)."""
    responses.add(responses.GET, AIDER_URL, json={"message": "forbidden"}, status=403)
    status, meta = check_repo_alive(AIDER, {})
    assert status == "unknown"
    assert meta is None


@responses.activate
def test_check_repo_alive_returns_unknown_on_5xx():
    """500 (сбой сервера GitHub) → ('unknown', None) — кратковременный сбой."""
    responses.add(responses.GET, AIDER_URL, json={"message": "server error"}, status=500)
    status, meta = check_repo_alive(AIDER, {})
    assert status == "unknown"
    assert meta is None


@responses.activate
def test_check_repo_alive_returns_unknown_on_connection_error():
    """ConnectionError (обрыв сети/timeout) → ('unknown', None)."""
    responses.add(responses.GET, AIDER_URL, body=responses.ConnectionError("dropped"))
    status, meta = check_repo_alive(AIDER, {})
    assert status == "unknown"
    assert meta is None


@responses.activate
def test_check_repo_alive_returns_unknown_on_broken_json():
    """HTTP 200 с не-JSON телом → ('unknown', None) — не доверяем проверке."""
    responses.add(responses.GET, AIDER_URL, body="<html>not json</html>", status=200,
                  content_type="text/html")
    status, meta = check_repo_alive(AIDER, {})
    assert status == "unknown"
    assert meta is None
