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
    cx = cy = 190
    radii = [58, 100, 142, 184]
    names = ["RELATIONAL &amp; TEAM", "ORGANIZATIONAL", "SYSTEMIC"]
    o = [f'<svg class="dg" id="diagram-a-ecological-systems" viewBox="0 0 380 380" xmlns="http://www.w3.org/2000/svg">',
         MARKERS.format(id="ma")]
    for i, r in enumerate(reversed(radii)):
        o.append(f'<circle class="{"band" if i % 2 == 0 else "bg"}" cx="{cx}" cy="{cy}" r="{r}"/>')
    for r in radii:
        o.append(f'<circle class="ring{" dash" if r != radii[-1] else ""}" cx="{cx}" cy="{cy}" r="{r}"/>')
    # level names along the top of each band, numbers along the bottom
    bands = [(radii[i], radii[i + 1]) for i in range(3)]
    for (a, b), n in zip(bands, names):
        m = (a + b) / 2
        o.append(f'<text class="lv" x="{cx}" y="{f(cy - m)}" text-anchor="middle" dominant-baseline="central">{n}</text>')
    for i, (a, b) in enumerate([(0, 58)] + bands):
        m = 40 if i == 0 else (a + b) / 2
        o.append(f'<text class="ln" x="{cx}" y="{f(cy + m)}" text-anchor="middle" dominant-baseline="central">0{i + 1}</text>')
    o.append(f'<text class="lv core" x="{cx}" y="{cy - 4}" text-anchor="middle" dominant-baseline="central">INDIVIDUAL</text>')
    # reciprocal arrows across every boundary on two diagonals
    for th in (-38, 142, 38, 218):
        u = (cos(radians(th)), sin(radians(th)))
        n = (-u[1], u[0])
        for r in radii[:3]:
            for s, (r1, r2) in ((4.2, (r - 12, r + 12)), (-4.2, (r + 12, r - 12))):
                x1, y1 = cx + u[0] * r1 + n[0] * s, cy + u[1] * r1 + n[1] * s
                x2, y2 = cx + u[0] * r2 + n[0] * s, cy + u[1] * r2 + n[1] * s
                o.append(f'<line class="arw" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" marker-end="url(#ma)"/>')
    o.append("</svg>")
    return "\n".join(o)


# ---------------------------------------------------------------- Diagram B
PILLAR_NAMES = ["Truth", "Connection", "Being", "Vision", "Meaning", "Creation"]


def diagram_b(cls="dg", id_="diagram-b-pillar-model", labels=True):
    cx = cy = 230
    R, outer = 150, 205
    pts = [pol(cx, cy, R, -90 + k * 60) for k in range(6)]
    vb = "-80 -6 620 472" if labels else "0 0 460 460"
    o = [f'<svg class="{cls}" id="{id_}" viewBox="{vb}" xmlns="http://www.w3.org/2000/svg">']
    o.append(f'<circle class="ring dash" cx="{cx}" cy="{cy}" r="{outer}"/>')
    o.append(f'<circle class="ring faint" cx="{cx}" cy="{cy}" r="{R + 22}"/>')
    o.append(f'<circle class="ring faint" cx="{cx}" cy="{cy}" r="{R - 22}"/>')
    for i in range(6):
        for j in range(i + 1, 6):
            (x1, y1), (x2, y2) = pts[i], pts[j]
            o.append(f'<line class="web" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}"/>')
    o.append(f'<circle class="ring strong" cx="{cx}" cy="{cy}" r="{R}"/>')
    o.append(f'<circle class="core-bg" cx="{cx}" cy="{cy}" r="66"/>')
    o.append(f'<circle class="core" cx="{cx}" cy="{cy}" r="66"/>')
    o.append(f'<circle class="ring faint" cx="{cx}" cy="{cy}" r="74"/>')
    o.append(f'<text class="ex" x="{cx}" y="{cy - 7}" text-anchor="middle" dominant-baseline="central">EXCELLENCE</text>')
    o.append(tlines(cx, cy + 17, ["The integration", "of the six pillars"], "exs", 12))
    for k, (x, y) in enumerate(pts):
        o.append(f'<circle class="col" cx="{f(x)}" cy="{f(y)}" r="13"/>')
        o.append(f'<circle class="col-in" cx="{f(x)}" cy="{f(y)}" r="4"/>')
        if labels:
            a = -90 + k * 60
            lx, ly = pol(cx, cy, 182, a)
            anchor = "middle" if k in (0, 3) else ("start" if k in (1, 2) else "end")
            if k == 0:
                ly -= 4
            if k == 3:
                ly += 6
            o.append(f'<text class="pn" x="{f(lx)}" y="{f(ly - 8)}" text-anchor="{anchor}" dominant-baseline="central">0{k + 1}</text>')
            o.append(f'<text class="pl" x="{f(lx)}" y="{f(ly + 7)}" text-anchor="{anchor}" dominant-baseline="central">{PILLAR_NAMES[k].upper()}</text>')
    o.append("</svg>")
    return "\n".join(o)


