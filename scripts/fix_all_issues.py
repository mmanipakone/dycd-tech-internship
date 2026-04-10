"""
fix_all_issues.py — v2: uses PDF redactions to permanently remove content.

The fundamental problem: paint-over hides text visually but it remains in the
PDF content stream and is still extractable. Only add_redact_annot +
apply_redactions() actually removes content from the stream.

Approach per page:
  1. add_redact_annot() for every zone that needs clearing
  2. apply_redactions() — permanently removes content, fills with white
  3. Paint colored backgrounds (cards, bars, boxes)
  4. Insert clean text
"""
import fitz, os

SRC = "revised_outputs/TechInternship_revised.pdf"
TMP = SRC + ".tmp"
AU  = '/Library/Fonts/Arial Unicode.ttf'

DB  = (0.03920, 0.14510, 0.25100)
OR  = (0.91000, 0.29410, 0.00000)
YL  = (1.00000, 0.90200, 0.00000)
WH  = (1.00000, 1.00000, 1.00000)
DK  = (26/255,  26/255,  26/255)
LG  = (0.886,   0.910,   0.941)
DR  = (0.102,   0.102,   0.102)

doc = fitz.open(SRC)


# ── Helpers ───────────────────────────────────────────────────────────────────
def redact(pg, rects):
    """Permanently remove all PDF content in given rects (text, graphics, images)."""
    for r in rects:
        pg.add_redact_annot(fitz.Rect(*r))
    pg.apply_redactions()

def paint(pg, rect, fill):
    s = pg.new_shape()
    s.draw_rect(fitz.Rect(*rect))
    s.finish(fill=fill, color=None)
    s.commit()

def txt(pg, xy, text, sz=8.5, font='helv', clr=None):
    pg.insert_text(xy, text, fontname=font, fontsize=sz,
                   color=clr if clr else DK)

def bold(pg, xy, text, sz=8.5, clr=None):
    txt(pg, xy, text, sz=sz, font='hebo', clr=clr)

def au(pg, xy, text, sz=9.0, clr=None):
    pg.insert_text(xy, text, fontname='arialuni', fontfile=AU,
                   fontsize=sz, color=clr if clr else DK)

def tw(text, font='helv', sz=8.0):
    return fitz.get_text_length(text, fontname=font, fontsize=sz)

def ctxt(pg, x0, x1, y, text, sz=8.0, font='helv', clr=WH):
    w = tw(text, font, sz)
    pg.insert_text(((x0 + x1) / 2 - w / 2, y), text,
                   fontname=font, fontsize=sz, color=clr)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — COVER: Restore yellow brand band
# ═══════════════════════════════════════════════════════════════════════════════
p0 = doc[0]

# Redact the band zone (removes old text, any image overflow)
redact(p0, [(0, 352, 612, 398)])

# Repaint brand band
paint(p0, (0, 352, 612, 398), YL)      # yellow base
paint(p0, (0, 352, 142, 398), DB)      # navy DYCD badge zone

# Insert cover image at corrected rect (stops above band)
new_cover = "studenttechpictures/241116_jca_inspiredu_1018_54364972816_l.jpg"
if os.path.exists(new_cover):
    p0.insert_image(fitz.Rect(0, 0, 612, 353), filename=new_cover,
                    keep_proportion=False, overlay=False)

# Brand text (white on navy)
bold(p0, (50, 369), "D Y C D", sz=7.5, clr=WH)
txt(p0,  (50, 383), "Department of Youth and Community Development", sz=7.5, clr=WH)

# Student Pathways logo (on yellow area)
logo_path = "Student Pathways Logos/PNG/NYCPS-Pathways-logo-white.png"
if os.path.exists(logo_path):
    p0.insert_image(fitz.Rect(440, 357, 576, 393),
                    filename=logo_path, keep_proportion=True, overlay=True)
print("✓ P1: Cover band restored")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — FULL LEFT COLUMN REBUILD + RIGHT COLUMN CLEANUP
# ═══════════════════════════════════════════════════════════════════════════════
p3 = doc[2]

# Redact all problem zones at once, then apply
redact(p3, [
    (36,  100, 312, 456),    # entire left column content
    (322, 236, 516, 266),    # right col: both age range versions
    (322, 300, 568, 328),    # right col: provider phrase
])

