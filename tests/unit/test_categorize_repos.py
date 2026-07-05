"""Tests for auto-categorization of trendshift-discovered repos."""
import datetime

from categorize_repos import (
    DEFAULT_CATEGORY,
    TOPIC_CATEGORY_MAP,
    categorize,
    enrich_repos_with_category,
)


def test_categorize_topic_match_wins():
    """GitHub topic → category (сильнейший сигнал)."""
    cat, reason = categorize({"topics": ["ai-agent"]})
    assert cat == "cli-agents"
    assert reason == "topic:ai-agent"


def test_categorize_description_fallback():
    """Нет topic, но описание содержит ключевую фразу → category из desc."""
    cat, reason = categorize({"description": "A coding agent for the terminal"})
    assert cat == "cli-agents"
    assert reason == "desc:coding agent"


def test_categorize_unknown_returns_needs_review_never_other():
    """Ничего не смэтчилось → 'needs-review' (НЕ 'other' — того нет в CATEGORIES)."""
    cat, _ = categorize({"topics": ["unrelated-topic"], "description": "a thing"})
    assert cat == "needs-review"
    assert cat == DEFAULT_CATEGORY
    assert cat != "other"


def test_categorize_topic_case_insensitive():
    """Topic 'AI-Agent' (mixed case) маппится так же, как 'ai-agent'."""
    cat, _ = categorize({"topics": ["AI-Agent"]})
    assert cat == "cli-agents"


def test_categorize_topic_priority_over_desc():
    """Topic имеет приоритет над описанием (topic — автор-куратор на GitHub)."""
    # topic → mcp, хотя описание могло бы смэтчить на что-то другое.
    cat, reason = categorize({"topics": ["mcp-server"], "description": "a coding agent"})
    assert cat == "mcp"
    assert reason == "topic:mcp-server"


def test_enrich_skips_repos_with_existing_category():
    """Репо с непустой category не рефетчится (инкрементальность)."""
    calls = []

    def fetcher(slug, headers):
        calls.append(slug)
        return {"topics": ["ai-agent"], "description": "x"}

    repos = [{"githubUrl": "https://github.com/foo/bar", "category": "cli-agents"}]
    enrich_repos_with_category(repos, fetcher=fetcher, max_per_run=10)

    assert calls == []  # не звали — категория уже есть
    assert repos[0]["category"] == "cli-agents"  # сохранена


def test_enrich_marks_uncategorized_on_rate_limit():
    """fetcher→None (rate-limit/404) → needs-review + uncategorized + categoryAt."""
    today = "2026-07-05"
    repos = [{"githubUrl": "https://github.com/foo/bar"}]
    enrich_repos_with_category(
        repos, fetcher=lambda slug, h: None, max_per_run=10, now=datetime.date(2026, 7, 5),
    )
    rec = repos[0]
    assert rec["category"] == "needs-review"
    assert rec["categoryReason"] == "uncategorized"
    assert rec["categoryAt"] == today


def test_enrich_respects_max_per_run():
    """max_per_run ограничивает число GitHub-запросов за прогон (rate-limit throttle)."""
    calls = []

    def fetcher(slug, headers):
        calls.append(slug)
        return {"topics": ["ai-agent"]}

    repos = [{"githubUrl": f"https://github.com/o/r{i}"} for i in range(100)]
    enrich_repos_with_category(repos, fetcher=fetcher, max_per_run=10)

    assert len(calls) == 10  # только 10 из 100
    categorized = sum(1 for r in repos if r.get("category") and r.get("category") != "needs-review" or r.get("categoryReason") == "topic:ai-agent")
    # 10 смэтчились на topic:ai-agent; остальные без category (ждут след. прогона).
    assert categorized == 10
    assert sum(1 for r in repos if "category" not in r) == 90


def test_enrich_persists_topics_and_language():
    """Обогащающие поля (topics/language/description/name) попадают на запись."""
    repos = [{"githubUrl": "https://github.com/foo/bar"}]
    enrich_repos_with_category(
        repos,
        fetcher=lambda slug, h: {
            "topics": ["ai-agent", "llm"], "language": "Python",
            "description": "An agent", "name": "bar",
        },
        max_per_run=10, now=datetime.date(2026, 7, 5),
    )
    rec = repos[0]
    assert rec["category"] == "cli-agents"
    assert rec["topics"] == ["ai-agent", "llm"]
    assert rec["language"] == "Python"
    assert rec["description"] == "An agent"
    assert rec["name"] == "bar"


def test_enrich_sleeps_between_requests(monkeypatch):
    """Между fetch-запросами есть sleep (уважение к rate-limit)."""
    sleeps = []
    monkeypatch.setattr("categorize_repos.time.sleep", lambda s: sleeps.append(s))
    repos = [{"githubUrl": f"https://github.com/o/r{i}"} for i in range(3)]
    enrich_repos_with_category(
        repos, fetcher=lambda slug, h: {"topics": ["ai-agent"]},
        max_per_run=10, sleep_between=0.5,
    )
    # 3 запроса → 2 sleep (не после последнего).
    assert len(sleeps) == 2
    assert all(s == 0.5 for s in sleeps)


def test_topic_category_map_only_known_categories():
    """Все категории в TOPIC_CATEGORY_MAP валидны (рассинхрон с taxonomy падает громко)."""
    from generate_readme import CATEGORY_MAP
    bad = [cat for cat in set(TOPIC_CATEGORY_MAP.values()) if cat not in CATEGORY_MAP]
    assert not bad, f"TOPIC_CATEGORY_MAP ссылается на неизвестные категории: {bad}"


def test_enrich_non_github_url_marked_needs_review():
    """URL без github slug (негитхаб) → needs-review без fetcher-вызова."""
    calls = []
    repos = [{"githubUrl": "https://example.com/some/tool"}]
    enrich_repos_with_category(repos, fetcher=lambda slug, h: calls.append(slug) or {}, max_per_run=10)
    assert repos[0]["category"] == "needs-review"
    assert calls == []
