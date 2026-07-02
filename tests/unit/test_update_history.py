"""Тесты update_history — dated-срезы звёзд для дельт 1д/7д."""
import json

from update_stars import HISTORY_DAYS, update_history


def test_update_history_creates_snapshot(tmp_path):
    hf = tmp_path / "stars-history.json"
    today = "2026-07-03"
    cache = {"u1": 100, "u2": 50}
    update_history(hf, today, cache)
    data = json.loads(hf.read_text(encoding="utf-8"))
    assert data["u1"][today] == 100
    assert data["u2"][today] == 50


def test_update_history_appends_new_day(tmp_path):
    hf = tmp_path / "stars-history.json"
    update_history(hf, "2026-07-02", {"u1": 90})
    update_history(hf, "2026-07-03", {"u1": 100})
    data = json.loads(hf.read_text(encoding="utf-8"))
    assert set(data["u1"].keys()) == {"2026-07-02", "2026-07-03"}


def test_update_history_idempotent_same_day(tmp_path):
    """Повторный прогон в тот же день перезаписывает срез, не дублирует."""
    hf = tmp_path / "stars-history.json"
    update_history(hf, "2026-07-03", {"u1": 100})
    update_history(hf, "2026-07-03", {"u1": 105})  # исправили число
    data = json.loads(hf.read_text(encoding="utf-8"))
    assert data["u1"] == {"2026-07-03": 105}


def test_update_history_trims_to_history_days(tmp_path):
    """Хранится только HISTORY_DAYS самых свежих дат."""
    hf = tmp_path / "stars-history.json"
    # заполняем 10 дней
    for i in range(10):
        day = f"2026-07-{i:02d}"
        update_history(hf, day, {"u1": i})
    data = json.loads(hf.read_text(encoding="utf-8"))
    assert len(data["u1"]) == HISTORY_DAYS
    # самые свежие даты остались
    assert "2026-07-09" in data["u1"]
    assert "2026-07-00" not in data["u1"]  # старая выкинута


def test_update_history_broken_existing(tmp_path):
    """Битый существующий файл не валит — начинаем с пустой истории."""
    hf = tmp_path / "stars-history.json"
    hf.write_text("{not json", encoding="utf-8")
    update_history(hf, "2026-07-03", {"u1": 100})
    data = json.loads(hf.read_text(encoding="utf-8"))
    assert data == {"u1": {"2026-07-03": 100}}
