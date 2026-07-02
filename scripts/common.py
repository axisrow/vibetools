"""Общий код для скриптов проекта.

Здесь живут функции, которые нужны нескольким скриптам, чтобы избежать
дублирования. Импортируется generate_readme, update_stars, fetch_candidates
и тестами.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


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


