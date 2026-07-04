from fetch_candidates import QUERIES
from generate_readme import CATEGORY_MAP


def test_fetch_candidate_queries_use_known_non_catchall_categories():
    legacy = {"other", "prompt-mcp", "workflow-automation", "learning"}
    categories = {category for _, category in QUERIES}

    assert categories <= set(CATEGORY_MAP)
    assert categories.isdisjoint(legacy)
