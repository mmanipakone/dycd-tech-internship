"""
Add Pages 15 & 16: Scenario D — Workplace Problem Solving & App Concept Design
Based on exact drawing/text measurements from existing Scenario C pages.
"""

import fitz
import os

SRC = "revised_outputs/TechInternship_revised.pdf"
TMP = SRC + ".tmp"
AU  = '/Library/Fonts/Arial Unicode.ttf'

# ── Colors ──────────────────────────────────────────────────────────────────
DB  = (0.03920, 0.14510, 0.25100)   # DARK_BLUE
OR  = (0.91000, 0.29410, 0.00000)   # ORANGE
YL  = (1.00000, 0.90200, 0.00000)   # YELLOW
WH  = (1.00000, 1.00000, 1.00000)   # WHITE
DK  = (26/255,  26/255,  26/255 )   # DARK (body text)
LB  = (0.96860, 0.97250, 0.98040)   # LIGHT_BLUE (alt table rows)
BB  = (0.88630, 0.90980, 0.94120)   # BLUE_BORDER (table row dividers)

# ── Helpers ─────────────────────────────────────────────────────────────────
def rect(pg, r, fill):
    s = pg.new_shape()
    s.draw_rect(fitz.Rect(*r))
    s.finish(fill=fill, color=None)
    s.commit()

def t(pg, xy, text, fn, sz, clr, ff=None):
    kw = {}
    if ff:
        kw['fontfile'] = ff
    pg.insert_text(xy, text, fontname=fn, fontsize=sz, color=clr, **kw)

def helv(pg, xy, text, sz=8.5, clr=None):
    t(pg, xy, text, 'helv', sz, clr or DK)

def hebo(pg, xy, text, sz=8.5, clr=None):
    t(pg, xy, text, 'hebo', sz, clr or DK)

def au(pg, xy, text, sz=8.5, clr=None):
    t(pg, xy, text, 'arialuni', sz, clr or DK, ff=AU)


# ── Open ─────────────────────────────────────────────────────────────────────
doc = fitz.open(SRC)
# Remove previously appended Scenario D pages if present
while doc.page_count > 14:
    doc.delete_page(doc.page_count - 1)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  PAGE 15 — SCENARIO D OVERVIEW                                          ║
# ╚══════════════════════════════════════════════════════════════════════════╝

p15 = doc.new_page(width=612, height=792)

# ── Background & structural fills ───────────────────────────────────────────
rect(p15, (0,   0,   612, 792),   WH)          # full page white
rect(p15, (0,   0,   612,  93.8), DB)          # header (2-line title → taller)
rect(p15, (0,   769.5, 612, 792), DB)          # footer

# Left col section-header orange accent bars (45 pt wide, 2.25 pt tall, 9 pt below header y)
# COMPANY BACKGROUND at 110.2 → bar at 119.2
rect(p15, (36,  119.2,  81,  121.45), OR)
# THE CHALLENGE at 258.0 → bar at 267.0
rect(p15, (36,  267.0,  81,  269.25), OR)
# RESEARCH APPROACH at 458.0 → bar at 467.0
rect(p15, (36,  467.0,  81,  469.25), OR)
# EXAMPLE PROBLEM AREAS at 573.0 → bar at 582.0
rect(p15, (36,  582.0,  81,  584.25), OR)

# Intern Mission box (dark blue) + yellow left accent
rect(p15, (37.875, 376.5, 299.25, 435), DB)
rect(p15, (36,     376.5,  39.75, 435), YL)

# Right col: TEAM ROLES orange accent bar (header at 108.8 → bar at 117.75)
rect(p15, (312.75, 117.75, 357.75, 120.0), OR)

# Team Roles table header row (dark blue)
rect(p15, (312.75, 129.0, 387.0, 150.75), DB)
rect(p15, (387.0,  129.0, 576.0, 150.75), DB)

