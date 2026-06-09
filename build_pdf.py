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

# Each question is (question_text, scale_descriptor)
PILLARS = [
    ("TRUTH — The Foundation: Confronting Reality", [
        ("How honest are you with yourself about where you truly are — in your performance, your relationships, and your inner life?",
         "1 = avoiding reality  ·  10 = radically honest"),
        ("To what degree do you believe you are aware of the patterns, beliefs, and blind spots that influence your decisions and behavior?",
         "1 = largely unaware  ·  10 = deeply self-aware"),
        ("How willing are you to confront uncomfortable truths about yourself rather than maintaining a more comfortable narrative?",
         "1 = highly avoidant  ·  10 = fully willing"),
    ]),
    ("CONNECTION — Emotional & Relational Intelligence", [
        ("How connected do you feel to yourself — your emotions, your needs, your inner experience?",
         "1 = disconnected  ·  10 = deeply in tune"),
        ("How would you rate the quality and depth of your most important relationships?",
         "1 = surface-level or strained  ·  10 = genuine and nourishing"),
        ("How effectively do you communicate, set boundaries, and show up relationally, including in professional contexts?",
         "1 = significant struggle  ·  10 = consistently strong"),
    ]),
    ("BEING — The Art of Embodiment", [
        ("How present are you in your daily life — or are you mostly operating on autopilot, in your head, or focused on what's next?",
         "1 = rarely present  ·  10 = consistently grounded"),
        ("How regulated does your nervous system feel on a day-to-day basis?",
         "1 = frequently dysregulated / overwhelmed  ·  10 = calm and resourced"),
        ("How well do you listen to and care for your physical body on a daily basis?",
         "1 = largely ignored  ·  10 = fully integrated"),
    ]),
    ("VISION — The Blueprint of Excellence", [
        ("How clear is your sense of purpose and long-term direction?",
         "1 = unclear or undefined  ·  10 = deeply clear"),
        ("How aligned are your current goals and daily actions with your deepest values?",
         "1 = significant misalignment  ·  10 = fully aligned"),
        ("How intentionally are you building your life — or are you reacting to circumstances rather than designing your path?",
         "1 = reactive  ·  10 = highly intentional"),
    ]),
    ("MEANING — The Core of Fulfillment", [
        ("How meaningful does your work feel to you — beyond titles, recognition, and external achievement?",
         "1 = largely hollow  ·  10 = deeply fulfilling"),
        ("How connected are your external accomplishments to a genuine sense of internal satisfaction?",
         "1 = disconnected  ·  10 = fully integrated"),
        ("How clearly can you articulate what makes your life and work feel worthwhile?",
         "1 = unclear  ·  10 = very clear"),
    ]),
    ("CREATION — The Execution of Mastery", [
        ("How effectively are you translating your vision and insight into deliberate, consistent action?",
         "1 = significant gap between knowing and doing  ·  10 = executing with discipline"),
        ("How frequently in your life are you holding back, procrastinating, or staying in planning mode rather than actively building?",
         "1 = frequently stuck  ·  10 = moving with clarity and momentum"),
        ("How well do feel you convert your potential into reality — turning what you're capable of into what you actually produce?",
         "1 = significant underperformance  ·  10 = fully actualized"),
    ]),
    ("EXCELLENCE — The Embodiment of Greatness", [
        ("How willing are you to change aspects of yourself to pursue greatness?",
         ""),
        ("How committed are you to the continuous refinement of yourself — not just your skills, but who you are?",
         "1 = not a priority  ·  10 = deeply committed"),
        ("Looking across all seven pillars, how cohesively are they working together in your life right now?",
         "1 = fragmented  ·  10 = fully integrated"),
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
    canvas.saveState()
    page_w, page_h = W, H
    margin = 36

    canvas.setFillColor(GOLD)
    canvas.setFont("Times-Roman", 18)
    canvas.drawCentredString(page_w / 2, page_h - 50, "AoE Self Assessment")

    logo_x = page_w - margin - 70
    logo_y = page_h - 62
    if os.path.exists(LOGO_PATH):
        canvas.drawImage(LOGO_PATH, logo_x, logo_y, width=70, height=28,
                         preserveAspectRatio=True, mask="auto")

    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.5)
    canvas.line(margin, page_h - 66, page_w - margin, page_h - 66)

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
        topMargin=80, bottomMargin=52,
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
    desc_style = ParagraphStyle(
        "Desc", fontName="Times-Italic", fontSize=7, leading=9,
        textColor=MID, spaceAfter=2, leftIndent=12,
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
        for q_num, (q_text, q_desc) in enumerate(questions, 1):
            block.append(Paragraph(f"{q_num}.  {q_text}", q_style))
            if q_desc:
                block.append(Paragraph(q_desc, desc_style))
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
