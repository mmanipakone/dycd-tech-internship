"""
apply_all_revisions.py
Apply all requested page-by-page edits to TechInternship_revised.pdf.

Changes implemented:
  P0  (Cover)  — Add Student Pathways logo; replace cover image
  P3           — Age range 14–24 → 16–21; remove ON-SITE from metric card;
                 remove "Supported by DYCD-funded SYEP provider"
  P5           — Remove "on-site" from opening paragraph + Key Requirement box
  P7           — Restructure skills table: Portrait of a Graduate as primary headers
  P8           — Remove Exit Survey line; shift Incident Reports up
  All pages    — Remove "DYCD-funded SYEP provider" language wherever found
  P13          — Reposition "Example Outcome" text below image (was overlapping)
  P14, P16     — Update contacts: DYCD Program Coordinator → SYEP Provider + correct DYCD URL

NOT implemented (require manual designer review):
  - Global sentence case conversion (100s of spans; high error risk without visual QA)
  - Full layout cleanup across all pages (needs page-by-page visual inspection)
"""
import fitz, os

SRC = "revised_outputs/TechInternship_revised.pdf"
TMP = SRC + ".tmp"
AU  = '/Library/Fonts/Arial Unicode.ttf'

DB  = (0.03920, 0.14510, 0.25100)   # navy
OR  = (0.91000, 0.29410, 0.00000)   # orange
YL  = (1.00000, 0.90200, 0.00000)   # yellow
WH  = (1.00000, 1.00000, 1.00000)
DK  = (26/255,  26/255,  26/255)    # near-black

doc = fitz.open(SRC)

# ── Shared helpers ────────────────────────────────────────────────────────────
def paint(pg, rect, fill):
    s = pg.new_shape()
    s.draw_rect(fitz.Rect(*rect))
    s.finish(fill=fill, color=None)
    s.commit()

def rule(pg, x0, y, x1, clr, h=0.5):
    s = pg.new_shape()
    s.draw_line(fitz.Point(x0, y), fitz.Point(x1, y))
    s.finish(color=clr, width=h)
    s.commit()

def txt(pg, xy, text, sz=8.0, font='helv', clr=None):
    pg.insert_text(xy, text, fontname=font, fontsize=sz,
                   color=clr if clr else DK)

def bold(pg, xy, text, sz=8.0, clr=None):
    txt(pg, xy, text, sz=sz, font='hebo', clr=clr)

# ═══════════════════════════════════════════════════════════════════════════
# COVER PAGE (index 0) — Replace image + add Student Pathways logo
# ═══════════════════════════════════════════════════════════════════════════
p0 = doc[0]

# Replace cover image with student tech photo
# Current image occupies y≈0–394; overlay with new image at same rect
new_cover = "studenttechpictures/241116_jca_inspiredu_1018_54364972816_l.jpg"
if os.path.exists(new_cover):
    p0.insert_image(fitz.Rect(0, 0, 612, 394.5), filename=new_cover,
                    keep_proportion=False, overlay=True)
    print("✓ Cover: student tech photo inserted")
else:
    print(f"  ⚠ Cover photo not found: {new_cover}")

# Add Student Pathways logo (white version for dark background)
# Place in header band, right side, next to DYCD badge
logo_path = "Student Pathways Logos/PNG/NYCPS-Pathways-logo-white.png"
if os.path.exists(logo_path):
    # Header band runs y=355–395 (yellow bar area). Logo goes right-aligned.
    p0.insert_image(fitz.Rect(440, 358, 576, 392),
                    filename=logo_path, keep_proportion=True, overlay=True)
    print("✓ Cover: Student Pathways logo added")
else:
    print(f"  ⚠ Logo not found: {logo_path}")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 3 (index 2) — Age range / ON-SITE metric / provider phrase
# ═══════════════════════════════════════════════════════════════════════════
p3 = doc[2]

