"""
global_sentence_case.py
Applies:
1. Global ALL CAPS → sentence case (16 pages)
2. Page 9: Security Analyst description fix + Data Analyst row insertion
3. Page 14: Program Contacts box rebuild (correct wording + colors)
4. Page 16: Program Contacts update + Employer Feedback line
"""
import fitz, os

SRC = "revised_outputs/TechInternship_revised.pdf"
TMP = SRC + ".tmp"

AB  = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
AU  = "/Library/Fonts/Arial Unicode.ttf"

DB   = (0.03920, 0.14510, 0.25100)
DB2  = (0.059,   0.204,   0.377  )  # P4 phase-4 col-1 shade
OR   = (0.91000, 0.29410, 0.00000)
OR2  = (0.788,   0.251,   0.0    )  # P4 phase-header col-2 shade
OR3  = (0.659,   0.208,   0.0    )  # P4 phase-header col-3 shade
YL   = (1.00000, 0.90200, 0.00000)
WH   = (1.00000, 1.00000, 1.00000)
DK   = (26/255,  26/255,  26/255 )
LB   = (0.969,   0.973,   0.980  )

doc = fitz.open(SRC)


def paint(pg, rect, fill):
    s = pg.new_shape()
    s.draw_rect(fitz.Rect(*rect))
    s.finish(fill=fill, color=None)
    s.commit()


def ab(pg, xy, text, sz, clr=WH):
    """Arial Bold"""
    pg.insert_text(xy, text, fontname='arialbold', fontfile=AB, fontsize=sz, color=clr)


def hebo(pg, xy, text, sz, clr=WH):
    """Helvetica Bold (built-in)"""
    pg.insert_text(xy, text, fontname='hebo', fontsize=sz, color=clr)


def helv(pg, xy, text, sz, clr=DK):
    """Helvetica (built-in)"""
    pg.insert_text(xy, text, fontname='helv', fontsize=sz, color=clr)


def au(pg, xy, text, sz, clr=WH):
    """Arial Unicode (for emoji support)"""
    pg.insert_text(xy, text, fontname='arialuni', fontfile=AU, fontsize=sz, color=clr)


def bl(y_top, sz, r=0.91):
    """Baseline from bbox_top."""
    return y_top + sz * r


# ══════════════════════════════════════════════════════════════════
# PAGE 1  (idx 0) — footer only
# ══════════════════════════════════════════════════════════════════
p = doc[0]
p.add_redact_annot(fitz.Rect(43, 767, 585, 779))
p.apply_redactions(images=0, graphics=0)
paint(p, (0, 769.5, 612, 792), DB)
ab(p, (43.2, bl(771.3, 8)),
   "New York City Department of Youth & Community Development", 8, WH)
print("✓ P1: footer updated")


# ══════════════════════════════════════════════════════════════════
# PAGE 2  (idx 1)
# ══════════════════════════════════════════════════════════════════
p = doc[1]
p.add_redact_annot(fitz.Rect(36,  11, 450,  26))   # TABLE OF CONTENTS
p.add_redact_annot(fitz.Rect(36,  63, 250, 106))   # WHAT'S / INSIDE
p.apply_redactions(images=0, graphics=0)
paint(p, (0, 0, 612, 40.5), DB)
ab(p, (36, bl(15.3, 8)),   "Table of contents",  8,  YL)
ab(p, (36, bl(67.7, 18)),  "What's",             18, OR)
ab(p, (36, bl(87.2, 18)),  "inside",             18, OR)
print("✓ P2: running head + section title updated")


# ══════════════════════════════════════════════════════════════════
# PAGE 3  (idx 2)
# ══════════════════════════════════════════════════════════════════
p = doc[2]
p.add_redact_annot(fitz.Rect(36,   11, 450,  26))   # running head
p.add_redact_annot(fitz.Rect(36,   64, 300,  86))   # WHY HOST A
p.add_redact_annot(fitz.Rect(313,  67, 576,  84))   # PORTRAIT OF A SYEP TECH INTERN
p.add_redact_annot(fitz.Rect(37,  229, 310, 260))   # WEEKS OF STRUCTURED / LEARNING / HOURS/WEEK
p.apply_redactions(images=0, graphics=0)
paint(p, (0, 0, 612, 40.5), DB)
ab(p, (36,   bl(15.3, 8)),  "Why host + portrait of an intern", 8,  YL)
ab(p, (36,   bl(68.8, 16)), "Why host a",                       16, OR)
ab(p, (313.5, bl(72.1, 14)), "Portrait of a SYEP tech intern",  14, OR)
# stat blocks (WH on DB)
paint(p, (37.0,  207.0, 162.5, 264.0), DB)
paint(p, (172.0, 207.0, 297.5, 264.0), DB)
helv(p, (50,   bl(234.4, 8)), "Weeks of structured", 8, WH)
helv(p, (79,   bl(248.4, 8)), "learning",            8, WH)
helv(p, (207,  bl(234.4, 8)), "Hours/week",          8, WH)
print("✓ P3: all headers updated")


