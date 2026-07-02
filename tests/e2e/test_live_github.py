"""Live e2e — против РЕАЛЬНОГО GitHub API.

По умолчанию ПРОПУСКАЮТСЯ (см. tests/conftest.py: pytest_collection_modifyitems).
Запуск: pytest -m live

В nightly workflow проходит с GITHUB_TOKEN (5000 req/h — более чем достаточно
для 1-2 репозиториев). Без сети/токена могут падать на rate-limit — это нормально
для live-теста.
"""
import json

import pytest

from common import github_slug
from update_stars import fetch_stars, main as update_main


@pytest.mark.live
def test_live_fetch_aider_stars():
    """Реальный GitHub API: Aider давно > 1k звёзд."""
    slug = github_slug("https://github.com/Aider-AI/aider")
    stars = fetch_stars(slug, {})
    assert stars is not None, "GitHub API не ответил (rate-limit/сеть?)"
    assert stars > 1000


@pytest.mark.live
def test_live_update_stars_one_repo(tmp_path):
    """Полный update_stars на tmp-репо с одной записью против реального API."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    tools_yml = data_dir / "tools.yml"
    stars_file = data_dir / "stars.json"
    tools_yml.write_text(
        "tools:\n"
        "  - name: Aider\n"
        "    url: https://github.com/Aider-AI/aider\n"
        "    category: cli-agents\n"
        "    description:\n"
        "      en: AI pair programming\n"
        "      ru: AI-парное программирование\n",
        encoding="utf-8",
    )

    rc = update_main(tools_yml, stars_file, out_dir=tmp_path)
    cache = json.loads(stars_file.read_text(encoding="utf-8"))
    assert rc == 0
    assert "https://github.com/Aider-AI/aider" in cache
    assert isinstance(cache["https://github.com/Aider-AI/aider"], int)
    assert cache["https://github.com/Aider-AI/aider"] > 1000
    # README регенерирован с бейджем.
    assert "img.shields.io/github/stars/Aider-AI/aider" in \
        (tmp_path / "README.md").read_text(encoding="utf-8")
