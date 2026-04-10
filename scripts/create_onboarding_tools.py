"""
create_onboarding_tools.py  v3
One-page DYCD onboarding resource — 6-week SYEP aligned.
All 6 resources linked; no 30-day references; 3-section layout.
"""
import fitz, os

OUT = "revised_outputs/Onboarding_Tools_for_High_School_Interns.pdf"

# ── Palette (matches playbook) ───────────────────────────────────────────────
DB = (0.03920, 0.14510, 0.25100)   # navy
OR = (0.91000, 0.29410, 0.00000)   # orange
YL = (1.00000, 0.90200, 0.00000)   # yellow
WH = (1.00000, 1.00000, 1.00000)
DK = (26/255,  26/255,  26/255)    # near-black text
LG = (0.886,   0.910,   0.941)     # light blue-gray
GR = (0.42,    0.42,    0.42)      # sublabel gray

# ── URLs ────────────────────────────────────────────────────────────────────
URL_SYEP_KIT  = "https://www.nyc.gov/assets/dycd/downloads/pdf/SYEP_Internship_Design_Kit.pdf"
URL_WORKABLE  = "https://resources.workable.com/onboarding-interns-checklist"
URL_EDSYSTEMS = "https://edsystemsniu.org/wp-content/uploads/dlm_uploads/2024/02/STAMP-Employer-Resources-20240202.pdf"
URL_ASE       = "https://www.slideshare.net/slideshow/ase-intern-orientation-100747502/100747502"
URL_SYEP_ORI  = "https://www.slideshare.net/slideshow/worksite-orientation-uau-syep-2021/249477124"
URL_NASPO     = "https://cms.naspo.org/wp-content/uploads/2023/07/2021_Internship_Toolkit_Partner_Version.pdf"

EXPECTED_URLS = {URL_SYEP_KIT, URL_WORKABLE, URL_EDSYSTEMS,
                 URL_ASE, URL_SYEP_ORI, URL_NASPO}

# ── Page ────────────────────────────────────────────────────────────────────
doc  = fitz.open()
page = doc.new_page(width=612, height=792)

# ── Primitives ───────────────────────────────────────────────────────────────
def paint(rect, fill):
    s = page.new_shape()
    s.draw_rect(fitz.Rect(*rect))
    s.finish(fill=fill, color=None)
    s.commit()

def hline(x0, y, x1, clr=LG, h=0.75):
    paint((x0, y, x1, y + h), clr)

def txt(xy, text, sz=9.0, font='helv', clr=None):
    page.insert_text(xy, text, fontname=font, fontsize=sz,
                     color=clr if clr else DK)

def bold(xy, text, sz=9.0, clr=None):
    txt(xy, text, sz=sz, font='hebo', clr=clr)

def underline(x, y, w, clr, t=0.5):
    s = page.new_shape()
    s.draw_line(fitz.Point(x, y + 1.5), fitz.Point(x + w, y + 1.5))
    s.finish(color=clr, width=t)
    s.commit()

def add_uri(x0, y_base, w, sz, url):
    page.insert_link({
        'kind': fitz.LINK_URI,
        'from': fitz.Rect(x0, y_base - sz - 1, x0 + w, y_base + 2),
        'uri':  url,
    })

def linked(x, y, text, url, sz=8.5, clr=None, font='hebo'):
    """Bold linked text with underline + URI annotation."""
    c = clr or DB
    page.insert_text((x, y), text, fontname=font, fontsize=sz, color=c)
    w = fitz.get_text_length(text, fontname=font, fontsize=sz)
    underline(x, y, w, c)
    add_uri(x, y, w, sz, url)
    return w

def cat_header(x0, x1, y, title, pre=10, bh=16):
    """Navy bar + orange accent + white title. Returns y of first content row."""
    y += pre
    paint((x0, y, x1, y + bh), DB)
    paint((x0, y, x0 + 4, y + bh), OR)
    bold((x0 + 9, y + bh - 3.5), title, sz=7.5, clr=WH)
    return y + bh + 8

