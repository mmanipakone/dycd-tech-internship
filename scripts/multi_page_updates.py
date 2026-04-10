"""
Multi-page updates:
  Part 1 — Page 1  (cover): DYCD → DEPARTMENT OF YOUTH AND COMMUNITY DEVELOPMENT
  Part 2 — Page 2  (TOC):   add entry 10; remove all orange right-side page numbers
  Part 3 — Page 3  (Why Host): shorten paragraph + bullet
  Part 4 — Page 16 (deliverables): tighten vertical spacing
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
LG  = (0.886,   0.910,   0.941)    # light-gray separator colour

doc = fitz.open(SRC)

def paint(pg, rect, fill):
    s = pg.new_shape()
    s.draw_rect(fitz.Rect(*rect))
    s.finish(fill=fill, color=None)
    s.commit()

def txt(pg, xy, t, sz=9.0, font='helv', clr=None, ff=None):
    pg.insert_text(xy, t, fontname=font, fontfile=ff, fontsize=sz,
                   color=clr if clr else DK)

def inject_glyph(doc, page, x, y, font_name, font_size, glyph_byte):
    pdf_y     = page.rect.height - y
    glyph_hex = format(glyph_byte, '02x')
    snippet   = (
        f"\nq BT /{font_name} {font_size:.2f} Tf "
        f"1 0 0 1 {x:.3f} {pdf_y:.3f} Tm "
        f"<{glyph_hex}> Tj ET Q\n"
    ).encode('latin-1')
    xrefs = page.get_contents()
    last  = xrefs[-1]
    doc.update_stream(last, doc.xref_stream(last) + snippet)

# ═══════════════════════════════════════════════════════════════════════════
# PART 1 — Page 1: replace cover branding text (all-caps)
# Yellow bar: Rect(43.5, 361.5, 332.25, 379.5)  baseline y=372.8  x=53.7
# Previous mixed-case text ended at x≈235.8 — paint yellow over that area
# New all-caps width: 218.8pt → ends at x≈272.5 — fits (bar right=332.25)
# ═══════════════════════════════════════════════════════════════════════════
p1 = doc[0]
paint(p1, (53.0, 361.5, 290.0, 379.5), YL)     # erase all previous text
txt(p1, (53.7, 372.8),
    "DEPARTMENT OF YOUTH AND COMMUNITY DEVELOPMENT",
    sz=7.5, font='hebo', clr=DB)
print("✓ Part 1: cover branding updated (all-caps)")

# ═══════════════════════════════════════════════════════════════════════════
# PART 2 — Page 2: TOC
#   a) Remove all orange page numbers (right side)
#   b) Add entry 10 — Scenario: Workplace Problem Solving & App Concept Design
# ═══════════════════════════════════════════════════════════════════════════
p2 = doc[1]

# ── a) Remove orange page numbers ─────────────────────────────────────────
# Numbers at x≈565-580; paint white over each one (14pt height clearance)
orange_nums = [
    (570.4, 92.2),    # 3
    (570.4, 135.8),   # 4
    (570.4, 179.2),   # 5
    (570.4, 222.0),   # 6
    (570.4, 265.5),   # 7
    (570.4, 309.0),   # 8
    (564.9, 351.0),   # 9
    (564.9, 402.0),   # 11
    (564.9, 452.2),   # 13
]
for (x, y) in orange_nums:
    paint(p2, (x - 4, y - 11, x + 20, y + 4), WH)
print("✓ Part 2a: orange page numbers removed")

# ── b) Add entry 10 ───────────────────────────────────────────────────────
# Pattern from entries 7-9: separator line → DB square → white number → title text
# Entry 9 ends at y=466.5; separator gap = 11pt; title gap after separator = 18pt

SEP_Y   = 477.75    # separator between entry 9 and 10
T1_Y    = 496.0     # first title line  "Scenario: Workplace Problem Solving &"
T2_Y    = 510.0     # second title line "App Concept Design"
CIR_Y0  = 484.0     # circle/square top
CIR_Y1  = 508.0     # circle/square bottom  (24×24, centred on y=496)
NUM_Y   = 499.0     # number "10" baseline (centre + 3)

# Separator line
paint(p2, (317.25, SEP_Y, 576.0, SEP_Y + 0.75), LG)

# DB square (same dimensions as entries 7-9: 24×24)
paint(p2, (317.2, CIR_Y0, 341.2, CIR_Y1), DB)

# White "10" centred in square
#   square centre x = 317.2 + 12 = 329.2
#   "10" width at 9.5pt hebo ≈ 11.5pt → start at 329.2 - 5.75 = 323.45
w10 = fitz.get_text_length("10", fontname='hebo', fontsize=9.5)
num_x = 329.2 - w10 / 2
txt(p2, (num_x, NUM_Y), "10", sz=9.5, font='hebo', clr=WH)

# Title lines in DB colour at x=351.8
txt(p2, (351.8, T1_Y), "Scenario: Workplace Problem Solving &",
    sz=10.0, font='hebo', clr=DB)
txt(p2, (351.8, T2_Y), "App Concept Design",
    sz=10.0, font='hebo', clr=DB)

print(f"✓ Part 2b: TOC entry 10 added  (title at y={T1_Y}–{T2_Y})")

# ═══════════════════════════════════════════════════════════════════════════
# PART 3 — Page 3: shorten paragraph + first bullet
# ═══════════════════════════════════════════════════════════════════════════
p3 = doc[2]

# ── a) Replace opening paragraph (y=131.2–191.2, 5 lines → 4 lines) ─────
# Column width: x=36 to x≈299 = 263pt; font helv 9.5pt
# Line breaks confirmed within 263pt; em-dash renders fine in helv
paint(p3, (35.0, 123.0, 310.0, 201.0), WH)

para_lines = [
    (131.2, "Hosting a SYEP tech intern creates a mutually beneficial"),
    (146.2, "experience \u2014 interns gain real-world skills aligned to the Portrait"),
    (161.2, "of a Graduate, while employers gain fresh perspectives,"),
    (176.2, "expanded capacity, and a pipeline of diverse future talent."),
]
for (y, line) in para_lines:
    txt(p3, (36.0, y), line, sz=9.5, font='helv', clr=DK)

# ── b) Shorten bullet at y=338.2 ─────────────────────────────────────────
paint(p3, (36.0, 330.0, 300.0, 347.0), WH)
txt(p3, (49.5, 338.2), "Mentor and support emerging talent",
    sz=9.0, font='helv', clr=DK)

print("✓ Part 3: paragraph and bullet updated")

# Verify widths
for (y, line) in para_lines:
    w = fitz.get_text_length(line, fontname='helv', fontsize=9.5)
    assert w <= 263, f"OVERFLOW at y={y}: {w:.1f}pt"
bw = fitz.get_text_length("Mentor and support emerging talent", fontname='helv', fontsize=9.0)
assert bw <= 263, f"Bullet overflow: {bw:.1f}pt"
print(f"  All page 3 lines within 263pt column ✓  (max={max(fitz.get_text_length(l, fontname='helv', fontsize=9.5) for _,l in para_lines):.1f}pt)")

# ═══════════════════════════════════════════════════════════════════════════
# PART 4 — Page 16: tighten deliverable spacing  29.3pt → 16pt
# Header "EXPECTED FINAL DELIVERABLES" at y=459 — do NOT cover
# F100 (✅, xref=86) already in page resources from previous runs
# ═══════════════════════════════════════════════════════════════════════════
p16     = doc[15]
p16_xref = p16.xref

# White out old deliverable area (y=468–635, left column only)
paint(p16, (36.0, 468.0, 300.0, 636.0), WH)

DELIVS = [
    ("Problem Statement",       " \u2014 clearly defined challenge"),
    ("Research Summary",        " \u2014 interviews, observations, insights"),
    ("Workflow Map",            " \u2014 current process visualization"),
    ("Solution Concept",        " \u2014 app/tool/system design"),
    ("Before/After Comparison", " \u2014 time saved or impact"),
    ("Final Presentation",      " \u201410\u201315 slides"),
]

Y_START  = 476.2
Y_STEP   = 16.0    # tightened from 29.3pt

for i, (label, body) in enumerate(DELIVS):
    y = Y_START + i * Y_STEP
    # ✅ glyph via F100 (appended to content stream — renders after white paint)
    inject_glyph(doc, p16, 49.5, y, 'F100', 9.0, 0x0e)
    # bold label
    txt(p16, (63.3, y), label, sz=9.0, font='hebo', clr=DK)
    # em-dash body (AU for unicode dash + digits)
    lw = fitz.get_text_length(label, fontname='hebo', fontsize=9.0)
    txt(p16, (63.3 + lw, y), body, sz=9.0, font='arialuni', ff=AU, clr=DK)

last_y = Y_START + (len(DELIVS) - 1) * Y_STEP
print(f"✓ Part 4: deliverables tightened  y={Y_START:.1f}–{last_y:.1f} (was 476.2–622.7)")

# Preserve F100/F28 in page 16 Resources (unchanged from prior sessions)
doc.xref_set_key(
    p16_xref, "Resources",
    "<</Font<</arialuni 2122 0 R/hebo 2120 0 R/helv 2121 0 R"
    "/F100 86 0 R/F28 26 0 R>>>>"
)

# ─────────────────────────────────────────────────────────────────────────
doc.save(TMP, garbage=2, deflate=True)
doc.close()
os.replace(TMP, SRC)
print("\nAll updates saved successfully.")
