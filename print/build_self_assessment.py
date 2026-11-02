"""Generates print/self-assessment.html (dark + light themes via #light / #dark)."""
from pathlib import Path

PILLARS = [
    ("01", "Truth", "The Foundation: Confronting Reality", [
        ("How honest are you with yourself about where you truly are — in your performance, your relationships, and your inner life?", "Avoiding reality", "Radically honest"),
        ("To what degree are you aware of the patterns, beliefs, and blind spots that influence your decisions and behavior?", "Largely unaware", "Deeply self-aware"),
        ("How willing are you to confront uncomfortable truths about yourself rather than maintain a more comfortable narrative?", "Highly avoidant", "Fully willing"),
    ]),
    ("02", "Connection", "Emotional &amp; Relational Intelligence", [
        ("How connected do you feel to yourself — your emotions, your needs, your inner experience?", "Disconnected", "Deeply in tune"),
        ("How would you rate the quality and depth of your most important relationships?", "Surface-level or strained", "Genuine and nourishing"),
        ("How effectively do you communicate, set boundaries, and show up relationally, including in professional contexts?", "Significant struggle", "Consistently strong"),
    ]),
    ("03", "Being", "The Art of Embodiment", [
        ("How present are you in your daily life — or are you mostly operating on autopilot, in your head, or focused on what’s next?", "Rarely present", "Consistently grounded"),
        ("How regulated does your nervous system feel on a day-to-day basis?", "Frequently dysregulated", "Calm and resourced"),
        ("How well do you listen to and care for your physical body on a daily basis?", "Largely ignored", "Fully integrated"),
    ]),
    ("04", "Vision", "The Blueprint of Excellence", [
        ("How clear is your sense of purpose and long-term direction?", "Unclear or undefined", "Deeply clear"),
        ("How aligned are your current goals and daily actions with your deepest values?", "Significant misalignment", "Fully aligned"),
        ("How intentionally are you building your life — or are you reacting to circumstances rather than designing your path?", "Reactive", "Highly intentional"),
    ]),
    ("05", "Meaning", "The Core of Fulfillment", [
        ("How meaningful does your work feel to you — beyond titles, recognition, and external achievement?", "Largely hollow", "Deeply fulfilling"),
        ("How connected are your external accomplishments to a genuine sense of internal satisfaction?", "Disconnected", "Fully integrated"),
        ("How clearly can you articulate what makes your life and work feel worthwhile?", "Unclear", "Very clear"),
    ]),
    ("06", "Creation", "The Execution of Mastery", [
        ("How effectively are you translating your vision and insight into deliberate, consistent action?", "Significant gap between knowing and doing", "Executing with discipline"),
        ("How often are you moving forward with clarity — rather than holding back, procrastinating, or staying in planning mode?", "Frequently stuck", "Moving with clarity and momentum"),
        ("How well do you feel you convert your potential into reality — turning what you’re capable of into what you actually produce?", "Significant underperformance", "Fully actualized"),
    ]),
    ("→", "Excellence", "The Embodiment of Greatness", [
        ("How willing are you to change aspects of yourself in pursuit of greatness?", "Resistant to change", "Fully willing"),
        ("How committed are you to the continuous refinement of yourself — not just your skills, but who you are?", "Not a priority", "Deeply committed"),
        ("Looking across all of the pillars, how cohesively are they working together in your life right now?", "Fragmented", "Fully integrated"),
    ]),
]

# Which pillars go on which page (index into PILLARS); page 1 also carries the intro.
LAYOUT = [[0, 1], [2, 3, 4], [5, 6]]
TOTAL_PAGES = len(LAYOUT)


def scale():
    return '<div class="scale">' + "".join(f"<span>{n}</span>" for n in range(1, 11)) + "</div>"


def pillar(num, name, sub, qs):
    out = [f'<section class="pillar">\n  <div class="ph"><div class="num">{num}</div>'
           f'<div class="pt"><h2>{name}</h2><div class="label">{sub}</div></div>'
           f'<div class="score"><span class="label">Score</span><span class="box"></span><span class="of">/ 30</span></div></div>']
    for i, (q, lo, hi) in enumerate(qs, 1):
        out.append(f'''  <div class="q">
    <div class="qn">{i}</div>
    <div class="qb">
      <p>{q}</p>
      <div class="srow-q"><span class="lo">{lo}</span>{scale()}<span class="hi">{hi}</span></div>
    </div>
  </div>''')
    out.append('</section>')
    return "\n".join(out)


def footer(n):
    return (f'<footer><span>Architecture of Excellence™ © 2026 Dr. Alina K. Schulhofer. All rights reserved. '
            f'Proprietary material — not for reproduction or distribution.</span><span class="pg">{n:02d} / {TOTAL_PAGES:02d}</span></footer>')


def runhead():
    return ('<div class="runhead"><span class="logo-sm"><img class="on-dark" src="aoe-logo.svg" alt="aoe">'
            '<img class="on-light" src="aoe-logo-dark.svg" alt="aoe"></span><span class="label">Self-Assessment</span></div>')


pages = []
for pi, idxs in enumerate(LAYOUT, 1):
    body = []
    if pi == 1:
        body.append('''<header>
    <h1><span class="dim">Self-</span><br>Assessment.</h1>
    <div class="logo"><img class="on-dark" src="aoe-logo.svg" alt="aoe"><img class="on-light" src="aoe-logo-dark.svg" alt="aoe"><span>ARCHITECTURE OF EXCELLENCE™</span></div>
  </header>
  <div class="intro">
    <p class="lead">A reflective inventory across the pillars of the Architecture of Excellence™ framework.</p>
    <p>Rate each statement from <strong>1</strong> (not at all) to <strong>10</strong> (fully / always) by circling the number that best reflects where you are today. There are no right or wrong answers — the value of this exercise lies in honest reflection.</p>
  </div>''')
    else:
        body.append(runhead())
    for k in idxs:
        body.append(pillar(*PILLARS[k]))
    if pi == TOTAL_PAGES:
        rows = "".join(f'<div class="srow"><span class="sn">{p[0]}</span><span class="sname">{p[1]}</span><span class="box"></span><span class="of">/ 30</span></div>' for p in PILLARS)
        body.append(f'''<section class="summary">
    <h2 class="sec"><span class="dim">Score</span> Summary.</h2>
    <div class="sgrid">
      <div class="stable">{rows}<div class="srow total"><span class="sn"></span><span class="sname">Total</span><span class="box"></span><span class="of">/ 210</span></div></div>
      <div class="reflect">
        <div class="label">Reflection</div>
        <p>Take some time to reflect and journal on your answers and consider which areas may represent continued areas for growth.</p>
        <div class="lines"><i></i><i></i><i></i><i></i><i></i></div>
      </div>
    </div>
  </section>''')
    body.append(footer(pi))
    pages.append('<section class="page">\n  ' + "\n  ".join(body) + "\n</section>")

CSS = Path(__file__).with_name("self-assessment.css").read_text()
html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Self-Assessment — Architecture of Excellence™</title>
<link rel="stylesheet" href="fonts/fonts.css">
<script>document.documentElement.dataset.theme = location.hash === '#light' ? 'light' : 'dark';</script>
<style>
{CSS}
</style>
</head>
<body>
{chr(10).join(pages)}
</body>
</html>
'''
Path(__file__).with_name("self-assessment.html").write_text(html)
print("wrote self-assessment.html")