# ══════════════════════════════════════════════════════════════════
# PAGE 4  (idx 3)
# ══════════════════════════════════════════════════════════════════
p = doc[3]
p.add_redact_annot(fitz.Rect(36,  11, 500,  26))   # running head
p.add_redact_annot(fitz.Rect(36,  57, 300,  78))   # THE 6-WEEK JOURNEY
# Phase column headers (section 1, y=95–128)
p.add_redact_annot(fitz.Rect(36,  96, 212, 128))   # col-1: PHASE 1, WEEKS 1–2
p.add_redact_annot(fitz.Rect(218, 96, 394, 128))   # col-2: PHASE 2, WEEKS 3–4
p.add_redact_annot(fitz.Rect(400, 96, 576, 128))   # col-3: PHASE 3, WEEK 5
# Phase column headers (section 2, y=302–335)
p.add_redact_annot(fitz.Rect(36,  303, 212, 335))  # col-1: PHASE 4, WEEK 5 CONT.
p.add_redact_annot(fitz.Rect(218, 303, 394, 335))  # col-2: PHASE 5, WEEK 6
p.add_redact_annot(fitz.Rect(400, 303, 576, 335))  # col-3: KEY DELIVERABLES, ALL 6 WEEKS
p.apply_redactions(images=0, graphics=0)
paint(p, (0, 0, 612, 40.5), DB)
ab(p, (36,  bl(15.3, 8)),  "The 6-week internship journey", 8,  YL)
ab(p, (36,  bl(61.3, 16)), "The 6-week journey",            16, OR)
# Repaint section-1 column header backgrounds
paint(p, (36.0,  95.2, 212.2, 128.2), OR)
paint(p, (218.2, 95.2, 393.8, 128.2), OR2)
paint(p, (399.8, 95.2, 576.0, 128.2), OR3)
# Repaint section-2 column header backgrounds
paint(p, (36.0,  302.2, 212.2, 335.2), DB2)
paint(p, (218.2, 302.2, 393.8, 335.2), DB)
paint(p, (399.8, 302.2, 576.0, 335.2), YL)
# Section-1 phase labels (sz=8, WH)
ab(p, (43.5,  bl(101.5, 8)), "Phase 1 \u2014 Explore", 8, WH)
ab(p, (225.5, bl(101.5, 8)), "Phase 2 \u2014 Build",   8, WH)
ab(p, (407.5, bl(101.5, 8)), "Phase 3 \u2014 Apply",   8, WH)
# Section-1 sub-labels (sz=7)
ab(p, (43.5,  bl(113.7, 7)), "Weeks 1\u20132", 7, WH)
ab(p, (225.5, bl(113.7, 7)), "Weeks 3\u20134", 7, WH)
ab(p, (407.5, bl(113.7, 7)), "Week 5",          7, WH)
# Section-2 phase labels (sz=8)
ab(p, (43.5,  bl(308.5, 8)), "Phase 4 \u2014 Reflect", 8, WH)
ab(p, (225.5, bl(308.5, 8)), "Phase 5 \u2014 Launch",  8, WH)
ab(p, (407.5, bl(308.5, 8)), "Key deliverables",        8, DB)
# Section-2 sub-labels (sz=7)
ab(p, (43.5,  bl(320.7, 7)), "Week 5 (cont.)", 7, WH)
ab(p, (225.5, bl(320.7, 7)), "Week 6",          7, WH)
ab(p, (407.5, bl(320.7, 7)), "All 6 weeks",     7, (0.20, 0.20, 0.20))
print("✓ P4: all headers updated")


# ══════════════════════════════════════════════════════════════════
# PAGE 5  (idx 4)
# ══════════════════════════════════════════════════════════════════
p = doc[4]
p.add_redact_annot(fitz.Rect(36,  11, 500,  26))   # running head
p.add_redact_annot(fitz.Rect(36,  58, 280,  78))   # WEEKLY SCHEDULE
p.add_redact_annot(fitz.Rect(36, 129,  86, 157))   # TIME / BLOCK
p.add_redact_annot(fitz.Rect(86, 129, 576, 157))   # MONDAY–FRIDAY headers
p.add_redact_annot(fitz.Rect(36, 323, 600, 340))   # WEEKLY HOURS BREAKDOWN + 6-WEEK HOUR TOTAL
p.add_redact_annot(fitz.Rect(36, 347, 305, 370))   # ACTIVITY CATEGORY + HOURS/WEEK + % OF TIME
p.apply_redactions(images=0, graphics=0)
paint(p, (0, 0, 612, 40.5), DB)
ab(p, (36, bl(15.3, 8)),  "Weekly schedule & 25-hour breakdown", 8, YL)
ab(p, (36, bl(62.2, 15)), "Weekly schedule",                     15, OR)
# TIME/BLOCK (WH on OR)
paint(p, (36.0, 129.0, 86.2, 156.8), OR)
ab(p, (52.8, bl(133.2, 7)), "Time",  7, WH)
ab(p, (48.6, bl(142.9, 7)), "block", 7, WH)
# Day name headers (DB on YL)
paint(p, (86.2,  129.0, 184.5, 156.8), YL)
paint(p, (184.5, 129.0, 282.0, 156.8), YL)
paint(p, (282.0, 129.0, 380.2, 156.8), YL)
paint(p, (380.2, 129.0, 477.8, 156.8), YL)
paint(p, (477.8, 129.0, 576.0, 156.8), YL)
ab(p, (119.8, bl(133.2, 7)), "Monday",    7, DB)
ab(p, (216.5, bl(133.2, 7)), "Tuesday",   7, DB)
ab(p, (308.1, bl(133.2, 7)), "Wednesday", 7, DB)
ab(p, (409.5, bl(133.2, 7)), "Thursday",  7, DB)
ab(p, (514.0, bl(133.2, 7)), "Friday",    7, DB)
# Section headers (DB text on WH — no repaint needed)
ab(p, (36,    bl(326.9, 10)), "Weekly hours breakdown",    10, DB)
ab(p, (310.5, bl(326.9, 10)), "6-week hour total: 150 hrs", 10, DB)
# Activity table headers (WH on DB)
paint(p, (36.0,  347.2, 173.2, 369.0), DB)
paint(p, (173.2, 347.2, 243.8, 369.0), DB)
paint(p, (243.8, 347.2, 301.5, 369.0), DB)
ab(p, (42.8,  bl(353.2, 7.5)), "Activity category", 7.5, WH)
ab(p, (180.2, bl(353.2, 7.5)), "Hours/week",         7.5, WH)
ab(p, (250.8, bl(353.2, 7.5)), "% of time",          7.5, WH)
print("✓ P5: all headers updated")


