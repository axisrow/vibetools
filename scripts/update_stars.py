#!/usr/bin/env python3
"""
Собирает число звёзд для каждой утилиты из data/tools.yml через GitHub API,
кэширует в data/stars.json и перегенерирует README.md / README.ru.md.

Запускается GitHub Action (.github/workflows/update-stars.yml) раз в сутки.
data/tools.yml НЕ модифицируется — он остаётся чистым source-of-truth для
контрибьюторов; звёзды живут отдельно (data/stars.json) и подмешиваются
генератором только для сортировки.

Использует GITHUB_TOKEN (если есть) для более высокого rate-лимита.

Локальный запуск:
    GITHUB_TOKEN=ghp_... python scripts/update_stars.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
TOOLS_YML = ROOT / "data" / "tools.yml"
STARS_FILE = ROOT / "data" / "stars.json"
API = "https://api.github.com/repos/{owner}/{repo}"

# Общий github_slug и github_headers — единые реализации для всех скриптов.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import github_headers, github_slug  # noqa: E402


def fetch_stars(slug: tuple[str, str], headers: dict) -> int | None:
    owner, repo = slug
    url = API.format(owner=owner, repo=repo)
    try:
        r = requests.get(url, headers=headers, timeout=20)
    except requests.RequestException as exc:
        print(f"  ! {owner}/{repo}: сетевая ошибка {exc}", file=sys.stderr)
        return None
    if r.status_code == 200:
        return r.json().get("stargazers_count")
    if r.status_code in (403, 429):
        print(f"  ! {owner}/{repo}: rate limit ({r.status_code}), пропускаю", file=sys.stderr)
    elif r.status_code == 404:
        print(f"  ! {owner}/{repo}: 404 — репозиторий исчез?", file=sys.stderr)
    else:
        print(f"  ! {owner}/{repo}: HTTP {r.status_code}", file=sys.stderr)
    return None


def main(
    tools_yml: Path = TOOLS_YML,
    stars_file: Path = STARS_FILE,
    regenerate: bool = True,
    out_dir: Path = ROOT,
) -> int:
    headers = github_headers()

    with tools_yml.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    tools = data.get("tools", []) if isinstance(data, dict) else (data or [])

    # Сохраняем прежний кэш, чтобы не терять данные при разовых сбоях запроса.
    cache: dict[str, int] = {}
    if stars_file.exists():
        try:
            cache = json.loads(stars_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            cache = {}

    updated = 0
    missing = 0
    for tool in tools:
        slug = github_slug(tool["url"])
        if not slug:
            continue
        stars = fetch_stars(slug, headers)
        if stars is None:
            missing += 1
            continue
        if cache.get(tool["url"]) != stars:
            cache[tool["url"]] = stars
            updated += 1
            print(f"  ✓ {tool['name']}: {stars}")

    stars_file.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"\nОбновлено: {updated}, не удалось получить: {missing}")

    # Перегенерируем README — прямой вызов (быстрее и тестируемее subprocess).
    # out_dir пробрасывается, чтобы при вызове из тестов README писался в tmp.
    if regenerate:
        from generate_readme import main as gen_main
        gen_main(tools_yml, stars_file, out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