def bullet(x0, y, label, sub=None, url=None, lsz=8.5, ssz=7.5, gap=15):
    """4pt orange marker + label + optional sublabel. Returns next y."""
    msz = 4.0
    my0 = y - lsz + 1.5
    paint((x0, my0, x0 + msz, my0 + msz), OR)
    tx = x0 + msz + 5
    if url:
        linked(tx, y, label, url, sz=lsz, clr=DB)
    else:
        bold((tx, y), label, sz=lsz, clr=DK)
    if sub:
        txt((tx, y + lsz + 2), sub, sz=ssz, clr=GR)
    step = lsz + 2 + (ssz + 2 if sub else 0)
    return y + step + gap

# ═══════════════════════════════════════════════════════════════════════════
# HEADER  y=0–60
# ═══════════════════════════════════════════════════════════════════════════
paint((0, 0, 612, 56), DB)
paint((0, 56, 612, 60), YL)

bold((36, 17), "DYCD", sz=10.0, clr=YL)
bold((36, 31), "SYEP EMPLOYER RESOURCE", sz=7.0, clr=OR)

title = "ONBOARDING TOOLS FOR HIGH SCHOOL INTERNS"
tw = fitz.get_text_length(title, fontname='hebo', fontsize=13.0)
bold(((612 - tw) / 2, 37), title, sz=13.0, clr=OR)

# ═══════════════════════════════════════════════════════════════════════════
# SUBHEADER BAND  y=63–92
# ═══════════════════════════════════════════════════════════════════════════
paint((0, 63, 612, 92), LG)
sub1 = "Supporting SYEP 6-Week Internship Implementation"
sub2 = "Use these tools to quickly onboard interns, set expectations, and support early success."
s1w = fitz.get_text_length(sub1, fontname='hebo', fontsize=8.5)
s2w = fitz.get_text_length(sub2, fontname='helv', fontsize=7.5)
bold(((612 - s1w) / 2, 76), sub1, sz=8.5, clr=DB)
txt( ((612 - s2w) / 2, 88), sub2, sz=7.5, clr=GR)

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1 — CORE ONBOARDING TOOLS
# ═══════════════════════════════════════════════════════════════════════════
sec1_label_y = 97
bold((36, sec1_label_y + 10), "SECTION 1  ·  CORE ONBOARDING TOOLS", sz=9.0, clr=OR)
hline(36, sec1_label_y + 13, 576, OR, h=1.0)

# Column geometry
L_X0, L_X1 = 36.0, 295.0
R_X0, R_X1 = 313.0, 576.0
ITEMS_TOP = 110

# ── LEFT COLUMN ─────────────────────────────────────────────────────────────
y = ITEMS_TOP

y = cat_header(L_X0, L_X1, y, "ONBOARDING & ORIENTATION", pre=0)
y = bullet(L_X0 + 2, y,
    "SYEP Internship Design Kit",
    "For employer use \u2014 DYCD guide to internship design",
    url=URL_SYEP_KIT)
y = bullet(L_X0 + 2, y,
    "Intern Onboarding Checklist",
    "Pre-arrival tasks, workspace, logins, first-day prep",
    url=URL_WORKABLE)
y = bullet(L_X0 + 2, y,
    "Orientation Agenda Template",
    "EdSystems STAMP resource \u2014 Week 1 structured agenda",
    url=URL_EDSYSTEMS)

y = cat_header(L_X0, L_X1, y, "PLANNING & PROJECT TOOLS")
# Single unified planning tool — label sized down to fit column width
y = bullet(L_X0 + 2, y,
    "Learning Plan Template (Project Organizer \u2014 Google Sheets)",
    "Tasks, goals, and progress tracking \u2014 one tool for both",
    lsz=7.5, ssz=7.0, gap=15)
