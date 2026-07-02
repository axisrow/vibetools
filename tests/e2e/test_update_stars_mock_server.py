"""E2E: весь пайплайн update_stars против локального mock-GitHub сервера.

В CI на каждый PR/пуш. monkeypatch подменяет update_stars.API на адрес сервера.
"""
import json

import update_stars
from update_stars import main as update_main


def _patch_api(monkeypatch, mock_github):
    """Подменяет шаблон API на URL mock-сервера."""
    monkeypatch.setattr(update_stars, "API", mock_github.base_url + "/repos/{owner}/{repo}")


def _cache(tmp_repo):
    return json.loads(tmp_repo["stars_file"].read_text(encoding="utf-8"))


def test_e2e_full_pipeline_success(tmp_repo, mock_github, monkeypatch):
    mock_github.register("a", "hi", stars=100)
    mock_github.register("a", "lo", stars=5)
    mock_github.register("b", "editor", stars=50)
    _patch_api(monkeypatch, mock_github)

    rc = update_main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"])
    cache = _cache(tmp_repo)
    assert rc == 0
    assert cache["https://github.com/a/hi"] == 100
    assert cache["https://github.com/a/lo"] == 5
    assert cache["https://github.com/b/editor"] == 50
    # README перегенерирован с бейджами.
    readme = (tmp_repo["root"] / "README.md").read_text(encoding="utf-8")
    assert "img.shields.io/github/stars/a/hi" in readme


def test_e2e_one_repo_404_does_not_break_run(tmp_repo, mock_github, monkeypatch):
    """2 ok + 1 (404): остальные обновились, 404-й сохранил прежнее значение, return 0."""
    tmp_repo["stars_file"].write_text(
        json.dumps({"https://github.com/a/lo": 3}), encoding="utf-8")
    mock_github.register("a", "hi", stars=100)
    mock_github.register("a", "lo", status=404)
    mock_github.register("b", "editor", stars=50)
    _patch_api(monkeypatch, mock_github)

    rc = update_main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"])
    cache = _cache(tmp_repo)
    assert rc == 0
    assert cache["https://github.com/a/hi"] == 100
    assert cache["https://github.com/a/lo"] == 3   # прежнее значение при 404
    assert cache["https://github.com/b/editor"] == 50


def test_e2e_rate_limit_429_keeps_cache(tmp_repo, mock_github, monkeypatch):
    tmp_repo["stars_file"].write_text(
        json.dumps({"https://github.com/a/hi": 42}), encoding="utf-8")
    mock_github.register("a", "hi", status=429)
    mock_github.register("a", "lo", stars=5)
    mock_github.register("b", "editor", stars=50)
    _patch_api(monkeypatch, mock_github)

    update_main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"])
    cache = _cache(tmp_repo)
    assert cache["https://github.com/a/hi"] == 42  # кэш сохранён при 429
    assert cache["https://github.com/a/lo"] == 5


def test_e2e_connection_refused(tmp_repo, monkeypatch):
    """API указывает на несуществующий порт → RequestException → None, кэш сохранён."""
    tmp_repo["stars_file"].write_text(
        json.dumps({"https://github.com/a/hi": 7}), encoding="utf-8")
    # Несуществующий локальный порт → connection refused.
    monkeypatch.setattr(update_stars, "API", "http://127.0.0.1:1/repos/{owner}/{repo}")

    rc = update_main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"])
    cache = _cache(tmp_repo)
    assert rc == 0
    assert cache["https://github.com/a/hi"] == 7  # прежний кэш уцелел


def test_e2e_token_passed_as_header(tmp_repo, mock_github, monkeypatch):
    """GITHUB_TOKEN в env → запрос несёт заголовок Authorization: Bearer ..."""
    mock_github.register("a", "hi", stars=100)
    mock_github.register("a", "lo", stars=5)
    mock_github.register("b", "editor", stars=50)
    _patch_api(monkeypatch, mock_github)
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_test_token_123")

    update_main(tmp_repo["tools_yml"], tmp_repo["stars_file"], out_dir=tmp_repo["root"])
    sent = mock_github.log[0][0]  # (Request, Response)
    assert sent.headers["Authorization"] == "Bearer ghp_test_token_123"
