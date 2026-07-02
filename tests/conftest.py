"""Общие фикстуры для всех уровней тестов.

Тестам нужен импорт скриптов из scripts/. Поскольку scripts/ — не пакет
(скрипты запускаются как `python scripts/x.py`), добавляем директорию в sys.path
через conftest, и тесты импортируют модули напрямую: generate_readme,
update_stars, common.
"""
import json
import sys
from pathlib import Path

import pytest
import yaml

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

# Скрипты импортируются тестами напрямую (import generate_readme и т.д.)
# после того, как директория scripts/ добавлена в sys.path выше.


def pytest_collection_modifyitems(config, items):
    """Авто-skip live-тестов, если не запрошен явный `-m live`.

    Без этого pytest просто запустит помеченные тесты и потратит время на сеть.
    Запуск против реального GitHub: `pytest -m live`.
    """
    marker_expr = config.getoption("-m") or ""
    if "live" in marker_expr:
        return
    skip_live = pytest.mark.skip(reason="needs -m live; hits real GitHub API")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)


@pytest.fixture
def sample_tool_github():
    """GitHub-утилита — даёт бейдж звёзд."""
    return {
        "name": "Aider",
        "url": "https://github.com/Aider-AI/aider",
        "category": "cli-agents",
        "description": {"en": "AI pair programming", "ru": "AI-парное программирование"},
    }


@pytest.fixture
def sample_tool_non_github():
    """Не-GitHub утилита — бейджа звёзд быть не должно."""
    return {
        "name": "SomeSaaS",
        "url": "https://example.com/tool",
        "category": "learning",
        "description": {"en": "A service", "ru": "Сервис"},
    }


@pytest.fixture
def tmp_tools_yml(tmp_path):
    """Фабрика: пишет список tools в YAML-файл в tmp_path, возвращает Path."""
    def _write(tools, filename="tools.yml"):
        data = {"tools": tools}
        p = tmp_path / filename
        p.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
        return p
    return _write


@pytest.fixture
def tmp_stars_file(tmp_path):
    """Фабрика: пишет url→stars в JSON-файл в tmp_path, возвращает Path."""
    def _write(mapping, filename="stars.json"):
        p = tmp_path / filename
        p.write_text(json.dumps(mapping), encoding="utf-8")
        return p
    return _write
