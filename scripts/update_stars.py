#!/usr/bin/env python3
"""
Собирает число звёзд для каждой утилиты из data/tools.yml через GitHub API,
кэширует в data/stars.json и перегенерирует README.md / README.ru.md.

Запускается GitHub Action (.github/workflows/update-stars.yml) раз в сутки.
data/tools.yml НЕ модифицируется — он остаётся чистым source-of-truth для
контрибьюторов; звёзды живут отдельно (data/stars.json + stars-history.json)
и подмешиваются генератором только для сортировки/отметок.

Также ведёт data/stars-history.json — dated-срезы звёзд (8 последних дней),
из которых генератор считает дельты за 1д/7д для выбора «репо дня/недели».

Использует GITHUB_TOKEN (если есть) для более высокого rate-лимита.

Локальный запуск:
    GITHUB_TOKEN=ghp_... python scripts/update_stars.py
"""
from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
TOOLS_YML = ROOT / "data" / "tools.yml"
STARS_FILE = ROOT / "data" / "stars.json"
HISTORY_FILE = ROOT / "data" / "stars-history.json"  # dated-срезы для дельт 1d/7d
META_FILE = ROOT / "data" / "repos-meta.json"  # метаданные репо (forks/createdAt/topics/...)
HISTORY_DAYS = 8  # сколько последних срезов хранить (8 = сегодня + 7 дней назад)
API = "https://api.github.com/repos/{owner}/{repo}"

# Общий github_slug и github_headers — единые реализации для всех скриптов.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import github_headers, github_slug, load_json_or_default  # noqa: E402


def fetch_repo(slug: tuple[str, str], headers: dict) -> dict | None:
    """Полный объект репо из GitHub API → нормализованный meta-словарь.

    Возвращает {stars, forks, openIssues, pushedAt, createdAt, topics, archived,
    language} или None при ошибке/rate-limit (звёзды при этом сохраняем из
    прежнего кэша вызывающей стороной, чтобы не терять данные).

    language — primary language репо (поле /repos/{owner}/{repo}.language,
    одна строка, напр. "TypeScript"); берётся из уже выполняемого запроса,
    0 дополнительных обращений к API. None, если GitHub не определил язык.
    """
    owner, repo = slug
    url = API.format(owner=owner, repo=repo)
    try:
        r = requests.get(url, headers=headers, timeout=20)
    except requests.RequestException as exc:
        print(f"  ! {owner}/{repo}: сетевая ошибка {exc}", file=sys.stderr)
        return None
    if r.status_code == 200:
        try:
            j = r.json()
        except requests.RequestException as exc:
            # HTTP-200 с не-JSON телом (страница прокси, обрезанный ответ).
            # JSONDecodeError — подкласс RequestException, ловим тем же блоком:
            # один битый ответ не должен валить весь дневной прогон.
            print(f"  ! {owner}/{repo}: битый JSON-ответ {exc}", file=sys.stderr)
            return None
        return {
            "stars": j.get("stargazers_count"),
            "forks": j.get("forks_count"),
            "openIssues": j.get("open_issues_count"),
            "pushedAt": j.get("pushed_at"),
            "createdAt": j.get("created_at"),
            "topics": j.get("topics", []) or [],
            "archived": bool(j.get("archived")),
            "language": j.get("language"),
        }
    if r.status_code in (403, 429):
        print(f"  ! {owner}/{repo}: rate limit ({r.status_code}), пропускаю", file=sys.stderr)
    elif r.status_code == 404:
        print(f"  ! {owner}/{repo}: 404 — репозиторий исчез?", file=sys.stderr)
    else:
        print(f"  ! {owner}/{repo}: HTTP {r.status_code}", file=sys.stderr)
    return None


def fetch_stars(slug: tuple[str, str], headers: dict) -> int | None:
    """Совместимость: только stargazers_count (используется в unit/e2e тестах)."""
    meta = fetch_repo(slug, headers)
    return meta.get("stars") if meta else None