# ---------------------------------------------------------------- Diagram C
CORE = [
    ["Self-Awareness,", "Integrity &amp;", "Accountability"],
    ["Emotional &amp;", "Relational", "Intelligence"],
    ["Presence &amp;", "Self-Regulation"],
    ["Purposeful", "Direction &amp;", "Strategic", "Alignment"],
    ["Purpose,", "Fulfillment &amp;", "Meaningful", "Engagement"],
    ["Intentional", "Action &amp;", "Continuous", "Development"],
]
SUBS = [
    [["Self-Awareness"], ["Psychological", "Insight"], ["Integrity"], ["Accountability"], ["Openness to", "Feedback"]],
    [["Emotional", "Intelligence"], ["Relational", "Intelligence"], ["Effective", "Communication"], ["Conflict", "Navigation"], ["Trust &amp;", "Collaboration"]],
    [["Self-Regulation"], ["Present-Moment", "Awareness"], ["Mind-Body", "Awareness"], ["Psychological", "Flexibility"], ["Stress", "Management"]],
    [["Vision", "Development"], ["Strategic", "Thinking"], ["Values", "Alignment"], ["Intentional", "Decision-Making"], ["Shared", "Direction"]],
    [["Purpose", "Awareness"], ["Intrinsic", "Motivation"], ["Values-Based", "Engagement"], ["Identity &amp;", "Fulfillment"], ["Belonging &amp;", "Contribution"]],
    [["Personal Agency"], ["Intentional", "Action"], ["Discipline &amp;", "Follow-Through"], ["Adaptability"], ["Continuous", "Learning"]],
]


def diagram_c():
    W, gap, lab = 678, 8, 0
    cw = (W - lab - gap * 5) / 6
    y_head, h_head = 0, 70
    y_core, h_core = 80, 84
    y_sub, h_sub, g_sub = 190, 52, 8
    y_ex = y_sub + 5 * (h_sub + g_sub) + 30
    H = y_ex + 44
    o = [f'<svg class="dg" id="diagram-c-competency-framework" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">']
    for k in range(6):
        x = lab + k * (cw + gap)
        mx = x + cw / 2
        o.append(f'<line class="rule" x1="{f(x)}" y1="0.5" x2="{f(x + cw)}" y2="0.5"/>')
        o.append(f'<circle class="numc" cx="{f(mx)}" cy="26" r="15"/>')
        o.append(f'<text class="numt" x="{f(mx)}" y="26" text-anchor="middle" dominant-baseline="central">0{k + 1}</text>')
        o.append(f'<text class="cname" x="{f(mx)}" y="58" text-anchor="middle" dominant-baseline="central">{PILLAR_NAMES[k]}</text>')
        o.append(f'<rect class="corebox" x="{f(x)}" y="{y_core}" width="{f(cw)}" height="{h_core}"/>')
        o.append(tlines(mx, y_core + h_core / 2, CORE[k], "ccore", 14))
        o.append(f'<line class="stem" x1="{f(mx)}" y1="{y_core + h_core}" x2="{f(mx)}" y2="{y_sub}"/>')
        for j, lines in enumerate(SUBS[k]):
            y = y_sub + j * (h_sub + g_sub)
            o.append(f'<rect class="subbox" x="{f(x)}" y="{y}" width="{f(cw)}" height="{h_sub}"/>')
            o.append(tlines(mx, y + h_sub / 2, lines, "csub", 13.5))
        yb = y_sub + 5 * (h_sub + g_sub) - g_sub
        o.append(f'<line class="stem" x1="{f(mx)}" y1="{yb}" x2="{f(mx)}" y2="{y_ex}"/>')
    o.append(f'<rect class="exbar" x="0" y="{y_ex}" width="{W}" height="40"/>')
    o.append(f'<text class="ex" x="{W / 2}" y="{y_ex + 20}" text-anchor="middle" dominant-baseline="central">EXCELLENCE · THE INTEGRATION OF THE SIX PILLARS</text>')
    o.append("</svg>")
    return "\n".join(o)