# Team Roles rows: 5 × 33.75 pt alternating fill + blue separator line at top of even rows
ROLE_ROWS = [
    (150.75, 184.5,  WH),   # Row 1 – Project Manager
    (184.5,  218.25, LB),   # Row 2 – Research Lead
    (218.25, 252.0,  WH),   # Row 3 – Process Analyst
    (252.0,  285.75, LB),   # Row 4 – Solution Designer
    (285.75, 319.5,  WH),   # Row 5 – Presentation Lead
]
for i, (y0, y1, fill) in enumerate(ROLE_ROWS):
    rect(p15, (312.75, y0, 387.0, y1), fill)
    rect(p15, (387.0,  y0, 576.0, y1), fill)
    if i > 0:  # border line at top of each row (except first)
        rect(p15, (312.75, y0, 387.0, y0+0.75), BB)
        rect(p15, (387.0,  y0, 576.0, y0+0.75), BB)

# Right col section bars
# SOLUTION OUTPUT at 341.5 → bar at 350.5
rect(p15, (312.75, 350.5, 357.75, 352.75), OR)
# SAMPLE OUTPUT at 490.0 → bar at 499.0
rect(p15, (312.75, 499.0, 357.75, 501.25), OR)

# No Coding Required note box (dark blue) + yellow accent
rect(p15, (312.75, 618.0, 576.0, 676.5), DB)
rect(p15, (312.75, 618.0, 316.5, 676.5), YL)


# ── HEADER TEXT ──────────────────────────────────────────────────────────────
# Track label (spaced caps, YELLOW)
au(p15,  (36.0, 21.0),
   'P R O J E C T  S C E N A R I O  D  \u2014  T R A C K :  W O R K P L A C E  P R O B L E M  S O L V I N G',
   sz=8.0, clr=YL)
# Title line 1
hebo(p15, (36.0, 42.8), 'WORKPLACE PROBLEM SOLVING', sz=18.0, clr=OR)
# Title line 2
hebo(p15, (36.0, 63.0), '& APP CONCEPT DESIGN',      sz=18.0, clr=OR)
# Info bar (arialuni for en-dash and non-breaking spaces)
au(p15, (36.0, 80.5),
   'Host Company: Any Industry (Retail, Nonprofit, Operations, Services)'
   ' \xa0|\xa0 Duration: 6 Weeks \xa0|\xa0 Team Size: 1\u20135 Interns',
   sz=9.0, clr=WH)


# ── LEFT COLUMN ──────────────────────────────────────────────────────────────

# COMPANY BACKGROUND
hebo(p15, (36.0, 110.2), 'COMPANY BACKGROUND', sz=12.0, clr=OR)

cb = [
    "Your organization operates in a fast-paced environment where staff",
    "regularly face real-world challenges, from customer experience issues",
    "to operational inefficiencies. Many such challenges go undocumented",
    "and unanalyzed.",
    "",   # paragraph break
    "Your intern team will act as a workplace innovation team: identify a",
    "real problem within the organization, research its causes, and design",
    "a technology-enabled solution. Supervised by employer staff, with",
    "support from a DYCD-funded SYEP provider.",
]
y = 140.2
for line in cb:
    if line:
        helv(p15, (36.0, y), line)
    y += 13.5
# last body line at 140.2 + 8*13.5 = 248.2; y = 261.7

# THE CHALLENGE
hebo(p15, (36.0, 258.0), 'THE CHALLENGE', sz=11.0, clr=OR)

tc = [
    "Every workplace has problems that could be improved with better",
    "systems, tools, or workflows. Your intern team will:",
    "- Identify a real workplace challenge",
    "- Conduct structured research to understand the problem",
    "- Design a solution (app, tool, or system concept)",
    "- Present a clear proposal grounded in real user needs",
]
y = 288.0
for line in tc:
    helv(p15, (36.0, y), line)
    y += 13.5
# last at 288 + 5*13.5 = 355.5; y = 369.0