# 1. Age range: "NYC high school students, ages 14–24" → "16–21"
#    Span: y=246-258, x=327-482, ArialUnicodeMS, #1a1a1a
paint(p3, (322, 241, 492, 262), WH)
p3.insert_text((327, 258), "NYC high school students, ages 16\u201321",
               fontname='arialuni', fontfile=AU, fontsize=9.0, color=DK)
print("✓ P3: Age range updated 14–24 → 16–21")

# 2. Metric card: "HOURS/WEEK ON-SITE" → "HOURS/WEEK"
#    Span at y=235-246, x=190-279, white text on DB background
#    DB metric container right card: R_X0=171, R_X1=298.5, centre x=234.75
paint(p3, (172, 231, 298, 252), DB)   # repaint DB to erase old label
w_hrs = fitz.get_text_length("HOURS/WEEK", fontname='helv', fontsize=8.0)
p3.insert_text((234.75 - w_hrs / 2, 247), "HOURS/WEEK",
               fontname='helv', fontsize=8.0, color=WH)
print("✓ P3: 'ON-SITE' removed from metric card")

# 3. Remove "Supported by a DYCD-funded SYEP provider" at y=309-321, x=327-508
paint(p3, (322, 304, 550, 330), WH)
print("✓ P3: DYCD provider language removed")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 5 (index 4) — Remove "on-site" (paragraph + Key Requirement box)
# ═══════════════════════════════════════════════════════════════════════════
p5 = doc[4]

# 4a. Opening paragraph: "Interns work [25 hours per week] on-site. Below is..."
#     "25 hours per week" ends at x≈159. Paint over x=155-576, y=92-111.
#     Line 2 "based on project needs..." at y=110-124, x=36-295 — repaint too.
paint(p5, (152, 92, 576, 124), WH)
txt(p5, (159, 107),
    ". Below is the recommended daily structure across the 6-week program. Supervisors should",
    sz=8.0, clr=DK)
txt(p5, (36, 122),
    "adjust based on project needs while maintaining the core learning structure.",
    sz=8.0, clr=DK)
print("✓ P5: 'on-site' removed from opening paragraph")

# 4b. Key Requirement box — white on orange background
#     Line 1: "All interns must maintain 25 hours/week on-" at y=357-366, x=407-564
#     Line 2: "site. Attendance and punctuality..." at y=369-378, x=326-528
#     Line 3: "compliance requirements." at y=381-389, x=326-418
#     Strategy: paint OR over text area, reinsert without "on-site"
paint(p5, (403, 352, 568, 372), OR)   # cover "on-" part of line 1
paint(p5, (322, 367, 532, 395), OR)   # cover lines 2 and 3
txt(p5, (407, 366), "All interns must maintain 25 hours/week.", sz=8.0, clr=WH)
txt(p5, (326, 380),
    "Attendance and punctuality are tracked by DYCD as compliance requirements.",
    sz=8.0, clr=WH)
print("✓ P5: 'on-site' removed from Key Requirement box")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 7 (index 6) — Restructure skills table
# Current: Skill Area | HOW TO BUILD IT (Portrait competency in parentheses)
# New:     COMPETENCY (Portrait primary) | HOW INTERNS DEVELOP THIS
# Table occupies x=36-302, y=163-343 (image starts at y=345)
# ═══════════════════════════════════════════════════════════════════════════
p7 = doc[6]

TABLE_X0  = 36
TABLE_X1  = 302
COL2_X    = 155   # left/right column divider
HDR_H     = 20    # header bar height
ROW_H     = 32    # per-row height
TABLE_TOP = 163

# Clear existing table area
paint(p7, (TABLE_X0 - 1, TABLE_TOP - 2, TABLE_X1 + 1, 344), WH)

