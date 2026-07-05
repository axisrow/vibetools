"""Integration: generate_site.main() — сборка docs/index.html + docs/data.json.

Проверяет: создаются оба файла (HTML без inline-данных, payload в data.json),
все tools на месте, search-поле lowercase (CJK-aware), stars fallback,
i18n title_zh.
"""
import datetime
import json
from pathlib import Path

import pytest

from generate_site import build_data_json, main as site_main


def _extract_payload(index_html_path: Path) -> dict:
    """Достаёт payload из docs/data.json (sibling index.html).

    Раньше payload вшивался inline в index.html как window.__DATA__; теперь
    данные вынесены в отдельный data.json и грузятся через fetch. Поэтому
    payload читаем из файла, а не из HTML.
    """
    data_path = index_html_path.parent / "data.json"
    assert data_path.exists(), f"data.json не создан рядом с {index_html_path}"
    return json.loads(data_path.read_text(encoding="utf-8"))


def test_site_uses_bootstrap_cdn_with_local_fallback(tmp_repo):
    """Сайт грузит Bootstrap 5.3.8 с CDN и имеет локальный fallback."""
    out = tmp_repo["root"] / "docs" / "index.html"
    site_main(tools_yml=tmp_repo["tools_yml"], stars_file=tmp_repo["stars_file"],
              out_file=out)
    html = out.read_text(encoding="utf-8")
    assert "cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" in html
    assert "cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" in html
    assert "vendor/bootstrap/5.3.8/css/bootstrap.min.css" in html
    assert "vendor/bootstrap/5.3.8/js/bootstrap.bundle.min.js" in html
    assert "sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" in html
    assert "sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" in html
    assert "__loadBootstrapCssFallback" in html
    assert 'id="bootstrap-js"' in html
    assert "setTimeout(() =>" in html
    assert "--bs-body-font-family" in html
    assert "window.bootstrap" in html


def test_bootstrap_fallback_assets_are_committed():
    """Локальный fallback Bootstrap лежит в docs/vendor и не является заглушкой."""
    root = Path(__file__).resolve().parents[2]
    css = root / "docs" / "vendor" / "bootstrap" / "5.3.8" / "css" / "bootstrap.min.css"
    js = root / "docs" / "vendor" / "bootstrap" / "5.3.8" / "js" / "bootstrap.bundle.min.js"
    assert css.is_file()
    assert js.is_file()
    assert "Bootstrap  v5.3.8" in css.read_text(encoding="utf-8")[:160]
    assert "Bootstrap v5.3.8" in js.read_text(encoding="utf-8")[:160]


