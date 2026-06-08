"""
Build AoE Self Assessment PDF — 2 pages:
  Page 1: AoE Wheel SVG rendered as vector graphics
  Page 2: 21 self-assessment questions (3 per pillar)
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, String, Circle, Line, Rect, Path, PolyLine
from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor, Color, black, white
import math, os

# ── COLOURS ────────────────────────────────────────────────────────────────────────────
GOLD   = HexColor("#B8952A")
DARK   = HexColor("#2C2C2C")
INK    = HexColor("#3B3835")
CREAM  = HexColor("#F7F3EC")
CREAM2 = HexColor("#EDE8DF")
CREAM3 = HexColor("#F2EDE4")
BAND1  = HexColor("#E6DFD2")
BAND2  = HexColor("#EBE4D7")
MID    = HexColor("#9A8A72")

W, H = letter  # 612 x 792 pt

# ── QUESTIONS ──────────────────────────────────────────────────────────────────────────
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

# ── PAGE 1: WHEEL ─────────────────────────────────────────────────────────────────────
def draw_wheel_page(c, doc):
    """Draw the AoE wheel directly onto the canvas."""
    c.saveState()

    margin = 40
    page_w, page_h = W, H

    # Background
    c.setFillColor(CREAM)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    # Title
    c.setFillColor(GOLD)
    c.setFont("Times-Roman", 11)
    title = "THE 7-PILLAR FRAMEWORK"
    tw = c.stringWidth(title, "Times-Roman", 11)
    tx = page_w / 2
    ty = page_h - 54
    c.drawCentredString(tx, ty, title)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.line(tx - tw/2, ty - 2, tx + tw/2, ty - 2)

    # Wheel parameters
    cx, cy = page_w / 2, page_h / 2 - 10
    outer_r = 230
    band_r  = 270
    inner_r = 62

    n = 7
    seg_angle = 2 * math.pi / n
    start_offset = -math.pi / 2 - seg_angle / 2

    def polar(r, angle):
        return cx + r * math.cos(angle), cy + r * math.sin(angle)

    boundaries = [start_offset + i * seg_angle for i in range(n + 1)]
    mid_angles = [start_offset + (i + 0.5) * seg_angle for i in range(n)]
    seg_fills = [CREAM2, CREAM3] * 4

    # Draw segments
    for i in range(n):
        a0, a1 = boundaries[i], boundaries[i + 1]
        ix0, iy0 = polar(inner_r, a0)
        ox0, oy0 = polar(outer_r, a0)
        ix1, iy1 = polar(inner_r, a1)
        p = c.beginPath()
        p.moveTo(ix0, iy0)
        p.lineTo(ox0, oy0)
        steps = 40
        for k in range(1, steps + 1):
            t = a0 + (a1 - a0) * k / steps
            p.lineTo(cx + outer_r * math.cos(t), cy + outer_r * math.sin(t))
        ox1, oy1 = polar(outer_r, a1)
        p.lineTo(ix1, iy1)
        for k in range(1, steps + 1):
            t = a1 + (a0 - a1) * k / steps
            p.lineTo(cx + inner_r * math.cos(t), cy + inner_r * math.sin(t))
        p.close()
        c.setFillColor(seg_fills[i])
        c.setLineWidth(0)
        c.drawPath(p, fill=1, stroke=0)

    # Label band fills
    band_fills = [BAND1, BAND2] * 4
    for i in range(n):
        a0, a1 = boundaries[i], boundaries[i + 1]
        ox0, oy0 = polar(outer_r, a0)
        bx0, by0 = polar(band_r, a0)
        ox1, oy1 = polar(outer_r, a1)
        p = c.beginPath()
        p.moveTo(ox0, oy0)
        p.lineTo(bx0, by0)
        steps = 40
        for k in range(1, steps + 1):
            t = a0 + (a1 - a0) * k / steps
            p.lineTo(cx + band_r * math.cos(t), cy + band_r * math.sin(t))
        p.lineTo(ox1, oy1)
        for k in range(1, steps + 1):
            t = a1 + (a0 - a1) * k / steps
            p.lineTo(cx + outer_r * math.cos(t), cy + outer_r * math.sin(t))
        p.close()
        c.setFillColor(band_fills[i])
        c.drawPath(p, fill=1, stroke=0)

    # Dividing lines
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.0)
    for a in boundaries[:-1]:
        xi, yi = polar(inner_r, a)
        xo, yo = polar(band_r, a)
        c.line(xi, yi, xo, yo)

    # Circles
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.6)
    c.circle(cx, cy, band_r, fill=0, stroke=1)
    c.setLineWidth(1.1)
    c.circle(cx, cy, outer_r, fill=0, stroke=1)
    c.setLineWidth(1.4)
    c.setFillColor(CREAM)
    c.circle(cx, cy, inner_r, fill=1, stroke=1)

    # Pillar labels
    label_r = (outer_r + band_r) / 2
    for i, (name, _) in enumerate(PILLARS):
        a_mid = mid_angles[i]
        tangent_deg = math.degrees(a_mid) + 90
        norm = a_mid % (2 * math.pi)
        if math.pi / 2 < norm < 3 * math.pi / 2:
            tangent_deg += 180
        lx, ly = polar(label_r, a_mid)
        font_size = 7.5
        c.saveState()
        c.translate(lx, ly)
        c.rotate(tangent_deg)
        c.setFont("Times-Roman", font_size)
        c.setFillColor(DARK)
        c.drawCentredString(0, -font_size * 0.35, name)
        c.restoreState()

    # Center AoE triangle mark
    svg_scale = outer_r / 300.0
    svg_cx, svg_cy = 500, 500

    def svg_to_pdf(sx, sy):
        return cx + (sx - svg_cx) * svg_scale, cy - (sy - svg_cy) * svg_scale

    c.setFillColor(INK)
    p = c.beginPath()
    pts_outer = [(500, 456), (465, 518), (535, 518)]
    pts_inner = [(500, 466), (478, 520), (522, 520)]
    x0, y0 = svg_to_pdf(*pts_outer[0])
    p.moveTo(x0, y0)
    for pt in pts_outer[1:]:
        p.lineTo(*svg_to_pdf(*pt))
    p.close()
    xi0, yi0 = svg_to_pdf(*pts_inner[0])
    p.moveTo(xi0, yi0)
    for pt in pts_inner[1:]:
        p.lineTo(*svg_to_pdf(*pt))
    p.close()
    c.drawPath(p, fill=1, stroke=0, fillMode=1)

    bar_x, bar_y_bottom = svg_to_pdf(458, 529)
    bar_x2, _ = svg_to_pdf(542, 529)
    _, bar_y_top = svg_to_pdf(458, 519)
    c.rect(bar_x, bar_y_bottom, bar_x2 - bar_x, bar_y_top - bar_y_bottom, fill=1, stroke=0)

    # Copyright
    c.setFillColor(MID)
    c.setFont("Times-Roman", 7)
    c.drawCentredString(page_w / 2, 30, "© 2026 Dr. Alina K. Schulhofer. All rights reserved.")

    c.restoreState()


# ── PAGE 2: QUESTIONS ─────────────────────────────────────────────────────────────────────
def build_questions_page(elements, styles):
    title_style = ParagraphStyle(
        "Title", fontName="Times-Roman", fontSize=20, leading=26,
        textColor=DARK, alignment=TA_CENTER, spaceAfter=4,
    )
    sub_style = ParagraphStyle(
        "Sub", fontName="Times-Roman", fontSize=9, leading=13,
        textColor=MID, alignment=TA_CENTER, spaceAfter=0,
    )
    pillar_style = ParagraphStyle(
        "Pillar", fontName="Times-Bold", fontSize=8, leading=11,
        textColor=GOLD, spaceBefore=10, spaceAfter=3,
    )
    q_style = ParagraphStyle(
        "Q", fontName="Times-Roman", fontSize=8, leading=11,
        textColor=DARK, spaceAfter=2, leftIndent=12,
    )
    instruction_style = ParagraphStyle(
        "Instr", fontName="Times-Italic", fontSize=7.5, leading=10,
        textColor=MID, spaceAfter=3, leftIndent=12,
    )
    scale_style = ParagraphStyle(
        "Scale", fontName="Times-Roman", fontSize=7, leading=10,
        textColor=MID, alignment=TA_CENTER, spaceAfter=6,
    )

    elements.append(Paragraph("AoE Self Assessment", title_style))
    elements.append(Paragraph(
        "Architecture of Excellence™  ·  Dr. Alina K. Schulhofer", sub_style
    ))
    elements.append(Spacer(1, 6))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=GOLD, spaceAfter=8))
    elements.append(Paragraph(
        "Rate each statement from <b>1</b> (not at all) to <b>10</b> (fully/always). "
        "Use the reflection lines to capture any thoughts or insights.",
        scale_style
    ))

    def scale_row():
        data = [
            [Paragraph(f"<b>{n}</b>", ParagraphStyle("nb", fontName="Times-Bold",
                fontSize=7, alignment=TA_CENTER, textColor=DARK))
             for n in range(1, 11)]
        ]
        t = Table(data, colWidths=[18]*10, rowHeights=[12])
        t.setStyle(TableStyle([
            ("BOX",       (0, 0), (-1, -1), 0.4, GOLD),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, GOLD),
            ("VALIGN",    (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN",     (0, 0), (-1, -1), "CENTER"),
            ("BACKGROUND",(0, 0), (-1, -1), HexColor("#FAF7F2")),
        ]))
        return t

    def reflection_lines():
        return [
            HRFlowable(width="100%", thickness=0.3, color=HexColor("#D4CEC4"), spaceAfter=5)
            for _ in range(2)
        ]

    for pillar, questions in PILLARS:
        block = []
        block.append(Paragraph(pillar, pillar_style))
        block.append(HRFlowable(width="100%", thickness=0.3, color=BAND1, spaceAfter=4))
        for q_num, q_text in enumerate(questions, 1):
            block.append(Paragraph(f"{q_num}. {q_text}", q_style))
            block.append(Spacer(1, 2))
            block.append(scale_row())
            block.append(Paragraph("Reflection:", instruction_style))
            block.extend(reflection_lines())
            block.append(Spacer(1, 2))
        elements.append(KeepTogether(block[:6]))
        for item in block[6:]:
            elements.append(item)


# ── MAIN ──────────────────────────────────────────────────────────────────────────────
def build():
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "aoe-self-assessment.pdf")
    from reportlab.pdfgen.canvas import Canvas
    import tempfile

    c = Canvas(out_path, pagesize=letter)
    draw_wheel_page(c, None)
    c.showPage()

    tmp = tempfile.mktemp(suffix=".pdf")
    doc = SimpleDocTemplate(
        tmp, pagesize=letter,
        leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=30,
    )
    elements = []
    build_questions_page(elements, getSampleStyleSheet())
    doc.build(elements)

    from PyPDF2 import PdfReader, PdfWriter
    c.save()
    writer = PdfWriter()
    for pg in PdfReader(out_path).pages:
        writer.add_page(pg)
    for pg in PdfReader(tmp).pages:
        writer.add_page(pg)
    with open(out_path, "wb") as f:
        writer.write(f)
    os.remove(tmp)
    print(f"PDF written to: {out_path}")


if __name__ == "__main__":
    build()
