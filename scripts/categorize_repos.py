#!/usr/bin/env python3
"""Авто-категоризация trendshift-discovered репо через GitHub API.

Отдельный автоген-источник: category/name/description/language/topics живут в
data/trendshift-repos.json (autogen), НИКОГДА в tools.yml (золотое правило).
Куратор вручную переносит запись в tools.yml, когда доверяет авто-категории.

Инкрементально: репо с непустым ``category`` пропускаются (fetcher не зовётся).
При rate-limit/404 (fetch_repo→None) запись помечается category='needs-review'
с categoryReason='uncategorized' и categoryAt=<today> — это сохраняет попытку,
чтобы не переспрашивать каждый день (лимит всё равно исчерпан), но оставляет
репо видимым на сайте под честным «needs-review».

Запуск:
    GITHUB_TOKEN=ghp_... python scripts/categorize_repos.py
"""
from __future__ import annotations

import datetime
import json
import sys
import time
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent.parent
TREND_SHIFT_REPOS_FILE = ROOT / "data" / "trendshift-repos.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import github_headers, github_slug, load_json_or_default  # noqa: E402
from generate_readme import CATEGORY_MAP  # noqa: E402 — единая таксономия
from update_stars import fetch_repo  # noqa: E402 — rate-limit-tolerant fetcher

# Категория по умолчанию для всего, что не смэтчилось. 'needs-review' (НЕ 'other'):
# 'other' ∈ LEGACY_CATEGORIES и отсутствует в CATEGORIES — группа осталась бы без
# заголовка на сайте/README. 'needs-review' ∈ CATEGORIES, с trilingual-заголовками,
# семантично честно: «нашли на trendshift, но не смогли авто-классифицировать».
DEFAULT_CATEGORY = "needs-review"

