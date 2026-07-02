"""Тесты load_stars — толерантность к отсутствию и битому кэшу."""
import generate_readme


def test_load_stars_missing_file(tmp_path):
    assert generate_readme.load_stars(tmp_path / "nope.json") == {}


def test_load_stars_valid(tmp_path):
    p = tmp_path / "stars.json"
    p.write_text('{"https://github.com/o/r": 42}', encoding="utf-8")
    assert generate_readme.load_stars(p) == {"https://github.com/o/r": 42}


def test_load_stars_broken_json(tmp_path):
    p = tmp_path / "stars.json"
    p.write_text("{not valid json", encoding="utf-8")
    assert generate_readme.load_stars(p) == {}


def test_load_stars_empty_file(tmp_path):
    p = tmp_path / "stars.json"
    p.write_text("", encoding="utf-8")
    assert generate_readme.load_stars(p) == {}
