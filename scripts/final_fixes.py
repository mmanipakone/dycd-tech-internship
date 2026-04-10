"""
Final round fixes:
  Page 3:
    1. Re-anchor paragraph with 14pt spacing so last line y=187.2 < container top 190.5
    2. Restore container tops (blue) that were white-painted by prior scripts
    3. Hide excess bullets at y=306.8, 322.5, 369.8
  Page 16:
    4. "6-WEEK PROJECT STRUCTURE"     → orange
    5. "EXPECTED FINAL DELIVERABLES"  → orange
    6. "KEY LEARNING OUTCOMES"        → orange
"""
import fitz, os

SRC = "revised_outputs/TechInternship_revised.pdf"
TMP = SRC + ".tmp"
AU  = '/Library/Fonts/Arial Unicode.ttf'

DB  = (0.03920, 0.14510, 0.25100)
OR  = (0.91000, 0.29410, 0.00000)
WH  = (1.0, 1.0, 1.0)
DK  = (26/255, 26/255, 26/255)

doc = fitz.open(SRC)

def paint(pg, rect, fill):
    s = pg.new_shape()
    s.draw_rect(fitz.Rect(*rect))
    s.finish(fill=fill, color=None)
    s.commit()

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 3
# ═══════════════════════════════════════════════════════════════════════════
p3 = doc[2]

# ── 1. White-paint paragraph area only (stop at container top y=190.5) ────
# Prior scripts painted to y=201 and y=205, covering container tops.
# This new layer (appended last) covers the paragraph area.
paint(p3, (35.0, 123.0, 310.0, 190.5), WH)

# ── 2. Re-insert paragraph with 14pt line spacing ─────────────────────────
# 5 lines: y = 131.2, 145.2, 159.2, 173.2, 187.2 — all < 190.5 ✓
SZ = 9.5
X  = 36.0

# Line 1
p3.insert_text((X, 131.2),
    "Hosting a SYEP tech intern creates a mutually beneficial",
    fontname='helv', fontsize=SZ, color=DK)

# Line 2 — helv + AU em-dash + helv to render "—" properly
pre_text  = "experience "
post_text = " interns gain real-world skills aligned to the"
w_pre     = fitz.get_text_length(pre_text, fontname='helv', fontsize=SZ)
p3.insert_text((X, 145.2), pre_text,
               fontname='helv', fontsize=SZ, color=DK)
x_dash = X + w_pre
p3.insert_text((x_dash, 145.2), "\u2014",
               fontname='arialuni', fontfile=AU, fontsize=SZ, color=DK)
w_dash_helv = fitz.get_text_length("\u2014", fontname='helv', fontsize=SZ)
x_post = x_dash + w_dash_helv + 3.86
p3.insert_text((x_post, 145.2), post_text,
               fontname='helv', fontsize=SZ, color=DK)

# Lines 3–5
for y, text in [
    (159.2, "Portrait of a Graduate, while employers gain fresh"),
    (173.2, "perspectives, expanded capacity, and a pipeline of diverse"),
    (187.2, "future talent."),
]:
    p3.insert_text((X, y), text, fontname='helv', fontsize=SZ, color=DK)

# ── 3. Restore container tops with blue ───────────────────────────────────
# Prior white paints covered y=190.5–205 in both containers.
# Repaint top strip blue (appended last = renders on top of white).
# These rects are the top 15.5pt of each container.
paint(p3, (36.0,  190.5, 163.5, 206.0), DB)   # left  container
paint(p3, (171.0, 190.5, 298.5, 206.0), DB)   # right container

# ── 4. Hide excess bullets ─────────────────────────────────────────────────
# Keep: y=338.2 "Mentor and support emerging talent"
#       y=354.0 "Strengthen commitment to community and workforce development"
# Hide: y=306.8 "Fresh perspectives..."
#       y=322.5 "Expanded team capacity..."  (single rect covers both)
#       y=369.8 "Contribute to preparing..."
paint(p3, (36.0, 298.0, 300.0, 330.0), WH)   # hides y=306.8 & y=322.5
paint(p3, (36.0, 360.0, 300.0, 381.0), WH)   # hides y=369.8

print("✓ Page 3: paragraph anchored (14pt spacing), containers restored, "
      "excess bullets hidden")

# Verify line widths
print("  Line widths (should all be ≤263pt):")
checks = [
    (131.2, "Hosting a SYEP tech intern creates a mutually beneficial"),
    (159.2, "Portrait of a Graduate, while employers gain fresh"),
    (173.2, "perspectives, expanded capacity, and a pipeline of diverse"),
    (187.2, "future talent."),
]
for y, t in checks:
    w = fitz.get_text_length(t, fontname='helv', fontsize=SZ)
    print(f"    y={y}  {w:.1f}pt  {repr(t[:60])}")

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 16
# ═══════════════════════════════════════════════════════════════════════════
p16 = doc[15]

# ── 5. "6-WEEK PROJECT STRUCTURE" → orange ────────────────────────────────
# Current: y=75.8, x=36, sz=15, hebo, color=DB
# Yellow decorative bar at y=81.75 — paint stops at 80.5 to preserve it
w_hdr1 = fitz.get_text_length("6-WEEK PROJECT STRUCTURE", fontname='hebo', fontsize=15.0)
paint(p16, (35.0, 62.0, 36.0 + w_hdr1 + 5, 80.5), WH)
p16.insert_text((36.0, 75.8), "6-WEEK PROJECT STRUCTURE",
                fontname='hebo', fontsize=15.0, color=OR)
print(f"✓ Page 16: '6-WEEK PROJECT STRUCTURE' → orange  (width={w_hdr1:.1f}pt)")

# ── 6. "EXPECTED FINAL DELIVERABLES" → orange ─────────────────────────────
# Current: y=459.0, x=36.0, sz=10, hebo, color=DB
w_hdr2 = fitz.get_text_length("EXPECTED FINAL DELIVERABLES", fontname='hebo', fontsize=10.0)
paint(p16, (35.0, 448.5, 36.0 + w_hdr2 + 5, 462.0), WH)
p16.insert_text((36.0, 459.0), "EXPECTED FINAL DELIVERABLES",
                fontname='hebo', fontsize=10.0, color=OR)
print(f"✓ Page 16: 'EXPECTED FINAL DELIVERABLES' → orange  (width={w_hdr2:.1f}pt)")

# ── 7. "KEY LEARNING OUTCOMES" → orange ───────────────────────────────────
# Current: y=459.0, x=311.2, sz=10, hebo, color=DB
w_hdr3 = fitz.get_text_length("KEY LEARNING OUTCOMES", fontname='hebo', fontsize=10.0)
paint(p16, (310.0, 448.5, 311.2 + w_hdr3 + 5, 462.0), WH)
p16.insert_text((311.2, 459.0), "KEY LEARNING OUTCOMES",
                fontname='hebo', fontsize=10.0, color=OR)
print(f"✓ Page 16: 'KEY LEARNING OUTCOMES' → orange  (width={w_hdr3:.1f}pt)")

# ─────────────────────────────────────────────────────────────────────────
doc.save(TMP, garbage=2, deflate=True)
doc.close()
os.replace(TMP, SRC)
print("\nDone.")