# ══════════════════════════════════════════════════════════════════
# PAGE 6  (idx 5)
# ══════════════════════════════════════════════════════════════════
p = doc[5]
p.add_redact_annot(fitz.Rect(36,  11, 500,  26))   # running head
p.add_redact_annot(fitz.Rect(36,  65, 360,  82))   # TECHNICAL SKILLS FRAMEWORK
p.add_redact_annot(fitz.Rect(36, 155, 290, 172))   # CYBERSECURITY + DATA ANALYTICS
p.add_redact_annot(fitz.Rect(36, 341, 295, 374))   # WORKFLOW/AUTOMATION + WEB & CODING
p.apply_redactions(images=0, graphics=0)
paint(p, (0, 0, 612, 40.5), DB)
ab(p, (36,    bl(15.3,  8)),   "Technical skills & project tracks", 8,   YL)
ab(p, (36,    bl(69.7,  15)),  "Technical skills framework",        15,  OR)
ab(p, (57.4,  bl(159.6, 8.5)), "Cybersecurity",                     8.5, OR)
ab(p, (192.0, bl(159.6, 8.5)), "Data analytics",                    8.5, OR)
ab(p, (57.4,  bl(346.3, 8.5)), "Workflow",                          8.5, OR)
ab(p, (46.5,  bl(359.1, 8.5)), "automation",                        8.5, OR)
ab(p, (192.0, bl(346.3, 8.5)), "Web & coding",                      8.5, OR)
print("✓ P6: all headers updated")


# ══════════════════════════════════════════════════════════════════
# PAGE 7  (idx 6)
# ══════════════════════════════════════════════════════════════════
p = doc[6]
p.add_redact_annot(fitz.Rect(36,  11, 575,  26))   # running head
p.add_redact_annot(fitz.Rect(36,  65, 305, 100))   # WORKPLACE & PROFESSIONAL / SKILLS
p.add_redact_annot(fitz.Rect(312, 67, 576,  84))   # SUPERVISION BEST PRACTICES
p.add_redact_annot(fitz.Rect(36, 162, 302, 184))   # COMPETENCY + HOW INTERNS DEVELOP THIS
p.apply_redactions(images=0, graphics=0)
paint(p, (0, 0, 612, 40.5), DB)
ab(p,   (36,    bl(15.3, 8)),   "Professional skills + supervision best practices", 8,  YL)
ab(p,   (36,    bl(69.7, 15)),  "Workplace & professional",                         15, OR)
ab(p,   (36,    bl(86.2, 15)),  "skills",                                           15, OR)
ab(p,   (312.8, bl(72.1, 14)),  "Supervision best practices",                       14, OR)
# Table header (WH on DB)
paint(p, (36.0, 163.0, 302.0, 183.0), DB)
hebo(p, (42,  bl(170.0, 7.5)), "Competency",             7.5, WH)
hebo(p, (160, bl(170.0, 7.5)), "How interns develop this", 7.5, WH)
print("✓ P7: all headers updated")


# ══════════════════════════════════════════════════════════════════
# PAGE 8  (idx 7)
# ══════════════════════════════════════════════════════════════════
p = doc[7]
p.add_redact_annot(fitz.Rect(36,  11, 500,  26))   # running head
p.add_redact_annot(fitz.Rect(36,  65, 300,  82))   # IMPLEMENTATION TOOLS
p.add_redact_annot(fitz.Rect(36,  99, 310, 115))   # RECOMMENDED DIGITAL TOOLS
p.add_redact_annot(fitz.Rect(312, 67, 576,  84))   # DYCD COMPLIANCE REQUIREMENTS
p.add_redact_annot(fitz.Rect(36, 124, 300, 146))   # CATEGORY + TOOLS
p.add_redact_annot(fitz.Rect(36, 353, 260, 368))   # ONBOARDING CHECKLIST
p.add_redact_annot(fitz.Rect(312, 162, 576, 178))  # REQUIRED DOCUMENTATION
p.add_redact_annot(fitz.Rect(312, 275, 576, 293))  # WORKPLACE SAFETY & CONDUCT
p.apply_redactions(images=0, graphics=0)
paint(p, (0, 0, 612, 40.5), DB)
ab(p, (36,    bl(15.3,  8)),  "Implementation tools + compliance",  8,  YL)
ab(p, (36,    bl(69.7,  15)), "Implementation tools",               15, OR)
ab(p, (36,    bl(103.4, 10)), "Recommended digital tools",          10, DB)
ab(p, (312.8, bl(72.1,  14)), "DYCD compliance requirements",       14, OR)
ab(p, (36,    bl(357.7, 10)), "Onboarding checklist",               10, DB)
ab(p, (312.8, bl(166.4, 10)), "Required documentation",             10, DB)
ab(p, (312.8, bl(280.0, 10)), "Workplace safety & conduct",         10, DB)
# CATEGORY/TOOLS table header (WH on DB)
paint(p, (36.0,  123.8, 131.2, 144.8), DB)
paint(p, (131.2, 123.8, 299.2, 144.8), DB)
ab(p, (42.8,  bl(129.7, 7.5)), "Category", 7.5, WH)
ab(p, (137.7, bl(129.7, 7.5)), "Tools",    7.5, WH)
print("✓ P8: all headers updated")