y = bullet(L_X0 + 2, y,
    "Weekly 1:1 Check-In Template",
    "See standalone template provided with this playbook")
y = bullet(L_X0 + 2, y,
    "Weekly Reflection",
    "May be created or adapted by employer \u2014 5 min each week",
    gap=0)

L_BOTTOM = y
# width QA for the merged planning tool label
_lw = fitz.get_text_length(
    "Learning Plan Template (Project Organizer \u2014 Google Sheets)",
    fontname='hebo', fontsize=7.5)
print(f"Left column bottom: y={L_BOTTOM:.0f}  "
      f"(Learning Plan label width: {_lw:.0f}pt / 248pt max)")

# ── RIGHT COLUMN ─────────────────────────────────────────────────────────────
y = ITEMS_TOP

y = cat_header(R_X0, R_X1, y, "OPTIONAL SUPPORT TOOLS", pre=0)
y = bullet(R_X0 + 2, y,
    "Intern Orientation Slides (ASE)",
    "Real example deck \u2014 adapt to your organization",
    url=URL_ASE)
y = bullet(R_X0 + 2, y,
    "Worksite Supervisor Orientation",
    "SYEP walkthrough example for site supervisors",
    url=URL_SYEP_ORI)
y = bullet(R_X0 + 2, y,
    "NASPO Internship Toolkit",
    "Comprehensive host guide \u2014 planning through close",
    url=URL_NASPO)

# ── Planning system note box (fills remaining right column to match L_BOTTOM) ─
NB_TOP = y + 10      # gap below Optional Support bullets
NB_BOT = L_BOTTOM    # align to left column bottom

# Light blue-gray background + orange top accent
paint((R_X0, NB_TOP, R_X1, NB_BOT), (0.958, 0.968, 0.980))
paint((R_X0, NB_TOP, R_X1, NB_TOP + 3), OR)   # orange top bar

bold((R_X0 + 9, NB_TOP + 13), "PLANNING SYSTEM NOTE", sz=7.5, clr=DB)
hline(R_X0 + 9, NB_TOP + 16, R_X1 - 6, DB, h=0.5)

note_lines = [
    "One template covers both planning and tracking.",
    "",
    "The Learning Plan Template (Google Sheets) serves",
    "as BOTH the internship learning plan AND the project",
    "organizer \u2014 no additional documents needed.",
    "",
    "Employers may recreate or adapt this tool.",
    "Contact your DYCD coordinator for access.",
]
nby = NB_TOP + 24
for nl in note_lines:
    if nl:
        txt((R_X0 + 9, nby), nl, sz=7.0, clr=DK)
    nby += 10.5

R_BOTTOM = NB_BOT
print(f"Right column bottom: y={R_BOTTOM:.0f}")

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2 — HOW TO USE THESE TOOLS (3 phase cards)
# ═══════════════════════════════════════════════════════════════════════════
SEC2_TOP = max(L_BOTTOM, R_BOTTOM) + 16
hline(36, SEC2_TOP, 576, LG)
SEC2_TOP += 8

bold((36, SEC2_TOP + 10), "SECTION 2  ·  HOW TO USE THESE TOOLS", sz=9.0, clr=OR)
hline(36, SEC2_TOP + 13, 576, OR, h=1.0)

CARD_TOP  = SEC2_TOP + 22
CARD_H    = 114   # height of each phase card
CARD_W    = 170   # (576-36-2×12)/3 ≈ 170
GAP       = 12

cx = [36, 36 + CARD_W + GAP, 36 + 2 * (CARD_W + GAP)]

PHASES = [
    ("WEEK 1", "Orientation & Setup", [
        "Complete onboarding checklist with intern",
        "Share SYEP Design Kit (for employer use)",
        "Assign peer buddy or point of contact",
        "Set Week 1 goals in Learning Plan Template",
    ]),
    ("WEEKS 2\u20134", "Project Work & Check-Ins", [
        "Weekly Learning Plan Template review",
        "Structured 1:1 check-in each week",
        "Track project progress and adjust scope",
        "Weekly reflection \u2014 5 min each week",
    ]),
    ("WEEKS 5\u20136", "Refinement & Presentation", [
        "Final project refinement with intern",
        "Complete end-of-program evaluation",
        "Prepare intern for final presentation",
        "Close out Learning Plan \u2014 review goals met",
    ]),
]

