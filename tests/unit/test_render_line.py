"""Тесты render_line — канонический формат awesome-list: - [Name](url) badge - Desc."""
from generate_readme import SHIELDS_STARS, render_line


def test_render_line_github_with_badge(sample_tool_github):
    line = render_line(sample_tool_github, "en")
    assert SHIELDS_STARS.format(owner="Aider-AI", repo="aider") in line
    assert line.startswith("- [Aider](https://github.com/Aider-AI/aider)")


def test_render_line_non_github_no_badge(sample_tool_non_github):
    line = render_line(sample_tool_non_github, "en")
    assert "![]" not in line
    assert "shields.io" not in line
    assert line == "- [SomeSaaS](https://example.com/tool) - A service."


def test_render_line_dash_separator(sample_tool_github):
    """Канонический разделитель — ' - ' (требование awesome-list-item)."""
    line = render_line(sample_tool_github, "en")
    assert " - " in line
    assert "—" not in line


def test_render_line_capitalized_description(sample_tool_github):
    """Описание должно начинаться с заглавной буквы (требование awesome-list-item)."""
    line = render_line(sample_tool_github, "en")
    # После бейджа и ' - ' идёт заглавная.
    desc = line.split(" - ", 1)[1]
    assert desc[0].isupper()


def test_render_line_ends_with_period(sample_tool_github):
    assert render_line(sample_tool_github, "en").rstrip().endswith(".")


def test_render_line_en(sample_tool_github):
    assert "AI pair programming" in render_line(sample_tool_github, "en")


def test_render_line_ru(sample_tool_github):
    assert "AI-парное программирование" in render_line(sample_tool_github, "ru")


def test_render_line_format_exact(sample_tool_github):
    expected = (
        "- [Aider](https://github.com/Aider-AI/aider) "
        f"![]({SHIELDS_STARS.format(owner='Aider-AI', repo='aider')}) "
        "- AI pair programming."
    )
    assert render_line(sample_tool_github, "en") == expected


def test_render_line_strips_leading_emoji():
    """Ведущие эмодзи в описании вычищаются (ломают awesome-list-item)."""
    tool = {"name": "X", "url": "https://github.com/o/r", "category": "cli-agents",
            "description": {"en": "🌐 Make websites", "ru": "Р"}}
    line = render_line(tool, "en")
    assert "🌐" not in line
    assert "Make" in line


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
