# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A curated awesome-list of **383 vibe-coding tools** (AI-assisted development: Claude Code, Cursor, MCP, agents). Two outputs share one data source:
- **README.md / README.ru.md** — canonical awesome-list (passes `awesome-lint`), for GitHub/awesome-index.
- **docs/index.html** — a user-friendly searchable static site (GitHub Pages at `https://axisrow.github.io/vibetools/`): full-text search, category/`new` filters, sort, i18n EN/RU/ZH, star-history-style metric cards.

The golden rule: **`data/tools.yml` contains only human-curated data** — `name`, `url`, `category`, `description{en,ru}`. Everything else (stars, forks, `createdAt`, rank, growth, `new` flag, repo-of-day/week) is **generated automatically** from the GitHub API and cached in `data/*.json`. Never add manual status flags to `tools.yml` — there is intentionally no `verified` field (it doesn't exist on star-history.com, so it doesn't exist here); `new` and `rank` are computed, not stored.

## Architecture: one data source, three generators

```
data/tools.yml  (source of truth — human-edited only)
       │
       ├── scripts/generate_readme.py  →  README.md, README.ru.md
       ├── scripts/generate_site.py    →  docs/index.html  (template: scripts/site_template.html)
       └── scripts/update_stars.py     →  data/stars.json, data/stars-history.json, data/repos-meta.json
              └── then calls generate_readme.main + generate_site.main to refresh outputs
```

**`scripts/update_stars.py` is the orchestrator** (runs daily via GitHub Action). Its `main()`:
1. For each repo, `fetch_repo()` → GitHub REST API `/repos/{owner}/{repo}` → full meta (stars, forks, `createdAt`, topics, archived). Writes `data/repos-meta.json`.
2. `update_history()` appends today's star counts as a dated snapshot to `data/stars-history.json` (keeps `HISTORY_DAYS=8`).
3. Regenerates README + site by calling `generate_readme.main(...)` and `generate_site.main(...)` directly (not subprocess — so all paths are injectable for tests).

**`scripts/common.py`** holds shared helpers imported by all three generators: `github_slug(url)`, `github_headers()` (GITHUB_TOKEN), `load_json_or_default(path, default)` (tolerant JSON cache reader). All `load_*` functions go through it — don't re-implement the try/except.

**`scripts/generate_readme.py`** owns the **taxonomy**: `CATEGORIES` (list of `(key, {title_en, title_ru, title_zh})`) is the single source of category order/names for README, site, and `fetch_candidates`. `CATEGORY_MAP` is exported for validation. `is_new(tool)` reads `created_at` (from repos-meta, enriched in `main`); `pick_featured()` selects repo-of-day/week by max positive star delta over `FEATURED_WINDOWS = {"day": 1, "week": 7}`.

**`scripts/generate_site.py`** `build_data_json()` merges tools.yml + stars + repos-meta + history into one dict inlined into the HTML as `window.__DATA__` (no fetch/CORS — works on Pages as-is). Computes `rank` (by stars), `starsPerWeek` (7-day delta from history), `isNew` (createdAt ≤ NEW_DAYS).

**`scripts/fetch_candidates.py`** — one-off CLI that searches GitHub for new repos to add; prints a YAML fragment to stdout (does NOT write tools.yml). Validates its category strings against `CATEGORY_MAP` at startup.

## Critical contracts (easy to break silently)

- **awesome-lint format.** `render_line()` MUST emit `- [Name](url) <badge> - Capitalized description.` — dash separator, capitalized first letter, trailing period, no inline marks/emoji. `awesome-lint` runs in CI (`.github/workflows/awesome-lint.yml`) and fails the build otherwise. The Awesome badge must sit **inside the H1 line** (not a separate paragraph) — `remark-lint:awesome-badge` requires it in the heading node.
- **History ↔ featured window contract.** `HISTORY_DAYS` (in update_stars) must be ≥ `max(FEATURED_WINDOWS.values()) + 1` (= 8) so the 7-day delta always has a snapshot. Repo-of-day/week needs **≥2 distinct dates** in stars-history.json — it's empty until the second daily run (not a bug).
- **Test isolation (mock-leak trap).** Every `update_stars.main(...)` call in tests MUST pass `meta_file=`, `history_file=`, `stars_file=`, and `out_dir=` pointing under `tmp_path` — otherwise `update_stars` writes to its module-level defaults (`ROOT/data/*.json`) and pollutes the real source tree with fixture URLs (`github.com/a/hi`, `a/lo`, `b/editor`). The `tmp_repo` fixtures (`tests/integration/conftest.py`, `tests/e2e/conftest.py`) provide all four keys including `meta_file` — use them. `tests/smoke/test_no_mock_leak.py` is a tripwire that fails CI if any of `data/{repos-meta,stars,stars-history}.json` contains those mock markers; it never `skip`s on a missing file (missing = no leak = pass). If you add a new `update_stars.main`/`generate_site.main` call, pass the tmp paths — the trap will catch you otherwise.

## Commands

```bash
# Regenerate outputs from current data (no network)
python scripts/generate_readme.py        # → README.md, README.ru.md
python scripts/generate_site.py          # → docs/index.html

# Refresh stars + meta from GitHub API (writes data/*.json, regenerates outputs)
GITHUB_TOKEN=ghp_... python scripts/update_stars.py

# Tests — 4 levels in tests/{unit,integration,smoke,e2e}
python -m pytest -m "not live"                       # everything except real-GitHub-API tests (default)
python -m pytest tests/unit/test_render_line.py -v   # single file
python -m pytest -m live                              # live tests (hit real GitHub; nightly CI only)

# Lint the README against awesome-list rules
npx awesome-lint

# Dev deps
pip install -r requirements-dev.txt
```

## CI (`.github/workflows/`)
- **`update-stars.yml`** — daily cron 03:17 UTC (also `workflow_dispatch`); runs `update_stars.py` with `GITHUB_TOKEN`, bot-commits `data/*.json` + README + site (`[skip ci]`). Pages auto-redeploys from `main/docs`.
- **`tests.yml`** — PR/push: unit + integration + smoke + e2e-mock (live tests excluded).
- **`tests-live.yml`** — nightly: `pytest -m live` against the real GitHub API.
- **`awesome-lint.yml`** — PR/push: enforces the awesome-list format above.

## Site (`docs/index.html`)
Generated from `scripts/site_template.html` (vanilla JS/CSS, no framework/build). The template has a `/*__DATA__*/{}` marker that `generate_site.py` replaces with the JSON payload. UI strings live in an `I18N` object (en/ru/zh); category names come from `__DATA__.categories[*].title_{lang}` (not duplicated in I18N). Language choice persists in `localStorage`.