# INTERN MISSION BOX
# ★ bullet indicator (U+2605, present in arialuni) replacing ⚡
au(p15,  (51.8, 394.5), '\u2605', sz=8.5, clr=YL)
hebo(p15,(62.2, 394.5), ' Intern Mission:', sz=8.5, clr=YL)
helv(p15,(156.0,394.5), ' Research a real workplace challenge,', sz=8.5, clr=WH)
helv(p15,(51.8, 406.5), 'gather input from staff or customers, and design a', sz=8.5, clr=WH)
helv(p15,(51.8, 418.5), 'technology-based solution that improves how work gets done.', sz=8.5, clr=WH)

# RESEARCH APPROACH
hebo(p15, (36.0, 458.0), 'RESEARCH APPROACH', sz=11.0, clr=OR)

ra = [
    "Interns should gather information using accessible methods:",
    "- Staff interviews (2\u20135 employees)",
    "- Customer observations or feedback (if appropriate)",
    "- Simple surveys (paper or Google Forms)",
    "- Observation of daily workflows",
]
y = 488.0
for line in ra:
    if '\u2013' in line:
        au(p15, (36.0, y), line)
    else:
        helv(p15, (36.0, y), line)
    y += 13.5
# last at 488 + 4*13.5 = 542; y = 555.5

# EXAMPLE PROBLEM AREAS
hebo(p15, (36.0, 573.0), 'EXAMPLE PROBLEM AREAS', sz=11.0, clr=OR)

epa = [
    "- Long customer wait times (retail, service)",
    "- Inefficient scheduling or communication",
    "- Inventory tracking challenges",
    "- Customer feedback not being captured",
    "- Manual processes that could be streamlined",
]
y = 603.0
for line in epa:
    helv(p15, (36.0, y), line)
    y += 13.5


# ── RIGHT COLUMN ─────────────────────────────────────────────────────────────

# TEAM ROLES header
hebo(p15, (312.75, 108.8), 'TEAM ROLES', sz=11.0, clr=OR)

# Table column headers
hebo(p15, (319.5, 141.8), 'ROLE',             sz=7.5, clr=WH)
hebo(p15, (393.9, 141.8), 'RESPONSIBILITIES',  sz=7.5, clr=WH)

# Row data: (name_lines, resp_lines)  — text baselines = row_top + 14 for L1, +12 for L2
roles = [
    # row_top,  name_lines,                resp_lines
    (150.75, ['Project Manager'],          ['Coordinates timeline, assigns tasks,', 'and tracks progress']),
    (184.5,  ['Research Lead'],            ['Conducts interviews/surveys;', 'documents findings']),
    (218.25, ['Process Analyst'],          ['Maps current workflow;', 'identifies inefficiencies']),
    (252.0,  ['Solution', 'Designer'],     ['Designs app/tool concept;', 'sketches user flow']),
    (285.75, ['Presentation', 'Lead'],     ['Builds final deck and delivers pitch']),
]
for row_top, name_lines, resp_lines in roles:
    y0 = row_top + 14.2
    for i, nl in enumerate(name_lines):
        hebo(p15, (319.5, y0 + i*12), nl)
    for i, rl in enumerate(resp_lines):
        helv(p15, (393.9, y0 + i*12), rl)

# SOLUTION OUTPUT
hebo(p15, (312.75, 341.5), 'SOLUTION OUTPUT', sz=11.0, clr=OR)

so_lines = [
    (374.0, "Interns will design a concept-level solution, such as:", 'helv'),
    (387.5, "A mobile app concept for staff or customers",             'helv'),
    (401.0, "A digital workflow or tracking tool",                     'helv'),
    (414.5, "A communication or scheduling system",                    'helv'),
    (428.0, "A dashboard for monitoring operations",                   'helv'),
]
for y_, text, fn in so_lines:
    if fn == 'helv':
        helv(p15, (319.5, y_), text)
    else:
        hebo(p15, (319.5, y_), text)