# New table data — Portrait of a Graduate competencies as primary headers
TABLE_DATA = [
    ("Effective Communicator",
     "Stand-ups, presentations, written updates, email norms"),
    ("Global Citizen",
     "Team roles, collaboration, group problem-solving, etiquette"),
    ("Critical Thinker",
     "Project analysis, peer review, retrospectives, research"),
    ("Creative Innovator",
     "Adapting scope, prototyping, exploring new approaches"),
    ("Reflective / Future Focused",
     "Goal-setting, time tracking, documentation, reflection"),
]

# Width QA
col1_avail = COL2_X - TABLE_X0 - 8
print(f"\n  Table column 1 available: {col1_avail:.0f}pt")
for label, _ in TABLE_DATA:
    w = fitz.get_text_length(label, fontname='hebo', fontsize=7.0)
    status = "✓" if w <= col1_avail else "⚠ OVERFLOW"
    print(f"    {status} '{label}': {w:.0f}pt")

# Draw header bar
paint(p7, (TABLE_X0, TABLE_TOP, TABLE_X1, TABLE_TOP + HDR_H), DB)
bold(p7, (TABLE_X0 + 6, TABLE_TOP + HDR_H - 5),
     "COMPETENCY", sz=7.5, clr=WH)
bold(p7, (COL2_X + 5, TABLE_TOP + HDR_H - 5),
     "HOW INTERNS DEVELOP THIS", sz=7.5, clr=WH)

# Draw outer border
s_outer = p7.new_shape()
s_outer.draw_rect(fitz.Rect(TABLE_X0, TABLE_TOP, TABLE_X1, TABLE_TOP + HDR_H + len(TABLE_DATA) * ROW_H))
s_outer.finish(color=(0.7, 0.72, 0.75), width=0.75, fill=None)
s_outer.commit()

# Draw data rows
ry = TABLE_TOP + HDR_H
for i, (label, content) in enumerate(TABLE_DATA):
    row_bg = (0.953, 0.965, 0.984) if i % 2 == 1 else WH
    paint(p7, (TABLE_X0, ry, TABLE_X1, ry + ROW_H), row_bg)

    # Column divider (vertical — use thin paint rect)
    paint(p7, (COL2_X, ry, COL2_X + 0.5, ry + ROW_H), (0.75, 0.77, 0.80))
    # Bottom border (horizontal)
    paint(p7, (TABLE_X0, ry + ROW_H - 0.5, TABLE_X1, ry + ROW_H), (0.78, 0.80, 0.83))

    # Left column: competency name (bold, navy)
    mid_y = ry + ROW_H / 2 + 3
    bold(p7, (TABLE_X0 + 6, mid_y), label, sz=7.0, clr=DB)

    # Right column: how they develop it (regular, DK)
    txt(p7, (COL2_X + 5, mid_y), content, sz=7.0, clr=DK)

    ry += ROW_H

print(f"\n✓ P7: Skills table rebuilt with 5 Portrait of a Graduate competencies (y={TABLE_TOP}–{ry:.0f})")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 8 (index 7) — Remove Exit Survey; shift Incident Reports up
# Required documentation list: Timesheets, Attendance, Mid-Eval, Final Eval,
#   [Exit Survey REMOVED], Incident Reports
# Exit Survey:     y=248 x=326-490
# Incident Reports: y=263 x=326-490
# ═══════════════════════════════════════════════════════════════════════════
p8 = doc[7]

# Paint white over both lines
paint(p8, (322, 242, 510, 278), WH)

# Reinsert Incident Reports at the Exit Survey y position
bold(p8, (326, 255), "Incident Reports:", sz=9.0, clr=DK)
txt(p8, (400, 255), "Any workplace incidents within 24 hrs", sz=9.0, clr=DK)
print("✓ P8: Exit Survey removed; Incident Reports shifted up")