def test_site_has_directory_redesign_hooks(tmp_repo):
    """Шаблон остаётся каталогом, а не набором дефолтных Bootstrap controls."""
    out = tmp_repo["root"] / "docs" / "index.html"
    site_main(tools_yml=tmp_repo["tools_yml"], stars_file=tmp_repo["stars_file"],
              out_file=out)
    html = out.read_text(encoding="utf-8")
    assert "masthead" in html
    assert "meta-row" in html
    assert "command-bar" in html
    assert "filter-rail" in html
    assert "filter-toggle" in html
    assert "featured-strip" in html
    assert "featured-list" in html
    assert "featured-achievements" in html
    assert "featured-achievement-day" in html
    assert "featured-achievement-week" in html
    assert "trendshift-achievements" in html
    assert "trendshift-achievement-day" in html
    assert "trendshift-achievement-week" in html
    assert "trendshiftDay" in html
    assert "trendshiftWeek" in html
    assert "featuredDelta" in html
    assert "bi-sprite" in html
    assert "bi-star-fill" in html
    assert "bi-trophy-fill" in html
    assert "bi-award-fill" in html
    assert "bi-calendar-week-fill" in html
    assert "bi-git" in html
    assert "featured-overline" not in html
    assert "featuredBadges" not in html
    assert "state-badge-featured" not in html
    assert "Day pick" not in html
    assert "Week pick" not in html
    assert "trendshift-badge-img" not in html
    assert "category-select" in html
    # Языковой фильтр (#11) должен пережить редизайн — regression guard.
    assert 'id="f-language"' in html
    assert 'id="f-trendshift"' in html
    assert 'id="f-year"' in html
    assert "DATA.languages" in html
    assert "activeTrendshift" in html
    assert "activeYear" in html
    assert "renderYears" in html
    assert "toolHasTrendshift" in html
    assert "toolYear" in html
    assert 'parts.push(t("new"))' in html
    assert "All years" in html
    assert "Все годы" in html
    assert 'id="f-achievement"' not in html
    assert "All achievements" not in html
    assert "category-tab" in html
    assert "tool-record" in html
    assert "tool-heading" in html
    assert "font-size: 1.22rem" in html
    assert "font-weight: 780" in html
    assert "font-size: .92rem" in html
    assert "metric-panel" in html
    assert "mobile-metrics" in html
    assert "submeta-separator" in html
    assert "state-badge" in html
    assert 'class="btn filter-toggle" type="button" id="f-new"' in html
    assert 'class="btn filter-toggle" type="button" id="f-trendshift"' in html
    assert 'aria-pressed="false"' in html
    assert "new-toggle" not in html
    assert 'id="language-menu"' in html
    assert 'data-bs-toggle="dropdown"' in html
    assert "language-option" in html
    assert "English" in html
    assert "Русский" in html
    assert "中文" in html
    assert "btn-group lang" not in html
    assert "brand-kicker" not in html
    assert "status-strip" not in html
    assert 'data-i18n-html="footer"' in html
    assert "el.innerHTML = I18N[lang][k]" in html
    assert "tool-name text-decoration-none fw-" not in html
    assert "btn-check" not in html
    assert "form-switch" not in html


def test_site_creates_index(tmp_tools_yml, sample_tool_github, tmp_path):
    tools_yml = tmp_tools_yml([sample_tool_github])
    out = tmp_path / "docs" / "index.html"
    site_main(tools_yml=tools_yml, stars_file=tmp_path / "stars.json", out_file=out)
    assert out.exists()
    html = out.read_text(encoding="utf-8")
    assert "Awesome Vibe Coding Tools" in html
    payload = _extract_payload(out)
    assert len(payload["tools"]) == 1


def test_site_contains_all_tools(tmp_repo):
    """Сайт включает все tools из tools.yml (через tmp_repo fixture)."""
    out = tmp_repo["root"] / "docs" / "index.html"
    site_main(tools_yml=tmp_repo["tools_yml"], stars_file=tmp_repo["stars_file"],
              out_file=out)
    payload = _extract_payload(out)
    assert len(payload["tools"]) == len(tmp_repo["tools"])
    names = {t["name"] for t in payload["tools"]}
    assert {"HiStars", "LoStars", "Editor", "NoGithub"} <= names


def test_site_search_field_is_lowercase(tmp_repo):
    """search-поле = lowercase name+en+ru — для мгновенного includes() в JS."""
    out = tmp_repo["root"] / "docs" / "index.html"
    site_main(tools_yml=tmp_repo["tools_yml"], stars_file=tmp_repo["stars_file"],
              out_file=out)
    payload = _extract_payload(out)
    for t in payload["tools"]:
        assert t["search"] == t["search"].lower()
        # name присутствует в haystack
        assert t["name"].lower() in t["search"]


def test_site_stars_fallback_when_no_stars(tmp_repo):
    """Без stars.json → stars=null, starsUrl (shields) есть для github репо."""
    tmp_repo["stars_file"].unlink()  # нет файла звёзд
    out = tmp_repo["root"] / "docs" / "index.html"
    site_main(tools_yml=tmp_repo["tools_yml"], stars_file=tmp_repo["stars_file"],
              out_file=out)
    payload = _extract_payload(out)
    github_tools = [t for t in payload["tools"] if "github.com" in t["url"]]
    assert github_tools
    for t in github_tools:
        assert t["stars"] is None  # fallback
        assert t["starsUrl"].startswith("https://img.shields.io/github/stars/")


