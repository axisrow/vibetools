"""Integration: generate_site.main() — сборка docs/index.html из tmp tools.yml.

Проверяет: создаётся валидный index.html со встроенными данными, все tools
на месте, search-поле lowercase (CJK-aware), stars fallback, i18n title_zh.
"""
import json
import re

from generate_site import build_data_json, main as site_main


def _extract_payload(html: str) -> dict:
    """Достаёт встроенный window.__DATA__ payload из HTML."""
    m = re.search(r"window\.__DATA__ = (\{.*?\});\n", html, re.S)
    assert m, "payload не найден в index.html"
    return json.loads(m.group(1))


def test_site_creates_index(tmp_tools_yml, sample_tool_github, tmp_path):
    tools_yml = tmp_tools_yml([sample_tool_github])
    out = tmp_path / "docs" / "index.html"
    site_main(tools_yml=tools_yml, stars_file=tmp_path / "stars.json", out_file=out)
    assert out.exists()
    html = out.read_text(encoding="utf-8")
    assert "Awesome Vibe Coding Tools" in html
    payload = _extract_payload(html)
    assert len(payload["tools"]) == 1


def test_site_contains_all_tools(tmp_repo):
    """Сайт включает все tools из tools.yml (через tmp_repo fixture)."""
    out = tmp_repo["root"] / "docs" / "index.html"
    site_main(tools_yml=tmp_repo["tools_yml"], stars_file=tmp_repo["stars_file"],
              out_file=out)
    payload = _extract_payload(out.read_text(encoding="utf-8"))
    assert len(payload["tools"]) == len(tmp_repo["tools"])
    names = {t["name"] for t in payload["tools"]}
    assert {"HiStars", "LoStars", "Editor", "NoGithub"} <= names


def test_site_search_field_is_lowercase(tmp_repo):
    """search-поле = lowercase name+en+ru — для мгновенного includes() в JS."""
    out = tmp_repo["root"] / "docs" / "index.html"
    site_main(tools_yml=tmp_repo["tools_yml"], stars_file=tmp_repo["stars_file"],
              out_file=out)
    payload = _extract_payload(out.read_text(encoding="utf-8"))
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
    payload = _extract_payload(out.read_text(encoding="utf-8"))
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
    payload = _extract_payload(out.read_text(encoding="utf-8"))
    hi = next(t for t in payload["tools"] if t["name"] == "HiStars")
    assert hi["stars"] == 1000  # из tmp_repo fixture stars.json


def test_site_categories_have_title_zh(tmp_repo):
    """Категории в payload несут title_zh для i18n переключателя."""
    out = tmp_repo["root"] / "docs" / "index.html"
    site_main(tools_yml=tmp_repo["tools_yml"], stars_file=tmp_repo["stars_file"],
              out_file=out)
    payload = _extract_payload(out.read_text(encoding="utf-8"))
    assert payload["categories"]
    for c in payload["categories"]:
        assert "title_zh" in c and c["title_zh"]


def test_site_cjk_search(tmp_tools_yml, tmp_path):
    """Репо с китайским описанием — CJK-текст попадает в search-поле (поиск работает)."""
    tool = {"name": "ai-guide", "url": "https://github.com/liyupi/ai-guide",
            "category": "learning",
            "description": {"en": "程序员鱼皮的 AI 资源大全", "ru": "AI ресурсы"}}
    tools_yml = tmp_tools_yml([tool])
    out = tmp_path / "docs" / "index.html"
    site_main(tools_yml=tools_yml, stars_file=tmp_path / "stars.json", out_file=out)
    payload = _extract_payload(out.read_text(encoding="utf-8"))
    t = payload["tools"][0]
    # Китайский иероглиф (U+7A0B 程) должен быть в lowercase haystack
    assert "程" in t["search"] or "ai-guide" in t["search"]


def test_build_data_json_structure(tmp_repo):
    """build_data_json возвращает ожидаемую структуру (без verified/added)."""
    data = build_data_json(tmp_repo["tools_yml"], tmp_repo["stars_file"])
    assert set(data.keys()) >= {"generatedAt", "categories", "tools"}
    tool = data["tools"][0]
    # verified/added убраны; добавлены forks/createdAt/topics/rank/starsPerWeek.
    assert set(tool.keys()) >= {
        "name", "url", "category", "isNew",
        "stars", "starsPerWeek", "starsUrl", "forks", "openIssues",
        "createdAt", "archived", "topics", "rank", "desc", "search"}
    assert "verified" not in tool and "added" not in tool


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
    meta_file.write_text(_json.dumps({url: {
        "stars": 1000, "forks": 42, "openIssues": 3,
        "pushedAt": "2026-07-01T00:00:00Z", "createdAt": "2026-06-25T00:00:00Z",
        "topics": ["ai", "agent"], "archived": False}}), encoding="utf-8")
    data = build_data_json(tmp_repo["tools_yml"], tmp_repo["stars_file"], meta_file=meta_file)
    hi = next(t for t in data["tools"] if t["name"] == "HiStars")
    assert hi["forks"] == 42
    assert hi["createdAt"] == "2026-06-25T00:00:00Z"
    assert "agent" in hi["topics"]
    assert hi["isNew"] is True  # 2026-06-25 в пределах 14д от сегодня
