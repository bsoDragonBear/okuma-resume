#!/usr/bin/env python3
"""Build a resume PDF from the data-pdf elements in an HTML source."""

import argparse
import reportlab
from html import escape
from html.parser import HTMLParser
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, SimpleDocTemplate


ROOT = Path(__file__).resolve().parents[1]
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class ResumeParser(HTMLParser):
    """Collect explicitly marked text, preserving HTML's nested inline content."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = []
        self.active = None
        self.depth = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.active is not None:
            if tag not in VOID_TAGS:
                self.depth += 1
            if tag == "br":
                self.parts.append(" ")
        elif "data-pdf" in attrs:
            self.active = (attrs["data-pdf"], attrs.get("data-page-break") == "before")
            self.depth = 1
            self.parts = []

    def handle_endtag(self, tag):
        if self.active is None or tag in VOID_TAGS:
            return
        self.depth -= 1
        if self.depth == 0:
            text = " ".join("".join(self.parts).split())
            if text:
                self.blocks.append((*self.active, text))
            self.active = None
            self.parts = []

    def handle_data(self, data):
        if self.active is not None:
            self.parts.append(data)


def build_pdf(source, output):
    parser = ResumeParser()
    parser.feed(source.read_text(encoding="utf-8"))
    parser.close()
    if not parser.blocks or parser.blocks[0][0] != "name" or parser.active is not None:
        raise ValueError("Expected a complete resume beginning with data-pdf='name'.")

    # Embed ReportLab's bundled fonts so rendering does not depend on the viewer.
    font_dir = Path(reportlab.__file__).resolve().parent / "fonts"
    for name, filename in (("Resume", "Vera.ttf"), ("ResumeBold", "VeraBd.ttf"), ("ResumeItalic", "VeraIt.ttf")):
        pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))

    ink = colors.HexColor("#17283B")
    muted = colors.HexColor("#4B5563")
    base = ParagraphStyle(
        "base", fontName="Resume", fontSize=10, leading=13,
        textColor=colors.HexColor("#20252B"), alignment=TA_LEFT,
        spaceAfter=5,
    )
    styles = {
        "name": ParagraphStyle("name", parent=base, fontName="ResumeBold", fontSize=23, leading=27, textColor=ink, spaceAfter=4, keepWithNext=True),
        "headline": ParagraphStyle("headline", parent=base, fontSize=11, leading=14, textColor=ink, spaceAfter=4, keepWithNext=True),
        "contact": ParagraphStyle("contact", parent=base, fontSize=9, leading=12, textColor=muted, spaceAfter=9, keepWithNext=True),
        "section": ParagraphStyle("section", parent=base, fontName="ResumeBold", fontSize=11.5, leading=15, textColor=ink, spaceBefore=9, spaceAfter=5, keepWithNext=True),
        "employer": ParagraphStyle("employer", parent=base, fontName="ResumeBold", fontSize=11, leading=14, spaceAfter=4, keepWithNext=True),
        "role": ParagraphStyle("role", parent=base, fontSize=9.5, leading=12.5, spaceAfter=3, keepWithNext=True),
        "note": ParagraphStyle("note", parent=base, fontName="ResumeItalic", fontSize=9, leading=12, textColor=muted, spaceBefore=5, spaceAfter=6, keepWithNext=True),
        "job": ParagraphStyle("job", parent=base, fontName="ResumeBold", fontSize=10.3, leading=13, spaceBefore=5, spaceAfter=2, keepWithNext=True),
        "dates": ParagraphStyle("dates", parent=base, fontSize=9, leading=11.5, textColor=muted, spaceAfter=4, keepWithNext=True),
        "body": base,
        "bullet": ParagraphStyle("bullet", parent=base, leftIndent=10, bulletIndent=0, spaceAfter=5),
        "skill": ParagraphStyle("skill", parent=base, fontSize=9.5, leading=12.5, spaceAfter=4),
    }
    story = []
    for kind, page_break, text in parser.blocks:
        if kind not in styles:
            raise ValueError(f"Unknown data-pdf kind: {kind}")
        if page_break:
            story.append(PageBreak())
        options = {"bulletText": "\u2022"} if kind == "bullet" else {}
        paragraph = Paragraph(escape(text), styles[kind], **options)
        story.append(KeepTogether([paragraph]) if kind in {"bullet", "body", "skill"} else paragraph)

    name = parser.blocks[0][2]

    def decorate_page(canvas, document):
        canvas.saveState()
        canvas.setFont("Resume", 8)
        canvas.setFillColor(muted)
        canvas.drawString(42, 25, name)
        canvas.drawRightString(letter[0] - 42, 25, f"Page {document.page}")
        canvas.restoreState()

    output.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(output), pagesize=letter, leftMargin=42, rightMargin=42,
        topMargin=36, bottomMargin=40,
        title=f"{name} - {next((text for kind, _, text in parser.blocks if kind == 'headline'), 'Resume')}", author=name,
    )
    document.build(story, onFirstPage=decorate_page, onLaterPages=decorate_page)
    print(f"Built {output}")


if __name__ == "__main__":
    arguments = argparse.ArgumentParser(description=__doc__)
    arguments.add_argument("--source", type=Path, default=ROOT / "index.html")
    arguments.add_argument("--output", type=Path, default=ROOT / "Resume - Okuma.pdf")
    args = arguments.parse_args()
    build_pdf(args.source, args.output)
