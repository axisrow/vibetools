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
import time
from pathlib import Path
from typing import Callable

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
TOOLS_YML = ROOT / "data" / "tools.yml"
STARS_FILE = ROOT / "data" / "stars.json"
HISTORY_FILE = ROOT / "data" / "stars-history.json"  # dated-срезы для дельт 1d/7d
META_FILE = ROOT / "data" / "repos-meta.json"  # метаданные репо (forks/createdAt/topics/...)
HISTORY_DAYS = 8  # сколько последних срезов хранить (8 = сегодня + 7 дней назад)
# API-URL вынесен в common.GITHUB_REPO_API (общий для fetch_repo и
# check_repo_alive); оставляем alias для обратной совместимости со старыми
# импортами (tests/unit/test_fetch_repo_language.py: from update_stars import API).
# Общий github_slug и github_headers — единые реализации для всех скриптов.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    GITHUB_REPO_API,
    check_repo_alive,
    github_headers,
    github_slug,
    load_json_or_default,
)
API = GITHUB_REPO_API


def fetch_repo(
    slug: tuple[str, str],
    headers: dict,
    now: datetime.date | None = None,
    budget: dict | None = None,
) -> dict | None:
    """Полный объект репо из GitHub API → нормализованный meta-словарь.

    Возвращает {stars, forks, openIssues, pushedAt, createdAt, topics, archived,
    language, description, checkedAt} или None при ошибке/rate-limit (звёзды при
    этом сохраняем из прежнего кэша вызывающей стороной, чтобы не терять данные).

    language — primary language репо (поле /repos/{owner}/{repo}.language,
    одна строка, напр. "TypeScript"); берётся из уже выполняемого запроса,
    0 дополнительных обращений к API. None, если GitHub не определил язык.

    description — описание репо из того же запроса; нужно авто-категоризации
    trendshift-репо (scripts/categorize_repos.py) и как en-описание для сайта.

    checkedAt — ISO-дата проверки (``now`` или сегодня). Нужен budget-aware
    ротации trendshift-repos (refresh_trendshift_meta): без маркера «когда
    проверяли» невозможно отсортировать старейшие первыми. В tools.yml-цикле
    поле избыточно (звёзды фетчатся каждый день), но в trendshift-ротации —
    основа инкрементальности.

    budget — опциональный mutable dict; если GitHub прислал числовой заголовок
    ``x-ratelimit-remaining``, пишем ``budget["remaining"] = int(...)``. Ниже
    budget_floor ротация останавливается (см. refresh_trendshift_meta), оставляя
    запас Actions-лимиту 1000/час. None/отсутствующий/нечисловой заголовок
    (Enterprise/прокси) → budget не трогаем (безопасно: throttle падает на
    max_per_run). Читается и при ошибке (429 → remaining=0 узнаём сразу).
    """
    owner, repo = slug
    url = API.format(owner=owner, repo=repo)
    try:
        r = requests.get(url, headers=headers, timeout=20)
    except requests.RequestException as exc:
        print(f"  ! {owner}/{repo}: сетевая ошибка {exc}", file=sys.stderr)
        return None
    # x-ratelimit-remaining читаем ДО проверки статуса: на 429 он тоже приходит
    # (remaining=0) — это сигнал «лимит исчерпан» для budget-aware ротации.
    if budget is not None:
        raw = r.headers.get("x-ratelimit-remaining")
        if raw is not None:
            try:
                budget["remaining"] = int(raw)
            except (TypeError, ValueError):
                pass  # нечисловой (прокси/Enterprise) — не трогаем budget
    checked_at = (now or datetime.date.today()).isoformat()
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
            "description": j.get("description"),
            "checkedAt": checked_at,
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


