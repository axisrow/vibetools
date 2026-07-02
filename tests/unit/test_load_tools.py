"""Тесты валидации load_tools — проверяют и поведение, и текст ошибок
(контрибьюторы должны видеть осмысленные сообщения)."""
import pytest

import generate_readme


def test_load_tools_valid(tmp_tools_yml, sample_tool_github):
    path = tmp_tools_yml([sample_tool_github])
    tools = generate_readme.load_tools(path)
    assert len(tools) == 1
    assert tools[0]["name"] == "Aider"


def test_load_tools_multiple(tmp_tools_yml, sample_tool_github, sample_tool_non_github):
    path = tmp_tools_yml([sample_tool_github, sample_tool_non_github])
    assert len(generate_readme.load_tools(path)) == 2


def test_load_tools_unknown_category(tmp_tools_yml):
    bad = {"name": "X", "url": "https://github.com/o/r",
           "category": "bogus", "description": {"en": "e", "ru": "р"}}
    path = tmp_tools_yml([bad])
    with pytest.raises(ValueError, match="Неизвестная категория 'bogus'"):
        generate_readme.load_tools(path)


def test_load_tools_missing_url(tmp_tools_yml):
    bad = {"name": "X", "category": "cli-agents",
           "description": {"en": "e", "ru": "р"}}
    path = tmp_tools_yml([bad])
    with pytest.raises(ValueError, match="Неполная запись"):
        generate_readme.load_tools(path)


def test_load_tools_missing_en(tmp_tools_yml):
    bad = {"name": "X", "url": "https://github.com/o/r",
           "category": "cli-agents", "description": {"ru": "р"}}
    path = tmp_tools_yml([bad])
    with pytest.raises(ValueError, match="Нет описания 'en'"):
        generate_readme.load_tools(path)


def test_load_tools_missing_ru(tmp_tools_yml):
    bad = {"name": "X", "url": "https://github.com/o/r",
           "category": "cli-agents", "description": {"en": "e"}}
    path = tmp_tools_yml([bad])
    with pytest.raises(ValueError, match="Нет описания 'ru'"):
        generate_readme.load_tools(path)


def test_load_tools_missing_description_key(tmp_tools_yml):
    bad = {"name": "X", "url": "https://github.com/o/r", "category": "cli-agents"}
    path = tmp_tools_yml([bad])
    with pytest.raises(ValueError, match="Неполная запись"):
        generate_readme.load_tools(path)


def test_load_tools_empty(tmp_tools_yml):
    path = tmp_tools_yml([])
    assert generate_readme.load_tools(path) == []


def test_load_tools_empty_file(tmp_path):
    path = tmp_path / "tools.yml"
    path.write_text("", encoding="utf-8")
    assert generate_readme.load_tools(path) == []