# ---------------------------------------------------------------- Diagram D
PHASES = ["Discovery &amp; Assessment", "Strategic Design", "Implementation &amp; Development",
          "Evaluation &amp; Refinement", "Integration &amp; Sustainability"]
PHASE_LINES = [["Discovery &amp;", "Assessment"], ["Strategic", "Design"], ["Implementation &amp;", "Development"],
               ["Evaluation &amp;", "Refinement"], ["Integration &amp;", "Sustainability"]]


def diagram_d():
    W, H = 678, 420
    cx, cy, R, nr = 339, 218, 146, 29
    o = [f'<svg class="dg" id="diagram-d-institutional-methodology" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
         MARKERS.format(id="md")]
    angs = [-90 + k * 72 for k in range(5)]
    d = degrees(asin((nr + 9) / R)) * 2
    o.append(f'<circle class="ring faint" cx="{cx}" cy="{cy}" r="{R + 20}"/>')
    for k in range(5):
        a1, a2 = angs[k] + d / 2 + 1, angs[k] + 72 - d / 2 - 1
        x1, y1 = pol(cx, cy, R, a1)
        x2, y2 = pol(cx, cy, R, a2)
        o.append(f'<path class="arc" d="M{f(x1)},{f(y1)} A{R},{R} 0 0 1 {f(x2)},{f(y2)}" marker-end="url(#md)"/>')
    # refinement loop: Evaluation (4) back to Implementation (3)
    p4 = pol(cx, cy, R - nr - 6, angs[3] - 12)
    p3 = pol(cx, cy, R - nr - 6, angs[2] + 12)
    o.append(f'<path class="loop" d="M{f(p4[0])},{f(p4[1])} Q{cx},{cy + 34} {f(p3[0])},{f(p3[1])}" marker-end="url(#md)"/>')
    o.append(f'<text class="lp" x="{cx}" y="{cy + 44}" text-anchor="middle" dominant-baseline="central">REFINE</text>')
    o.append(tlines(cx, cy - 12, ["Structured", "yet adaptable"], "ctr", 17))
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
    o = ['<svg class="dg" id="diagram-e-institutional-applications" viewBox="0 0 340 340" xmlns="http://www.w3.org/2000/svg">']
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
    ("Ethical &amp; Professional Boundaries", "Education, coaching, consulting, organizational assessment, and clinical services remain appropriately differentiated. Participation, confidentiality, safeguarding, and professional responsibilities are addressed according to the nature of each engagement."),
]

LOGO_SMALL = '<img class="on-dark" src="aoe-logo.svg" alt="aoe"><img class="on-light" src="aoe-logo-dark.svg" alt="aoe">'
COPY = "Architecture of Excellence™<span class=\"sep\">|</span>© 2026 Dr. Alina K. Schulhofer. All rights reserved."


def page(n, label, body, cls=""):
    return f"""
<!-- ============ PAGE {n:02d} ============ -->
<section class="page {cls}">
  <div class="runhead"><span class="label">{label}</span>{LOGO_SMALL}</div>
{body}
  <footer><span>{COPY}</span><span class="pg">{n:02d} / {TOTAL}</span></footer>
</section>"""


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


