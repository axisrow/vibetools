"""Общий код для скриптов проекта.

Здесь живут функции, которые нужны нескольким скриптам, чтобы избежать
дублирования. Импортируется generate_readme, update_stars, fetch_candidates
и тестами.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Literal

import requests

# Базовый URL GitHub REST API для метаданных репозитория. Вынесен из
# update_stars.py в общее место, чтобы update_stars.fetch_repo и
# common.check_repo_alive не дублировали URL (раньше жил приватно в
# update_stars.API — см._alias ниже).
GITHUB_REPO_API = "https://api.github.com/repos/{owner}/{repo}"

AliveStatus = Literal["alive", "dead", "unknown"]


def github_slug(url: str) -> tuple[str, str] | None:
    """Достаёт (owner, repo) из GitHub URL, иначе None (бейдж не рисуем).

    Принимает любой scheme (https/http/git) и хост github.com.
    Убирает trailing-slash и .git-суффикс у имени репозитория.

    Известное ограничение: для URL с путём глубже /owner/repo
    (например .../repo/issues) второй сегмент возвращается как есть
    ('repo/issues'). В data/tools.yml таких URL нет, поэтому поведение
    зафиксировано тестом и не «чинится» без явного требования.
    """
    if "github.com/" not in url:
        return None
    parts = url.split("github.com/", 1)[1].split("/")
    if len(parts) < 2:
        return None
    owner, repo = parts[0], parts[1].removesuffix(".git")
    return owner, repo


def github_headers() -> dict:
    """Заголовки для запросов к GitHub API: Accept + опциональный токен.

    GITHUB_TOKEN берётся из окружения (если есть) для более высокого
    rate-лимита. Единое место — чтобы все скрипты и тесты использовали
    один рецепт аутентификации и не разъезжались.
    """
    h = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def load_json_or_default(path: Path, default: Any) -> Any:
    """Читает JSON-файл, при отсутствии/битом возвращает default.

    Единое место для толерантной загрузки опциональных JSON-кэшей
    (stars.json, stars-history.json). Устраняет копирование блока
    try/except (JSONDecodeError, OSError) по скриптам.
    """
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def check_repo_alive(slug: tuple[str, str], headers: dict) -> tuple[AliveStatus, dict | None]:
    """Проверяет живость репо через GitHub API; возвращает (статус, meta|None).

    В отличие от update_stars.fetch_repo (который схлопывает ВСЕ ошибки в None
    ради контракта «None → сохранить прежний кэш»), различает три исхода:

    - ``"alive"`` (HTTP 200): репо существует → нормализованный meta-словарь
      (тот же набор полей, что у fetch_repo: stars, archived, …). Вызывающая
      сторона может дополнительно отфильтровать по archived/stars.
    - ``"dead"`` (HTTP 404): репозиторий удалён/недоступен → безопасно выкинуть
      из автособранного кэша.
    - ``"unknown"`` (403/429/5xx/timeout/RequestException): «не смогли
      проверить» — НЕ приравнивается к мёртвому. Любое сомнение трактуется в
      пользу сохранения (симметрия с fetch_repo → None): обрыв сети или
      rate-limit не должен выкашивать живые репо из коллекции.

    На курируемый tools.yml НЕ влияет — применяется только к автособранным
    trendshift-репо (см. update_trendshift._prune_dead_new_repos).
    """
    owner, repo = slug
    url = GITHUB_REPO_API.format(owner=owner, repo=repo)
    try:
        response = requests.get(url, headers=headers, timeout=20)
    except requests.RequestException as exc:
        print(f"  ! {owner}/{repo}: alive-check сетевая ошибка {exc}", file=sys.stderr)
        return "unknown", None
    if response.status_code == 404:
        return "dead", None
    if response.status_code != 200:
        # 403/429 (rate-limit), 5xx, прочее — не знаем, жив ли репо.
        print(f"  ! {owner}/{repo}: alive-check HTTP {response.status_code}", file=sys.stderr)
        return "unknown", None
    try:
        payload = response.json()
    except requests.RequestException as exc:
        # HTTP-200 с не-JSON телом — не можем доверять проверке, считаем unknown.
        print(f"  ! {owner}/{repo}: alive-check битый JSON {exc}", file=sys.stderr)
        return "unknown", None
    return "alive", {
        "stars": payload.get("stargazers_count"),
        "forks": payload.get("forks_count"),
        "openIssues": payload.get("open_issues_count"),
        "pushedAt": payload.get("pushed_at"),
        "createdAt": payload.get("created_at"),
        "topics": payload.get("topics", []) or [],
        "archived": bool(payload.get("archived")),
        "language": payload.get("language"),
        "description": payload.get("description"),
    }