# ── Rebuild left column ───────────────────────────────────────────────────────
# 1. Intro paragraph
for i, line in enumerate([
    "Hosting a SYEP tech intern creates a mutually beneficial",
    "experience \u2014 interns gain real-world skills aligned to the",
    "Portrait of a Graduate, while employers gain fresh",
    "perspectives, expanded capacity, and a pipeline of diverse",
    "future talent.",
]):
    au(p3, (36, 130 + i * 15), line, sz=9.5, clr=DK)

# 2. Metric cards
LC_X0, LC_X1 = 36.0, 163.5
RC_X0, RC_X1 = 171.0, 298.5
CT, CB = 207.0, 264.0
LC_CTR, RC_CTR = (LC_X0 + LC_X1) / 2, (RC_X0 + RC_X1) / 2

paint(p3, (LC_X0 + 1, CT, LC_X1 - 1, CB), DB)
paint(p3, (RC_X0 + 1, CT, RC_X1 - 1, CB), DB)

for num_t, ctr in [("6", LC_CTR), ("25", RC_CTR)]:
    w = tw(num_t, 'hebo', 24.0)
    p3.insert_text((ctr - w / 2, 229), num_t, fontname='hebo', fontsize=24.0, color=YL)

for lbl, ctr, yl in [
    ("WEEKS OF STRUCTURED", LC_CTR, 243),
    ("LEARNING",             LC_CTR, 257),
    ("HOURS/WEEK",           RC_CTR, 243),
]:
    w = tw(lbl, 'helv', 8.0)
    p3.insert_text((ctr - w / 2, yl), lbl, fontname='helv', fontsize=8.0, color=WH)

# 3. Benefits header (orange bar)
paint(p3, (36, 271, 306, 292), OR)
bold(p3, (42, 286), "Benefits to Your Organization", sz=8.5, clr=WH)

# 4. Five bullets
BULLETS_P3 = [
    "Fresh perspectives and innovative ideas on real projects",
    "Expanded project capacity at no direct labor cost",
    "Early access to diverse NYC talent pipeline",
    "Strengthen community ties and corporate responsibility",
    "Mentor and support emerging talent",
]
MK_X0, MK_SZ, MK_STEP, FIRST_MK = 39.0, 3.0, 15.75, 305.0
for i, btext in enumerate(BULLETS_P3):
    my0 = FIRST_MK + i * MK_STEP
    my1 = my0 + MK_SZ
    ty  = (my0 + my1) / 2 + 2.25
    paint(p3, (MK_X0, my0, MK_X0 + MK_SZ, my1), DR)
    txt(p3, (49.5, ty), btext, sz=8.5, clr=DK)

# 5. Impact Statement box
IB_TOP, IB_BOT = 393.0, 450.0
paint(p3, (36, IB_TOP, 306, IB_BOT), LG)
paint(p3, (36, IB_TOP,  40, IB_BOT), OR)   # left accent
iy = IB_TOP + 13
bold(p3, (52, iy), "Impact Statement:", sz=8.5, clr=DB)
iy += 13
for line in [
    "Each intern you host supports a NYC student in developing",
    "skills needed to think critically, communicate effectively,",
    "and grow as a future-ready contributor.",
]:
    txt(p3, (52, iy), line, sz=8.5, clr=DK)
    iy += 13

# ── Right column fixes ────────────────────────────────────────────────────────
au(p3, (327, 257), "NYC high school students, ages 16\u201321", sz=9.0, clr=DK)
# Provider phrase zone left blank (already redacted)
print("✓ P3: Left column rebuilt, right column cleaned")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — WEEKLY SCHEDULE
# ═══════════════════════════════════════════════════════════════════════════════
p5 = doc[4]

redact(p5, [
    (36,  86, 576, 132),     # intro paragraph (both versions)
    (322, 346, 576, 408),    # Key Requirement box text area
])

# Intro paragraph (chained bold/regular)
y0 = 107.0
p1t = "Interns work "
p2t = "25 hours per week"
p3t = ". Below is the recommended daily structure across the 6-week program. Supervisors should"
txt(p5,  (36, y0), p1t, sz=8.5, clr=DK)
bold(p5, (36 + tw(p1t, 'helv', 8.5), y0), p2t, sz=8.5, clr=DK)
txt(p5,  (36 + tw(p1t, 'helv', 8.5) + tw(p2t, 'hebo', 8.5), y0), p3t, sz=8.5, clr=DK)
txt(p5,  (36, 120),
    "adjust based on project needs while maintaining the core learning structure.",
    sz=8.5, clr=DK)