def build():
    css = (HERE / "institutional.css").read_text()
    pages = []

    # 01 — Cover
    pages.append(f"""
<!-- ============ PAGE 01 · COVER ============ -->
<section class="page cover">
  <header>
    <span class="label">Institutional Framework</span>
    <div class="logo"><img class="on-dark" src="aoe-logo.svg" alt="aoe"><img class="on-light" src="aoe-logo-dark.svg" alt="aoe"><span>ARCHITECTURE OF EXCELLENCE™</span></div>
  </header>
  <div class="cover-art">{diagram_b(cls="dg art", id_="cover-mark", labels=False)}</div>
  <div class="cover-title">
    <div class="label">Architecture of Excellence™</div>
    <h1><span class="dim">Institutional Competency Framework</span><br>&amp; Implementation Methodology.</h1>
    <div class="rule"></div>
    <p class="by">Developed by Dr. Alina K. Schulhofer</p>
  </div>
  <footer><span>{COPY}</span><span class="pg">01 / {TOTAL}</span></footer>
</section>""")

    # 02 — Overview
    pages.append(page(2, "Overview", """
  <div class="stack">
    <h1 class="pt"><span class="dim">Architecture of</span><br>Excellence™.</h1>
    <p class="sub">Architecture of Excellence™ (AOE) is a proprietary, science-based approach designed to support the psychological, emotional, and relational conditions required to develop and sustain excellence and well-being in high-performance environments.</p>
    <div class="cols2 ov">
      <p>Integrating psychological, relational, and systemic perspectives with high-performance strategy, AOE addresses the human dimensions of performance across individuals, teams, leadership, and organizations.</p>
      <p>The institutional framework translates AOE’s six foundational pillars — <strong>Truth, Connection, Being, Vision, Meaning, and Creation</strong> — into competencies and organizational practices that can be developed, implemented, and evaluated across diverse environments.</p>
    </div>
    <div class="quote">
      <div class="label">Excellence</div>
      <p>Excellence represents the integration of the six primary dimensions: targeting not simply the achievement of exceptional outcomes, but the ongoing development of the people, relationships, and conditions that make those outcomes possible and sustainable.</p>
    </div>
    <div class="dims">
      <div><span class="label">Individuals</span></div><div><span class="label">Teams</span></div><div><span class="label">Leadership</span></div><div><span class="label">Organizations</span></div>
    </div>
  </div>""", "overview"))

    # 03 — Systems
    levels = [("Individual", "Developing core psychological, emotional, and relational capacities, including self-awareness, emotional intelligence, and interpersonal skills."),
              ("Relational and Team", "Strengthening relational patterns, communication, trust, collaboration, and collective functioning."),
              ("Organizational", "Improving leadership practices, organizational culture, processes, and working conditions."),
              ("Systemic", "Supporting alignment, shared practices, and development across interconnected stakeholders, teams, and organizations.")]
    lv = "".join(f'<div class="lvl"><div class="num sm">0{i + 1}</div><div><h3>{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(levels))
    pages.append(page(3, "A Systems-Based Approach", f"""
  <h1 class="pt"><span class="dim">A Systems-Based</span><br>Approach to Excellence.</h1>
  <div class="cols2 mt20">
    <p>Individual performance, team effectiveness, and organizational functioning are shaped by the environments in which people operate. These dynamics are ever-present, bi-directional and can manifest in a variety of ways.</p>
    <p>For example, leadership influences organizational culture and individual behavior. Organizational structures shape relationships and decision-making processes, while team dynamics affect individual performance, motivation, and well-being. These factors are constantly interacting and interconnected, often in unseen ways.</p>
  </div>
  <div class="eco">
    <figure>{diagram_a()}
      <figcaption><svg viewBox="0 0 30 14" class="dg key"><defs><marker id="mk" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ah" d="M1,1.2 L9,5 L1,8.8"/></marker></defs><line class="arw" x1="2" y1="4" x2="27" y2="4" marker-end="url(#mk)"/><line class="arw" x1="27" y1="10.5" x2="2" y2="10.5" marker-end="url(#mk)"/></svg>Bidirectional influence across every level</figcaption>
    </figure>
    <div class="levels"><p class="intro">AOE therefore approaches transformation at four interconnected levels:</p>{lv}</div>
  </div>
  <p class="closing-line">The framework recognizes that sustainable excellence requires attention to both <strong>personal capacities, collective functioning, and environmental conditions</strong>. Individuals alone cannot compensate for ineffective organizational structures, just as structural improvements cannot replace individual responsibility and development.</p>
""", "systems"))

    # 04 — Part I + pillar model
    pages.append(page(4, "Part I — The AOE Competency Framework", f"""
  <h1 class="pt"><span class="dim">The Six</span> Pillars.</h1>
  <div class="cols2 mt20 p1">
    <p>The AOE Competency Framework translates six core psychological principles into capabilities that support individual development, effective team functioning, and organizational excellence.</p>
    <p>Each pillar represents a core competency domain supported by specific developmental competencies.</p>
  </div>
  <figure class="pillar-fig">{diagram_b()}</figure>
  <div class="excellence">
    <div class="ex-h"><div class="num">→</div><div><h2>Excellence</h2><div class="label tag">The Integration of the Six Pillars</div><div class="label tag soft">The Embodiment of Greatness</div></div></div>
    <div class="cols2">
      <p>Within Architecture of Excellence™, Excellence is not treated as an isolated competency or a final destination. It represents the integration and ongoing expression of the six pillars across individual functioning, relationships, leadership, and organizational life.</p>
      <p>Excellence involves the continuous pursuit of development, integrity, meaningful achievement, and psychological sustainability. At an institutional level, this means pursuing exceptional outcomes while cultivating the human and organizational conditions necessary to achieve and sustain them.</p>
    </div>
  </div>""", "part1"))

    # 05 — Competency matrix
    pages.append(page(5, "Part I — The AOE Competency Framework", f"""
  <h1 class="pt"><span class="dim">From Principles</span><br>to Competencies.</h1>
  <p class="lead">Each pillar represents a core competency domain supported by specific developmental competencies.</p>
  <div class="matrix-key"><span class="label">Pillar</span><span class="arrow">→</span><span class="label">Core Competency</span><span class="arrow">→</span><span class="label">Core Subcompetencies</span></div>
  <figure class="matrix">{diagram_c()}</figure>
""", "competencies"))

    # 06–08 — pillars
    for i in range(3):
        a, b = PILLARS[2 * i], PILLARS[2 * i + 1]
        pages.append(page(6 + i, f"The Six Pillars — {a['n']} · {b['n']}", pillar_block(a) + pillar_block(b), "pillars"))

    # 09 — Part II + cycle
    pages.append(page(9, "Part II — The AOE Institutional Methodology", f"""
  <h1 class="pt"><span class="dim">The AOE Institutional</span><br>Methodology.</h1>
  <div class="cols2 mt20">
    <p>The AOE Institutional Methodology provides a structured yet adaptable process for translating psychological principles and competencies into meaningful organizational development.</p>
    <p>The methodology is designed for application across organizations, teams, and high-performance environments, with interventions tailored to the needs, priorities, and context of each institution.</p>
  </div>
  <figure class="cycle">{diagram_d()}</figure>
  <div class="outcomes">
    {"".join(f'<div class="oc"><div class="label">Phase 0{k + 1} · Outcome</div><p>{PHASE_TEXT[k][2]}</p></div>' for k in range(5))}
  </div>""", "method"))

    # 10 — Phases detail
    rows = "".join(f"""
    <div class="phase">
      <div class="ph"><div class="num sm">0{k + 1}</div><div><h3>{PHASES[k]}</h3><div class="label tag">{t}</div></div></div>
      <div class="phb"><p>{" ".join(body)}</p><div class="out"><span class="k">Outcome</span><p>{o}</p></div></div>
    </div>""" for k, (t, body, o) in enumerate(PHASE_TEXT))
    pages.append(page(10, "Part II — The Five Phases", f'<div class="phases">{rows}</div>', "phases-pg"))

    # 11 — Applications
    cards = "".join(f"""
    <div class="appc{' wide' if k == 3 else ''}">
      <div class="ah2"><div class="num sm">0{k + 1}</div><h3>{t}</h3></div>
      <p>{lead}</p>{ul(items)}{f'<p class="note">{note}</p>' if note else ''}
    </div>""" for k, (t, lead, items, note) in enumerate(APPS))
    pages.append(page(11, "Part III — Institutional Applications", f"""
  <div class="apps-top">
    <div>
      <h1 class="pt"><span class="dim">Institutional</span><br>Applications.</h1>
      <p class="lead">AOE can be implemented through several interconnected developmental pathways.</p>
      <p class="lead">The appropriate combination of services and initiatives is determined through institutional assessment and strategic design.</p>
    </div>
    <figure class="apps-fig">{diagram_e()}</figure>
  </div>
  <div class="apps">{cards}</div>""", "apps-pg"))

    # 12 — Part IV
    lv = "".join(f"""
    <div class="lv-c{' future' if i == 3 else ''}">
      <div class="label">Level {i + 1}</div><h3>{t}</h3><p>{d}</p>
      {f'<p class="rec"><span class="k">Potential recognition</span>{r}</p>' if r else '<p class="rec"><span class="k">Status</span>Any certification or mandatory educational requirements would require further development, validation, governance arrangements, and appropriate institutional agreements.</p>'}
    </div>""" for i, (t, d, r) in enumerate(LEVELS))
    pages.append(page(12, "Part IV — Institutional Standards &amp; Future Development", f"""
  <h1 class="pt"><span class="dim">Institutional Standards</span><br>&amp; Future Development.</h1>
  <div class="cols2 mt20">
    <p>Architecture of Excellence™ is designed to support the progressive development of shared competencies and institutional practices.</p>
    <p>As the framework is implemented and evaluated, it may provide the foundation for more formal educational standards, professional development pathways, and institutional recognition.</p>
  </div>
  <figure class="steps">{diagram_f()}</figure>
  <div class="levels4">{lv}</div>
  <p class="caveat">These levels represent a proposed developmental pathway, not an existing certification or accreditation system.</p>""", "standards"))

    # 13 — Principles
    pr = "".join(f'<div class="pr"><div class="num sm">0{i + 1}</div><div><h3>{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(PRINCIPLES))
    pages.append(page(13, "Foundational Implementation Principles", f"""
  <h1 class="pt"><span class="dim">Foundational Implementation</span><br>Principles.</h1>
  <p class="lead">All applications of the AOE Institutional Framework should be guided by the following commitments.</p>
  <div class="principles">{pr}</div>""", "principles-pg"))

    # 14 — Closing
    pages.append(f"""
<!-- ============ PAGE 14 · CLOSING ============ -->
<section class="page closing">
  <div class="runhead"><span class="label">Closing Statement</span>{LOGO_SMALL}</div>
  <div class="close-stage">
    <div class="close-mark">{diagram_b(cls="dg art", id_="close-mark", labels=False)}</div>
    <p class="cl">Architecture of Excellence™ provides a unified psychological and strategic foundation for developing individuals, strengthening relationships, advancing leadership, and transforming organizational environments.</p>
    <p class="cl">By translating its six foundational pillars into competencies, developmental interventions, and institutional practices, AOE offers a structured and adaptable approach to cultivating excellence across high-performance ecosystems.</p>
    <div class="rule"></div>
    <p class="final">The objective is not merely to improve individual performance, but to develop the people, relationships, cultures, and institutional conditions through which excellence can be achieved and sustained.</p>
  </div>
  <div class="contact">
    <div class="logo"><img class="on-dark" src="aoe-logo.svg" alt="aoe"><img class="on-light" src="aoe-logo-dark.svg" alt="aoe"><span>ARCHITECTURE OF EXCELLENCE™</span></div>
    <div class="ct">
      <div><span class="label">Founder</span><p>Dr. Alina K. Schulhofer</p></div>
      <div><span class="label">Contact</span><p>alina@architectureofexcellence.com</p></div>
    </div>
  </div>
  <p class="legal">Proprietary working framework. Institutional competency definitions, implementation pathways, and proposed standards are developmental and subject to further refinement and validation. This document does not establish a clinical treatment protocol or an existing certification program.</p>
  <footer><span>{COPY}</span><span class="pg">{TOTAL} / {TOTAL}</span></footer>
</section>""")

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Institutional Framework — Architecture of Excellence™</title>
<link rel="stylesheet" href="fonts/fonts.css">
<script>document.documentElement.dataset.theme = location.hash === '#light' ? 'light' : 'dark';</script>
<style>
{css}
</style>
</head>
<body>
{"".join(pages)}
</body>
</html>
"""
    (HERE / "institutional.html").write_text(html)
    print("wrote institutional.html,", len(pages), "pages")


if __name__ == "__main__":
    build()
