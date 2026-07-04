# Contributing to Awesome Vibe Coding Tools

First off, thanks for taking the time to contribute! 🎉

This is a **curated** list — quality beats quantity. Every entry is hand-picked, has a live repository, and is genuinely useful for **vibe coders** (developers building software with AI assistants).

> A list should be a curation, not a collection. — [the Awesome Manifesto](https://github.com/sindresorhus/awesome/blob/main/awesome.md)

## What belongs here

A tool qualifies if **all** of these are true:

- It helps developers **build software with AI assistance** (agents, prompts, context, evals, MCP, workflow).
- It has a **live, public repository** we can link to.
- It is **actively maintained** (commits/issues in roughly the last year) and not archived.
- It has a **meaningful amount of traction** (≈ 1k+ stars for general tools; the bar is lower for niche categories like context/memory, but the project must be real and usable).
- It is **not a duplicate** of an existing entry.

What does **not** belong: closed-source products without an open repo, vaporware, your side project with 3 stars and no README, AI-generated list-filler.

## How to add a tool

1. **Fork** this repo.
2. **Edit `data/tools.yml`** — add a single entry under the right category. Do **not** edit `README.md` / `README.ru.md` directly; they are generated.

   ```yaml
   - name: Your Tool
     url: https://github.com/owner/repo
     category: cli-agents        # see the list below
     description:
       en: "One neutral sentence (≤ 90 chars)"
       ru: "Одно нейтральное предложение (≤ 90 символов)"
   ```

   Valid categories:
   `cli-agents`, `cloud-coding-agents`, `editor-integrations`,
   `code-review-testing`, `devops-cloud`, `security-agents`,
   `browser-automation`, `design-frontend`, `app-builders-low-code`,
   `game-dev`, `context-memory`, `mcp`, `agent-skills-prompts`,
   `ai-assistants`, `observability-eval`, `docs-research`,
   `learning-resources`, `ai-infra`, `domain-agents`, `needs-review`.

### Choosing a category

- Use `cli-agents`, `cloud-coding-agents`, or `editor-integrations` for direct coding assistants, depending on where the user runs them.
- Use `mcp` only for generic MCP servers, clients, frameworks, gateways, or directories. A task-specific MCP server belongs with its task, such as browser automation, DevOps, security, or docs.
- Use `agent-skills-prompts` for Claude Skills, prompt packs, rules, hooks, slash commands, and system-prompt collections.
- Use `ai-assistants` for always-on personal assistants, agent platforms, multi-agent routers, and workflow-oriented agent harnesses.
- Use `app-builders-low-code` for low-code/no-code app builders and visual automation platforms.
- Use `ai-infra` for model serving, fine-tuning, LLM gateways, RAG platforms, vector stores, and generic AI infrastructure.
- Use `learning-resources` for courses, awesome lists, guides, tutorials, books, and benchmarks.
- Use `domain-agents` for finance, legal, marketing, science, video, and other domain-specific agents that are adjacent to coding but not general coding tools.
- Use `needs-review` only for existing entries that need maintainer review; new PRs should choose a real category or explain why the tool belongs in the list.

3. **Regenerate the READMEs** so your tool shows up:

   ```bash
   pip install pyyaml   # if needed
   python scripts/generate_readme.py
   ```

   Commit the regenerated `README.md` and `README.ru.md` along with your `tools.yml` change.

4. **Open a Pull Request** — one tool per PR. Fill in the PR template checklist.

### Writing the description

- **Neutral tone.** No marketing, no exclamation marks, no "the best/fastest/most powerful".
- **Factual, one sentence.** What does it do, in the fewest words.
- **Two languages**, `en` and `ru`, same meaning.
- ≤ 90 characters each.

❌ `The ultimate AI agent that will 10x your productivity!!!`
✅ `Terminal AI coding agent with multi-provider model support`

## Editing an existing entry

Found a stale description, a wrong URL, or a repo that moved? Open a PR editing the `tools.yml` entry — no need to add anything new.

## Reviewing

Maintainers will check: live URL, category fit, description tone, no duplicate, READMEs regenerated. We may ask you to tweak the wording or category before merging — this is normal and keeps the list tight.

## Updating star counts

You don't need to. A GitHub Action refreshes star badges and the `data/stars.json` cache daily. Star data lives **outside** `tools.yml` on purpose, so the source-of-truth file stays clean for human editing.

## Code of Conduct

By participating you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md). Be kind.
