"""Общий код для скриптов проекта.

Здесь живут функции, которые нужны и generate_readme, и update_stars,
чтобы избежать дублирования. Импортируется обоими скриптами и тестами.
"""
from __future__ import annotations


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