# ══════════════════════════════════════════════════════════════════
# PAGE 9  (idx 8)  — Scenario A  (DO NOT touch letter-spaced banner)
# ══════════════════════════════════════════════════════════════════
p = doc[8]
# Orange/white-bg text in banner (repaint needed)
p.add_redact_annot(fitz.Rect(36,  22, 400,  58))   # CYBERSECURITY TABLETOP + INVESTIGATION
# Orange/white-bg section headers (below banner, white bg — no repaint)
p.add_redact_annot(fitz.Rect(36, 114, 270, 132))   # COMPANY BACKGROUND
p.add_redact_annot(fitz.Rect(273, 113, 435, 131))  # TEAM ROLES
p.add_redact_annot(fitz.Rect(36, 239, 270, 258))   # THE CHALLENGE
p.add_redact_annot(fitz.Rect(273, 347, 440, 365))  # FRICTION LOG TEMPLATE
p.add_redact_annot(fitz.Rect(36, 435, 220, 453))   # DATASET OPTIONS
# Team roles table header (WH on DB, y=149.2–170.2)
p.add_redact_annot(fitz.Rect(273, 149, 576, 171))
# Friction log column headers (WH on DB, y=383.2–415.5)
p.add_redact_annot(fitz.Rect(273, 383, 576, 416))
# Security Analyst responsibilities (replace description only)
p.add_redact_annot(fitz.Rect(359, 170, 577, 204))
p.apply_redactions(images=0, graphics=0)
# Repaint banner zone for subtitle text
paint(p, (0,     26,    612,   58   ), DB)
# Repaint team roles header row
paint(p, (273.8, 149.2, 359.2, 170.2), DB)
paint(p, (359.2, 149.2, 576.0, 170.2), DB)
# Repaint friction log header cells
paint(p, (273.8, 383.2, 291.8, 415.5), DB)
paint(p, (291.8, 383.2, 352.5, 415.5), DB)
paint(p, (352.5, 383.2, 387.8, 415.5), DB)
paint(p, (387.8, 383.2, 441.0, 415.5), DB)
paint(p, (441.0, 383.2, 481.5, 415.5), DB)
paint(p, (481.5, 383.2, 534.8, 415.5), DB)
paint(p, (534.8, 383.2, 576.0, 415.5), DB)
# Reinsert banner titles (OR on DB)
ab(p, (36, bl(26.5, 18)), "Cybersecurity tabletop",          18, OR)
ab(p, (36, bl(46.0, 18)), "investigation + friction log",    18, OR)
# Section headers (OR on WH)
ab(p, (36,    bl(118.9, 12)), "Company background",     12, OR)
ab(p, (273.6, bl(118.3, 11)), "Team roles",             11, OR)
ab(p, (36,    bl(244.1, 12)), "The challenge",          12, OR)
ab(p, (273.6, bl(352.3, 11)), "Friction log template",  11, OR)
ab(p, (36,    bl(439.3, 11)), "Dataset options",        11, OR)
# Table headers
ab(p, (280.4, bl(155.2, 7.5)), "Role",             7.5, WH)
ab(p, (365.6, bl(155.2, 7.5)), "Responsibilities", 7.5, WH)
# Friction log headers
ab(p, (298.4, bl(394.5, 7.5)), "Timestamp", 7.5, WH)
ab(p, (358.9, bl(389.2, 7.5)), "User",      7.5, WH)
ab(p, (394.8, bl(399.7, 7.5)), "address",   7.5, WH)
ab(p, (447.6, bl(389.2, 7.5)), "Event",     7.5, WH)
ab(p, (447.6, bl(399.7, 7.5)), "type",      7.5, WH)
ab(p, (487.9, bl(394.5, 7.5)), "Severity",  7.5, WH)
ab(p, (541.5, bl(394.5, 7.5)), "Notes",     7.5, WH)
# ── Security Analyst: new description (row 1, white bg)
helv(p, (365.6, bl(176.1, 8.5)),
     "Reviews login data to identify suspicious activity,", 8.5, DK)
helv(p, (365.6, bl(188.8, 8.5)),
     "flags anomalies, and documents potential security risks", 8.5, DK)
# ── Data Analyst: insert into empty row 2 (LB background, y=204–238.5)
helv(p, (280.4, bl(210.0, 8.5)), "Data Analyst",                                   8.5, DK)
helv(p, (365.6, bl(210.0, 8.5)), "Cleans and organizes dataset; builds charts",    8.5, DK)
helv(p, (365.6, bl(223.5, 8.5)), "showing login trends over time",                 8.5, DK)
print("✓ P9: sentence case + Security Analyst + Data Analyst updated")


