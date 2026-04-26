#!/usr/bin/env python3
"""Добавляет явные {: #id} к заголовкам для совпадения с ссылками angular.io."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "angular"


def ensure_heading_anchor(content: str, anchor: str, heading_prefix: str) -> str:
    lines = content.splitlines(keepends=True)
    out: list[str] = []
    done = False
    for line in lines:
        if not done and line.startswith(heading_prefix):
            stripped = line.rstrip("\n")
            if re.search(r"\{\s*:\s*#[^}]+\}\s*$", stripped):
                out.append(line)
            else:
                out.append(f"{stripped} {{: #{anchor}}}\n")
            done = True
        else:
            out.append(line)
    if not done:
        raise ValueError(f"Заголовок не найден: {heading_prefix!r}")
    return "".join(out)


def inject_before_line(content: str, needle: str, replacement: str) -> str:
    if needle not in content:
        raise ValueError(f"Строка не найдена: {needle!r}")
    if replacement.split("\n")[0] in content:
        return content
    return content.replace(needle, replacement, 1)


# (файл, якорь, префикс строки заголовка)
SUFFIXES: list[tuple[str, str, str]] = [
    ("angular-compiler-options.md", "angular-compiler-options", "# Параметры компилятора Angular"),
    ("architecture-components.md", "component-metadata", "## Метаданные компонента"),
    ("architecture-components.md", "templates-and-views", "## Шаблоны и представления"),
    ("architecture-components.md", "template-syntax", "## Синтаксис шаблонов"),
    ("architecture-components.md", "data-binding", "### Привязка данных"),
    ("architecture-components.md", "pipes", "### Пайпы"),
    ("architecture-components.md", "directives", "### Директивы"),
    ("built-in-directives.md", "built-in-attribute-directives", "## Встроенные директивы атрибутов"),
    ("built-in-directives.md", "ngClass", "## Добавление и удаление классов с помощью `NgClass`"),
    (
        "built-in-directives.md",
        "displaying-and-updating-properties-with-ngmodel",
        "## Отображение и обновление свойств с помощью `ngModel`",
    ),
    ("built-in-directives.md", "ngModel", "### `NgModel` и аксессоры значений"),
    ("built-in-directives.md", "built-in-structural-directives", "## Встроенные структурные директивы"),
    ("structural-directives.md", "shorthand", "## Сокращение структурных директив"),
    ("structural-directives.md", "one-per-element", "## Одна структурная директива на элемент"),
    (
        "structural-directives.md",
        "directive-type-checks",
        "## Улучшение проверки типов шаблонов для пользовательских директив",
    ),
    ("structural-directives.md", "asterisk", "### Как Angular переводит стенографические директивы"),
    ("router.md", "route-order", "### Порядок маршрутов"),
    ("router.md", "404-page-how-to", "## Отображение страницы 404"),
    ("router.md", "accessing-query-parameters-and-fragments", "## Доступ к параметрам запроса и фрагментам"),
    ("router.md", "preventing-unauthorized-access", "## Предотвращение несанкционированного доступа"),
    ("router.md", "link-parameters-array", "## Массив параметров ссылки"),
]

# Два id на одном разделе — через <a id="...">
INJECT: list[tuple[str, str, str]] = [
    (
        "router.md",
        "## Настройка маршрутов wildcard",
        '<a id="wildcard-route-how-to"></a>\n\n## Настройка маршрутов wildcard {: #setting-up-wildcard-routes}',
    ),
    (
        "router.md",
        "## `LocationStrategy` и стили URL браузера",
        '<a id="browser-url-styles"></a>\n\n## `LocationStrategy` и стили URL браузера {: #location-strategy}',
    ),
]


def main() -> None:
    for fname, needle, repl in INJECT:
        path = DOCS / fname
        text = path.read_text(encoding="utf-8")
        text = inject_before_line(text, needle, repl)
        path.write_text(text, encoding="utf-8")

    by_file: dict[str, list[tuple[str, str]]] = {}
    for fname, anchor, prefix in SUFFIXES:
        by_file.setdefault(fname, []).append((anchor, prefix))

    for fname, items in by_file.items():
        path = DOCS / fname
        text = path.read_text(encoding="utf-8")
        for anchor, prefix in items:
            text = ensure_heading_anchor(text, anchor, prefix)
        path.write_text(text, encoding="utf-8")

    print("apply_doc_anchors: batch 1 OK")


if __name__ == "__main__":
    main()
