"""
Build AoE Self Assessment PDF — questions only, no wheel page.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle,
    KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.colors import HexColor
import os

GOLD  = HexColor("#B8952A")
DARK  = HexColor("#2C2C2C")
CREAM = HexColor("#F7F3EC")
BAND1 = HexColor("#E6DFD2")
MID   = HexColor("#9A8A72")
RULE  = HexColor("#D4CEC4")

W, H = letter

COPYRIGHT = (
    "Architecture of Excellence™  ©  2026 Dr. Alina K. Schulhofer.  |  All rights reserved.\n"
    "This material is proprietary and intended for informational purposes only. "
    "Unauthorized reproduction or distribution is not permitted."
)
CLOSING = (
    "Take some time to reflect and journal on your answers and consider "
    "which areas may represent continued areas for growth."
)

LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "aoe-logo.png")

PILLARS = [
    ("TRUTH", [
        "How honest are you with yourself about what you truly want, feel, and believe?",
        "To what degree do you act in alignment with your values, even when it is uncomfortable?",
        "How willing are you to examine and challenge the narratives you hold about yourself and your life?",
    ]),
    ("CONNECTION", [
        "How present and genuine are you in your most important relationships?",
        "How well do you communicate your needs, boundaries, and emotions to others?",
        "How supported do you feel by the people in your life, and how much do you invest in those connections?",
    ]),
    ("BEING", [
        "How well do you listen to and care for your physical body on a daily basis?",
        "How much do you prioritize rest, recovery, and practices that restore your inner calm?",
        "How grounded and present do you feel in your daily experience?",
    ]),
    ("VISION", [
        "How clearly can you articulate what you are building and where you are headed?",
        "How aligned are your daily actions with your longer-term goals and aspirations?",
        "How often do you create space to think expansively about your future?",
    ]),
    ("MEANING", [
        "How deeply connected do you feel to a sense of purpose in your work and life?",
        "How often do you experience genuine fulfilment, as opposed to simply achieving?",
        "How much does what you do reflect what actually matters to you?",
    ]),
    ("CREATION", [
        "How freely do you express your ideas, perspectives, and creative impulses?",
        "How actively are you building, contributing, or bringing something new into the world?",
        "How much do you allow yourself to take creative risks without fear of judgement?",
    ]),
    ("EXCELLENCE", [
        "How committed are you to continuous growth and the refinement of your craft?",
        "How willing are you to change aspects of yourself to pursue greatness?",
        "How consistently do you hold yourself to a standard that reflects your full potential?",
    ]),
]


def scale_row():
    box_w = 20
    box_h = 14
    nb = ParagraphStyle("nb", fontName="Times-Bold", fontSize=7.5,
                        alignment=TA_CENTER, textColor=DARK)
    data = [[Paragraph(f"<b>{n}</b>", nb) for n in range(1, 11)]]
    t = Table(data, colWidths=[box_w] * 10, rowHeights=[box_h])
    t.setStyle(TableStyle([
        ("BOX",        (0, 0), (-1, -1), 0.5, GOLD),
        ("INNERGRID",  (0, 0), (-1, -1), 0.5, GOLD),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#FAF7F2")),
        ("TOPPADDING",    (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def on_every_page(canvas, doc):
    """Draw header and footer on every page."""
    canvas.saveState()
    page_w, page_h = W, H
    margin = 36

    # ── HEADER — centered title, logo top-right if available ──
    canvas.setFillColor(GOLD)
    canvas.setFont("Times-Roman", 18)
    canvas.drawCentredString(page_w / 2, page_h - 50, "AoE Self Assessment")

    logo_x = page_w - margin - 70
    logo_y = page_h - 62
    if os.path.exists(LOGO_PATH):
        canvas.drawImage(LOGO_PATH, logo_x, logo_y, width=70, height=28,
                         preserveAspectRatio=True, mask="auto")

    # Header rule
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.5)
    canvas.line(margin, page_h - 66, page_w - margin, page_h - 66)

    # ── FOOTER ──
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.3)
    canvas.line(margin, 40, page_w - margin, 40)

    canvas.setFillColor(MID)
    canvas.setFont("Times-Roman", 6.5)
    lines = COPYRIGHT.split("\n")
    canvas.drawCentredString(page_w / 2, 30, lines[0])
    if len(lines) > 1:
        canvas.drawCentredString(page_w / 2, 20, lines[1])

    canvas.restoreState()


def build():
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "assets", "aoe-self-assessment.pdf")
    margin = 36
    doc = SimpleDocTemplate(
        out_path, pagesize=letter,
        leftMargin=margin, rightMargin=margin,
        topMargin=80,   # room for header
        bottomMargin=52,
    )

    pillar_style = ParagraphStyle(
        "Pillar", fontName="Times-Bold", fontSize=9, leading=12,
        textColor=GOLD, spaceBefore=12, spaceAfter=4,
    )
    q_style = ParagraphStyle(
        "Q", fontName="Times-Roman", fontSize=8.5, leading=12,
        textColor=DARK, spaceAfter=3, leftIndent=12,
    )
    intro_style = ParagraphStyle(
        "Intro", fontName="Times-Roman", fontSize=7.5, leading=11,
        textColor=MID, alignment=TA_CENTER, spaceAfter=8,
    )
    closing_style = ParagraphStyle(
        "Closing", fontName="Times-Italic", fontSize=9, leading=14,
        textColor=GOLD, alignment=TA_CENTER, spaceBefore=18, spaceAfter=6,
    )

    elements = []
    elements.append(Paragraph(
        "Rate each statement from <b>1</b> (not at all) to <b>10</b> (fully / always).",
        intro_style
    ))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=GOLD, spaceAfter=10))

    for pillar, questions in PILLARS:
        block = []
        block.append(Paragraph(pillar, pillar_style))
        block.append(HRFlowable(width="100%", thickness=0.3, color=BAND1, spaceAfter=5))
        for q_num, q_text in enumerate(questions, 1):
            block.append(Paragraph(f"{q_num}.  {q_text}", q_style))
            block.append(Spacer(1, 3))
            block.append(scale_row())
            block.append(Spacer(1, 6))
        elements.append(KeepTogether(block[:5]))
        for item in block[5:]:
            elements.append(item)

    elements.append(HRFlowable(width="100%", thickness=0.5, color=GOLD, spaceBefore=12, spaceAfter=0))
    elements.append(Paragraph(CLOSING, closing_style))

    doc.build(elements, onFirstPage=on_every_page, onLaterPages=on_every_page)
    print(f"PDF written to: {out_path}")


if __name__ == "__main__":
    build()
