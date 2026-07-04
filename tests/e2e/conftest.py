"""Fixtures для e2e-тестов: mock GitHub API + готовое мини-репо."""
import pytest
import yaml


@pytest.fixture
def tmp_repo(tmp_path):
    """Готовое мини-репо для e2e: 3 github-утилиты + 1 не-github.

    Возвращает dict: {tools_yml, stars_file, history_file, root, tools}.
    history_file указывает в tmp, чтобы тесты не писали mock-данные в
    реальный source tree.
    """
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    tools_yml = data_dir / "tools.yml"
    stars_file = data_dir / "stars.json"
    history_file = data_dir / "stars-history.json"
    meta_file = data_dir / "repos-meta.json"

    tools = [
        {"name": "HiStars", "url": "https://github.com/a/hi",
         "category": "cli-agents",
         "description": {"en": "High stars", "ru": "Много звёзд"}},
        {"name": "LoStars", "url": "https://github.com/a/lo",
         "category": "cli-agents",
         "description": {"en": "Low stars", "ru": "Мало звёзд"}},
        {"name": "Editor", "url": "https://github.com/b/editor",
         "category": "editor-integrations",
         "description": {"en": "An editor", "ru": "Редактор"}},
        {"name": "NoGithub", "url": "https://example.com/tool",
         "category": "learning-resources",
         "description": {"en": "Not on github", "ru": "Не на github"}},
    ]
    tools_yml.write_text(
        yaml.safe_dump({"tools": tools}, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return {"tools_yml": tools_yml, "stars_file": stars_file,
            "history_file": history_file, "meta_file": meta_file,
            "root": tmp_path, "tools": tools}


@pytest.fixture
def mock_github(httpserver):
    """Настраивает pytest-httpserver отвечать как api.github.com/repos/*.

    Возвращает функцию register(owner, repo, stars=..., status=200), которой
    тест регистрирует ответы. Базовый URL доступен как mock_github.base_url.
    """
    def register(owner, repo, stars=None, status=200, language=None):
        path = f"/repos/{owner}/{repo}"
        if status == 200:
            httpserver.expect_request(path).respond_with_json(
                {"stargazers_count": stars, "language": language}, status=200)
        else:
            httpserver.expect_request(path).respond_with_data("", status=status)
    httpserver.register = register
    httpserver.base_url = httpserver.url_for("").rstrip("/")
    return httpserver
