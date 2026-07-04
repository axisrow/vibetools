"""Fixtures для integration-тестов: готовое мини-репо в tmp_path."""
import json

import pytest
import yaml


@pytest.fixture
def tmp_repo(tmp_path):
    """Создаёт мини-репо: tmp_path/data/tools.yml (3 записи 2 категорий,
    одна не-github), tmp_path/data/stars.json.

    Возвращает dict с путями: {tools_yml, stars_file, history_file, root}.
    history_file указывает в tmp, чтобы тесты не писали mock-данные в
    реальный source tree (data/stars-history.json).
    """
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    tools_yml = data_dir / "tools.yml"
    stars_file = data_dir / "stars.json"
    history_file = data_dir / "stars-history.json"
    meta_file = data_dir / "repos-meta.json"
    trendshift_file = data_dir / "trendshift.json"

    tools = [
        {"name": "HiStars", "url": "https://github.com/a/hi",
         "category": "cli-agents",
         "description": {"en": "High stars tool", "ru": "Много звёзд"}},
        {"name": "LoStars", "url": "https://github.com/a/lo",
         "category": "cli-agents",
         "description": {"en": "Low stars tool", "ru": "Мало звёзд"}},
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
    # HiStars=1000, LoStars=10 → внутри cli-agents HiStars должен идти первым.
    stars_file.write_text(json.dumps({
        "https://github.com/a/hi": 1000,
        "https://github.com/a/lo": 10,
    }), encoding="utf-8")

    return {"tools_yml": tools_yml, "stars_file": stars_file,
            "history_file": history_file, "meta_file": meta_file,
            "trendshift_file": trendshift_file,
            "root": tmp_path, "tools": tools}
