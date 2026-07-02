"""Тесты render_line — формат строки, наличие/отсутствие бейджа звёзд."""
from generate_readme import SHIELDS_STARS, render_line


def test_render_line_github_with_badge(sample_tool_github):
    line = render_line(sample_tool_github, "en")
    assert SHIELDS_STARS.format(owner="Aider-AI", repo="aider") in line
    assert line.startswith("- [Aider](https://github.com/Aider-AI/aider)")


def test_render_line_non_github_no_badge(sample_tool_non_github):
    line = render_line(sample_tool_non_github, "en")
    assert "![]" not in line
    assert "shields.io" not in line
    assert line == "- [SomeSaaS](https://example.com/tool) — A service"


def test_render_line_en(sample_tool_github):
    assert "AI pair programming" in render_line(sample_tool_github, "en")


def test_render_line_ru(sample_tool_github):
    assert "AI-парное программирование" in render_line(sample_tool_github, "ru")


def test_render_line_format_exact(sample_tool_github):
    expected = (
        "- [Aider](https://github.com/Aider-AI/aider) "
        f"![]({SHIELDS_STARS.format(owner='Aider-AI', repo='aider')}) "
        "— AI pair programming"
    )
    assert render_line(sample_tool_github, "en") == expected


def test_render_line_dot_git_url():
    tool = {"name": "X", "url": "https://github.com/owner/repo.git",
            "category": "cli-agents",
            "description": {"en": "desc", "ru": "оп"}}
    line = render_line(tool, "en")
    # Текст ссылки остаётся как в исходном URL (с .git)...
    assert "https://github.com/owner/repo.git)" in line
    # ...а бейдж строится из github_slug, который .git убирает.
    assert "repo.git?" not in line
    assert SHIELDS_STARS.format(owner="owner", repo="repo") in line


# --- Пороги звёзд (эмодзи-префиксы ⭐/🌟/✨) ---

def test_render_line_star_tier_50k():
    line = render_line(sample_tool_github(), "en", stars=50000)
    assert "⭐" in line


def test_render_line_star_tier_10k():
    line = render_line(sample_tool_github(), "en", stars=10000)
    assert "🌟" in line
    assert "⭐" not in line


def test_render_line_star_tier_1k():
    line = render_line(sample_tool_github(), "en", stars=1000)
    assert "✨" in line


def test_render_line_star_tier_below_1k():
    line = render_line(sample_tool_github(), "en", stars=999)
    assert "✨" not in line and "🌟" not in line and "⭐" not in line


# --- Отметки (🏆/📅/🏅/🆕) ---

def test_render_line_marks_day_week():
    line = render_line(sample_tool_github(), "en", marks={"day", "week"})
    assert "🏆" in line and "📅" in line


def test_render_line_mark_verified():
    line = render_line(sample_tool_github(), "en", marks={"verified"})
    assert "🏅" in line


def test_render_line_mark_new():
    line = render_line(sample_tool_github(), "en", marks={"new"})
    assert "🆕" in line


def sample_tool_github():
    return {"name": "Aider", "url": "https://github.com/Aider-AI/aider",
            "category": "cli-agents",
            "description": {"en": "AI pair programming", "ru": "AI-парное программирование"}}