# Topic (kebab-case, как реальные GitHub topics) → category. Свежая таблица — НЕ
# выводится из fetch_candidates.QUERIES: там search-query→category с in:-квалификаторами,
# derive = хрупко и теряет сигнал (query-фраза — не topic). Порядок dict намеренный
# (Python 3.7+ сохраняет insertion order): cli-agents/cloud/editor первыми — ядро
# vibe-coding. Первое совпадение топика выигрывает.
TOPIC_CATEGORY_MAP: dict[str, str] = {
    # cli-agents — ядро vibe-coding поверхности
    "cli": "cli-agents", "coding-agent": "cli-agents", "ai-coding": "cli-agents",
    "ai-agent": "cli-agents", "ai-coding-agent": "cli-agents",
    "coding-assistant": "cli-agents", "agentic": "cli-agents",
    "claude-code": "cli-agents", "agentic-coding": "cli-agents",
    "agents": "cli-agents", "agent": "cli-agents", "terminal": "cli-agents",
    "terminal-emulators": "cli-agents", "developer-tools": "cli-agents",
    # cloud-coding-agents
    "cloud-ide": "cloud-coding-agents", "cloud-coding": "cloud-coding-agents",
    "dev-environment": "cloud-coding-agents", "devcontainer": "cloud-coding-agents",
    # editor-integrations
    "vscode-extension": "editor-integrations", "vscode": "editor-integrations",
    "neovim": "editor-integrations", "jetbrains": "editor-integrations",
    "ide": "editor-integrations", "code-editor": "editor-integrations",
    "cursor": "editor-integrations",
    # code-review-testing
    "code-review": "code-review-testing", "testing": "code-review-testing",
    "linting": "code-review-testing", "linter": "code-review-testing",
    "static-analysis": "code-review-testing", "unit-testing": "code-review-testing",
    "testing-framework": "code-review-testing",
    # devops-cloud
    "devops": "devops-cloud", "kubernetes": "devops-cloud", "terraform": "devops-cloud",
    "infrastructure-as-code": "devops-cloud", "ci-cd": "devops-cloud",
    "devops-tools": "devops-cloud", "container": "devops-cloud",
    "docker": "devops-cloud", "self-hosted": "devops-cloud",
    # security-agents
    "security": "security-agents", "pentest": "security-agents",
    "application-security": "security-agents", "sast": "security-agents",
    "cybersecurity": "security-agents",
    # browser-automation
    "browser-automation": "browser-automation", "playwright": "browser-automation",
    "puppeteer": "browser-automation", "selenium": "browser-automation",
    "web-scraping": "browser-automation", "web-automation": "browser-automation",
    # design-frontend
    "design-to-code": "design-frontend", "frontend": "design-frontend",
    "ui-components": "design-frontend", "figma": "design-frontend",
    "design-system": "design-frontend", "flutter": "design-frontend",
    "ui": "design-frontend", "react": "design-frontend",
    # app-builders-low-code
    "low-code": "app-builders-low-code", "no-code": "app-builders-low-code",
    "app-builder": "app-builders-low-code",
    # game-dev
    "game-development": "game-dev", "gamedev": "game-dev", "unity": "game-dev",
    # context-memory
    "context-window": "context-memory", "codebase-indexing": "context-memory",
    "embeddings": "context-memory", "rag": "context-memory",
    "vector-database": "context-memory", "code-memory": "context-memory",
    # mcp
    "mcp-server": "mcp", "mcp-client": "mcp",
    "model-context-protocol": "mcp", "mcp": "mcp",
    # agent-skills-prompts
    "prompt-engineering": "agent-skills-prompts", "agent-skills": "agent-skills-prompts",
    "prompts": "agent-skills-prompts", "prompt": "agent-skills-prompts",
    "codex-skills": "agent-skills-prompts",
    # ai-assistants
    "ai-assistant": "ai-assistants", "personal-assistant": "ai-assistants",
    "multi-agent": "ai-assistants", "assistant": "ai-assistants",
    # observability-eval
    "observability": "observability-eval", "llm-evaluation": "observability-eval",
    "tracing": "observability-eval", "telemetry": "observability-eval",
    "evaluation": "observability-eval",
    # docs-research
    "documentation": "docs-research", "research": "docs-research",
    "knowledge-management": "docs-research", "docs": "docs-research",
    # learning-resources
    "tutorial": "learning-resources", "awesome-list": "learning-resources",
    "education": "learning-resources", "awesome": "learning-resources",
    "resources": "learning-resources", "free": "learning-resources",
    # ai-infra — ML/LLM общие темы (много trendshift-топов тут)
    "llm": "ai-infra", "llm-inference": "ai-infra", "llm-gateway": "ai-infra",
    "model-serving": "ai-infra", "inference": "ai-infra", "inference-server": "ai-infra",
    "ai": "ai-infra", "artificial-intelligence": "ai-infra",
    "deep-learning": "ai-infra", "machine-learning": "ai-infra",
    "generative-ai": "ai-infra", "transformer": "ai-infra",
    "chatgpt": "ai-infra", "openai": "ai-infra",
    # domain-agents намеренно разрежен — большинство доменных репо → needs-review
    # (требуют ручной кураторской классификации).
}

# Слово/фраза → category для substring-match по описанию (lowercased). Слабее
# topics (описание свободной формы), поэтому только уверенные сигнатуры.
DESC_KEYWORD_CATEGORY: dict[str, str] = {
    "coding agent": "cli-agents",
    "code review": "code-review-testing",
    "mcp server": "mcp",
    "model context protocol": "mcp",
    "browser automation": "browser-automation",
    "low-code": "app-builders-low-code",
    "low code": "app-builders-low-code",
    "llm gateway": "ai-infra",
    "llm inference": "ai-infra",
}


def categorize(meta: dict) -> tuple[str, str]:
    """Маппит fetch_repo()-результат в (category, categoryReason).

    Приоритет: topic > desc-keyword > 'needs-review'. Topics — сильнейший сигнал
    (автор-куратор на GitHub). Первое совпадение выигрывает; порядок dict в
    TOPIC_CATEGORY_MAP намеренный. Возвращает кортеж, чтобы вызывающая сторона
    могла записать categoryReason для аудита (grep uncategorized и т. п.).
    """
    if not isinstance(meta, dict):
        return DEFAULT_CATEGORY, "uncategorized"
    topics = [t.lower() for t in (meta.get("topics") or []) if isinstance(t, str)]
    for topic in topics:
        if topic in TOPIC_CATEGORY_MAP:
            return TOPIC_CATEGORY_MAP[topic], f"topic:{topic}"
    desc = (meta.get("description") or "")
    if isinstance(desc, str):
        desc_lower = desc.lower()
        for needle, cat in DESC_KEYWORD_CATEGORY.items():
            if needle in desc_lower:
                return cat, f"desc:{needle}"
    return DEFAULT_CATEGORY, "uncategorized"