CARD_BOT = CARD_TOP + CARD_H
for i, (week_label, card_title, items) in enumerate(PHASES):
    x0 = cx[i]
    x1 = x0 + CARD_W

    # Card background
    paint((x0, CARD_TOP, x1, CARD_BOT), (0.965, 0.973, 0.984))   # very light blue

    # DB header bar
    CHDR_H = 28
    paint((x0, CARD_TOP, x1, CARD_TOP + CHDR_H), DB)
    paint((x0, CARD_TOP, x0 + 4, CARD_TOP + CHDR_H), OR)

    # Week label (small, YL) + title (white, smaller)
    week_w = fitz.get_text_length(week_label, fontname='hebo', fontsize=7.0)
    bold((x0 + (CARD_W - week_w) / 2, CARD_TOP + 10), week_label, sz=7.0, clr=YL)
    title_w = fitz.get_text_length(card_title, fontname='helv', fontsize=6.5)
    txt((x0 + (CARD_W - title_w) / 2, CARD_TOP + 21), card_title, sz=6.5, clr=WH)

    # Bullets
    by = CARD_TOP + CHDR_H + 10
    for item in items:
        # Small orange dash marker
        txt((x0 + 6, by), "\u2022", sz=6.5, clr=OR)
        txt((x0 + 14, by), item, sz=6.5, clr=DK)
        by += 10

SEC2_BOTTOM = CARD_BOT
print(f"Section 2 bottom: y={SEC2_BOTTOM:.0f}")

# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3 — IMPLEMENTATION NOTE (callout box)
# ═══════════════════════════════════════════════════════════════════════════
SEC3_TOP = SEC2_BOTTOM + 16
hline(36, SEC3_TOP, 576, LG)
SEC3_TOP += 8

bold((36, SEC3_TOP + 10), "SECTION 3  ·  IMPLEMENTATION NOTE", sz=9.0, clr=OR)
hline(36, SEC3_TOP + 13, 576, OR, h=1.0)

BOX_TOP = SEC3_TOP + 22
BOX_BOT = BOX_TOP + 100

# Warm cream background + DB left accent
paint((36, BOX_TOP, 576, BOX_BOT), (1.0, 0.965, 0.878))
paint((36, BOX_TOP, 42, BOX_BOT), DB)

bold((50, BOX_TOP + 14), "For employers implementing a 6-week SYEP tech internship:", sz=8.5, clr=DB)

notes = [
    "Employers do not need to build everything from scratch.",
    "Use available templates where possible and adapt tools to your workplace context.",
    "For resources without links, simple versions can be created in Google Docs, Slides, or Sheets.",
    "(May be created or adapted by employer.)",
    "",
    "The Learning Plan Template (Google Sheets) is the single planning tool for the internship.",
    "It serves as both the learning plan AND the project organizer \u2014 one document, not two.",
]
ny = BOX_TOP + 28
for note in notes:
    if note:
        txt((50, ny), note, sz=7.5, clr=DK)
    ny += 10

SEC3_BOTTOM = BOX_BOT
print(f"Section 3 bottom: y={SEC3_BOTTOM:.0f}")

# ═══════════════════════════════════════════════════════════════════════════
# QUICK REFERENCE STRIP  (all 6 linked resources in a compact 2-col grid)
# ═══════════════════════════════════════════════════════════════════════════
REF_TOP = SEC3_BOTTOM + 12
hline(36, REF_TOP, 576, LG)
REF_TOP += 6

bold((36, REF_TOP + 10), "DOWNLOADABLE RESOURCES", sz=8.5, clr=DB)
hline(36, REF_TOP + 13, 576, DB, h=0.75)

