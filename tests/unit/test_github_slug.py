"""Тесты github_slug (общий код в scripts/common.py)."""
import pytest

from common import github_slug


@pytest.mark.parametrize("url, expected", [
    ("https://github.com/anthropics/claude-code", ("anthropics", "claude-code")),
    ("https://github.com/Aider-AI/aider", ("Aider-AI", "aider")),
    ("http://github.com/owner/repo", ("owner", "repo")),            # без https
    ("https://github.com/owner/repo.git", ("owner", "repo")),       # .git-суффикс
    ("https://github.com/owner/repo/", ("owner", "repo")),          # trailing slash
    ("git://github.com/owner/repo", ("owner", "repo")),             # git:// scheme
    ("https://gitlab.com/owner/repo", None),                         # не github
    ("https://example.com/foo", None),                               # не github.com
    ("https://github.com/onlyowner", None),                          # нет второго сегмента
    ("https://github.com/", None),
    ("", None),
    ("not a url", None),
])
def test_github_slug(url, expected):
    assert github_slug(url) == expected


def test_github_slug_deep_path_truncates_to_second_segment():
    """Путь глубже /owner/repo тихо обрезается до второго сегмента.

    split("/") даёт ['owner','repo','issues'], берётся только parts[1]='repo' —
    глубокие сегменты отбрасываются. Это безопасное поведение для наших данных
    (в tools.yml только /owner/repo URL). Зафиксировано тестом.
    """
    assert github_slug("https://github.com/owner/repo/issues") == ("owner", "repo")