# ══════════════════════════════════════════════════════════════════
# PAGE 10  (idx 9)  — Scenario A deliverables/structure
# ══════════════════════════════════════════════════════════════════
p = doc[9]
p.add_redact_annot(fitz.Rect(36,  11, 576,  26))   # running head
p.add_redact_annot(fitz.Rect(36,  58, 300,  78))   # 6-WEEK PROJECT STRUCTURE
p.add_redact_annot(fitz.Rect(36,  95, 576, 116))   # WEEK/PHASE/ACTIVITIES/DELIVERABLE
p.add_redact_annot(fitz.Rect(36, 389, 300, 405))   # EXPECTED FINAL DELIVERABLES
p.add_redact_annot(fitz.Rect(311, 471, 576, 487))  # KEY LEARNING OUTCOMES
# KLO label tags (DB on YL)
p.add_redact_annot(fitz.Rect(311, 490, 576, 510))  # row 1 labels
p.add_redact_annot(fitz.Rect(311, 508, 576, 528))  # row 2 labels
p.add_redact_annot(fitz.Rect(311, 526, 576, 546))  # row 3 labels
p.add_redact_annot(fitz.Rect(311, 544, 576, 564))  # row 4 labels
p.apply_redactions(images=0, graphics=0)
paint(p, (0, 0, 612, 40.5), DB)
ab(p, (36,    bl(15.3,  8)),  "Scenario A: Cybersecurity \u2014 6-week structure & deliverables", 8,  YL)
ab(p, (36,    bl(62.2,  15)), "6-week project structure",   15, OR)
# Table column headers (WH on DB)
paint(p, (36.0,  94.5, 86.2,  115.5), DB)
paint(p, (86.2,  94.5, 129.8, 115.5), DB)
paint(p, (129.8, 94.5, 418.5, 115.5), DB)
paint(p, (418.5, 94.5, 576.0, 115.5), DB)
ab(p, (42.8,  bl(100.5, 7.5)), "Week",        7.5, WH)
ab(p, (93.1,  bl(100.5, 7.5)), "Phase",       7.5, WH)
ab(p, (136.2, bl(100.5, 7.5)), "Activities",  7.5, WH)
ab(p, (424.9, bl(100.5, 7.5)), "Deliverable", 7.5, WH)
# Section headers (DB on WH — no repaint)
ab(p, (36,    bl(393.7, 10)), "Expected final deliverables", 10, DB)
ab(p, (311.2, bl(475.4, 10)), "Key learning outcomes",       10, DB)
# KLO label tags — repaint YL then reinsert lowercase (DB on YL)
paint(p, (311.2, 493.5, 382.5, 507.8), YL)
paint(p, (387.8, 493.5, 493.5, 507.8), YL)
paint(p, (311.2, 511.5, 389.2, 525.8), YL)
paint(p, (394.5, 511.5, 479.2, 525.8), YL)
paint(p, (311.2, 529.5, 411.0, 544.5), YL)
paint(p, (416.2, 529.5, 537.0, 544.5), YL)
paint(p, (311.2, 548.2, 368.2, 562.5), YL)
paint(p, (373.5, 548.2, 460.5, 562.5), YL)
ab(p, (317.2, bl(496.2, 7)), "Data analysis",         7, DB)
ab(p, (394.1, bl(496.2, 7)), "Threat identification", 7, DB)
ab(p, (317.2, bl(514.2, 7)), "Documentation",         7, DB)
ab(p, (400.7, bl(514.2, 7)), "Risk assessment",       7, DB)
ab(p, (317.2, bl(532.2, 7)), "Presentation skills",   7, DB)
ab(p, (422.4, bl(532.2, 7)), "Cybersecurity concepts", 7, DB)
ab(p, (317.2, bl(550.9, 7)), "Teamwork",              7, DB)
ab(p, (379.6, bl(550.9, 7)), "Critical thinking",     7, DB)
print("✓ P10: all headers updated")


# ══════════════════════════════════════════════════════════════════
# PAGE 11  (idx 10)  — Scenario B  (DO NOT touch letter-spaced banner)
# ══════════════════════════════════════════════════════════════════
p = doc[10]
# Banner subtitle (in DB banner y=0–74.2)
p.add_redact_annot(fitz.Rect(36, 22, 400, 44))    # DATA INSIGHTS DASHBOARD
# Section headers (OR on WH)
p.add_redact_annot(fitz.Rect(36,  95, 270, 112))  # COMPANY BACKGROUND
p.add_redact_annot(fitz.Rect(312, 94, 576, 111))  # TEAM ROLES
p.add_redact_annot(fitz.Rect(36, 206, 270, 223))  # THE CHALLENGE
p.add_redact_annot(fitz.Rect(36, 403, 270, 420))  # THE DATASET
p.add_redact_annot(fitz.Rect(312, 365, 576, 382)) # RECOMMENDED TOOLS
# Team roles table header (WH on DB, y=129–150.8)
p.add_redact_annot(fitz.Rect(312, 129, 576, 152))
# Dataset table header (WH on DB, y=458.2–479.2)
p.add_redact_annot(fitz.Rect(36, 458, 300, 480))
p.apply_redactions(images=0, graphics=0)
# Repaint banner area
paint(p, (0, 26, 612, 44), DB)
# Repaint team roles header
paint(p, (312.8, 129.0, 385.5, 150.8), DB)
paint(p, (385.5, 129.0, 576.0, 150.8), DB)
# Repaint dataset table header
paint(p, (36.0,  458.2, 107.2, 479.2), DB)
paint(p, (107.2, 458.2, 204.8, 479.2), DB)
paint(p, (204.8, 458.2, 299.2, 479.2), DB)
# Reinsert
ab(p, (36,    bl(26.5,  18)), "Data insights dashboard",       18, OR)
ab(p, (36,    bl(99.4,  12)), "Company background",            12, OR)
ab(p, (312.8, bl(98.8,  11)), "Team roles",                   11, OR)
ab(p, (36,    bl(210.5, 11)), "The challenge",                 11, OR)
ab(p, (36,    bl(407.8, 11)), "The dataset",                  11, OR)
ab(p, (312.8, bl(369.5, 11)), "Recommended tools",            11, OR)
ab(p, (319.5, bl(135.0, 7.5)), "Role",             7.5, WH)
ab(p, (391.9, bl(135.0, 7.5)), "Responsibilities", 7.5, WH)
ab(p, (42.8,  bl(464.2, 7.5)), "Column",      7.5, WH)
ab(p, (114.4, bl(464.2, 7.5)), "Description", 7.5, WH)
ab(p, (211.2, bl(464.2, 7.5)), "Example",     7.5, WH)
print("✓ P11: all headers updated")


