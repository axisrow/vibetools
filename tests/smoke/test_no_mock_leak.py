"""Smoke-ловушка: кэши data/*.json не должны содержать mock-URL из тестовых fixtures.

Защита от регрессии утечки: если какой-то тест пишет в реальные
data/repos-meta.json / stars.json / stars-history.json без tmp-изоляции,
mock-маркеры (github.com/a/hi, a/lo, b/editor, example.com/tool) всплывут
здесь, и CI упадёт ДО коммита.

Маркеры взяты из tmp_repo fixtures (tests/integration/conftest.py,
tests/e2e/conftest.py).
"""
import pytest

from generate_readme import ROOT

# URL-маркеры тестовых fixtures — их НИКОГДА не должно быть в реальных кэшах.
MOCK_MARKERS = [
    "github.com/a/hi",
    "github.com/a/lo",
    "github.com/b/editor",
    "example.com/tool",
]
CACHE_FILES = ["data/repos-meta.json", "data/stars.json", "data/stars-history.json"]


@pytest.mark.parametrize("rel", CACHE_FILES)
def test_no_mock_data_in_caches(rel):
    """Кэш-файл не содержит ни одного mock-маркера из тестовых fixtures."""
    path = ROOT / rel
    if not path.exists():
        pytest.skip(f"{rel} ещё не сгенерирован (Action/update_stars не запускался)")
    content = path.read_text(encoding="utf-8")
    leaked = [m for m in MOCK_MARKERS if m in content]
    assert not leaked, (
        f"{rel} загрязнён mock-данными из тестов: {leaked}. "
        "Какой-то вызов update_stars.main()/generate_site.main() пишет в реальный "
        "кэш без tmp-изоляции — добавь meta_file=/history_file=/stars_file= в тест."
    )
