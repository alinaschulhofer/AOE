"""Generates institutional.html — the AOE Institutional Framework brochure.

Copy is taken from the master document "AOE Institutional Competency Framework &
Implementation Methodology". Diagrams are inline SVG, themed via CSS variables
(dark by default, light with #light). Run:  python3 build.py && node render.js
"""
from math import cos, sin, radians, asin, degrees
from pathlib import Path

HERE = Path(__file__).parent
TOTAL = 14


def f(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")


def pol(cx, cy, r, a):
    return cx + r * cos(radians(a)), cy + r * sin(radians(a))


def tlines(x, y, lines, cls, lh, anchor="middle"):
    """Multi-line SVG text, vertically centred on y."""
    y0 = y - (len(lines) - 1) * lh / 2
    spans = "".join(f'<tspan x="{f(x)}" y="{f(y0 + i * lh)}">{t}</tspan>' for i, t in enumerate(lines))
    return f'<text class="{cls}" text-anchor="{anchor}" dominant-baseline="central">{spans}</text>'


MARKERS = """<defs>
  <marker id="{id}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path class="ah" d="M1,1.2 L9,5 L1,8.8"/>
  </marker>
</defs>"""


# ---------------------------------------------------------------- Diagram A
def diagram_a():
    cx = cy = 200
    radii = [56, 104, 152, 198]
    names = ["RELATIONAL &amp; TEAM", "ORGANIZATIONAL", "BROADER SYSTEMS"]
    o = [f'<svg class="dg" id="diagram-a-ecological-systems" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">',
         MARKERS.format(id="ma")]
    for i, r in enumerate(reversed(radii)):
        o.append(f'<circle class="{"band" if i % 2 == 0 else "bg"}" cx="{cx}" cy="{cy}" r="{r}"/>')
    for r in radii:
        o.append(f'<circle class="ring{" dash" if r == radii[-1] else ""}" cx="{cx}" cy="{cy}" r="{r}"/>')
    for k, n in enumerate(names):
        m = (radii[k] + radii[k + 1]) / 2
        o.append(f'<text class="lv" x="{cx}" y="{f(cy - m)}" text-anchor="middle" dominant-baseline="central">{n}</text>')
    o.append(f'<text class="lv core" x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="central">INDIVIDUAL</text>')
    # a reciprocal pair of arrows across each of the three boundaries, on the two lower diagonals
    for th in (45, 135):
        u = (cos(radians(th)), sin(radians(th)))
        n = (-u[1], u[0])
        for r in radii[:3]:
            for s, (r1, r2) in ((4.5, (r - 15, r + 15)), (-4.5, (r + 15, r - 15))):
                x1, y1 = cx + u[0] * r1 + n[0] * s, cy + u[1] * r1 + n[1] * s
                x2, y2 = cx + u[0] * r2 + n[0] * s, cy + u[1] * r2 + n[1] * s
                o.append(f'<line class="arw" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" marker-end="url(#ma)"/>')
    o.append("</svg>")
    return "\n".join(o)


# ---------------------------------------------------------------- Diagram B
PILLAR_NAMES = ["Truth", "Connection", "Being", "Vision", "Meaning", "Creation"]


def diagram_b():
    o = ['<svg class="dg temple" id="diagram-b-pillar-model" viewBox="0 0 820 520" xmlns="http://www.w3.org/2000/svg">',
         '<polygon class="t-ln" points="20,118 410,14 800,118"/>',
         '<text class="t-ex" x="410" y="92" text-anchor="middle">EXCELLENCE</text>',
         '<line class="t-ln" x1="60" y1="136" x2="760" y2="136"/>']
    xs = [62 + k * 122 + 43 for k in range(6)]
    # interdependence: each pillar linked to its neighbours and, more faintly, to every other pillar
    for i in range(6):
        for j in range(i + 1, 6):
            if j - i == 1:
                continue
            mid = (xs[i] + xs[j]) / 2
            o.append(f'<path class="t-link faint" d="M{xs[i]},158 Q{mid},{158 - 6 - 3 * (j - i)} {xs[j]},158"/>')
    for i in range(5):
        mid = (xs[i] + xs[i + 1]) / 2
        o.append(f'<path class="t-link" d="M{xs[i]},158 Q{mid},144 {xs[i + 1]},158"/>')
    for k, name in enumerate(PILLAR_NAMES):
        x = 62 + k * 122
        o.append(f'<rect class="t-col" x="{x}" y="172" width="86" height="276"/>')
        o.append(f'<line class="t-tie" x1="{x + 43}" y1="158" x2="{x + 43}" y2="172"/>')
        o.append(f'<circle class="t-node" cx="{x + 43}" cy="158" r="3.2"/>')
        o.append(f'<text class="t-cn" x="{x + 43}" y="198" text-anchor="middle">0{k + 1}</text>')
        o.append(f'<text class="t-vl" transform="translate({x + 48},330) rotate(-90)" text-anchor="middle">{name.upper()}</text>')
    o += ['<rect class="t-band" x="20" y="460" width="780" height="44"/>',
          '<text class="t-base" x="410" y="487" text-anchor="middle">ARCHITECTURE OF EXCELLENCE</text>',
          '</svg>']
    return "\n".join(o)


# ---------------------------------------------------------------- Diagram C
CORE2 = [["Self-Awareness, Integrity", "&amp; Accountability"], ["Emotional &amp; Relational", "Intelligence"],
         ["Presence &amp; Self-Regulation"], ["Purposeful Direction", "&amp; Strategic Alignment"],
         ["Purpose, Fulfillment", "&amp; Meaningful Engagement"], ["Intentional Action", "&amp; Continuous Development"]]
SUB_NAMES = [
    ["Self-Awareness", "Psychological Insight", "Integrity", "Accountability", "Openness to Feedback"],
    ["Emotional Intelligence", "Relational Intelligence", "Effective Communication", "Conflict Navigation", "Trust &amp; Collaboration"],
    ["Self-Regulation", "Present-Moment Awareness", "Mind-Body Awareness", "Psychological Flexibility", "Stress Management"],
    ["Vision Development", "Strategic Thinking", "Values Alignment", "Intentional Decision-Making", "Shared Direction"],
    ["Purpose Awareness", "Intrinsic Motivation", "Values-Based Engagement", "Identity &amp; Fulfillment", "Belonging &amp; Contribution"],
    ["Personal Agency", "Intentional Action", "Discipline &amp; Follow-Through", "Adaptability", "Continuous Learning"],
]


def diagram_c():
    W, top, rh = 678, 30, 101
    xc, xs = 196, 450
    H = top + 6 * rh + 2
    o = [f'<svg class="dg" id="diagram-c-competency-framework" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
         MARKERS.format(id="mc")]
    for x, t in ((0, "PILLAR"), (xc, "CORE COMPETENCY"), (xs, "CORE SUBCOMPETENCIES")):
        o.append(f'<text class="phl" x="{x}" y="10" dominant-baseline="central">{t}</text>')
    o.append(f'<line class="rule" x1="0" y1="{top - .5}" x2="{W}" y2="{top - .5}"/>')
    for k in range(6):
        y = top + k * rh
        m = y + rh / 2
        if k % 2 == 0:
            o.append(f'<rect class="rowband" x="0" y="{y}" width="{W}" height="{rh}"/>')
        o.append(f'<circle class="numc" cx="18" cy="{m}" r="17"/>')
        o.append(f'<text class="numt" x="18" y="{m}" text-anchor="middle" dominant-baseline="central">0{k + 1}</text>')
        o.append(f'<text class="rname" x="50" y="{m}" dominant-baseline="central">{PILLAR_NAMES[k]}</text>')
        o.append(tlines(xc, m, CORE2[k], "rcore", 17, "start"))
        o.append(f'<line class="arw soft" x1="{xs - 46}" y1="{m}" x2="{xs - 18}" y2="{m}" marker-end="url(#mc)"/>')
        for j, t in enumerate(SUB_NAMES[k]):
            yy = m + (j - 2) * 17.5
            o.append(f'<line class="rule" x1="{xs}" y1="{f(yy)}" x2="{xs + 6}" y2="{f(yy)}"/>')
            o.append(f'<text class="rsub" x="{xs + 14}" y="{f(yy)}" dominant-baseline="central">{t}</text>')
        o.append(f'<line class="rule faint" x1="0" y1="{y + rh - .5}" x2="{W}" y2="{y + rh - .5}"/>')
    o.append("</svg>")
    return "\n".join(o)


# ---------------------------------------------------------------- Diagram D
PHASES = ["Discovery &amp; Assessment", "Strategic Design", "Implementation &amp; Development",
          "Evaluation &amp; Refinement", "Integration &amp; Sustainability"]
PHASE_LINES = [["Discovery &amp;", "Assessment"], ["Strategic", "Design"], ["Implementation &amp;", "Development"],
               ["Evaluation &amp;", "Refinement"], ["Integration &amp;", "Sustainability"]]


def diagram_d():
    W, H = 678, 420
    cx, cy, R, nr, cr = 339, 214, 146, 29, 66
    o = [f'<svg class="dg" id="diagram-d-institutional-methodology" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
         MARKERS.format(id="md")]
    angs = [-90 + k * 72 for k in range(5)]
    d = degrees(asin((nr + 9) / R)) * 2
    o.append(f'<circle class="ring faint" cx="{cx}" cy="{cy}" r="{R + 20}"/>')
    # progression 01 → 05 and back to 01 (iterative cycle)
    for k in range(5):
        a1, a2 = angs[k] + d / 2 + 1, angs[k] + 72 - d / 2 - 1
        x1, y1 = pol(cx, cy, R, a1)
        x2, y2 = pol(cx, cy, R, a2)
        o.append(f'<path class="arc" d="M{f(x1)},{f(y1)} A{R},{R} 0 0 1 {f(x2)},{f(y2)}" marker-end="url(#md)"/>')
    # continuous monitoring & learning: two-way feedback between the centre and every phase
    for k in range(5):
        x1, y1 = pol(cx, cy, cr + 8, angs[k])
        x2, y2 = pol(cx, cy, R - nr - 8, angs[k])
        o.append(f'<line class="spoke" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" marker-start="url(#md)" marker-end="url(#md)"/>')
    o.append(f'<circle class="core-bg" cx="{cx}" cy="{cy}" r="{cr}"/>')
    o.append(f'<circle class="core" cx="{cx}" cy="{cy}" r="{cr}"/>')
    o.append(tlines(cx, cy, ["CONTINUOUS", "MONITORING", "&amp; LEARNING"], "exm", 14))
    pos = [("middle", 0, -52), ("start", 44, 0), ("start", 34, 30), ("end", -34, 30), ("end", -44, 0)]
    for k in range(5):
        x, y = pol(cx, cy, R, angs[k])
        o.append(f'<circle class="node" cx="{f(x)}" cy="{f(y)}" r="{nr}"/>')
        o.append(f'<text class="numt big" x="{f(x)}" y="{f(y)}" text-anchor="middle" dominant-baseline="central">0{k + 1}</text>')
        an, dx, dy = pos[k]
        o.append(f'<text class="phl" x="{f(x + dx)}" y="{f(y + dy - 18)}" text-anchor="{an}" dominant-baseline="central">PHASE 0{k + 1}</text>')
        o.append(tlines(x + dx, y + dy + 4, PHASE_LINES[k], "phn", 16, an))
    o.append("</svg>")
    return "\n".join(o)


# ---------------------------------------------------------------- Diagram E
def diagram_e():
    cx = cy = 170
    names = [["Education &amp; Development", "of Core Competencies"], ["Leadership &amp;", "Individual Development"],
             ["Team &amp; Relational", "Development"], ["Organizational", "Development &amp; Culture"],
             ["System-Wide", "Development &amp; Integration"]]
    o = ['<svg class="dg" id="diagram-e-institutional-applications" viewBox="-170 -46 680 420" xmlns="http://www.w3.org/2000/svg">']
    o.append(f'<circle class="ring dash" cx="{cx}" cy="{cy}" r="160"/>')
    for k in range(5):
        x, y = pol(cx, cy, 82, -90 + k * 72)
        o.append(f'<circle class="petal" cx="{f(x)}" cy="{f(y)}" r="62"/>')
    for k in range(5):
        x, y = pol(cx, cy, 82, -90 + k * 72)
        o.append(f'<circle class="petal-line" cx="{f(x)}" cy="{f(y)}" r="62"/>')
    for k in range(5):
        x, y = pol(cx, cy, 112, -90 + k * 72)
        o.append(f'<text class="numt big" x="{f(x)}" y="{f(y)}" text-anchor="middle" dominant-baseline="central">0{k + 1}</text>')
        a = -90 + k * 72
        lx, ly = pol(cx, cy, 182, a)
        anchor = "middle" if k == 0 else ("start" if k in (1, 2) else "end")
        if k == 0:
            ly -= 6
        if k in (2, 3):
            ly += 8
        o.append(tlines(lx, ly, names[k], "phn", 17, anchor))
    o.append(f'<circle class="core-bg" cx="{cx}" cy="{cy}" r="46"/>')
    o.append(f'<circle class="core" cx="{cx}" cy="{cy}" r="46"/>')
    o.append(tlines(cx, cy, ["ASSESSMENT", "&amp; STRATEGIC", "DESIGN"], "exm", 12))
    o.append("</svg>")
    return "\n".join(o)

# ---------------------------------------------------------------- Diagram F (levels)
def diagram_f():
    W, H, base, gap = 678, 236, 228, 8
    w = (W - 3 * gap) / 4
    o = [f'<svg class="dg" id="diagram-f-developmental-pathway" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    names = [["Foundational", "Education"], ["Competency", "Development"], ["Institutional", "Integration"], ["Institutional Standards", "&amp; Certification"]]
    for i in range(4):
        h = 92 + i * 44
        x, y = i * (w + gap), base - h
        cls = "step dash" if i == 3 else "step"
        o.append(f'<rect class="{cls}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{h}"/>')
        o.append(f'<text class="phl" x="{f(x + 16)}" y="{f(y + 22)}" dominant-baseline="central">LEVEL {i + 1}</text>')
        o.append(tlines(x + 16, y + 52, names[i], "phn", 17, "start"))
        if i == 3:
            o.append(tlines(x + 16, base - 26, ["PROPOSED", "FUTURE PATHWAY"], "lp", 13, "start"))
    o.append(f'<line class="rule" x1="0" y1="{base + .5}" x2="{W}" y2="{base + .5}"/>')
    o.append("</svg>")
    return "\n".join(o)


# ---------------------------------------------------------------- Content
PILLARS = [
    dict(n="01", name="Truth", core="Self-Awareness, Integrity &amp; Accountability", tag="The Foundation: Confronting Reality",
         intro=["Truth involves the capacity to recognize and engage with reality honestly, including aspects of ourselves, our relationships, and our organizations that may be uncomfortable or difficult to acknowledge."],
         subs=[("Self-Awareness", "Recognizing one’s thoughts, emotions, motivations, behaviors, and their impact on others."),
               ("Psychological Insight", "Understanding patterns, assumptions, biases, and underlying influences that shape behavior and decision-making."),
               ("Integrity", "Acting consistently with stated values and ethical principles."),
               ("Accountability", "Taking responsibility for decisions, actions, and their consequences."),
               ("Openness to Feedback", "Demonstrating the willingness to question assumptions, receive feedback, and confront uncomfortable information.")],
         app="Organizations demonstrate Truth through transparent communication, ethical leadership, meaningful accountability, openness to feedback, and the willingness to identify and address organizational problems.",
         ex=["Leadership reflection and development processes.", "Structured feedback and organizational assessment.",
             "Transparent decision-making and accountability mechanisms.", "Regular evaluation of alignment between organizational values and actual practices.",
             "Accessible processes for raising concerns and addressing problems."]),
    dict(n="02", name="Connection", core="Emotional &amp; Relational Intelligence", tag="The Framework of Emotional and Relational Intelligence",
         intro=["Connection involves the capacity to understand ourselves and others, establish meaningful relationships, communicate effectively, and create environments characterized by trust, respect, and constructive collaboration."],
         subs=[("Emotional Intelligence", "Recognizing and understanding emotions in oneself and others."),
               ("Relational Intelligence", "Understanding how personal behavior and interpersonal patterns influence relationships."),
               ("Effective Communication", "Communicating clearly, respectfully, and constructively."),
               ("Conflict Navigation", "Addressing disagreements and relational difficulties with openness, accountability, and appropriate repair processes."),
               ("Trust &amp; Collaboration", "Building relationships that support cooperation, mutual respect, and collective effectiveness.")],
         app="Organizations demonstrate Connection through relational leadership, effective communication practices, constructive conflict management, and cultures that support trust, collaboration, and belonging.",
         ex=["Leadership development.", "Team-building and collaborative learning initiatives.", "Conflict-resolution processes.",
             "Regular opportunities for feedback and relationship development.", "Practices that strengthen trust, inclusion, and psychological safety."]),
    dict(n="03", name="Being", core="Presence &amp; Self-Regulation", tag="The Art of Embodiment",
         intro=["Being involves the capacity to remain present, aware, and responsive to internal and external experiences. It supports effective functioning under pressure, psychological flexibility, and the integration of mind and body."],
         subs=[("Self-Regulation", "Managing emotional, physiological, and behavioral responses effectively."),
               ("Present-Moment Awareness", "Maintaining attention and awareness in the here and now."),
               ("Mind-Body Awareness", "Recognizing the relationship between psychological and physical experiences."),
               ("Psychological Flexibility", "Responding adaptively to uncertainty, challenges, and changing circumstances."),
               ("Stress Management", "Dealing effectively with stress to preserve inner clarity, composure, and responsiveness in demanding situations.")],
         app="Organizations demonstrate Being by cultivating environments that support psychological well-being, healthy stress management, effective functioning under pressure, sustainable workplaces, and responsive leadership.",
         ex=["Psychological skills and stress-management education.", "Leadership development focused on presence and self-regulation practices.",
             "Organizational practices supporting recovery and sustainable performance.", "Assessment of environmental stressors and workload demands.",
             "Initiatives supporting psychological health and well-being."]),
    dict(n="04", name="Vision", core="Purposeful Direction &amp; Strategic Alignment", tag="The Blueprint of Excellence",
         intro=["Vision involves the capacity to establish meaningful direction, identify desired outcomes, and align decisions and actions with long-term aspirations and values."],
         subs=[("Vision Development", "Establishing a clear and meaningful direction for future development."),
               ("Strategic Thinking", "Understanding priorities, opportunities, challenges, and long-term implications."),
               ("Values Alignment", "Ensuring that decisions and actions reflect core values and guiding principles."),
               ("Intentional Decision-Making", "Making thoughtful choices that consistently support desired outcomes."),
               ("Shared Direction", "Developing clarity, communication, and alignment around collective goals and priorities.")],
         app="Organizations demonstrate Vision through clear strategic direction, values-based leadership, coherent priorities, and alignment between organizational purpose, decisions, and actions.",
         ex=["Organizational vision and strategy development.", "Leadership alignment and strategic planning sessions.", "Values-based decision-making processes.",
             "Individual and team development planning.", "Regular review of strategic priorities and organizational direction."]),
    dict(n="05", name="Meaning", core="Purpose, Fulfillment &amp; Meaningful Engagement", tag="The Core of Fulfillment",
         intro=["Meaning involves the capacity to connect achievement and external success with deeper sources of purpose, fulfillment, and personal significance.",
                "It recognizes that sustained excellence depends not only on what individuals and organizations accomplish, but also on the meaning and value associated with those accomplishments."],
         subs=[("Purpose Awareness", "Understanding what gives one’s work, efforts, and achievements significance."),
               ("Intrinsic Motivation", "Developing engagement that extends beyond external rewards and recognition."),
               ("Values-Based Engagement", "Connecting daily activities with personally and collectively meaningful values."),
               ("Identity &amp; Fulfillment", "Developing a sense of identity and fulfillment that is not dependent exclusively on achievement."),
               ("Belonging &amp; Contribution", "Experiencing meaningful participation, connection, and contribution within a larger collective.")],
         app="Organizations demonstrate Meaning by connecting institutional objectives with shared purpose, recognizing individual contributions, supporting belonging, and creating environments in which people experience their work as valuable and meaningful.",
         ex=["Purpose-centered leadership development.", "Organizational mission and values initiatives.",
             "Programs supporting personal identity and development beyond professional achievement.", "Integration of meaningful recognition and contribution practices.",
             "Initiatives strengthening belonging and shared purpose."]),
    dict(n="06", name="Creation", core="Intentional Action &amp; Continuous Development", tag="The Execution of Mastery",
         intro=["Creation involves the capacity to translate awareness, knowledge, vision, and intention into purposeful action.",
                "It represents the movement from understanding and possibility toward execution, adaptation, and tangible development."],
         subs=[("Personal Agency", "Recognizing one’s capacity and responsibility to influence outcomes."),
               ("Intentional Action", "Translating goals and insights into purposeful behavior."),
               ("Discipline &amp; Follow-Through", "Sustaining effort and commitment toward meaningful objectives."),
               ("Adaptability", "Adjusting approaches in response to changing circumstances and new information."),
               ("Continuous Learning", "Using experience, feedback, and reflection to support ongoing improvement.")],
         app="Organizations demonstrate Creation through effective implementation, adaptive leadership, organizational learning, innovation, and the continuous refinement of practices and processes.",
         ex=["Strategic implementation and action planning.", "Leadership and team accountability and feedback processes.",
             "Structured organizational learning and reflection.", "Continuous development and accountability initiatives.",
             "Mechanisms for evaluating progress and adapting interventions."]),
]

PHASE_TEXT = [
    ("Understanding the organization and its environment",
     ["The process begins with understanding the organization’s current functioning, strategic priorities, leadership structures, relationships, culture, and developmental needs.",
      "Potential methods include stakeholder consultations, interviews, surveys, organizational assessments, facilitated discussions, and reviews of existing structures and practices.",
      "Assessment considers both individual capabilities and environmental conditions."],
     "A clear understanding of organizational strengths, developmental priorities, and opportunities for improvement."),
    ("Translating assessment into a tailored development strategy",
     ["Based on the findings, AOE competencies are mapped to organizational priorities.",
      "Relevant stakeholder groups, developmental objectives, interventions, resources, responsibilities, and evaluation methods are identified.",
      "The resulting strategy may involve individual leadership development, team interventions, organizational initiatives, educational programs, or a combination of approaches."],
     "A tailored institutional development plan with defined priorities, interventions, and intended outcomes."),
    ("Translating the framework into practice",
     ["AOE principles and competencies are translated into educational experiences, developmental interventions, and organizational practices.",
      "Implementation may include leadership consulting, coaching, training, facilitated dialogue, team development, and organizational change initiatives.",
      "Activities are adapted to the organization’s size, structure, resources, and objectives."],
     "Active development of competencies and implementation of practices that support organizational effectiveness and sustainable performance."),
    ("Assessing progress and identifying opportunities for improvement",
     ["Progress is evaluated against the objectives established during strategic design.",
      "Evaluation may consider participation, learning, demonstrated competencies, behavioral changes, stakeholder experiences, organizational practices, and relevant performance or well-being indicators.",
      "Findings inform adjustments to the development strategy and ongoing interventions."],
     "Evidence-informed understanding of progress, challenges, and opportunities for further development."),
    ("Embedding development into organizational functioning",
     ["The final phase focuses on sustaining progress beyond individual programs or interventions.",
      "This may involve integrating competencies into leadership development, educational systems, organizational processes, professional development pathways, and institutional expectations.",
      "Ongoing review, internal capacity-building, and continued learning support long-term development."],
     "A sustainable approach through which AOE principles and competencies become increasingly embedded in organizational functioning."),
]

APPS = [
    ("Education &amp; Development of Core Competencies", "Development of psychological, relational, and leadership competencies through:",
     ["Online courses and structured educational modules.", "Workshops, seminars, and webinars.", "Leadership and professional development programs.",
      "Conferences, events, and institutional learning initiatives.", "Educational resources and continuing development opportunities."],
     "Programs may be tailored to executives, administrators, coaches, athletes, teams, and other stakeholder groups."),
    ("Leadership &amp; Individual Development", "Targeted development for individuals operating within organizational environments, including:",
     ["Executive coaching for leadership.", "Personal development opportunities for stakeholders.", "Individual professional development planning and ongoing advisory support."],
     "Individual work supports broader institutional objectives while respecting professional boundaries, confidentiality, and the distinction between consulting and clinical services."),
    ("Team &amp; Relational Development", "Interventions designed to strengthen collective functioning, including:",
     ["Team development and collaboration.", "Communication and relational intelligence training.", "Leadership-team alignment.", "Mediation and conflict resolution."], None),
    ("Organizational Development &amp; Culture", "Institutional initiatives that address the broader conditions influencing performance and well-being, including:",
     ["Organizational culture assessment and development.", "Development of mental health and performance programs.", "Leadership and governance practices.",
      "Values and strategic alignment.", "Communication and accountability structures.", "Psychological sustainability and organizational well-being.",
      "Change management and organizational learning."], None),
    ("System-Wide Development &amp; Integration", "For institutions overseeing multiple organizations, departments, or affiliated bodies, AOE may support broader initiatives such as:",
     ["Shared educational frameworks.", "Organization-wide competency development.", "Development pathways for affiliated organizations.",
      "Leadership education across institutional levels.", "Institutional resource libraries."], None),
]

LEVELS = [
    ("Foundational Education", "Introduction to AOE principles, competencies, and their application through structured educational programs.",
     "Completion of foundational education."),
    ("Competency Development", "More advanced development of relevant competencies through applied learning, reflection, and demonstrated understanding.",
     "Completion of defined competency-development requirements, with assessment appropriate to the role and learning objectives."),
    ("Institutional Integration", "Organizations adopt and demonstrate AOE-informed practices across relevant leadership, team, and organizational functions.",
     "Institutional participation or recognition based on documented implementation criteria."),
    ("Institutional Standards &amp; Certification", "A potential future pathway involving formalized standards, competency requirements, evaluation procedures, and periodic review. Such a model could support recognition of institutions or qualified participants demonstrating alignment with defined AOE standards.",
     None),
]

PRINCIPLES = [
    ("Ecological Responsibility", "Development addresses both individual capabilities and the environmental conditions influencing behavior, performance, and well-being."),
    ("Contextual Adaptability", "The framework provides a consistent conceptual foundation while allowing implementation to reflect each organization’s needs, culture, resources, and priorities."),
    ("Psychological Depth &amp; Practical Accessibility", "The methodology draws on psychoanalytic, relational, and systemic perspectives while translating complex psychological concepts into accessible, practical approaches."),
    ("Integration Over Isolation", "Competencies are interconnected and should not be treated as entirely independent skills. Institutional development considers their relationships and combined influence."),
    ("Sustainable Excellence", "High performance is pursued alongside psychological health, meaningful development, ethical responsibility, and organizational sustainability."),
    ("Continuous Development", "Excellence is understood as an ongoing process of reflection, learning, refinement, and adaptation rather than a fixed achievement."),
]

LOGO_SMALL = '<img class="on-dark" src="aoe-logo.svg" alt="aoe"><img class="on-light" src="aoe-logo-dark.svg" alt="aoe">'
LOGO_BLOCK = '<div class="logo{cls}"><img class="on-dark" src="aoe-logo.svg" alt="aoe"><img class="on-light" src="aoe-logo-dark.svg" alt="aoe"><span>ARCHITECTURE OF EXCELLENCE{tm}</span></div>'
COPY_TM = "Architecture of Excellence™<span class=\"sep\">|</span>© 2026 Dr. Alina K. Schulhofer. All rights reserved."
COPY = "Architecture of Excellence<span class=\"sep\">|</span>© 2026 Dr. Alina K. Schulhofer. All rights reserved."
LEGAL = ("Proprietary working framework. Institutional competency definitions, implementation pathways, and proposed standards "
         "are developmental and subject to further refinement and validation. This document does not establish a clinical "
         "treatment protocol or an existing certification program.")
CONTACT = """
  <div class="contact">
    """ + LOGO_BLOCK.format(cls="", tm="") + """
    <div class="ct">
      <div><span class="label">Founder</span><p>Dr. Alina K. Schulhofer</p></div>
      <div><span class="label">Contact</span><p>alina@architectureofexcellence.com</p></div>
    </div>
  </div>
  <p class="legal">""" + LEGAL + "</p>"


def ul(items, cls="dash"):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def pillar_block(p):
    subs = "".join(f'<div class="sc"><dt>{t}</dt><dd>{d}</dd></div>' for t, d in p["subs"])
    intro = "".join(f"<p>{t}</p>" for t in p["intro"])
    return f"""
  <article class="pillar">
    <div class="p-head">
      <div class="num">{p['n']}</div>
      <div><h2>{p['name']}</h2><div class="label tag">{p['tag']}</div></div>
      <div class="core-c"><span class="label">Core Competency</span><span class="cc">{p['core']}</span></div>
    </div>
    <div class="p-body">
      <div class="p-def">{intro}</div>
      <div class="p-grid">
        <div><div class="k">Core Subcompetencies</div><dl>{subs}</dl></div>
        <div>
          <div class="k">Institutional Application</div><p class="app">{p['app']}</p>
          <div class="k mt">Examples of Institutional Practices</div>{ul(p['ex'])}
        </div>
      </div>
    </div>
  </article>"""


# ------------------------------------------------------------------ pages
# Each page function returns (running-head label, body html, css class).
# Labels may carry a "Part X — " prefix, which is shown only in Document A.

def p_overview():
    return "About", """
  <div class="stack">
    <h1 class="about-h">About.</h1>
    <p class="sub">Architecture of Excellence™ (AOE) is a proprietary method informed by psychology and high-performance science, designed to support the psychological, emotional, and relational conditions required to develop and sustain excellence and well-being in high-performance environments.</p>
    <p class="value"><span class="label">Institutional Value</span>For institutions, AOE offers a shared framework and a structured process for developing the people, relationships, leadership, and organizational conditions on which sustainable performance and well-being depend.</p>
    <div class="cols2 ov">
      <p>Integrating psychological, relational, and systemic perspectives with high-performance strategy, AOE addresses the human dimensions of performance across individuals, teams, leadership, and organizations.</p>
      <p>The institutional framework translates AOE’s six foundational pillars into competencies and organizational practices that can be developed, implemented, and evaluated across diverse environments.</p>
    </div>
    <div class="quote">
      <div class="label">Excellence</div>
      <p>Excellence represents the integration of the six primary dimensions: targeting not simply the achievement of exceptional outcomes, but the ongoing development of the people, relationships, and conditions that make those outcomes possible and sustainable.</p>
    </div>
    <div class="label dims-h">Applications Across the High-Performance Ecosystem</div>
    <div class="dims">
      <div><span class="label">Individuals</span></div><div><span class="label">Teams</span></div><div><span class="label">Leadership</span></div><div><span class="label">Organizations</span></div>
    </div>
  </div>""", "overview"


LEVELS4 = [("Individual", "Developing core psychological, emotional, and relational capacities, including self-awareness, emotional intelligence, and interpersonal skills."),
           ("Relational &amp; Team", "Strengthening relational patterns, communication, trust, collaboration, and collective functioning."),
           ("Organizational", "Improving the internal functioning of the organization: its leadership practices, culture, structures, processes, and working conditions."),
           ("Broader Systems", "Supporting alignment, shared practices, and the development of competencies across the institutional and social environments.")]


def p_systems():
    lv = "".join(f'<div class="lvl"><div class="label">Level 0{i + 1}</div><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(LEVELS4))
    return "An Ecological, Systems-Based Approach", f"""
  <h1 class="pt"><span class="dim">An Ecological, Systems-Based</span><br>Approach to Excellence.</h1>
  <div class="cols2 mt20">
    <p>Individual performance, team effectiveness, and organizational functioning are shaped by the environments in which people operate. These dynamics are ever-present, bidirectional and can manifest in a variety of ways.</p>
    <p>Leadership influences organizational culture and individual behavior. Organizational structures shape relationships and decision-making processes, while team dynamics affect individual performance, motivation, and well-being.</p>
  </div>
  <figure class="eco-fig">{diagram_a()}
    <figcaption>Bidirectional influence across all four levels</figcaption>
  </figure>
  <p class="levels-intro">AOE targets transformation at four main interconnected levels:</p>
  <div class="levels-row">{lv}</div>
  <p class="closing-line">The framework recognizes that sustainable excellence requires attention to both <strong>personal capacities, collective functioning, and environmental conditions</strong>. Individuals alone cannot compensate for ineffective organizational structures, just as structural improvements cannot replace individual responsibility and development.</p>
""", "systems"


EXCELLENCE_BLOCK = """
  <div class="excellence">
    <div class="ex-h"><h2>Excellence</h2><div class="label tag">The Integration of the Six Pillars</div></div>
    <div class="cols2">
      <p>AOE’s philosophy views excellence not as an isolated competency or a final destination. It represents the integration and ongoing expression of the six pillars across individual functioning, relationships, leadership, and organizational life.</p>
      <p>At an institutional level, this means pursuing exceptional outcomes while cultivating the human and organizational conditions necessary to achieve and sustain them.</p>
    </div>
  </div>"""


def p_model():
    return "Part I — The AOE Competency Framework", f"""
  <h1 class="pt"><span class="dim">The</span> Framework.</h1>
  <div class="cols2 mt20 p1">
    <p>The AOE philosophy translates six core psychological principles into capacities to support individual development, team functioning, and organizational excellence.</p>
    <p>The six pillars are interconnected developmental dimensions rather than sequential stages: each informs and depends on the others, and Excellence emerges from their integration.</p>
  </div>
  <figure class="pillar-fig">{diagram_b()}</figure>
{EXCELLENCE_BLOCK}""", "part1"


def p_matrix():
    return "Part I — The AOE Competency Framework", f"""
  <h1 class="pt"><span class="dim">Core</span> Competencies.</h1>
  <p class="lead">Each pillar represents a core competency domain supported by specific developmental competencies.</p>
  <figure class="matrix">{diagram_c()}</figure>
  <p class="matrix-note">The AOE competencies are developed and expressed across individual, relational, team, and organizational contexts. Their application considers both the capabilities of people and the conditions that enable or constrain their expression.</p>
""", "competencies"


def p_pillar(i):
    p = PILLARS[i]
    subs = "".join(f'<div class="ps"><dt>{t}</dt><dd>{d}</dd></div>' for t, d in p["subs"])
    intro = "".join(f"<p>{t}</p>" for t in p["intro"])
    return f"The Six Pillars — {p['n']}", f"""
  <div class="pp-head">
    <div class="pp-title">
      <div class="label">Pillar {p['n']}</div>
      <h1>{p['name']}.</h1>
      <div class="label tag">{p['tag']}</div>
    </div>
    <div class="pp-core"><span class="label">Core Competency</span><p>{p['core']}</p></div>
  </div>
  <div class="pp-def">{intro}</div>
  <div class="pp-sec">
    <div class="k">Core Subcompetencies</div>
    <dl class="pp-subs">{subs}</dl>
  </div>
  <div class="pp-cols">
    <div><div class="k">Institutional Application</div><p>{p['app']}</p></div>
    <div><div class="k">Examples of Institutional Practices</div>{ul(p['ex'])}</div>
  </div>""", "pillar-pg"


def p_method():
    return "Part II — The AOE Institutional Methodology", f"""
  <h1 class="pt"><span class="dim">The AOE Institutional</span><br>Methodology.</h1>
  <div class="cols2 mt20">
    <p>The AOE Institutional Methodology provides a structured yet adaptable process for translating psychological principles and competencies into meaningful organizational development.</p>
    <p>The methodology is designed for application across organizations, teams, and high-performance environments, with interventions tailored to the needs, priorities, and context of each institution.</p>
  </div>
  <div class="method-stage">
    <figure class="cycle">{diagram_d()}</figure>
    <p class="cml"><span class="label">Continuous Monitoring &amp; Learning</span>Progress is observed and reviewed throughout implementation, and what is learned at each phase informs ongoing development. The process is therefore iterative rather than strictly linear.</p>
  </div>""", "method"


def p_phases():
    rows = "".join(f"""
    <div class="phase">
      <div class="ph"><div class="label">Phase 0{k + 1}</div><h3>{PHASES[k]}</h3><p class="sub2">{t}</p></div>
      <div class="phb"><p>{" ".join(body)}</p><p class="out"><span class="k">Outcome</span>{o}</p></div>
    </div>""" for k, (t, body, o) in enumerate(PHASE_TEXT))
    return "Part II — The Five Phases", f'<div class="phases">{rows}</div>', "phases-pg"


def p_apps():
    return "Part III — Institutional Applications", f"""
  <h1 class="pt"><span class="dim">Institutional</span> Applications.</h1>
  <div class="cols2 mt20">
    <p>AOE can be implemented through several interconnected developmental pathways.</p>
    <p>The appropriate combination of services and initiatives is determined through institutional assessment and strategic design.</p>
  </div>
  <figure class="apps-fig">{diagram_e()}</figure>""", "apps-pg"


def p_pathways():
    rows = "".join(f"""
    <div class="pw-card{' wide' if k == 4 else ''}">
      <div class="pw-top"><span class="pw-n">0{k + 1}</span><h3>{t}</h3></div>
      <p class="pw-lead">{lead}</p>{ul(items, "dash two" if k == 4 else "dash")}{f'<p class="note">{note}</p>' if note else ''}
    </div>""" for k, (t, lead, items, note) in enumerate(APPS))
    return "Part III — The Five Pathways", f'<div class="pathways">{rows}</div>', "pathways-pg"


def p_standards():
    lv = "".join(f"""
    <div class="lv-c{' future' if i == 3 else ''}">
      <div class="label">Level {i + 1}</div><h3>{t}</h3><p>{d}</p>
      {f'<p class="rec"><span class="k">Potential recognition</span>{r}</p>' if r else '<p class="rec"><span class="k">Status</span>Any certification or mandatory educational requirements would require further development, validation, governance arrangements, and appropriate institutional agreements.</p>'}
    </div>""" for i, (t, d, r) in enumerate(LEVELS))
    return "Part IV — Institutional Standards &amp; Future Development", f"""
  <h1 class="pt"><span class="dim">Institutional Standards</span><br>&amp; Future Development.</h1>
  <div class="cols2 mt20">
    <p>Architecture of Excellence is designed to support the progressive development of shared competencies and institutional practices.</p>
    <p>As the framework is implemented and evaluated, it may provide the foundation for more formal educational standards, professional development pathways, and institutional recognition.</p>
  </div>
  <figure class="steps">{diagram_f()}</figure>
  <div class="levels4">{lv}</div>
  <p class="caveat">These levels represent a proposed developmental pathway, not an existing certification or accreditation system.</p>""", "standards"


def p_principles(with_contact=False):
    pr = "".join(f'<div class="pr"><div class="num sm">0{i + 1}</div><div><h3>{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(PRINCIPLES))
    return "Foundational Implementation Principles", f"""
  <h1 class="pt"><span class="dim">Foundational Implementation</span><br>Principles.</h1>
  <p class="lead">All applications of the AOE Institutional Framework are guided by the following commitments.</p>
  <div class="principles">{pr}</div>{CONTACT if with_contact else ""}""", "principles-pg" + (" compact" if with_contact else "")


# ------------------------------------------------------------------ documents
def cover(title_html):
    return f"""
<!-- ============ COVER ============ -->
<section class="page cover">
  <div class="cover-center">
    {LOGO_BLOCK.format(cls=" cover-logo", tm="™")}
    <h1>{title_html}</h1>
  </div>
  <footer class="center"><span>{COPY_TM}</span></footer>
</section>"""


def closing(n, total):
    return f"""
<!-- ============ CLOSING ============ -->
<section class="page closing">
  <div class="close-stage">
    <p class="cl">Architecture of Excellence provides a unified psychological and strategic foundation for developing individuals, strengthening relationships, advancing leadership, and strengthening organizational environments.</p>
    <p class="cl">By translating its six foundational pillars into competencies, developmental interventions, and institutional practices, AOE offers a structured and adaptable approach to cultivating excellence across high-performance ecosystems.</p>
    <div class="rule"></div>
    <p class="final">The objective is not merely to improve individual performance, but to develop the people, relationships, cultures, and institutional conditions through which excellence can be achieved and sustained.</p>
  </div>
{CONTACT}
  <footer><span>{COPY}</span><span class="pg">{n:02d} / {total}</span></footer>
</section>"""


DOCS = {
    "institutional": dict(
        title="Institutional Framework &amp; Methodology",
        cover='<span class="dim">Institutional Competency Framework</span><br>&amp; Implementation Methodology.',
        parts=True,
        pages=[p_overview, p_systems, p_model, p_matrix, *[lambda i=i: p_pillar(i) for i in range(6)],
               p_method, p_phases, p_apps, p_pathways, p_standards, p_principles, "closing"]),
    "competency-framework": dict(
        title="Institutional Competency Framework",
        cover='<span class="dim">Institutional</span><br>Competency Framework.',
        parts=False,
        pages=[p_overview, p_systems, p_model, p_matrix, *[lambda i=i: p_pillar(i) for i in range(6)],
               "closing"]),
    "implementation-methodology": dict(
        title="Institutional Implementation Methodology",
        cover='<span class="dim">Institutional</span><br>Implementation Methodology.',
        parts=False,
        pages=[p_overview, p_method, p_phases, p_apps, p_pathways, p_standards, lambda: p_principles(with_contact=True)]),
}


def assemble(key):
    d = DOCS[key]
    total = len(d["pages"]) + 1
    out = [cover(d["cover"])]
    for n, fn in enumerate(d["pages"], start=2):
        if fn == "closing":
            out.append(closing(n, total))
            continue
        label, body, cls = fn()
        if not d["parts"] and " — " in label and label.startswith("Part"):
            label = label.split(" — ", 1)[1]
        out.append(f"""
<!-- ============ PAGE {n:02d} ============ -->
<section class="page {cls}">
  <div class="runhead"><span class="label">{label}</span>{LOGO_SMALL}</div>
{body}
  <footer><span>{COPY}</span><span class="pg">{n:02d} / {total}</span></footer>
</section>""")
    css = (HERE / "institutional.css").read_text()
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{d['title']} — Architecture of Excellence™</title>
<link rel="stylesheet" href="fonts/fonts.css">
<script>document.documentElement.dataset.theme = location.hash === '#light' ? 'light' : 'dark';</script>
<style>
{css}
</style>
</head>
<body>
{"".join(out)}
</body>
</html>
"""
    (HERE / f"{key}.html").write_text(html)
    print(f"wrote {key}.html, {total} pages")


if __name__ == "__main__":
    for k in DOCS:
        assemble(k)