# Key Requirement box — dark blue background, yellow accent, white text
KR_X0, KR_X1, KR_TOP, KR_BOT = 322.0, 576.0, 348.0, 408.0
paint(p5, (KR_X0, KR_TOP, KR_X1, KR_BOT), DB)
paint(p5, (KR_X0, KR_TOP, KR_X1, KR_TOP + 4), YL)
y = KR_TOP + 17
bold(p5, (KR_X0 + 6, y), "Key Requirement:", sz=8.0, clr=YL)
y += 13
txt(p5, (KR_X0 + 6, y),
    "All interns must maintain 25 hours/week. Attendance and", sz=8.0, clr=WH)
y += 13
txt(p5, (KR_X0 + 6, y),
    "punctuality are tracked by DYCD as compliance requirements.", sz=8.0, clr=WH)
print("✓ P5: Intro para and Key Requirement box fixed")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — TECHNICAL TRACKS: Remove duplicate Track D
# ═══════════════════════════════════════════════════════════════════════════════
p6 = doc[5]

redact(p6, [(308, 316, 576, 458)])

# Track D — single clean version
bold(p6, (322, 333), "Track D \u2014 Workplace Problem Solving & App Concept Design",
     sz=8.5, clr=DB)
for offset, line in enumerate([
    "Example project: Interns may identify a real workplace challenge,",
    "conduct research with staff or customers, and design a",
    "technology-enabled solution (app, tool, or system) to improve",
    "how work gets done.",
]):
    txt(p6, (313, 352 + offset * 13), line, sz=8.5, clr=DK)

# Single Project Selection note
paint(p6, (322, 416, 576, 458), LG)
bold(p6, (328, 430), "Project Selection", sz=8.0, clr=DB)
txt(p6,  (328, 443),
    "Employers are encouraged to design projects aligned to their", sz=8.0, clr=DK)
txt(p6,  (328, 455), "organization's work, using these examples as a starting point.",
    sz=8.0, clr=DK)
print("✓ P6: Track D deduplicated")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — SKILLS TABLE: Wipe old table, redraw new one
# ═══════════════════════════════════════════════════════════════════════════════
p7 = doc[6]

# Wider redact zone to catch all old table content (old right col reached x≈302+)
redact(p7, [(36, 158, 318, 402)])

TABLE_X0, TABLE_X1 = 36, 302
COL2_X = 155
HDR_H, ROW_H, TBL_TOP = 20, 32, 163

TABLE_DATA = [
    ("Effective Communicator",    "Stand-ups, presentations, written updates, email norms"),
    ("Global Citizen",            "Team roles, collaboration, group problem-solving, etiquette"),
    ("Critical Thinker",          "Project analysis, peer review, retrospectives, research"),
    ("Creative Innovator",        "Adapting scope, prototyping, exploring new approaches"),
    ("Reflective / Future Focused", "Goal-setting, time tracking, documentation, reflection"),
]

# Header
paint(p7, (TABLE_X0, TBL_TOP, TABLE_X1, TBL_TOP + HDR_H), DB)
bold(p7, (TABLE_X0 + 6, TBL_TOP + HDR_H - 5), "COMPETENCY",              sz=7.5, clr=WH)
bold(p7, (COL2_X + 5,   TBL_TOP + HDR_H - 5), "HOW INTERNS DEVELOP THIS", sz=7.5, clr=WH)

# Border
s = p7.new_shape()
s.draw_rect(fitz.Rect(TABLE_X0, TBL_TOP, TABLE_X1,
                       TBL_TOP + HDR_H + len(TABLE_DATA) * ROW_H))
s.finish(color=(0.70, 0.72, 0.75), width=0.75, fill=None)
s.commit()