# ═══════════════════════════════════════════════════════════════════════════
# GLOBAL — Remove DYCD-funded SYEP provider language across all pages
# ═══════════════════════════════════════════════════════════════════════════
PROVIDER_PHRASES = [
    "with support from a DYCD-funded SYEP provider",
    "supported by a DYCD-funded SYEP provider",
    "Supported by a DYCD-funded SYEP provider",
]
found_count = 0
for pg_i in range(len(doc)):
    pg = doc[pg_i]
    for block in pg.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                t = span["text"]
                for phrase in PROVIDER_PHRASES:
                    if phrase.lower() in t.lower():
                        b = span["bbox"]
                        # Match the background to erase cleanly
                        col = span["color"]
                        bg = WH  # default to white
                        paint(pg, (b[0] - 1, b[1] - 2, b[2] + 1, b[3] + 2), bg)
                        found_count += 1
                        print(f"  ✓ P{pg_i+1}: erased '{t[:60]}'  (y={b[1]:.0f})")

print(f"✓ Global: {found_count} provider phrase instance(s) removed")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 13 (index 12) — Fix "Example Outcome" text overlapping image
# Image at Rect(312.75, 454.5, 576.0, 652.5)
# Text at y=518-572, x=320 — INSIDE the image bounds → moved below image
# ═══════════════════════════════════════════════════════════════════════════
p13 = doc[12]

# 1. White-paint over old text (currently inside the image area)
paint(p13, (310, 513, 578, 580), WH)

# 2. Reinsert below image (image bottom y=652.5, footer at y=776)
ey = 664
bold(p13, (313, ey), "Example Outcome:", sz=8.0, clr=DK)
ey += 13
lines_eo = [
    "Before automation, each inquiry required a 5-step manual process taking",
    "20\u201330 minutes. After the intern team built the automation prototype,",
    "processing time dropped to under 5 minutes \u2014 with fewer errors and",
    "improved response consistency across all client inquiries.",
]
for line_eo in lines_eo:
    txt(p13, (313, ey), line_eo, sz=8.0, clr=DK)
    ey += 13

print(f"✓ P13: 'Example Outcome' repositioned below image (y=664–{ey:.0f}; footer at y=776)")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 14 (index 13) — Update contacts section
# "DYCD Program Coordinator" at y=644, "— Contact via your program portal" y=644
# "DYCD Main Office" at y=656, "— dycd.nyc.gov" at y=656
# ═══════════════════════════════════════════════════════════════════════════
p14 = doc[13]

# Paint white over old contact lines
paint(p14, (319, 638, 578, 672), WH)

# Reinsert updated contacts
bold(p14, (322, 650), "SYEP Provider", sz=8.0, clr=DK)
txt(p14,  (398, 650), "\u2014 contact via your SYEP worksite portal", sz=8.0, clr=DK)
bold(p14, (322, 664), "DYCD", sz=8.0, clr=DK)
txt(p14,  (344, 664), "\u2014 nyc.gov/dycd  |  1-800-246-4646", sz=8.0, clr=DK)
print("✓ P14: Contacts updated (SYEP Provider + nyc.gov/dycd | 1-800-246-4646)")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 16 (index 15) — Update contacts section
# "DYCD Program Coordinator" at y=648, "— Contact via your program portal" y=648
# ═══════════════════════════════════════════════════════════════════════════
p16 = doc[15]

paint(p16, (319, 642, 578, 678), WH)

bold(p16, (322, 654), "SYEP Provider", sz=8.0, clr=DK)
txt(p16,  (398, 654), "\u2014 contact via your SYEP worksite portal", sz=8.0, clr=DK)
bold(p16, (322, 668), "DYCD", sz=8.0, clr=DK)
txt(p16,  (344, 668), "\u2014 nyc.gov/dycd  |  1-800-246-4646", sz=8.0, clr=DK)
print("✓ P16: Contacts updated")

# ═══════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════
doc.save(TMP, garbage=2, deflate=True)
doc.close()
os.replace(TMP, SRC)
print(f"\nAll changes saved → {SRC}")