REF_ITEMS_TOP = REF_TOP + 20

ALL_RESOURCES = [
    # (col, label, short_desc, url)
    ("L", "SYEP Internship Design Kit",
          "Official DYCD internship framework (PDF)",
          URL_SYEP_KIT),
    ("L", "Intern Onboarding Checklist",
          "Workable \u2014 pre-arrival + Day 1 tasks",
          URL_WORKABLE),
    ("L", "Orientation Agenda Template",
          "EdSystems STAMP employer toolkit",
          URL_EDSYSTEMS),
    ("R", "Intern Orientation Slides (ASE)",
          "Example intern deck \u2014 adaptable",
          URL_ASE),
    ("R", "Worksite Supervisor Orientation",
          "SYEP example walkthrough \u2014 SlideShare",
          URL_SYEP_ORI),
    ("R", "NASPO Internship Toolkit",
          "End-to-end host guide (PDF)",
          URL_NASPO),
]

LCL = 36.0
RCL = 314.0
ly  = REF_ITEMS_TOP
ry  = REF_ITEMS_TOP
STEP = 16

for col, label, desc, url in ALL_RESOURCES:
    cx2 = LCL if col == "L" else RCL
    cy  = ly  if col == "L" else ry
    lw  = linked(cx2, cy, label, url, sz=7.5, clr=DB)
    sep = " \u2014 "
    sw  = fitz.get_text_length(sep, fontname='helv', fontsize=7.0)
    txt((cx2 + lw, cy), sep, sz=7.0, clr=GR)
    txt((cx2 + lw + sw, cy), desc, sz=7.0, clr=GR)
    if col == "L":
        ly += STEP
    else:
        ry += STEP

REF_BOTTOM = max(ly, ry)
print(f"Reference strip bottom: y={REF_BOTTOM:.0f}")

# ═══════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════
F_TOP = 762
paint((0, F_TOP, 612, 792), DB)
paint((0, F_TOP, 612, F_TOP + 3), YL)

fl = "NYC Department of Youth and Community Development  |  SYEP Tech Internship Program"
fr = "nyc.gov/dycd"
frw = fitz.get_text_length(fr, fontname='helv', fontsize=7.5)
txt((36,           F_TOP + 15), fl, sz=7.5, clr=WH)
txt((576 - frw,    F_TOP + 15), fr, sz=7.5, clr=YL)

gap_to_footer = F_TOP - REF_BOTTOM
print(f"Gap from reference strip to footer: {gap_to_footer:.0f}pt")
if gap_to_footer < 8:
    print("  ⚠ WARNING: content may overlap footer — reduce spacing or content")
elif gap_to_footer > 80:
    print("  ℹ  Large gap — consider increasing spacing or adding content")
else:
    print("  ✓ Gap looks good")

# ═══════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════
os.makedirs("revised_outputs", exist_ok=True)
doc.save(OUT, garbage=2, deflate=True)
doc.close()
print(f"\nSaved: {OUT}")

# ── Post-save link verification ───────────────────────────────────────────────
vdoc   = fitz.open(OUT)
vlinks = [l for l in vdoc[0].get_links() if l.get('kind') == fitz.LINK_URI]
vdoc.close()

found   = {l['uri'] for l in vlinks}
missing = EXPECTED_URLS - found

print(f"\nLink verification: {len(vlinks)} URI annotations in saved PDF")
if missing:
    for u in missing:
        print(f"  ✗ MISSING: {u}")
else:
    print(f"  ✓ All 6 URLs confirmed present")

# Each URL appears twice (column bullet + reference strip)
from collections import Counter
url_counts = Counter(l['uri'] for l in vlinks)
for url, count in sorted(url_counts.items(), key=lambda x: -x[1]):
    short = url.split('/')[2] + '/...'
    print(f"  {count}× {short}")

print("\nDone.")