def test_site_stars_from_cache(tmp_repo):
    """Со stars.json → числовые звёзды подставляются."""
    out = tmp_repo["root"] / "docs" / "index.html"
    site_main(tools_yml=tmp_repo["tools_yml"], stars_file=tmp_repo["stars_file"],
              out_file=out)
    payload = _extract_payload(out)
    hi = next(t for t in payload["tools"] if t["name"] == "HiStars")
    assert hi["stars"] == 1000  # из tmp_repo fixture stars.json


def test_site_categories_have_title_zh(tmp_repo):
    """Категории в payload несут title_zh для i18n переключателя."""
    out = tmp_repo["root"] / "docs" / "index.html"
    site_main(tools_yml=tmp_repo["tools_yml"], stars_file=tmp_repo["stars_file"],
              out_file=out)
    payload = _extract_payload(out)
    assert payload["categories"]
    for c in payload["categories"]:
        assert "title_zh" in c and c["title_zh"]


def test_site_cjk_search(tmp_tools_yml, tmp_path):
    """Репо с китайским описанием — CJK-текст попадает в search-поле (поиск работает)."""
    tool = {"name": "ai-guide", "url": "https://github.com/liyupi/ai-guide",
            "category": "learning-resources",
            "description": {"en": "程序员鱼皮的 AI 资源大全", "ru": "AI ресурсы"}}
    tools_yml = tmp_tools_yml([tool])
    out = tmp_path / "docs" / "index.html"
    site_main(tools_yml=tools_yml, stars_file=tmp_path / "stars.json", out_file=out)
    payload = _extract_payload(out)
    t = payload["tools"][0]
    # Китайский иероглиф (U+7A0B 程) должен быть в lowercase haystack
    assert "程" in t["search"] or "ai-guide" in t["search"]


def test_build_data_json_structure(tmp_repo):
    """build_data_json возвращает ожидаемую структуру (без verified/added)."""
    data = build_data_json(tmp_repo["tools_yml"], tmp_repo["stars_file"])
    assert set(data.keys()) >= {"generatedAt", "categories", "featured", "tools"}
    tool = data["tools"][0]
    # verified/added убраны; добавлены forks/createdAt/topics/rank/starsPerWeek.
    assert set(tool.keys()) >= {
        "name", "url", "category", "isNew",
        "stars", "starsPerWeek", "starsUrl", "forks", "openIssues",
        "createdAt", "archived", "topics", "rank", "desc", "search"}
    assert "verified" not in tool and "added" not in tool


def test_build_data_json_featured_from_history(tmp_repo):
    """Сайт получает тот же featured-сигнал, что README: day/week из истории звёзд."""
    today = datetime.date.today()
    history = {
        "https://github.com/a/hi": {
            (today - datetime.timedelta(days=1)).isoformat(): 900,
            (today - datetime.timedelta(days=7)).isoformat(): 700,
        },
        "https://github.com/a/lo": {
            (today - datetime.timedelta(days=1)).isoformat(): 9,
            (today - datetime.timedelta(days=7)).isoformat(): 5,
        },
    }
    tmp_repo["history_file"].write_text(json.dumps(history), encoding="utf-8")

    data = build_data_json(
        tmp_repo["tools_yml"],
        tmp_repo["stars_file"],
        history_file=tmp_repo["history_file"],
    )

    assert data["featured"] == [
        {"kind": "day", "url": "https://github.com/a/hi",
         "delta": 100, "days": 1, "windowComplete": True},
        {"kind": "week", "url": "https://github.com/a/hi",
         "delta": 300, "days": 7, "windowComplete": True},
    ]