def refresh_trendshift_meta(
    trendshift_repos: list[dict],
    meta: dict[str, dict],
    cache: dict[str, int],
    fetched_this_run: set[str],
    headers: dict,
    fetcher: Callable = fetch_repo,
    max_per_run: int = 100,
    sleep_between: float = 0.5,
    min_stars: int = 0,
    now: datetime.date | None = None,
    budget: dict | None = None,
    budget_floor: int = 100,
    alive_checker: Callable = check_repo_alive,
) -> tuple[int, int, list[str]]:
    """Инкрементально обновляет meta trendshift-repos и выкидывает мёртвые.

    Паттерн categorize_repos.enrich_repos_with_category: инкрементальность по
    ``checkedAt`` (старейшие/непроверенные первыми), ``max_per_run`` режет пачку,
    ``budget`` (x-ratelimit-remaining) останавливает ротацию у пола, оставляя
    запас Actions-лимиту 1000/час. ~791 репо / ~100 в день ≈ полная пере-валидация
    за 8 дней (хеджирует наивный «рефетчить всё», который вылетел бы за лимит).

    Мутирует ``trendshift_repos`` (удаляет pruned), ``meta`` и ``cache`` (добавляет
    свежие). Возвращает ``(updated, missing, pruned_urls)``.

    Алгоритм для каждого кандидата (до ``max_per_run`` и пока budget ≥ floor):

    - skip если ``checkedAt == today`` (идемпотентность повтора в тот же день).
    - ``repo_meta = fetcher(slug, headers, now=now, budget=budget)``; ``sleep``
      между запросами (не после последнего).
    - 404-pass: ``repo_meta is None`` → один ``alive_checker(slug, headers)``:
      ``dead`` → prune (удалить из trendshift_repos); ``unknown`` → ``missing``,
      meta не трогаем (сохраняем прежний кэш, остаётся кандидатом). +1 запрос
      только для None-случаев (редко: rate-limit или 404), не для живых.
    - alive-pass: ``repo_meta`` not None → archived/low-stars фильтр: ``archived``
      или ``stars < min_stars`` → prune; иначе ``meta[url] = repo_meta`` (с уже
      проставленным fetcher'ом ``checkedAt``), ``cache[url] = repo_meta["stars"]``.
    """
    today = (now or datetime.date.today()).isoformat()
    updated = 0
    missing = 0
    pruned_urls: list[str] = []

    # Кандидаты: url-строка, не дубль tools.yml (fetched_this_run), валидный slug.
    candidates: list[tuple[str, tuple[str, str]]] = []
    for rec in trendshift_repos:
        if not isinstance(rec, dict):
            continue
        url = rec.get("githubUrl")
        if not isinstance(url, str) or url in fetched_this_run:
            continue
        slug = github_slug(url)
        if not slug:
            continue
        candidates.append((url, slug))
    # Старейшие первыми: checkedAt ASC ("" / отсутствие = «никогда» = первый),
    # url как secondary key для детерминизма (стабильный git-diff ежедневных
    # прогонов; иначе порядок плавал бы от сортировки Python).
    candidates.sort(key=lambda us: (meta.get(us[0], {}).get("checkedAt") or "", us[0]))

    fetched = 0
    for url, slug in candidates:
        if meta.get(url, {}).get("checkedAt") == today:
            continue  # уже проверяли сегодня — идемпотентность
        if fetched >= max_per_run:
            continue  # лимит исчерпан — оставшиеся ждут след. прогона
        remaining = budget.get("remaining") if budget is not None else None
        if remaining is not None and remaining < budget_floor:
            break  # у потолка лимита — стоп, оставляем запас (tools.yml уже фетчнут)
        if fetched:
            time.sleep(sleep_between)  # уважаем rate-limit, но не перед первым
        repo_meta = fetcher(slug, headers, now=now, budget=budget)
        fetched += 1
        if repo_meta is None:
            # fetch_repo схлопнул ошибку в None (404/rate-limit/битый JSON).
            # Один alive-check различает «мёртвый» (404 → prune) и «не уверены»
            # (rate-limit → сохраняем прежний кэш, остаётся кандидатом).
            status, _ = alive_checker(slug, headers)
            if status == "dead":
                pruned_urls.append(url)
                _remove_trendshift_repo(trendshift_repos, url)
            else:
                missing += 1
                # unknown («не уверены»: rate-limit/timeout/5xx) — сохраняем
                # прежний кэш, НО двигаем checkedAt на today, иначе persistent-
                # unknown навсегда остался бы первым в сортировке ротации и
                # монополизировал max_per_run, замораживая meta для репо позади
                # него (тот же stale-meta баг, что рефактор должен устранить).
                # Дата ротации отделена от «свежести успеха»: мы знаем, что
                # проверяли, но не получили новый meta — прежняя запись остаётся.
                entry = meta.get(url)
                if isinstance(entry, dict):
                    entry["checkedAt"] = today
                else:
                    meta[url] = {"checkedAt": today}
            continue
        # Живой: archived/low-stars фильтр.
        if repo_meta.get("archived"):
            pruned_urls.append(url)
            _remove_trendshift_repo(trendshift_repos, url)
            continue
        stars = repo_meta.get("stars")
        if isinstance(stars, int) and stars < min_stars:
            pruned_urls.append(url)
            _remove_trendshift_repo(trendshift_repos, url)
            continue
        meta[url] = repo_meta
        cache[url] = stars if stars is not None else 0
        fetched_this_run.add(url)
        updated += 1

    return updated, missing, pruned_urls


