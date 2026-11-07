#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка глав диссертации из Markdown в docx.

Решает две задачи, которые pandoc сам не решает:

1. Номера формул. Конструкция \\tag{3.5} внутри $$...$$ при преобразовании в
   OMML отбрасывается: формулы в docx остаются без номеров, тогда как по тексту
   на них расставлены ссылки вида (3.5). Скрипт выносит номер из формулы в
   отдельный абзац со стилем «Формула-номер», который в Word достаточно один раз
   настроить на выключку вправо.

2. Подписи рисунков и таблиц получают стили «Подрисуночная-подпись» и
   «Подпись-таблицы», чтобы форматировать их по ГОСТ разом, а не поштучно.

Использование:
    python3 tools/build-docx.py thesis/chapter3.md
    python3 tools/build-docx.py thesis/chapter3.md --reference gost.docx
"""
import argparse
import pathlib
import re
import subprocess
import sys
import tempfile

EQ_STYLE = "Формула-номер"
FIG_STYLE = "Подрисуночная-подпись"
TAB_STYLE = "Подпись-таблицы"


def div(style, text):
    return f'\n\n::: {{custom-style="{style}"}}\n{text}\n:::\n'


def preprocess(md: str) -> tuple[str, dict]:
    stats = {"формул": 0, "рисунков": 0, "таблиц": 0}

    def eq(m):
        body, num = m.group(1), m.group(2)
        stats["формул"] += 1
        # «\(» — иначе номер вида (1) pandoc примет за маркер нумерованного списка
        return f"$$\n{body.strip()}\n$$" + div(EQ_STYLE, f"\\({num})")

    # $$ ... \tag{3.N} $$  ->  формула + абзац с номером
    md = re.sub(r"\$\$(.*?)\\tag\{([^}]+)\}\s*\$\$", eq, md, flags=re.S)

    def fig(m):
        stats["рисунков"] += 1
        return div(FIG_STYLE, m.group(1))

    # *Рисунок 3.1 — ...* на отдельной строке
    md = re.sub(r"^\*(Рисунок [^*\n]+)\*$", fig, md, flags=re.M)

    def tab(m):
        stats["таблиц"] += 1
        return div(TAB_STYLE, m.group(1))

    md = re.sub(r"^\*\*(Таблица [^*\n]+)\*\*$", tab, md, flags=re.M)

    md = re.sub(r"\n{3,}", "\n\n", md)
    return md, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="файл главы, например thesis/chapter3.md")
    ap.add_argument("-o", "--output", help="имя docx (по умолчанию — по имени главы)")
    ap.add_argument("--reference", help="reference.docx со стилями по ГОСТ")
    a = ap.parse_args()

    src = pathlib.Path(a.source)
    if not src.exists():
        sys.exit(f"нет файла {src}")
    out = pathlib.Path(a.output) if a.output else src.with_suffix(".docx")

    md, stats = preprocess(src.read_text(encoding="utf-8"))

    remaining = re.findall(r"\\tag\{", md)
    if remaining:
        sys.exit(f"остались необработанные \\tag: {len(remaining)}")

    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8",
                                     delete=False, dir=src.parent) as f:
        f.write(md)
        tmp = pathlib.Path(f.name)

    cmd = ["pandoc", str(tmp), "-o", str(out),
           f"--resource-path={src.parent}", "--from", "markdown+tex_math_dollars"]
    if a.reference:
        cmd += ["--reference-doc", a.reference]

    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            sys.exit(f"pandoc: {r.stderr.strip()}")
    finally:
        tmp.unlink(missing_ok=True)

    print(f"собрано: {out}")
    print(f"  вынесено номеров формул: {stats['формул']}")
    print(f"  подписей рисунков:       {stats['рисунков']}")
    print(f"  подписей таблиц:         {stats['таблиц']}")
    print(f"\nВ Word настроить три стиля: «{EQ_STYLE}» (выключка вправо), "
          f"«{FIG_STYLE}» и «{TAB_STYLE}» (по ГОСТ).")


if __name__ == "__main__":
    main()