def test_build_data_json_surfaces_trendshift_cache(tmp_repo):
    """Trendshift cache enriches matching tools without changing tools.yml."""
    tmp_repo["trendshift_file"].write_text(json.dumps({
        "https://github.com/a/hi": {
            "trendshiftId": "50668",
            "pageUrl": "https://trendshift.io/repositories/50668",
            "badges": [
                {
                    "kind": "day",
                    "badgeUrl": "https://trendshift.io/api/badge/trendshift/repositories/50668/daily",
                },
                {
                    "kind": "week",
                    "badgeUrl": "https://trendshift.io/api/badge/trendshift/repositories/50668/weekly",
                },
            ],
            "updatedAt": "2026-07-04",
        }
    }), encoding="utf-8")

    data = build_data_json(
        tmp_repo["tools_yml"],
        tmp_repo["stars_file"],
        trendshift_file=tmp_repo["trendshift_file"],
    )

    hi = next(t for t in data["tools"] if t["name"] == "HiStars")
    lo = next(t for t in data["tools"] if t["name"] == "LoStars")
    assert hi["trendshift"] == {
        "badges": [
            {
                "kind": "day",
                "badgeUrl": "https://trendshift.io/api/badge/trendshift/repositories/50668/daily",
            },
            {
                "kind": "week",
                "badgeUrl": "https://trendshift.io/api/badge/trendshift/repositories/50668/weekly",
            },
        ],
        "trendshiftId": "50668",
        "pageUrl": "https://trendshift.io/repositories/50668",
        "updatedAt": "2026-07-04",
    }
    assert "trendshift" not in lo


def test_build_data_json_no_verified_anywhere(tmp_repo):
    """verified полностью отсутствует в данных сайта (на star-history его нет)."""
    data = build_data_json(tmp_repo["tools_yml"], tmp_repo["stars_file"])
    blob = json.dumps(data, ensure_ascii=False)
    assert "verified" not in blob


def test_build_data_json_rank_by_stars(tmp_repo):
    """rank — ранг по звёздам: топ базы (#1) = максимум звёзд."""
    data = build_data_json(tmp_repo["tools_yml"], tmp_repo["stars_file"])
    with_stars = [t for t in data["tools"] if t["stars"] is not None]
    ranked = sorted(with_stars, key=lambda t: t["rank"])
    assert ranked[0]["rank"] == 1
    # HiStars (1000★) должен быть выше LoStars (10★).
    names_by_rank = [t["name"] for t in ranked]
    assert names_by_rank.index("HiStars") < names_by_rank.index("LoStars")


def test_build_data_json_meta_enriches(tmp_repo, tmp_path):
    """Если есть repos-meta.json — forks/createdAt/topics подставляются."""
    meta_file = tmp_path / "repos-meta.json"
    url = "https://github.com/a/hi"
    import json as _json
    # createdAt считаем от сегодня (в пределах NEW_DAYS=14), а не хардкодим
    # дату — иначе тест краснеет ровно через 15 дней после захардкоженной даты.
    recent = (datetime.date.today() - datetime.timedelta(days=3)).isoformat()
    created_iso = f"{recent}T00:00:00Z"
    meta_file.write_text(_json.dumps({url: {
        "stars": 1000, "forks": 42, "openIssues": 3,
        "pushedAt": "2026-07-01T00:00:00Z", "createdAt": created_iso,
        "topics": ["ai", "agent"], "archived": False}}), encoding="utf-8")
    data = build_data_json(tmp_repo["tools_yml"], tmp_repo["stars_file"], meta_file=meta_file)
    hi = next(t for t in data["tools"] if t["name"] == "HiStars")
    assert hi["forks"] == 42
    assert hi["createdAt"] == created_iso
    assert "agent" in hi["topics"]
    assert hi["isNew"] is True  # 3 дня назад — в пределах NEW_DAYS


def test_build_data_json_surfaces_language(tmp_repo, tmp_path):
    """language из repos-meta прокидывается в tool + search-haystack."""
    meta_file = tmp_path / "repos-meta.json"
    import json as _json
    meta_file.write_text(_json.dumps({
        "https://github.com/a/hi": {"stars": 1000, "language": "Rust"},
        "https://github.com/a/lo": {"stars": 10, "language": "Python"},
    }), encoding="utf-8")
    data = build_data_json(tmp_repo["tools_yml"], tmp_repo["stars_file"], meta_file=meta_file)
    hi = next(t for t in data["tools"] if t["name"] == "HiStars")
    lo = next(t for t in data["tools"] if t["name"] == "LoStars")
    assert hi["language"] == "Rust"
    assert lo["language"] == "Python"
    # Язык попадает в lowercase haystack → находится полнотекстовым поиском.
    assert "rust" in hi["search"]
    assert "python" in lo["search"]