# Rows
ry = TBL_TOP + HDR_H
for i, (label, content) in enumerate(TABLE_DATA):
    paint(p7, (TABLE_X0, ry, TABLE_X1, ry + ROW_H),
          (0.953, 0.965, 0.984) if i % 2 == 1 else WH)
    paint(p7, (COL2_X, ry, COL2_X + 0.5, ry + ROW_H), (0.75, 0.77, 0.80))
    paint(p7, (TABLE_X0, ry + ROW_H - 0.5, TABLE_X1, ry + ROW_H), (0.78, 0.80, 0.83))
    mid = ry + ROW_H / 2 + 3
    bold(p7, (TABLE_X0 + 6, mid), label,   sz=7.0, clr=DB)
    txt(p7,  (COL2_X + 5,   mid), content, sz=7.0, clr=DK)
    ry += ROW_H
print(f"✓ P7: Table rebuilt y={TBL_TOP}–{ry}")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 8 — REQUIRED DOCUMENTATION
# ═══════════════════════════════════════════════════════════════════════════════
p8 = doc[7]

# Redact wide enough to cover "Any workplace incidents within 24 hrs" (extends to ~x580)
redact(p8, [(318, 236, 585, 288)])

# Single clean Incident Reports line
bold(p8, (326, 252), "Incident Reports:", sz=9.0, clr=DK)
txt(p8,  (408, 252),
    "Any workplace incidents must be reported within 24 hrs", sz=9.0, clr=DK)
print("✓ P8: Exit Survey removed, Incident Reports deduplicated")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 9 — CYBERSECURITY SCENARIO
# ═══════════════════════════════════════════════════════════════════════════════
p9 = doc[8]

redact(p9, [
    (36,  210, 455, 243),    # provider language (last 2 lines of company background)
    (270, 546, 582, 642),    # friction log guidance (all 3 duplicate versions)
])

# Clean ending for company background paragraph
txt(p9, (36, 223),
    "will act as a junior cybersecurity task force, supervised by employer staff.",
    sz=8.5, clr=DK)

# Friction log guidance — single clean version
gy = 562.0
txt(p9, (274, gy), "Use the friction log to record events and identify patterns.", sz=8.5, clr=DK)
gy += 17
txt(p9, (274, gy), "Consider:", sz=8.5, clr=DK)
gy += 13
for item in [
    "\u2022  What were you expecting?",
    "\u2022  What patterns or anomalies stand out?",
    "\u2022  What would you flag or investigate next?",
]:
    txt(p9, (280, gy), item, sz=8.5, clr=DK)
    gy += 13
print("✓ P9: Provider phrase removed, friction log deduplicated")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 13 — WORKFLOW SCENARIO: Remove overlapping Example Outcome
# ═══════════════════════════════════════════════════════════════════════════════
p13 = doc[12]

redact(p13, [
    (308, 507, 582, 587),    # old Example Outcome (inside image area)
    (36,  42,  576,  62),    # header line (team size clipped)
])

# Clean header line
txt(p13, (36, 57),
    "Host Company: BrightPath (Tech Consulting Firm)  \u2502  Duration: 6 Weeks  \u2502  Team Size: 1\u20135 Interns",
    sz=9.0, clr=DK)
# Clean version at y=655+ already present from apply_all_revisions.py — kept
print("✓ P13: Overlapping Example Outcome removed, team size fixed")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 14 — PROGRAM CONTACTS
# ═══════════════════════════════════════════════════════════════════════════════
p14 = doc[13]

redact(p14, [(318, 626, 585, 678)])

bold(p14, (322, 643), "SYEP Provider", sz=8.0, clr=DK)
txt(p14,  (406, 643),
    "\u2014 contact information available via your worksite portal", sz=8.0, clr=DK)
bold(p14, (322, 657), "DYCD", sz=8.0, clr=DK)
txt(p14,  (344, 657), "\u2014 nyc.gov/dycd  |  1-800-246-4646", sz=8.0, clr=DK)
print("✓ P14: Contacts cleaned")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 15 — REMOVE PROVIDER LANGUAGE
# ═══════════════════════════════════════════════════════════════════════════════
p15 = doc[14]

redact(p15, [(36, 191, 576, 222)])

# Reinsert without "DYCD-funded SYEP provider support"
txt(p15, (36, 203),
    "Your intern team will identify a real problem, research its causes, and design a",
    sz=8.5, clr=DK)
txt(p15, (36, 216),
    "technology-enabled solution, supervised by employer staff.",
    sz=8.5, clr=DK)
print("✓ P15: Provider language removed")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 16 — FULL LOWER HALF REBUILD
# ═══════════════════════════════════════════════════════════════════════════════
p16 = doc[15]