hebo(p15, (319.5, 446.0), 'Tools (no coding required):')
helv(p15, (319.5, 459.5), 'Paper sketches / Google Slides / Canva / Figma (optional)')

# SAMPLE OUTPUT
hebo(p15, (312.75, 490.0), 'SAMPLE OUTPUT', sz=11.0, clr=OR)

hebo(p15, (319.5, 521.0), 'Example Outcome:')
sample = [
    (534.5, "At a retail store, interns found that employees spent"),
    (548.0, "15\u201320 minutes per shift manually checking inventory."),
    (561.5, "They designed a simple app concept for real-time"),
    (575.0, "updates, cutting this to under 5 minutes and"),
    (588.5, "improving accuracy across departments."),
]
for y_, text in sample:
    if '\u2013' in text:
        au(p15, (319.5, y_), text)
    else:
        helv(p15, (319.5, y_), text)

# NO CODING REQUIRED note box
au(p15,  (324.5, 636.0), '\u2605', sz=8.5, clr=YL)
hebo(p15,(335.0, 636.0), ' No Coding Required:', sz=8.5, clr=YL)
helv(p15,(324.5, 648.0), 'Interns are not expected to build a working app.', sz=8.5, clr=WH)
helv(p15,(324.5, 660.0), 'A well-researched concept, wireframe, or prototype', sz=8.5, clr=WH)
helv(p15,(324.5, 672.0), 'is sufficient to demonstrate the value of the solution.', sz=8.5, clr=WH)


# ── FOOTER ────────────────────────────────────────────────────────────────────
au(p15,   (36.0,  782.2),
   'NYC DYCD \u2014 Scenario D: Workplace Problem Solving & App Concept Design',
   sz=7.0, clr=WH)
hebo(p15, (566.9, 783.0), '15', sz=7.5, clr=YL)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  PAGE 16 — SCENARIO D  6-WEEK STRUCTURE                                 ║
# ╚══════════════════════════════════════════════════════════════════════════╝

p16 = doc.new_page(width=612, height=792)

# ── Background & structural fills ───────────────────────────────────────────
rect(p16, (0, 0,   612, 792),   WH)
rect(p16, (0, 0,   612,  40.5), DB)   # short header strip
rect(p16, (0, 769.5, 612, 792), DB)   # footer

# Yellow accent bar under title
rect(p16, (36, 81.75, 81, 84.0), YL)

# 6-week table – column header row
WCOL = [(36.0, 86.25), (86.25, 129.0), (129.0, 418.5), (418.5, 576.0)]
for x0, x1 in WCOL:
    rect(p16, (x0, 94.5, x1, 115.5), DB)

# 6-week table – data rows (53 pt each, alternating)
WK_ROWS = [
    (115.5,  168.5,  WH),   # W1
    (168.5,  221.5,  LB),   # W2
    (221.5,  274.5,  WH),   # W3
    (274.5,  327.5,  LB),   # W4
    (327.5,  380.5,  WH),   # W5
    (380.5,  433.5,  LB),   # W6
]
for x0, x1 in WCOL:
    for y0, y1, fill in WK_ROWS:
        rect(p16, (x0, y0, x1, y1), fill)

# Scope note box (left col) + yellow accent
rect(p16, (37.875, 645.75, 299.25, 706.5), DB)
rect(p16, (36,     645.75,  39.75, 706.5), YL)

# Program contacts box (right col)
rect(p16, (312.75, 607.5, 576.0, 706.5), DB)


# ── HEADER TEXT ──────────────────────────────────────────────────────────────
au(p16,  (36.0, 22.5),
   'SCENARIO D: WORKPLACE PROBLEM SOLVING \u2014 6-WEEK STRUCTURE & DELIVERABLES',
   sz=8.0, clr=YL)
hebo(p16,(567.1, 22.5), '16', sz=8.0, clr=WH)

hebo(p16, (36.0, 75.8), '6-WEEK PROJECT STRUCTURE', sz=15.0, clr=DB)