def test_build_data_json_languages_catalog(tmp_repo, tmp_path):
    """Каталог languages: unique + sorted, без None; есть на верхнем уровне."""
    meta_file = tmp_path / "repos-meta.json"
    import json as _json
    meta_file.write_text(_json.dumps({
        "https://github.com/a/hi": {"stars": 1000, "language": "Rust"},
        "https://github.com/a/lo": {"stars": 10, "language": "Python"},
        "https://github.com/b/editor": {"stars": 50, "language": "Rust"},
        # NoGithub (example.com) — нет в meta → language=None, в каталог не попадает.
    }), encoding="utf-8")
    data = build_data_json(tmp_repo["tools_yml"], tmp_repo["stars_file"], meta_file=meta_file)
    assert "languages" in data
    # unique (Rust дважды, но один раз), sorted, None от NoGithub отброшен.
    assert data["languages"] == ["Python", "Rust"]


def test_build_data_json_language_none_when_meta_missing(tmp_repo):
    """Без repos-meta.json → language=None у каждого tool, каталог пустой."""
    data = build_data_json(tmp_repo["tools_yml"], tmp_repo["stars_file"])
    for tool in data["tools"]:
        assert tool["language"] is None
    assert data["languages"] == []


def test_main_writes_payload_to_data_json_not_inline(tmp_tools_yml, tmp_path):
    """Данные вынесены из index.html в отдельный data.json.

    Раньше payload вшивался inline как window.__DATA__ (с экранированием «</»
    против stored-XSS через описания из GitHub API). Теперь данные лежат в
    docs/data.json (Content-Type: application/json — XSS-вектор отпадает сам
    собой), HTML их не содержит, а описание попадает в data.json дословно
    (без «<\\/»-экранирования — это был артефакт инлайн-режима).
    """
    from generate_site import main as site_main
    tool = {"name": "evil", "url": "https://github.com/x/y",
            "category": "cli-agents",
            "description": {"en": "clean", "ru": "</script><img onerror=alert(1)>"}}
    tools_yml = tmp_tools_yml([tool])
    out = tmp_path / "docs" / "index.html"
    site_main(tools_yml=tools_yml, stars_file=tmp_path / "stars.json", out_file=out)
    html = out.read_text(encoding="utf-8")
    # HTML больше не несёт inline-payload: ни placeholder-маркера, ни
    # присваивания объекта (window.__DATA__ = {...}). Присваивание после fetch
    # (window.__DATA__ = data;) легитимно — это не inline-данные.
    assert "/*__DATA__*/" not in html
    assert "window.__DATA__ = {" not in html
    # Payload живёт в data.json — целиком, валидный JSON, описание дословно
    # (без «<\\/»-экранирования, которое было нужно только внутри <script>).
    data_path = out.parent / "data.json"
    assert data_path.exists()
    payload = json.loads(data_path.read_text(encoding="utf-8"))
    assert payload["tools"][0]["desc"]["ru"] == "</script><img onerror=alert(1)>"


def test_render_index_html_rejects_inline_marker(tmp_path):
    """Регрессионный guard: если в шаблон вернётся inline-маркер данных
    (window.__DATA__ = /*__DATA__*/{}), render_index_html явно raise'ит —
    иначе деплой ляжет пустым сайтом при зелёном CI (данных-то nobody не
    подставляет в маркер больше)."""
    from generate_site import render_index_html
    bad_template = tmp_path / "bad.html"
    bad_template.write_text(
        '<script>window.__DATA__ = /*__DATA__*/{};</script>', encoding="utf-8")
    with pytest.raises(ValueError, match="inline-маркер"):
        render_index_html(template=bad_template)


