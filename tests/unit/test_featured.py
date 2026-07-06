"""Тесты is_new (отметка [new]) и HISTORY_FILE-константы."""
import datetime

from generate_readme import HISTORY_FILE, is_new


# --- is_new ---
# is_new читает только created_at (из repos-meta) — золотое правило tools.yml
# запрещает ручное поле «added», поэтому legacy-fallback убран.

def test_is_new_recent():
    today = datetime.date(2026, 7, 3)
    tool = {"created_at": "2026-06-25T00:00:00Z"}  # 8 дней назад
    assert is_new(tool, today) is True


def test_is_new_old():
    today = datetime.date(2026, 7, 3)
    tool = {"created_at": "2026-06-01T00:00:00Z"}  # >14 дней
    assert is_new(tool, today) is False


def test_is_new_no_created_at():
    assert is_new({}) is False


def test_is_new_bad_date():
    assert is_new({"created_at": "not-a-date"}) is False


def test_history_file_constant():
    """HISTORY_FILE указывает на data/stars-history.json."""
    assert HISTORY_FILE.name == "stars-history.json"