# Table column headers
hebo(p16, (42.8,  107.2), 'WEEK',        sz=7.5, clr=WH)
hebo(p16, (93.1,  107.2), 'PHASE',       sz=7.5, clr=WH)
hebo(p16, (136.0, 107.2), 'ACTIVITIES',  sz=7.5, clr=WH)
hebo(p16, (425.5, 107.2), 'DELIVERABLE', sz=7.5, clr=WH)


# ── 6-WEEK TABLE ROWS ─────────────────────────────────────────────────────────
# Each row: (week_label, phase_lines, act_lines, del_lines)
weeks = [
    (
        'Week 1',
        ['Explore'],
        [
            'Learn about company operations; observe daily workflows; identify',
            'potential challenges; assign team roles; set up project plan',
        ],
        ['List of 2\u20133 workplace', 'challenges'],
    ),
    (
        'Week 2',
        ['Explore', '+', 'Build'],
        [
            'Conduct staff interviews and surveys; analyze findings; draft problem',
            'statement; select focus area with supervisor feedback',
        ],
        ['Problem statement +', 'research summary'],
    ),
    (
        'Week 3',
        ['Build'],
        [
            'Map current workflow in detail; identify inefficiencies; brainstorm',
            'solution ideas; select concept direction with supervisor',
        ],
        ['Workflow map +', 'solution concept draft'],
    ),
    (
        'Week 4',
        ['Build +', 'Apply'],
        [
            'Design solution concept (sketches, wireframes, or slides); define key',
            'features; gather feedback from 2\u20133 staff; mid-program check-in',
        ],
        ['Draft solution design +', 'feedback notes; mid-program', 'self-assessment'],
    ),
    (
        'Week 5',
        ['Apply'],
        [
            'Refine solution based on feedback; create before/after comparison;',
            'build presentation deck; practice presenting with supervisor',
        ],
        ['Final solution concept +', 'presentation draft'],
    ),
    (
        'Week 6',
        ['Launch', '+', 'Reflect'],
        [
            'Present solution to employer leadership (10\u201315 min); receive feedback;',
            'complete DYCD exit survey; team debrief; write personal reflection',
        ],
        ['Final presentation +', 'personal reflection'],
    ),
]

for w_idx, (wk, phase, acts, deliv) in enumerate(weeks):
    row_top = WK_ROWS[w_idx][0]
    y0 = row_top + 12.7   # first text baseline in row

    # WEEK
    hebo(p16, (42.8, y0), wk, sz=8.0)

    # PHASE
    for i, ph in enumerate(phase):
        helv(p16, (93.1, y0 + i*11.3), ph, sz=8.0)

    # ACTIVITIES
    for i, act in enumerate(acts):
        if '\u2013' in act:
            au(p16, (136.0, y0 + i*11.3), act, sz=8.0)
        else:
            helv(p16, (136.0, y0 + i*11.3), act, sz=8.0)

    # DELIVERABLE
    for i, dl in enumerate(deliv):
        if '\u2013' in dl:
            au(p16, (425.5, y0 + i*11.3), dl, sz=8.0)
        else:
            helv(p16, (425.5, y0 + i*11.3), dl, sz=8.0)


# ── EXPECTED FINAL DELIVERABLES ───────────────────────────────────────────────
hebo(p16, (36.0, 459.0), 'EXPECTED FINAL DELIVERABLES', sz=10.0, clr=DB)

deliverables = [
    ('Problem Statement',     'clearly defined workplace challenge'),
    ('Research Summary',      'interviews, observations, or survey insights'),
    ('Workflow Map',          'current process documented and visualized'),
    ('Solution Concept',      'app, tool, or system design (no code required)'),
    ('Before/After Comparison','time saved, efficiency gained, or impact shown'),
    ('Final Presentation',    '10\u201315 slides delivered to employer'),
]