def _remove_trendshift_repo(trendshift_repos: list[dict], url: str) -> None:
    """Удаляет запись с данным githubUrl из list (in-place).

    Удаление по url, а не по индексу: candidates собирались до мутаций, индексы
    могли бы съехать; url — стабильный ключ. Список маленький (≤791), O(n) на
    удаление приемлемо.
    """
    trendshift_repos[:] = [
        rec for rec in trendshift_repos
        if not (isinstance(rec, dict) and rec.get("githubUrl") == url)
    ]



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
    trendshift_repos_file: Path = ROOT / "data" / "trendshift-repos.json",
    now: datetime.date | None = None,
) -> int:
    headers = github_headers()
    today_date = now or datetime.date.today()

    with tools_yml.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    tools = data.get("tools", []) if isinstance(data, dict) else (data or [])

    # Прежние кэши — не теряем данные при разовых сбоях запроса.
    cache: dict[str, int] = load_json_or_default(stars_file, {}) or {}
    meta: dict[str, dict] = load_json_or_default(meta_file, {}) or {}

    updated = 0
    missing = 0
    fetched = 0  # успешных fetch (для определения тотального сбоя)
    # url, уже фетчнутые в ЭТОМ прогоне. Раньше trendshift-цикл skip'ил по
    # персистентному cache (stars.json прошлого прогона) — это замораживало meta
    # любого trendshift-repo после первого fetch'а (PR #20 планировал skip только
    # дублей tools.yml, но условие `url in cache` было слишком широким). skip по
    # fetched_this_run ровно то, что задумано: дубль url из tools.yml не фетчится
    # дважды, но однажды обогащённый trendshift-repo рефетчится каждый день.
    fetched_this_run: set[str] = set()
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
        fetched_this_run.add(tool["url"])

    # Свежесть/живость meta для trendshift-discovered репо (которых нет в
    # tools.yml), чтобы карточки на сайте показывали актуальные stars/createdAt и
    # не показывали мёртвые/заархивированные как «живые». Идёт ПОСЛЕ tools.yml-цикла
    # — кураторские репо гарантированно получают звёзды первыми, даже если упрёмся
    # в rate-limit. Budget-aware ротация (refresh_trendshift_meta): старейшие по
    # checkedAt первыми, max_per_run режет пачку, x-ratelimit-remaining держит
    # лимит 1000/час, archived/low-stars/404 выкидываются. ~791 репо / ~100 в день
    # ≈ полная пере-валидация за 8 дней (наивный «рефетчить всё» вылетел бы за лимит).
    trendshift_repos = load_json_or_default(trendshift_repos_file, []) or []
    budget: dict = {"remaining": None}
    ts_updated, ts_missing, ts_pruned_urls = refresh_trendshift_meta(
        trendshift_repos, meta, cache, fetched_this_run, headers,
        now=today_date, budget=budget,
    )

    stars_file.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    meta_file.write_text(
        json.dumps(meta, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    # refresh_trendshift_meta выкинул мёртвые/заархивированные/low-stars из
    # trendshift_repos (in-place) — фиксируем урезанный список на диске, чтобы
    # они не всплывали снова (liveness теперь в update_stars, отдельный
    # валидатор-скрипт не нужен). Пишем только при наличии pruned: иначе ежедневный
    # коммит шумел бы перезаписью идентичного файла (сортировка/indent стабильны,
    # но лишняя запись ни к чему).
    if ts_pruned_urls:
        trendshift_repos_file.parent.mkdir(parents=True, exist_ok=True)
        trendshift_repos_file.write_text(
            json.dumps(trendshift_repos, indent=2, ensure_ascii=False,
                       sort_keys=True) + "\n",
            encoding="utf-8",
        )

    # Dated-срез звёзд для дельт 1д/7д (репо дня/недели).
    # При тотальном сбое (0 успешных fetch) НЕ портим history устаревшим
    # срезом — см. update_history(skip=...).
    today = today_date.isoformat()
    total_failure = fetched == 0
    update_history(history_file, today, cache, skip=total_failure)

    print(f"\nОбновлено: {updated}, не удалось получить: {missing}")
    # Ротация trendshift-repos: updated (свежий meta), pruned (выкинуты), budget
    # — production-монитор steady-state (~488/день против наивных 1174 за лимитом).
    print(f"Trendshift rotation: updated={ts_updated}, missing={ts_missing}, "
          f"pruned={len(ts_pruned_urls)}, budget_remaining={budget.get('remaining')}")

    # Перегенерируем README — прямой вызов (быстрее и тестируемее subprocess).
    # out_dir пробрасывается, чтобы при вызове из тестов README писался в tmp.
    # Все инъектируемые пути пробрасываем дальше (контракт тест-изоляции):
    # иначе README/site регенерируются из реальных data/*.json, а сайт теряет
    # Featured (нужен history_file), [new] (нужен meta_file) и trendshift-бейджи.
    if regenerate:
        from generate_readme import main as gen_main
        gen_main(tools_yml, stars_file, out_dir, history_file, meta_file=meta_file)
        # Статический сайт (docs/index.html) — тоже из обновлённых данных.
        # trendshift_repos_file пробрасывается, чтобы сайт подмешивал обнаруженные
        # репо (stage 4); в тестах указывает в tmp (test-isolation).
        from generate_site import main as site_main
        site_kwargs = dict(
            tools_yml=tools_yml, stars_file=stars_file,
            out_file=(out_dir / "docs" / "index.html"),
            meta_file=meta_file, history_file=history_file,
            trendshift_repos_file=trendshift_repos_file,
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
