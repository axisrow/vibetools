"""Integration: полный цикл generate_readme.main() на временном репо."""
import re

from generate_readme import SHIELDS_STARS, gh_anchor, main


def test_main_creates_both_readmes(tmp_repo):
    main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"])
    assert (tmp_repo["root"] / "README.md").exists()
    assert (tmp_repo["root"] / "README.ru.md").exists()


def test_main_readme_contains_all_tools(tmp_repo):
    main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"])
    for name in ("HiStars", "LoStars", "Editor", "NoGithub"):
        en = (tmp_repo["root"] / "README.md").read_text(encoding="utf-8")
        ru = (tmp_repo["root"] / "README.ru.md").read_text(encoding="utf-8")
        assert name in en
        assert name in ru


def test_main_readme_contains_shields_badges(tmp_repo):
    main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"])
    en = (tmp_repo["root"] / "README.md").read_text(encoding="utf-8")
    assert SHIELDS_STARS.format(owner="a", repo="hi") in en
    assert SHIELDS_STARS.format(owner="b", repo="editor") in en


def test_main_readme_no_badge_for_non_github(tmp_repo):
    main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"])
    # Строка NoGithub не содержит бейджа.
    line = next(
        l for l in (tmp_repo["root"] / "README.md").read_text(encoding="utf-8").splitlines()
        if "NoGithub" in l
    )
    assert "![]" not in line
    assert "shields.io" not in line


def test_main_toc_anchors_resolve_to_sections(tmp_repo):
    """КРИТИЧНО: каждый якорь в TOC соответствует заголовку секции (gh_anchor)."""
    main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"])
    text = (tmp_repo["root"] / "README.md").read_text(encoding="utf-8")
    toc_anchors = set(re.findall(r"\(#([^)]+)\)", text))
    section_titles = re.findall(r"^## (.+)$", text, re.M)
    section_anchors = {gh_anchor(t) for t in section_titles}
    unresolved = toc_anchors - section_anchors
    assert not unresolved, f"TOC-якоря без секции: {unresolved}"


def test_main_sorting_reflected_in_output(tmp_repo):
    """Внутри cli-agents HiStars (1000) идёт раньше LoStars (10)."""
    main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"])
    lines = (tmp_repo["root"] / "README.md").read_text(encoding="utf-8").splitlines()
    i_hi = next(i for i, l in enumerate(lines) if "HiStars" in l)
    i_lo = next(i for i, l in enumerate(lines) if "LoStars" in l)
    assert i_hi < i_lo


def test_main_empty_category_omitted(tmp_repo):
    """Категория без tools не появляется ни в TOC, ни в теле."""
    main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"])
    text = (tmp_repo["root"] / "README.md").read_text(encoding="utf-8")
    # Остальные реальные категории пусты в mini-fixture и не должны попадать в README.
    assert "Observability" not in text
    assert "Context" not in text


def test_main_no_stars_file(tmp_repo):
    """Без stars.json сортировка устойчива (все = 0), README создаётся."""
    tmp_repo["stars_file"].unlink()
    main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"])
    assert (tmp_repo["root"] / "README.md").exists()


def test_main_idempotent(tmp_repo):
    """Два вызова main дают байт-идентичные файлы."""
    main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"])
    first_en = (tmp_repo["root"] / "README.md").read_text(encoding="utf-8")
    first_ru = (tmp_repo["root"] / "README.ru.md").read_text(encoding="utf-8")
    main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"])
    second_en = (tmp_repo["root"] / "README.md").read_text(encoding="utf-8")
    second_ru = (tmp_repo["root"] / "README.ru.md").read_text(encoding="utf-8")
    assert first_en == second_en
    assert first_ru == second_ru
