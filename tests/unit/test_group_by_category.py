"""Тесты group_by_category — сортировка, стабильность, полнота категорий."""
from generate_readme import CATEGORIES, group_by_category

URL_HI = "https://github.com/a/hi"
URL_MID = "https://github.com/a/mid"
URL_LO = "https://github.com/a/lo"
URL_NOSTARS = "https://github.com/a/nostars"


def _tool(name, url, category="cli-agents"):
    return {"name": name, "url": url, "category": category,
            "description": {"en": "e", "ru": "р"}}


def test_group_sorts_descending_by_stars():
    tools = [_tool("Lo", URL_LO), _tool("Hi", URL_HI), _tool("Mid", URL_MID)]
    stars = {URL_HI: 100, URL_MID: 50, URL_LO: 10}
    groups = group_by_category(tools, stars)
    order = [t["url"] for t in groups["cli-agents"]]
    assert order == [URL_HI, URL_MID, URL_LO]


def test_group_missing_stars_treated_as_zero():
    tools = [_tool("Hi", URL_HI), _tool("NoStars", URL_NOSTARS)]
    stars = {URL_HI: 100}  # URL_NOSTARS отсутствует → 0 → в конце
    groups = group_by_category(tools, stars)
    order = [t["url"] for t in groups["cli-agents"]]
    assert order == [URL_HI, URL_NOSTARS]


def test_group_equal_stars_stable():
    """Равные звёзды — сохраняют входной порядок (sorted стабилен)."""
    tools = [_tool("First", URL_HI), _tool("Second", URL_MID), _tool("Third", URL_LO)]
    stars = {URL_HI: 50, URL_MID: 50, URL_LO: 50}
    groups = group_by_category(tools, stars)
    order = [t["url"] for t in groups["cli-agents"]]
    assert order == [URL_HI, URL_MID, URL_LO]


def test_group_all_categories_present():
    groups = group_by_category([], {})
    for key, _ in CATEGORIES:
        assert key in groups
        assert groups[key] == []


def test_group_tools_in_correct_category():
    tools = [_tool("A", URL_HI, "cli-agents"),
             _tool("B", URL_MID, "editor-integrations")]
    groups = group_by_category(tools, {})
    assert [t["url"] for t in groups["cli-agents"]] == [URL_HI]
    assert [t["url"] for t in groups["editor-integrations"]] == [URL_MID]


def test_group_empty_tools():
    groups = group_by_category([], {URL_HI: 100})
    assert all(v == [] for v in groups.values())