def update_history(history_file: Path, today: str, cache: dict[str, int],
                   skip: bool = False) -> dict | None:
    """Дописывает dated-срез звёзд за today, обрезает до HISTORY_DAYS последних.

    Формат: {url: {"YYYY-MM-DD": stars, ...}}. Возвращает обновлённую историю.
    Сегодняшний срез перезаписывает прежний за ту же дату (идемпотентность
    при повторном прогоне в тот же день).

    skip=True — тотальный сбой API (ни одного успешного fetch): НЕ штампуем
    сегодняшний срез из устаревшего кэша, иначе через несколько дней окно
    состоит из копий одного среза, все дельты обнуляются, а первый успешный
    день приписывает многодневный прирост одной дате. Файл не трогаем,
    возвращаем None, чтобы вызывающая сторона знала, что записи не было.
    """
    if skip:
        return None
    history = load_json_or_default(history_file, {}) or {}

    for url, stars in cache.items():
        per_url = history.get(url, {})
        per_url[today] = stars
        # Оставляем только HISTORY_DAYS самых свежих дат.
        keep = sorted(per_url.keys(), reverse=True)[:HISTORY_DAYS]
        history[url] = {d: per_url[d] for d in keep}

    history_file.write_text(
        json.dumps(history, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return history


def main(
    tools_yml: Path = TOOLS_YML,
    stars_file: Path = STARS_FILE,
    regenerate: bool = True,
    out_dir: Path = ROOT,
    history_file: Path = HISTORY_FILE,
    meta_file: Path = META_FILE,
    trendshift_file: Path | None = None,
) -> int:
    headers = github_headers()

    with tools_yml.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    tools = data.get("tools", []) if isinstance(data, dict) else (data or [])

    # Прежние кэши — не теряем данные при разовых сбоях запроса.
    cache: dict[str, int] = load_json_or_default(stars_file, {}) or {}
    meta: dict[str, dict] = load_json_or_default(meta_file, {}) or {}

    updated = 0
    missing = 0
    fetched = 0  # успешных fetch (для определения тотального сбоя)
    for tool in tools:
        slug = github_slug(tool["url"])
        if not slug:
            continue
        repo_meta = fetch_repo(slug, headers)
        if repo_meta is None or repo_meta.get("stars") is None:
            missing += 1
            continue
        fetched += 1
        stars = repo_meta["stars"]
        if cache.get(tool["url"]) != stars:
            cache[tool["url"]] = stars
            updated += 1
            print(f"  ✓ {tool['name']}: {stars}")
        meta[tool["url"]] = repo_meta

    stars_file.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    meta_file.write_text(
        json.dumps(meta, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    # Dated-срез звёзд для дельт 1д/7д (репо дня/недели).
    # При тотальном сбое (0 успешных fetch) НЕ портим history устаревшим
    # срезом — см. update_history(skip=...).
    today = datetime.date.today().isoformat()
    total_failure = fetched == 0
    update_history(history_file, today, cache, skip=total_failure)

    print(f"\nОбновлено: {updated}, не удалось получить: {missing}")

    # Перегенерируем README — прямой вызов (быстрее и тестируемее subprocess).
    # out_dir пробрасывается, чтобы при вызове из тестов README писался в tmp.
    # Все инъектируемые пути пробрасываем дальше (контракт тест-изоляции):
    # иначе README/site регенерируются из реальных data/*.json, а сайт теряет
    # Featured (нужен history_file), [new] (нужен meta_file) и trendshift-бейджи.
    if regenerate:
        from generate_readme import main as gen_main
        gen_main(tools_yml, stars_file, out_dir, history_file, meta_file=meta_file)
        # Статический сайт (docs/index.html) — тоже из обновлённых данных.
        from generate_site import main as site_main
        site_kwargs = dict(
            tools_yml=tools_yml, stars_file=stars_file,
            out_file=(out_dir / "docs" / "index.html"),
            meta_file=meta_file, history_file=history_file,
        )
        # trendshift.json обновляется ОТДЕЛЬНЫМ шагом (update_trendshift.py)
        # после update_stars. В live-run мы хотим, чтобы регенерируемый здесь
        # сайт нёс trendshift-бейджи — поэтому читаем тот же canonical путь.
        # trendshift_file=None → site_main берёт свой дефолт (data/trendshift.json);
        # в тестах путь инъектируется в tmp, чтобы не читать реальный кэш.
        if trendshift_file is not None:
            site_kwargs["trendshift_file"] = trendshift_file
        site_main(**site_kwargs)

    # Тотальный сбой (например, истёкший GITHUB_TOKEN): данные сохранены в
    # кэше, но свежего среза нет — возвращаем nonzero, чтобы CI покраснел и
    # кто-то узнал, а не считал дельты по копии вчерашнего снимка.
    return 1 if total_failure else 0


if __name__ == "__main__":
    sys.exit(main())
