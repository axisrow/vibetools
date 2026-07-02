"""Тесты выбора репо дня/недели и отметок: is_new, pick_featured, render_featured."""
import datetime

from generate_readme import (HISTORY_FILE, is_new, pick_featured,
                             render_featured)


# --- is_new ---

def test_is_new_recent():
    today = datetime.date(2026, 7, 3)
    tool = {"added": "2026-06-25"}  # 8 дней назад
    assert is_new(tool, today) is True


def test_is_new_old():
    today = datetime.date(2026, 7, 3)
    tool = {"added": "2026-06-01"}  # >14 дней
    assert is_new(tool, today) is False


def test_is_new_no_added():
    assert is_new({}) is False


def test_is_new_bad_date():
    assert is_new({"added": "not-a-date"}) is False


# --- pick_featured ---

def _tool(url):
    return {"name": "X", "url": url, "category": "cli-agents",
            "description": {"en": "e", "ru": "р"}}


def test_pick_featured_day_and_week():
    today = datetime.date.today()
    y1 = (today - datetime.timedelta(days=1)).isoformat()
    y7 = (today - datetime.timedelta(days=7)).isoformat()
    tools = [_tool("u1"), _tool("u2"), _tool("u3")]
    stars = {"u1": 110, "u2": 60, "u3": 30}
    # u1 вырос на 10 за 1д (макс день), u3 вырос на 25 за 7д (макс неделя)
    history = {
        "u1": {y1: 100},
        "u2": {y1: 55},
        "u3": {y7: 5},
    }
    featured = pick_featured(tools, stars, history)
    assert "day" in featured["u1"]
    assert "week" in featured["u3"]


def test_pick_featured_no_history():
    """Без истории дельты не считаются → пустой featured."""
    tools = [_tool("u1")]
    assert pick_featured(tools, {"u1": 100}, {}) == {}


def test_pick_featured_no_positive_delta():
    """Звёзды не выросли → репо дня/недели нет."""
    today = datetime.date.today()
    y1 = (today - datetime.timedelta(days=1)).isoformat()
    tools = [_tool("u1")]
    featured = pick_featured(tools, {"u1": 100}, {"u1": {y1: 100}})
    assert featured == {}


def test_pick_featured_missing_current_stars():
    """Нет текущего числа звёзд → пропуск."""
    tools = [_tool("u1")]
    assert pick_featured(tools, {}, {"u1": {"2026-07-02": 100}}) == {}


# --- render_featured ---

def test_render_featured_empty():
    assert render_featured({}, {}, "en") == ""


def test_render_featured_day_only():
    featured = {"u1": {"day"}}
    by_url = {"u1": _tool("u1")}
    out = render_featured(featured, by_url, "en")
    assert "## Featured" in out
    assert "Repo of the day" in out
    assert "u1" in out


def test_render_featured_ru():
    featured = {"u1": {"week"}}
    by_url = {"u1": _tool("u1")}
    out = render_featured(featured, by_url, "ru")
    assert "Репозиторий недели" in out


def test_render_featured_day_and_week_same_repo():
    featured = {"u1": {"day", "week"}}
    by_url = {"u1": _tool("u1")}
    out = render_featured(featured, by_url, "en")
    assert "Repo of the day" in out
    assert "Repo of the week" in out


def test_history_file_constant():
    """HISTORY_FILE указывает на data/stars-history.json."""
    assert HISTORY_FILE.name == "stars-history.json"