y_del = 476.2
for bold_label, body_text in deliverables:
    # checkmark
    au(p16,   (49.5, y_del), '\u2713', sz=9.0, clr=DK)
    helv(p16, (60.8, y_del), ' ', sz=9.0)
    # bold label + em-dash body (all through arialuni to handle any Unicode chars)
    label_end_x = 63.3 + fitz.get_text_length(bold_label, fontname='hebo', fontsize=9.0)
    hebo(p16, (63.3, y_del), bold_label, sz=9.0)
    au(p16, (label_end_x, y_del), ' \u2014 ' + body_text, sz=9.0, clr=DK)
    y_del += 29.3   # matches Scenario C inter-item spacing


# ── KEY LEARNING OUTCOMES ─────────────────────────────────────────────────────
hebo(p16, (311.2, 459.0), 'KEY LEARNING OUTCOMES', sz=10.0, clr=DB)

outcomes_rows = [
    [('317.2', 'PROBLEM SOLVING'),    ('420.0', 'USER RESEARCH')],
    [('317.2', 'PROCESS ANALYSIS'),   ('420.0', 'CRITICAL THINKING')],
    [('317.2', 'COMMUNICATION'),      ('420.0', 'DESIGN THINKING')],
    [('317.2', 'WORKPLACE COLLABORATION')],
]
y_pill = 476.2
for row in outcomes_rows:
    for xs, label in row:
        hebo(p16, (float(xs), y_pill), label, sz=7.0, clr=DB)
    y_pill += 18.8


# ── SCOPE NOTE BOX ────────────────────────────────────────────────────────────
au(p16,  (51.8, 663.75), '\u2605', sz=8.5, clr=YL)
hebo(p16,(62.2, 663.75), ' Scope Note:', sz=8.5, clr=YL)
helv(p16,(143.0,663.75), ' Interns are not expected to build', sz=8.5, clr=WH)
helv(p16,(51.8, 675.75), 'a working app or deploy a live system.', sz=8.5, clr=WH)
helv(p16,(51.8, 687.75), 'A researched concept or prototype is sufficient.', sz=8.5, clr=WH)


# ── PROGRAM CONTACTS ─────────────────────────────────────────────────────────
au(p16,  (321.8, 625.5), '\u260e', sz=8.0, clr=YL)     # ☎ phone symbol
hebo(p16,(334.0, 625.5), ' PROGRAM CONTACTS', sz=8.0, clr=YL)
helv(p16,(321.8, 643.5),
     'For DYCD SYEP support, compliance questions, or to report issues:',
     sz=8.0, clr=WH)
hebo(p16,(321.8, 657.0), 'DYCD Program Coordinator', sz=8.0, clr=WH)
au(p16,  (436.2, 657.0), ' \u2014 Contact via your program portal', sz=8.0, clr=WH)
hebo(p16,(321.8, 670.5), 'Urban Assembly (UA)', sz=8.0, clr=WH)
au(p16,  (403.6, 670.5), ' \u2014 urbanassembly.org', sz=8.0, clr=WH)
hebo(p16,(321.8, 684.0), 'The Knowledge House (TKH)', sz=8.0, clr=WH)
au(p16,  (431.5, 684.0), ' \u2014 theknowledgehouse.org', sz=8.0, clr=WH)
hebo(p16,(321.8, 697.5), 'DYCD Main Office', sz=8.0, clr=WH)
au(p16,  (389.7, 697.5), ' \u2014 dycd.nyc.gov', sz=8.0, clr=WH)


# ── FOOTER ────────────────────────────────────────────────────────────────────
au(p16,   (36.0,  782.2),
   'NYC DYCD \u2014 Scenario D: Workplace Problem Solving & App Concept Design',
   sz=7.0, clr=WH)
hebo(p16, (566.9, 783.0), '16', sz=7.5, clr=YL)


# ── SAVE ─────────────────────────────────────────────────────────────────────
doc.save(TMP, garbage=4, deflate=True)
doc.close()
os.replace(TMP, SRC)
print(f"Saved — now {fitz.open(SRC).page_count} pages.")