def test_render_index_html_returns_template_as_is(tmp_path):
    """Шаблон без маркера отдаётся как есть — данные не инлайнятся."""
    from generate_site import render_index_html
    ok_template = tmp_path / "ok.html"
    body = "<html><body>каталог без данных</body></html>"
    ok_template.write_text(body, encoding="utf-8")
    assert render_index_html(template=ok_template) == body


def test_site_template_validates_lang_from_localstorage():
    """#8: lang из localStorage валидируется по ключам I18N — иначе TypeError.

    Регрессионный guard на текст шаблона: невалидное значение («de», «ru-RU»)
    из общего для GitHub Pages localStorage не должно ронять applyI18n.
    """
    root = Path(__file__).resolve().parents[2]
    tpl = (root / "scripts" / "site_template.html").read_text(encoding="utf-8")
    # Валидация: сброс к «en», если lang не входит в I18N.
    assert 'hasOwnProperty.call(I18N, lang)' in tpl
    assert 'lang = "en"' in tpl


def test_site_template_has_pagination_hooks():
    """Pagination (#2): page-size select + pager + I18N + slicing в шаблоне.

    Регрессионный guard на текст шаблона: каталог вырос до 1000+ записей —
    нужна пагинация (10/50/100) с pager внизу. Проверяем структуру шаблона,
    не запуская сайт: селектор размера, контейнер пейджера, I18N-троица,
    константа PAGE_SIZES и слайсинг списка (не безусловный list.forEach).
    """
    root = Path(__file__).resolve().parents[2]
    tpl = (root / "scripts" / "site_template.html").read_text(encoding="utf-8")
    # UI-хуки: селектор размера страницы + контейнер пейджера.
    assert 'id="f-page-size"' in tpl
    assert 'id="pager"' in tpl
    # Опции размера страницы 10/50/100.
    assert '<option value="10">10</option>' in tpl
    assert '<option value="50">50</option>' in tpl
    assert '<option value="100">100</option>' in tpl
    # I18N-троица для размера страницы (en/ru/zh).
    assert 'pageSize: "Page size"' in tpl
    assert 'pageSize: "Размер страницы"' in tpl
    assert 'pageSize: "每页数量"' in tpl
    # I18N page(n, total) на трёх языках.
    assert 'page: (n, total) => `Page ${n} of ${total}`' in tpl
    assert 'page: (n, total) => `Страница ${n} из ${total}`' in tpl
    assert 'page: (n, total) => `第 ${n} / ${total} 页`' in tpl
    # Состояние: PAGE_SIZES + валидация + fallback 50.
    assert "const PAGE_SIZES = [10, 50, 100];" in tpl
    assert "localStorage.getItem(\"vibetools:pageSize\")" in tpl
    assert "PAGE_SIZES.includes(pageSize)" in tpl
    assert "pageSize = 50" in tpl
    # Слайсинг: список рендерится по странице, а не целиком.
    assert "list.slice(" in tpl
    assert "pageItems.forEach" in tpl
    # Пейджер-функция присутствует.
    assert "function renderPager(" in tpl
    # applyI18n выставляет выбранный размер страницы в селекторе.
    assert '("f-page-size").value = String(pageSize)' in tpl


def test_site_pagination_payload_tools_not_truncated(tmp_repo):
    """Pagination режет только DOM-список, не payload: все tools на месте."""
    out = tmp_repo["root"] / "docs" / "index.html"
    site_main(tools_yml=tmp_repo["tools_yml"], stars_file=tmp_repo["stars_file"],
              out_file=out)
    payload = _extract_payload(out)
    # Пагинация slice'ит client-side; payload.tools не должен быть урезан.
    assert len(payload["tools"]) == len(tmp_repo["tools"])



# ---- stage 4: trendshift-repos surfaced on the site ----

