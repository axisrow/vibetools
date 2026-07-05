#!/usr/bin/env python3
"""
Собирает кандидатов в список через GitHub Search API и выводит YAML-фрагмент.

Не пишет в data/tools.yml — только печатает готовые записи на stdout для
ручного кураторского отбора и слияния. Запуск:
    GITHUB_TOKEN=ghp_... python scripts/fetch_candidates.py

queries: список (запрос, категория). Категории задаются явно, без общего
ведра "other", чтобы кандидатский скрипт не возвращал мусорную свалку обратно
в кураторский список. Фильтр по звёздам (MIN_STARS) добавляется прямо в
поисковый запрос, чтобы фильтровать на сервере, а не на клиенте.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import requests
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import github_headers  # noqa: E402
from generate_readme import CATEGORY_MAP  # noqa: E402 — единая таксономия

SEARCH = "https://api.github.com/search/repositories"
MIN_STARS = 500  # добавляется в каждый запрос как stars:>=N (серверный фильтр)
PER_PAGE = 30    # sort=stars ⇒ топ релевантных; дальше — ниже кураторской планки

# (GitHub-поисковый запрос, категория в нашем списке).
# Категории валидируются против CATEGORY_MAP при старте (см. main), чтобы
# рассинхрон с generate_readme.CATEGORIES падал громко, а не молча пропускал.
QUERIES = [
    ("ai-coding-agent in:name,description,topics", "cli-agents"),
    ("coding agent in:topics", "cli-agents"),
    ("terminal coding agent in:name,description,topics", "cli-agents"),
    ("cloud coding agent in:name,description,topics", "cloud-coding-agents"),
    ("ai coding platform in:name,description,topics", "cloud-coding-agents"),
    ("code assistant in:name,description", "editor-integrations"),
    ("vscode ai coding assistant in:name,description,topics", "editor-integrations"),
    ("ai code review in:name,description,topics", "code-review-testing"),
    ("ai testing code review in:name,description,topics", "code-review-testing"),
    ("ai devops agent in:name,description,topics", "devops-cloud"),
    ("infrastructure ai agent in:name,description,topics", "devops-cloud"),
    ("security ai agent in:name,description,topics", "security-agents"),
    ("pentest ai agent in:name,description,topics", "security-agents"),
    ("browser automation agent in:name,description,topics", "browser-automation"),
    ("ai web scraping agent in:name,description,topics", "browser-automation"),
    ("design to code ai in:name,description,topics", "design-frontend"),
    ("frontend ai coding in:name,description,topics", "design-frontend"),
    ("low-code ai agent builder in:name,description,topics", "app-builders-low-code"),
    ("text to app ai in:name,description,topics", "app-builders-low-code"),
    ("game dev ai coding in:name,description,topics", "game-dev"),
    ("codebase memory ai agent in:name,description,topics", "context-memory"),
    ("codebase indexing ai in:name,description,topics", "context-memory"),
    ("model context protocol in:topics", "mcp"),
    ("mcp-server in:topics", "mcp"),
    ("mcp-client in:topics", "mcp"),
    ("agent skills in:name,description,topics", "agent-skills-prompts"),
    ("claude skills in:name,description,topics", "agent-skills-prompts"),
    ("prompt-engineering in:topics", "agent-skills-prompts"),
    ("personal ai assistant in:name,description,topics", "ai-assistants"),
    ("autonomous ai assistant in:name,description,topics", "ai-assistants"),
    ("multi-agent orchestration in:name,description,topics", "ai-assistants"),
    ("llm observability in:name,description", "observability-eval"),
    ("llm evaluation framework in:topics", "observability-eval"),
    ("ai documentation assistant in:name,description,topics", "docs-research"),
    ("ai research agent in:name,description,topics", "docs-research"),
    ("ai coding guide in:name,description,topics", "learning-resources"),
    ("vibe coding awesome in:name,description,topics", "learning-resources"),
    ("llm gateway in:name,description,topics", "ai-infra"),
    ("llm inference server in:name,description,topics", "ai-infra"),
    ("domain specific ai agent in:name,description,topics", "domain-agents"),
]


def search_once(query: str, per_page: int = PER_PAGE) -> list[dict]:
    # MIN_STARS задаётся сервером прямо в запросе — клиентский отсчёт не нужен.
    params = {"q": f"{query} stars:>={MIN_STARS}",
              "sort": "stars", "order": "desc", "per_page": per_page}
    r = requests.get(SEARCH, headers=github_headers(), params=params, timeout=30)
    if r.status_code == 200:
        return r.json().get("items", [])
    print(f"  ! [{r.status_code}] {query}: {r.text[:120]}", file=sys.stderr)
    return []


def main() -> int:
    # Защита от рассинхрона таксономии: каждая категория в QUERIES должна
    # быть известна generate_readme.CATEGORY_MAP.
    bad = [cat for _, cat in QUERIES if cat not in CATEGORY_MAP]
    assert not bad, f"QUERIES ссылается на неизвестные категории: {bad}"

    seen: set[str] = set()
    records: list[dict] = []
    for i, (query, category) in enumerate(QUERIES):
        if i:  # спим между запросами, но не после последнего
            time.sleep(2)
        print(f"# query: {query}  →  {category}", file=sys.stderr)
        for it in search_once(query):
            full = it["full_name"]
            if full in seen or it.get("archived"):
                continue
            seen.add(full)
            records.append({
                "name": it["name"],
                "url": it["html_url"],
                "category": category,
                "description": {
                    "en": (it.get("description") or "TODO: description").strip(),
                    "ru": "TODO: перевод",
                },
            })

    records.sort(key=lambda r: (r["category"], r["name"]))
    print(yaml.safe_dump(records, sort_keys=False, allow_unicode=True), end="")
    print(f"# всего кандидатов: {len(records)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