# ══════════════════════════════════════════════════════════════════
# PAGE 12  (idx 11)  — Scenario B deliverables/structure
# ══════════════════════════════════════════════════════════════════
p = doc[11]
p.add_redact_annot(fitz.Rect(36,  11, 576,  26))   # running head
p.add_redact_annot(fitz.Rect(36,  58, 300,  78))   # 6-WEEK PROJECT STRUCTURE
p.add_redact_annot(fitz.Rect(36,  95, 576, 116))   # WEEK/PHASE/ACTIVITIES/DELIVERABLE
p.add_redact_annot(fitz.Rect(36, 400, 300, 416))   # EXPECTED FINAL DELIVERABLES
p.add_redact_annot(fitz.Rect(311, 493, 576, 509))  # KEY LEARNING OUTCOMES
# KLO label rows
p.add_redact_annot(fitz.Rect(311, 511, 576, 533))  # row 1 (3 labels)
p.add_redact_annot(fitz.Rect(311, 530, 576, 551))  # row 2 (2 labels)
p.add_redact_annot(fitz.Rect(311, 548, 576, 570))  # row 3 (2 labels)
p.apply_redactions(images=0, graphics=0)
paint(p, (0, 0, 612, 40.5), DB)
ab(p, (36,    bl(15.3,  8)),  "Scenario B: Data insights dashboard \u2014 6-week structure & deliverables", 8, YL)
ab(p, (36,    bl(62.2,  15)), "6-week project structure",  15, OR)
paint(p, (36.0,  94.5,  86.2, 115.5), DB)
paint(p, (86.2,  94.5, 129.8, 115.5), DB)
paint(p, (129.8, 94.5, 418.5, 115.5), DB)
paint(p, (418.5, 94.5, 576.0, 115.5), DB)
ab(p, (42.8,  bl(100.5, 7.5)), "Week",        7.5, WH)
ab(p, (93.1,  bl(100.5, 7.5)), "Phase",       7.5, WH)
ab(p, (136.1, bl(100.5, 7.5)), "Activities",  7.5, WH)
ab(p, (426.5, bl(100.5, 7.5)), "Deliverable", 7.5, WH)
ab(p, (36,    bl(404.9, 10)), "Expected final deliverables", 10, DB)
ab(p, (311.2, bl(497.9, 10)), "Key learning outcomes",       10, DB)
# KLO labels P12
paint(p, (311.2, 515.2, 384.8, 530.2), YL)
paint(p, (390.0, 515.2, 464.2, 530.2), YL)
paint(p, (469.5, 515.2, 561.8, 530.2), YL)
paint(p, (311.2, 534.0, 402.0, 548.2), YL)
paint(p, (407.2, 534.0, 521.2, 548.2), YL)
paint(p, (311.2, 552.0, 403.5, 567.0), YL)
paint(p, (408.8, 552.0, 508.5, 567.0), YL)
ab(p, (317.2, bl(517.9, 7)), "Data cleaning",        7, DB)
ab(p, (396.1, bl(517.9, 7)), "Excel / Sheets",       7, DB)
ab(p, (475.8, bl(517.9, 7)), "Data visualization",   7, DB)
ab(p, (317.2, bl(536.7, 7)), "Business analysis",    7, DB)
ab(p, (413.2, bl(536.7, 7)), "Storytelling with data", 7, DB)
ab(p, (317.2, bl(554.7, 7)), "Dashboard design",     7, DB)
ab(p, (414.9, bl(554.7, 7)), "Presentation skills",  7, DB)
print("✓ P12: all headers updated")


# ══════════════════════════════════════════════════════════════════
# PAGE 13  (idx 12)  — Scenario C  (DO NOT touch letter-spaced banner)
# ══════════════════════════════════════════════════════════════════
p = doc[12]
# Section headers (OR on WH — no repaint, below banner)
p.add_redact_annot(fitz.Rect(36,  95, 270, 112))  # COMPANY BACKGROUND
p.add_redact_annot(fitz.Rect(312, 94, 576, 111))  # TEAM ROLES
p.add_redact_annot(fitz.Rect(36, 219, 270, 237))  # THE CHALLENGE
p.add_redact_annot(fitz.Rect(36, 416, 270, 434))  # THE DATASET
p.add_redact_annot(fitz.Rect(312, 338, 576, 356)) # CURRENT MANUAL WORKFLOW (5 STEPS)
# Team roles table header (WH on DB, y=129–150.8)
p.add_redact_annot(fitz.Rect(312, 129, 576, 152))
# Dataset table header (WH on DB, y=471.8–492.8)
p.add_redact_annot(fitz.Rect(36, 471, 300, 494))
p.apply_redactions(images=0, graphics=0)
# Repaint team roles header
paint(p, (312.8, 129.0, 387.0, 150.8), DB)
paint(p, (387.0, 129.0, 576.0, 150.8), DB)
# Repaint dataset table header
paint(p, (36.0,  471.8, 133.5, 492.8), DB)
paint(p, (133.5, 471.8, 299.2, 492.8), DB)
# Reinsert
ab(p, (36,    bl(99.4,  12)), "Company background",                12, OR)
ab(p, (312.8, bl(98.8,  11)), "Team roles",                        11, OR)
ab(p, (36,    bl(224.0, 11)), "The challenge",                     11, OR)
ab(p, (36,    bl(421.3, 11)), "The dataset",                       11, OR)
ab(p, (312.8, bl(343.3, 11)), "Current manual workflow (5 steps)", 11, OR)
ab(p, (319.5, bl(135.0, 7.5)), "Role",             7.5, WH)
ab(p, (393.9, bl(135.0, 7.5)), "Responsibilities", 7.5, WH)
ab(p, (42.8,  bl(477.7, 7.5)), "Column",      7.5, WH)
ab(p, (140.1, bl(477.7, 7.5)), "Description", 7.5, WH)
print("✓ P13: all headers updated")


