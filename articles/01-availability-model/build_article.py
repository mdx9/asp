"""Сборка article.md в article.docx по требованиям журнала
«Экономика и качество систем связи» (Times New Roman 12, интервал 1,0, поля 3 см,
абзацный отступ 1,25 см — стили в reference.docx, см. make_reference.py).

1) Подготовка текста: alt у рисунков убирается (подпись — курсивная строка под
   рисунком, иначе pandoc дублирует её); τ_min, ν_max, ν_Г → нижние индексы;
   ^(…) и ^k → верхние индексы.
2) build-docx.py: номера формул выносятся в абзацы «Формула-номер».
3) Формула и номер сводятся в таблицу без рамок: формула по центру, номер справа.
4) Таблицам с данными — рамки и шрифт 11; рисунки — по центру, не шире 15 см.
"""
import pathlib
import re
import subprocess
import sys

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

here = pathlib.Path(__file__).parent
out = here / "article.docx"


def prepare(md: str) -> str:
    md = re.sub(r"!\[[^\]]*\]\(", "![](", md)
    parts = re.split(r"(\$\$.*?\$\$)", md, flags=re.S)  # формулы не трогать
    for i in range(0, len(parts), 2):
        s = parts[i]
        s = re.sub(r"(τ|ν)_(min|max|Г)", r"\1~\2~", s)
        s = re.sub(r"\^(\*[a-z]\*)", r"^\1^", s)           # *p*^*k* → *p*^*k*^
        s = re.sub(r"\^\(([^()\s]+)\)", r"^\1^", s)       # ^(*k*−1) → ^*k*−1^
        parts[i] = s
    return "".join(parts)


tmp = here / "_build.md"
tmp.write_text(prepare((here / "article.md").read_text(encoding="utf-8")), encoding="utf-8")
try:
    subprocess.run([sys.executable, str(here.parent.parent / "build-docx.py"), str(tmp),
                    "-o", str(out), "--reference", str(here / "reference.docx")], check=True)
finally:
    tmp.unlink(missing_ok=True)

d = Document(str(out))


def borders(tbl, val):
    tblPr = tbl.find(qn("w:tblPr"))
    old = tblPr.find(qn("w:tblBorders"))
    if old is not None:
        tblPr.remove(old)
    b = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{side}")
        e.set(qn("w:val"), val)
        if val != "nil":
            e.set(qn("w:sz"), "4")
            e.set(qn("w:color"), "000000")
        b.append(e)
    tblPr.append(b)


for t in d.tables:
    borders(t._tbl, "single")
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                p.paragraph_format.first_line_indent = Cm(0)
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.size = Pt(11)

n = 0
for p in list(d.paragraphs):
    if p.style.name != "Формула-номер":
        continue
    prev = p._p.getprevious()
    if prev is None or prev.find(".//" + qn("m:oMathPara")) is None:
        continue
    tbl = d.add_table(rows=1, cols=2)
    borders(tbl._tbl, "nil")
    tbl.autofit = False
    c0, c1 = tbl.rows[0].cells
    for c, w in ((c0, Cm(14.0)), (c1, Cm(1.0))):
        c.width = w
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    c0._tc.remove(c0.paragraphs[0]._p)
    c0._tc.append(prev)
    c1.paragraphs[0].text = p.text
    c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    c1.paragraphs[0].paragraph_format.first_line_indent = Cm(0)
    p._p.addprevious(tbl._tbl)
    p._p.getparent().remove(p._p)
    n += 1

for p in d.paragraphs:
    if p._p.find(".//" + qn("w:drawing")) is not None:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
for s in d.inline_shapes:
    if s.width > Cm(15):
        r = Cm(15) / s.width
        s.width = Cm(15)
        s.height = int(s.height * r)

d.save(str(out))
print("формул:", n, "| таблиц с данными:", len(d.tables) - n, "| рисунков:", len(d.inline_shapes))