def test_build_data_json_includes_trendshift_repos(tmp_repo):
    """trendshift-repos.json → записи подмешиваются в tools с trendshiftDiscovered."""
    tmp_repo["trendshift_repos_file"].write_text(json.dumps([{
        "githubUrl": "https://github.com/discovered/repo",
        "trendshiftId": "99999",
        "category": "cli-agents",
        "name": "discovered-repo",
        "description": "A discovered coding agent",
        "language": "Python",
        "topics": ["ai-agent"],
        "badges": [{"kind": "week", "rank": 3, "badgeUrl": "https://trendshift.io/api/badge/trendshift/repositories/99999/weekly"}],
    }]), encoding="utf-8")

    data = build_data_json(
        tmp_repo["tools_yml"], tmp_repo["stars_file"],
        trendshift_repos_file=tmp_repo["trendshift_repos_file"],
    )

    discovered = [t for t in data["tools"] if t.get("trendshiftDiscovered")]
    assert len(discovered) == 1
    rec = discovered[0]
    assert rec["url"] == "https://github.com/discovered/repo"
    assert rec["category"] == "cli-agents"
    assert rec["name"] == "discovered-repo"
    assert rec["isNew"] is False  # discovery ≠ tool-new
    assert rec["desc"] == {
        "en": "A discovered coding agent",
        "ru": "A discovered coding agent",   # нет descriptionRu → fallback на en
        "zh": "A discovered coding agent",   # нет descriptionZh → fallback на en
    }
    assert rec["language"] == "Python"
    assert "trendshift" in rec  # badges прокинулись


def test_build_data_json_dedups_trendshift_repos_against_tools_yml(tmp_repo):
    """URL, уже в tools.yml, не дублируется из trendshift-repos."""
    # https://github.com/a/hi уже есть в tmp_repo tools.yml.
    tmp_repo["trendshift_repos_file"].write_text(json.dumps([{
        "githubUrl": "https://github.com/a/hi",
        "category": "cli-agents",
    }]), encoding="utf-8")

    data = build_data_json(
        tmp_repo["tools_yml"], tmp_repo["stars_file"],
        trendshift_repos_file=tmp_repo["trendshift_repos_file"],
    )

    hi = [t for t in data["tools"] if t["url"] == "https://github.com/a/hi"]
    assert len(hi) == 1  # без дубля
    assert not hi[0].get("trendshiftDiscovered")  # остался кураторским


def test_build_data_json_trendshift_repo_needs_review_fallback(tmp_repo):
    """Запись без category → 'needs-review' (никогда не теряется, видна на сайте)."""
    tmp_repo["trendshift_repos_file"].write_text(json.dumps([{
        "githubUrl": "https://github.com/foo/bar",
        # без category
    }]), encoding="utf-8")

    data = build_data_json(
        tmp_repo["tools_yml"], tmp_repo["stars_file"],
        trendshift_repos_file=tmp_repo["trendshift_repos_file"],
    )

    rec = next(t for t in data["tools"] if t["url"] == "https://github.com/foo/bar")
    assert rec["category"] == "needs-review"
    assert rec.get("trendshiftDiscovered") is True


def test_build_data_json_trendshift_repo_stars_from_cache(tmp_repo, tmp_path):
    """Звёзды для trendshift-репо берутся из stars.json (собирает update_stars)."""
    meta_file = tmp_path / "repos-meta.json"
    url = "https://github.com/discovered/repo"
    meta_file.write_text(json.dumps({url: {
        "stars": 500, "forks": 5, "createdAt": "2026-01-01T00:00:00Z",
        "topics": ["ai"], "language": "Go"}}), encoding="utf-8")
    tmp_repo["trendshift_repos_file"].write_text(json.dumps([{
        "githubUrl": url, "category": "cli-agents",
    }]), encoding="utf-8")

    data = build_data_json(
        tmp_repo["tools_yml"], tmp_repo["stars_file"],
        meta_file=meta_file, trendshift_repos_file=tmp_repo["trendshift_repos_file"],
    )

    rec = next(t for t in data["tools"] if t["url"] == url)
    assert rec["forks"] == 5
    assert rec["createdAt"] == "2026-01-01T00:00:00Z"
    assert rec["language"] == "Go"