# ══════════════════════════════════════════════════════════════════
# PAGE 14  (idx 13)  — Scenario C deliverables + Program Contacts fix
# ══════════════════════════════════════════════════════════════════
p = doc[13]
p.add_redact_annot(fitz.Rect(36,  11, 576,  26))   # running head
p.add_redact_annot(fitz.Rect(36,  58, 300,  78))   # 6-WEEK PROJECT STRUCTURE
p.add_redact_annot(fitz.Rect(36,  95, 576, 116))   # WEEK/PHASE/ACTIVITIES/DELIVERABLE
p.add_redact_annot(fitz.Rect(36, 445, 300, 461))   # EXPECTED FINAL DELIVERABLES
p.add_redact_annot(fitz.Rect(311, 445, 576, 461))  # KEY LEARNING OUTCOMES
# KLO label rows
p.add_redact_annot(fitz.Rect(311, 463, 576, 485))  # row 1
p.add_redact_annot(fitz.Rect(311, 482, 576, 503))  # row 2
p.add_redact_annot(fitz.Rect(311, 500, 576, 521))  # row 3
p.add_redact_annot(fitz.Rect(311, 518, 576, 540))  # row 4
# Program Contacts box — full text rebuild
p.add_redact_annot(fitz.Rect(311, 604, 592, 662))
p.apply_redactions(images=0, graphics=0)
paint(p, (0, 0, 612, 40.5), DB)
ab(p, (36,    bl(15.3,  8)),  "Scenario C: Workflow automation \u2014 6-week structure & deliverables", 8, YL)
ab(p, (36,    bl(62.2,  15)), "6-week project structure",  15, OR)
paint(p, (36.0,  94.5,  86.2, 115.5), DB)
paint(p, (86.2,  94.5, 129.0, 115.5), DB)
paint(p, (129.0, 94.5, 418.5, 115.5), DB)
paint(p, (418.5, 94.5, 576.0, 115.5), DB)
ab(p, (42.8,  bl(100.5, 7.5)), "Week",        7.5, WH)
ab(p, (93.1,  bl(100.5, 7.5)), "Phase",       7.5, WH)
ab(p, (136.0, bl(100.5, 7.5)), "Activities",  7.5, WH)
ab(p, (425.5, bl(100.5, 7.5)), "Deliverable", 7.5, WH)
ab(p, (36,    bl(449.9, 10)), "Expected final deliverables", 10, DB)
ab(p, (311.2, bl(449.9, 10)), "Key learning outcomes",       10, DB)
# KLO labels P14
paint(p, (311.2, 467.2, 397.5, 482.2), YL)
paint(p, (402.7, 467.2, 471.8, 482.2), YL)
paint(p, (311.2, 486.0, 408.8, 500.2), YL)
paint(p, (414.7, 486.0, 472.5, 500.2), YL)
paint(p, (311.2, 504.0, 408.0, 518.2), YL)
paint(p, (414.0, 504.0, 499.5, 518.2), YL)
paint(p, (311.2, 522.0, 387.0, 537.0), YL)
paint(p, (392.2, 522.0, 516.8, 537.0), YL)
ab(p, (317.2, bl(469.9, 7)), "Process mapping",        7, DB)
ab(p, (409.1, bl(469.9, 7)), "Zapier / Make",          7, DB)
ab(p, (317.2, bl(488.7, 7)), "Google Apps Script",     7, DB)
ab(p, (420.4, bl(488.7, 7)), "QA testing",             7, DB)
ab(p, (317.2, bl(506.7, 7)), "Efficiency analysis",    7, DB)
ab(p, (419.6, bl(506.7, 7)), "Problem solving",        7, DB)
ab(p, (317.2, bl(524.7, 7)), "No-code tools",          7, DB)
ab(p, (398.5, bl(524.7, 7)), "Technical documentation", 7, DB)
# ── Program Contacts box rebuild (DB navy background retained)
paint(p, (311.2, 603.8, 576.0, 702.8), DB)   # ensure box background solid
au(p,  (321.8, 619.0), "\U0001f4de Program contacts",              8, YL)
helv(p, (322.0, 632.0),
     "For DYCD SYEP support, compliance questions, or to report issues:", 8, WH)
helv(p, (322.0, 645.0), "SYEP Provider \u2014 contact information available",   8, WH)
helv(p, (322.0, 658.0), "via worksite portal",                                   8, WH)
helv(p, (322.0, 671.0), "DYCD \u2014 nyc.gov/dycd  |  1-800-246-4646",          8, WH)
print("✓ P14: all headers + Program Contacts box updated")


# ══════════════════════════════════════════════════════════════════
# PAGE 15  (idx 14)  — Scenario D  (DO NOT touch letter-spaced banner)
# ══════════════════════════════════════════════════════════════════
p = doc[14]
# Banner subtitles (in DB banner y=0–93.8), font=Helvetica-Bold
p.add_redact_annot(fitz.Rect(36,  19,  400, 57))   # WORKPLACE PROBLEM SOLVING + & APP CONCEPT DESIGN
# Section headers (OR on WH, Helvetica-Bold)
p.add_redact_annot(fitz.Rect(36,  93,  270, 110))  # COMPANY BACKGROUND
p.add_redact_annot(fitz.Rect(312, 93,  576, 110))  # TEAM ROLES
p.add_redact_annot(fitz.Rect(312, 325, 576, 343))  # SOLUTION OUTPUT (NO CODING REQUIRED)
p.add_redact_annot(fitz.Rect(36,  442, 270, 459))  # RESEARCH APPROACH
p.add_redact_annot(fitz.Rect(36,  557, 270, 574))  # EXAMPLE PROBLEM AREAS
# Team roles table header (WH on DB, y=129–150.8)
p.add_redact_annot(fitz.Rect(312, 129, 576, 152))
p.apply_redactions(images=0, graphics=0)
# Repaint banner zone
paint(p, (0, 23, 612, 57), DB)
# Repaint team roles header
paint(p, (312.8, 129.0, 387.0, 150.8), DB)
paint(p, (387.0, 129.0, 576.0, 150.8), DB)
# Reinsert (Helvetica-Bold)
hebo(p, (36,    bl(23.5,  18)), "Workplace problem solving", 18, OR)
hebo(p, (36,    bl(43.7,  18)), "& app concept design",      18, OR)
hebo(p, (36,    bl(97.4,  12)), "Company background",        12, OR)
hebo(p, (312.8, bl(97.0,  11)), "Team roles",                11, OR)
hebo(p, (312.8, bl(329.7, 11)), "Solution output (no coding required)", 11, OR)
hebo(p, (36,    bl(446.2, 11)), "Research approach",         11, OR)
hebo(p, (36,    bl(561.2, 11)), "Example problem areas",     11, OR)
hebo(p, (319.5, bl(133.8, 7.5)), "Role",             7.5, WH)
hebo(p, (393.9, bl(133.8, 7.5)), "Responsibilities", 7.5, WH)
print("✓ P15: all headers updated")