def _coerce_category(category: str) -> str:
    """Нормализует категорию: неизвестную/легаси → DEFAULT_CATEGORY.

    Защита от битого кэша (вдруг categoryReason topic указывал на категорию,
    которую потом переименовали). CATEGORY_MAP — единая таксономия из
    generate_readme; 'other' в ней отсутствует (LEGACY_CATEGORIES).
    """
    if isinstance(category, str) and category in CATEGORY_MAP:
        return category
    return DEFAULT_CATEGORY


def enrich_repos_with_category(
    repos: list[dict],
    headers: dict | None = None,
    fetcher: Callable = fetch_repo,
    sleep_between: float = 0.5,
    max_per_run: int = 50,
    now=None,
) -> list[dict]:
    """Добавляет category/categoryReason/categoryAt/name/description/language/topics
    репо без category (инкрементально).

    Инкрементальность: репо с непустым ``category`` пропускается (fetcher не
    зовётся). fetcher→None (rate-limit/404) → помечаем category='needs-review',
    categoryReason='uncategorized', categoryAt=<today> (сохраняем попытку, не
    переспрашиваем каждый день). ``max_per_run`` ограничивает GitHub-запросы за
    один прогон — при сотнях uncategorized категоризация растягивается на
    несколько дней (по 50/день), оставаясь в квоте.
    """
    today = (now or datetime.date.today()).isoformat()
    fetched = 0
    for rec in repos:
        if not isinstance(rec, dict):
            continue
        existing = rec.get("category")
        if isinstance(existing, str) and existing.strip():
            # Уже категоризовано — только нормализуем (на случай переименования).
            rec["category"] = _coerce_category(existing)
            continue
        if fetched >= max_per_run:
            continue  # лимит исчерпан — оставшиеся ждут след. прогона
        url = rec.get("githubUrl")
        slug = github_slug(url) if isinstance(url, str) else None
        if not slug:
            rec["category"] = DEFAULT_CATEGORY
            rec["categoryReason"] = "uncategorized"
            rec["categoryAt"] = today
            continue
        meta = fetcher(slug, headers or {})
        if fetched:
            time.sleep(sleep_between)  # уважаем rate-limit, но не после последнего
        fetched += 1
        if meta is None:
            rec["category"] = DEFAULT_CATEGORY
            rec["categoryReason"] = "uncategorized"
            rec["categoryAt"] = today
            continue
        category, reason = categorize(meta)
        rec["category"] = category
        rec["categoryReason"] = reason
        rec["categoryAt"] = today
        # Сохраняем обогащающие поля (сайт использует их для карточек/поиска).
        if isinstance(meta.get("name"), str):
            rec["name"] = meta["name"]
        if meta.get("description") is not None:
            rec["description"] = meta.get("description")
        if meta.get("language") is not None:
            rec["language"] = meta.get("language")
        if isinstance(meta.get("topics"), list):
            rec["topics"] = meta["topics"]
    return repos


def main(
    trendshift_repos_file: Path = TREND_SHIFT_REPOS_FILE,
    max_per_run: int = 50,
) -> int:
    repos = load_json_or_default(trendshift_repos_file, []) or []
    if not repos:
        print("trendshift-repos.json пуст — нечего категоризовать.")
        return 0
    before = sum(1 for r in repos if isinstance(r, dict) and r.get("category"))
    enrich_repos_with_category(
        repos, github_headers(), max_per_run=max_per_run,
    )
    after = sum(1 for r in repos if isinstance(r, dict) and r.get("category"))
    trendshift_repos_file.parent.mkdir(parents=True, exist_ok=True)
    trendshift_repos_file.write_text(
        json.dumps(repos, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Categorized: {after}/{len(repos)} (+{after - before} this run, "
          f"max_per_run={max_per_run})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
