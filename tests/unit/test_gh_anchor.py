"""Тесты gh_anchor — эмуляции якоря заголовка GitHub.

КРИТИЧНЫЙ модуль: неверный якорь = битая ссылка в оглавлении README.
Тесты фиксируют текущее поведение как контракт.

Известное ограничение: реализация самосогласована (TOC-ссылки резолвятся
в сгенерированном README), но НЕ гарантирует совпадения с тем, как
github.com рендерит якоря на сайте (GitHub применяет собственные правила
для эмодзи/Unicode normalization). Внутреннюю согласованность покрываем;
браузерный тест (playwright) выходит за рамки этого набора.
"""
import re

import pytest

import generate_readme
from generate_readme import CATEGORIES, gh_anchor


@pytest.mark.parametrize("text, expected", [
    # ASCII база
    ("Editor Integrations", "editor-integrations"),
    ("Context / Memory", "context-memory"),
    ("Prompts / MCP", "prompts-mcp"),
    # эмодзи в начале удаляется, ведущего дефиса НЕТ (инвариант README TOC)
    ("🤖 AI Coding Agents / CLI", "ai-coding-agents-cli"),
    ("🤖 AI-агенты кодинга / CLI", "ai-агенты-кодинга-cli"),
    # composed emoji с VS16 — критичный edge case
    ("🛠️ Workflow / Automation", "workflow-automation"),
    # кириллица сохраняется (isalnum() для кириллицы = True)
    ("Обучение / Ресурсы", "обучение-ресурсы"),
    # пунктуация → пробел → дефис
    ("avante.nvim", "avante-nvim"),
    ("12-Factor Agents", "12-factor-agents"),
    # схлопывание пробелов и дефисов
    ("   multiple   spaces   ", "multiple-spaces"),
    ("a--b  c", "a-b-c"),
    # регистр
    ("MixedCASE Word", "mixedcase-word"),
    # спецсимволы: ! ? ( ) & @ # удаляются
    ("Hello! World? (test) & co.", "hello-world-test-co"),
    # пустая строка и только-эмодзи
    ("", ""),
    ("🚀", ""),
    # слэш как разделитель
    ("A / B / C", "a-b-c"),
    # только дефисы/пунктуация
    ("---", "-"),
    ("...", ""),
])
def test_gh_anchor(text, expected):
    assert gh_anchor(text) == expected


def test_gh_anchor_toc_consistency():
    """Для каждой категории gh_anchor(title) должен совпадать с якорем,
    который реально стоит в закоммиченном README TOC.

    Ловит regression: кто-то поменял gh_anchor или title и забыл
    перегенерировать README — TOC и заголовки разъедутся.
    """
    repo_root = generate_readme.ROOT
    for readme_name, lang in (("README.md", "en"), ("README.ru.md", "ru")):
        readme = (repo_root / readme_name).read_text(encoding="utf-8")
        toc_anchors = set(re.findall(r"\(#([^)]+)\)", readme))
        title_key = f"title_{lang}"
        expected_anchors = {
            gh_anchor(meta[title_key])
            for _, meta in CATEGORIES
        }
        # Каждый ожидаемый якорь должен присутствовать среди TOC-ссылок.
        missing = expected_anchors - toc_anchors
        assert not missing, f"{readme_name}: в TOC нет якорей {missing}"