redact(p16, [
    (36,  50,  400,  78),    # duplicate section title
    (36, 434, 576, 708),     # entire lower half (deliverables, pills, contacts)
])

# ── Section title (sentence case, once) ───────────────────────────────────────
bold(p16, (36, 72), "6-Week Project Structure", sz=15.0, clr=DK)

# ══ LEFT — Expected Final Deliverables ═══════════════════════════════════════
paint(p16, (36, 440, 295, 460), OR)
bold(p16, (42, 455), "Expected Final Deliverables", sz=9.0, clr=WH)

DELIVERABLES_16 = [
    ("Problem Statement",       "\u2014 clearly defined challenge with supporting evidence"),
    ("Research Summary",        "\u2014 interviews, observations, insights"),
    ("Workflow Map",            "\u2014 current process visualization"),
    ("Solution Concept",        "\u2014 app / tool / system design"),
    ("Before/After Comparison", "\u2014 time saved or impact shown"),
    ("Final Presentation",      "\u2014 10\u201315 slides"),
]
dy = 473.0
for label, desc in DELIVERABLES_16:
    check = "\u2713  "
    bold(p16, (50, dy), check + label, sz=8.5, clr=DB)
    lw = tw(check + label, 'hebo', 8.5)
    txt(p16, (50 + lw, dy), " " + desc, sz=8.5, clr=DK)
    dy += 16.0

# Scope Note box
SN_TOP = dy + 8
SN_BOT = SN_TOP + 54
paint(p16, (36, SN_TOP, 295, SN_BOT), LG)
paint(p16, (36, SN_TOP,  40, SN_BOT), OR)
sy = SN_TOP + 14
bold(p16, (48, sy), "Prototype Scope Note:", sz=8.0, clr=DB)
sy += 13
txt(p16, (48, sy),
    "Interns are not expected to build a working app or deploy", sz=8.0, clr=DK)
sy += 12
txt(p16, (48, sy),
    "a live system. A researched concept or prototype is sufficient.", sz=8.0, clr=DK)

# ══ RIGHT — Key Learning Outcomes ════════════════════════════════════════════
paint(p16, (305, 440, 576, 460), OR)
bold(p16, (311, 455), "Key Learning Outcomes", sz=9.0, clr=WH)

PILLS_16 = [
    ("PROBLEM SOLVING",         "USER RESEARCH"),
    ("PROCESS ANALYSIS",        "CRITICAL THINKING"),
    ("COMMUNICATION",           "DESIGN THINKING"),
    ("WORKPLACE COLLABORATION",  None),
]
P_X0, P_X1 = 311, 576
P_MID = (P_X0 + P_X1) // 2   # 443
ply = 472.0

for left_p, right_p in PILLS_16:
    lw = tw(left_p, 'hebo', 6.5) + 10
    paint(p16, (P_X0,    ply - 9, P_X0 + lw,    ply + 4), YL)
    bold(p16,  (P_X0 + 5, ply),   left_p, sz=6.5, clr=DK)
    if right_p:
        rw = tw(right_p, 'hebo', 6.5) + 10
        paint(p16, (P_MID,    ply - 9, P_MID + rw,   ply + 4), YL)
        bold(p16,  (P_MID + 5, ply),  right_p, sz=6.5, clr=DK)
    ply += 20.0

# Program Contacts
CY = ply + 14
bold(p16, (311, CY), "Program Contacts", sz=8.5, clr=DB)
CY += 13
txt(p16,  (311, CY),
    "For DYCD SYEP support, compliance questions, or to report issues:",
    sz=8.0, clr=DK)
CY += 13
bold(p16, (311, CY), "SYEP Provider", sz=8.0, clr=DK)
txt(p16,  (393, CY), "\u2014 contact via your SYEP worksite portal", sz=8.0, clr=DK)
CY += 12
bold(p16, (311, CY), "DYCD", sz=8.0, clr=DK)
txt(p16,  (333, CY), "\u2014 nyc.gov/dycd  |  1-800-246-4646", sz=8.0, clr=DK)

print(f"✓ P16: Lower half rebuilt (deliverables y=473–{dy:.0f}, scope note y={SN_TOP:.0f})")


# ═══════════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════════
doc.save(TMP, garbage=4, deflate=True)
doc.close()
os.replace(TMP, SRC)
print(f"\n✅  Saved → {SRC}")
