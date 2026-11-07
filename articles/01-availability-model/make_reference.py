"""Создаёт reference.docx по требованиям журнала «Экономика и качество систем связи»:
Times New Roman 12, интервал 1,0, поля 3 см, абзацный отступ 1,25 см."""
import sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

src, dst = sys.argv[1], sys.argv[2]
d = Document(src)
for s in d.sections:
    s.page_height, s.page_width = Cm(29.7), Cm(21.0)
    s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Cm(3)

def font(st, size=12, bold=None, italic=None):
    f = st.font
    f.name = "Times New Roman"; f.size = Pt(size); f.color.rgb = RGBColor(0, 0, 0)
    if bold is not None: f.bold = bold
    if italic is not None: f.italic = italic
    rpr = st.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = rpr.makeelement(qn("w:rFonts"), {}); rpr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), "Times New Roman")
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rf.get(qn(a)) is not None: del rf.attrib[qn(a)]

def para(st, indent=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY, before=0, after=0):
    pf = st.paragraph_format
    pf.line_spacing = 1.0; pf.space_before = Pt(before); pf.space_after = Pt(after)
    pf.first_line_indent = Cm(1.25) if indent else Cm(0)
    pf.alignment = align

byname = {s.name.lower(): s for s in d.styles}
names = list(byname)
for n in ("Normal", "Body Text", "First Paragraph", "Compact", "Block Text"):
    if n.lower() in names:
        font(byname[n.lower()]); para(byname[n.lower()], indent=n not in ("Compact",))
for n, sz in (("Title", 14), ("Heading 1", 14), ("Heading 2", 12), ("Heading 3", 12)):
    if n.lower() in names:
        font(byname[n.lower()], sz, bold=True, italic=False)
        para(byname[n.lower()], indent=False, align=WD_ALIGN_PARAGRAPH.CENTER if n in ("Title", "Heading 1") else WD_ALIGN_PARAGRAPH.LEFT, before=6, after=6)
for n in ("Image Caption", "Table Caption", "Caption"):
    if n.lower() in names:
        font(byname[n.lower()], 12, italic=False); para(byname[n.lower()], indent=False, align=WD_ALIGN_PARAGRAPH.CENTER, after=6)
d.save(dst)
