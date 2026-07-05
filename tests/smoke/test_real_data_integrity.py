"""Smoke-тесты: проверка РЕАЛЬНОГО репозитория на диске (без сети).

Самый ценный здесь — test_real_readme_not_stale: он делает невозможным
коммит «я правил tools.yml, но забыл перегенерировать README».
"""
from collections import Counter
import re
import urllib.error
import urllib.request

import pytest

import generate_readme
from generate_readme import CATEGORIES, CATEGORY_MAP, LEGACY_CATEGORIES, ROOT, TOOLS_YML, TRENDSHIFT_ONLY_CATEGORIES, gh_anchor, load_tools


def test_real_tools_yml_loads():
    """Реальный tools.yml валидируется load_tools без ValueError."""
    tools = load_tools(TOOLS_YML)
    assert tools, "tools.yml пустой"


def test_real_tools_yml_count_reasonable():
    """Ловит случайную порчу/очистку списка."""
    n = len(load_tools(TOOLS_YML))
    assert 10 <= n <= 2000, f"подозрительное число утилит: {n}"


def test_real_tools_yml_all_categories_known():
    for t in load_tools(TOOLS_YML):
        assert t["category"] in CATEGORY_MAP, f"неизвестная категория: {t['category']}"


def test_real_tools_yml_no_legacy_catchall_categories():
    categories = {t["category"] for t in load_tools(TOOLS_YML)}
    assert categories.isdisjoint(LEGACY_CATEGORIES)


def test_real_tools_yml_all_declared_categories_used():
    counts = Counter(t["category"] for t in load_tools(TOOLS_YML))
    # TRENDSHIFT_ONLY_CATEGORIES наполняются только trendshift-discovered репо
    # (обще-разработческие тулы) — в tools.yml их быть не должно, поэтому из
    # проверки «категория должна использоваться» их исключаем.
    empty = [key for key, _ in CATEGORIES
             if counts[key] == 0 and key not in TRENDSHIFT_ONLY_CATEGORIES]
    assert not empty, f"пустые категории: {empty}"


def test_real_tools_yml_needs_review_is_bounded():
    counts = Counter(t["category"] for t in load_tools(TOOLS_YML))
    assert counts["needs-review"] <= 40


def test_real_tools_yml_key_taxonomy_assignments():
    by_name = {t["name"]: t for t in load_tools(TOOLS_YML)}

    assert by_name["OpenCode"]["category"] == "cli-agents"
    assert by_name["hermes-agent"]["category"] == "ai-assistants"
    assert by_name["nanoclaw"]["category"] == "ai-assistants"


def test_real_tools_yml_all_have_en_and_ru():
    for t in load_tools(TOOLS_YML):
        assert "en" in t["description"] and t["description"]["en"], f"нет en: {t['name']}"
        assert "ru" in t["description"] and t["description"]["ru"], f"нет ru: {t['name']}"


def test_real_readmes_non_empty():
    for name in ("README.md", "README.ru.md"):
        p = ROOT / name
        assert p.exists(), f"{name} отсутствует"
        assert p.stat().st_size > 500, f"{name} подозрительно маленький"


def test_real_readme_toc_links_resolve():
    """Все (#anchor) в TOC обоих README резолвятся в gh_anchor section title."""
    for readme_name in ("README.md", "README.ru.md"):
        text = (ROOT / readme_name).read_text(encoding="utf-8")
        toc_anchors = set(re.findall(r"\(#([^)]+)\)", text))
        section_titles = re.findall(r"^## (.+)$", text, re.M)
        section_anchors = {gh_anchor(t) for t in section_titles}
        unresolved = toc_anchors - section_anchors
        assert not unresolved, f"{readme_name}: битые TOC-якоря {unresolved}"


def _strip_featured_block(readme_text: str) -> str:
    """Убирает блок «## Featured» целиком — он date-dependent и не относится
    к «stale tools.yml».

    pick_featured сверяет звёзды с dated-срезами stars-history.json через
    наивный date.today(), а закоммиченный README генерируется кроном в 03:17 UTC
    своей даты. Поэтому Featured-блок законно расходится между свежей
    регенерацией и коммитом в окне 00:00–03:17 UTC (или после пропущенного
    крона) — это не признак того, что куратор забыл перегенерировать README.
    Тело списка (категории/строки) при этом обязано совпадать побайтово.
    """
    # Блок идёт от «## <Featured-title>\n» до следующей «## »-секции. Заголовок
    # секции зависит от языка (en «Featured», ru «Избранное»), поэтому берём
    # объединение FEATURED_TITLES. Берём всё до и всё после блока.
    titles = "|".join(re.escape(t) for t in generate_readme.FEATURED_TITLES.values())
    pattern = rf"^## (?:{titles})\n.*?(?=^## )"
    parts = re.split(pattern, readme_text, flags=re.M | re.S, maxsplit=1)
    return "".join(parts)


def test_real_readme_not_stale():
    """Перегенерировать README в tmp и сравнить с закоммиченным — идентично.

    Ловит «правил tools.yml, забыл перегенерировать README». Featured-блок
    исключён из сравнения — он зависит от наивного today (см. _strip_featured_block).
    """
    import json
    stars_path = ROOT / "data" / "stars.json"
    stars = {}
    if stars_path.exists():
        try:
            stars = json.loads(stars_path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            stars = {}
    tmp_stars = ROOT / "data" / "stars.json.smoke"
    tmp_stars.write_text(json.dumps(stars), encoding="utf-8")

    try:
        # Генерируем во временную директорию и сравниваем с закоммиченным.
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            from pathlib import Path
            generate_readme.main(TOOLS_YML, tmp_stars, out_dir=Path(td))
            for name in ("README.md", "README.ru.md"):
                fresh = _strip_featured_block(
                    (Path(td) / name).read_text(encoding="utf-8"))
                committed = _strip_featured_block(
                    (ROOT / name).read_text(encoding="utf-8"))
                assert fresh == committed, (
                    f"{name}: закоммиченный README не соответствует data/tools.yml. "
                    "Запустите `python scripts/generate_readme.py`."
                )
    finally:
        tmp_stars.unlink(missing_ok=True)


@pytest.mark.live
def test_real_urls_alive():
    """Опционально (маркер live): все URL отвечают < 400. Требует сеть."""
    import urllib.request
    for t in load_tools(TOOLS_YML):
        try:
            req = urllib.request.Request(t["url"], method="HEAD",
                                         headers={"User-Agent": "vibetools-smoke"})
            code = urllib.request.urlopen(req, timeout=15).status
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception:
            pytest.skip("нет сети для live URL-проверки")
        assert code < 400, f"{t['name']}: {t['url']} → {code}"