# ══════════════════════════════════════════════════════════════════
# PAGE 16  (idx 15)  — Scenario D deliverables + contacts + feedback
# ══════════════════════════════════════════════════════════════════
p = doc[15]
p.add_redact_annot(fitz.Rect(36,  10, 576,  25))   # running head
p.add_redact_annot(fitz.Rect(36,  95, 576, 116))   # WEEK/PHASE/ACTIVITIES/DELIVERABLE
# KLO labels P16 (DB on YL)
p.add_redact_annot(fitz.Rect(311, 458, 576, 480))  # row 1
p.add_redact_annot(fitz.Rect(311, 478, 576, 500))  # row 2
p.add_redact_annot(fitz.Rect(311, 498, 576, 520))  # row 3
p.add_redact_annot(fitz.Rect(311, 518, 576, 540))  # row 4
# Program Contacts text (right column, white bg)
p.add_redact_annot(fitz.Rect(311, 553, 576, 568))  # "Program Contacts" header
p.add_redact_annot(fitz.Rect(311, 579, 576, 604))  # SYEP Provider + DYCD lines
p.apply_redactions(images=0, graphics=0)
paint(p, (0, 0, 612, 40.5), DB)
ab(p, (36, bl(14.0, 8)), "Scenario D: Workplace problem solving \u2014 6-week structure & deliverables", 8, YL)
# Table column headers (WH on DB)
paint(p, (36.0,  94.5,  86.2, 115.5), DB)
paint(p, (86.2,  94.5, 129.0, 115.5), DB)
paint(p, (129.0, 94.5, 418.5, 115.5), DB)
paint(p, (418.5, 94.5, 576.0, 115.5), DB)
hebo(p, (42.8,  bl(99.2, 7.5)), "Week",        7.5, WH)
hebo(p, (93.1,  bl(99.2, 7.5)), "Phase",       7.5, WH)
hebo(p, (136.0, bl(99.2, 7.5)), "Activities",  7.5, WH)
hebo(p, (425.5, bl(99.2, 7.5)), "Deliverable", 7.5, WH)
# KLO labels P16
paint(p, (311.0, 463.0, 384.6, 476.0), YL)
paint(p, (443.0, 463.0, 509.3, 476.0), YL)
paint(p, (311.0, 483.0, 387.5, 496.0), YL)
paint(p, (443.0, 483.0, 516.6, 496.0), YL)
paint(p, (311.0, 503.0, 377.7, 516.0), YL)
paint(p, (443.0, 503.0, 511.1, 516.0), YL)
paint(p, (311.0, 523.0, 422.5, 536.0), YL)
hebo(p, (316.0, bl(465.0, 6.5)), "Problem solving",       6.5, (0.10, 0.10, 0.10))
hebo(p, (448.0, bl(465.0, 6.5)), "User research",         6.5, (0.10, 0.10, 0.10))
hebo(p, (316.0, bl(485.0, 6.5)), "Process analysis",      6.5, (0.10, 0.10, 0.10))
hebo(p, (448.0, bl(485.0, 6.5)), "Critical thinking",     6.5, (0.10, 0.10, 0.10))
hebo(p, (316.0, bl(505.0, 6.5)), "Communication",         6.5, (0.10, 0.10, 0.10))
hebo(p, (448.0, bl(505.0, 6.5)), "Design thinking",       6.5, (0.10, 0.10, 0.10))
hebo(p, (316.0, bl(525.0, 6.5)), "Workplace collaboration", 6.5, (0.10, 0.10, 0.10))
# Program Contacts — update to sentence case + correct wording
# "Program contacts" header (hebo sz=8.5, DK — matching existing style)
hebo(p, (311.0, bl(556.9, 8.5)), "Program contacts", 8.5, DK)
# "For DYCD SYEP support..." line at y=570.4 is UNCHANGED (not redacted)
# SYEP Provider line (wrap to 2 lines)
helv(p, (311.0, bl(583.4, 8)), "SYEP Provider \u2014 contact information available", 8, DK)
helv(p, (311.0, bl(596.4, 8)), "via worksite portal",                                8, DK)
# DYCD line (shifted down 13pt due to added wrap line)
helv(p, (311.0, bl(609.4, 8)), "DYCD \u2014 nyc.gov/dycd  |  1-800-246-4646",       8, DK)
# Employer Feedback Form line (new, ~13pt below DYCD)
helv(p, (311.0, bl(622.4, 8)),
     "Employer Feedback Form \u2014 ______________________________", 8, DK)
print("✓ P16: running head, KLO labels, contacts, employer feedback updated")


# ══════════════════════════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════════════════════════
doc.save(TMP, garbage=4, deflate=True)
doc.close()
os.replace(TMP, SRC)
print(f"\n\u2705  Saved \u2192 {SRC}")
