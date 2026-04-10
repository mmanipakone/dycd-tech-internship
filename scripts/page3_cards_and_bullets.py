"""
page3_cards_and_bullets.py
  Issue 1: Metric cards ('6'/'25') — shift content down 8pt inside containers
            for clear top padding (no touching top border)
  Issue 2: Benefits bullets — replace with full 5-bullet list,
            matching original dark-square markers and 15.75pt line spacing
"""
import fitz, os

SRC = "revised_outputs/TechInternship_revised.pdf"
TMP = SRC + ".tmp"

DB  = (0.03920, 0.14510, 0.25100)
WH  = (1.0, 1.0, 1.0)
DK  = (26/255, 26/255, 26/255)
YL  = (1.0, 0.902, 0.0)          # #ffe600 — metric numbers
DR  = (0.102, 0.102, 0.102)       # ~#1a1a1a — bullet square markers

doc = fitz.open(SRC)
p3  = doc[2]

def paint(pg, rect, fill):
    s = pg.new_shape()
    s.draw_rect(fitz.Rect(*rect))
    s.finish(fill=fill, color=None)
    s.commit()

# ═══════════════════════════════════════════════════════════════════════════
# ISSUE 1 — Move metric cards down SHIFT pt
# ═══════════════════════════════════════════════════════════════════════════
SHIFT = 8.0

# Container geometry
L_X0, L_X1 = 36.0, 163.5   # left  container x bounds
R_X0, R_X1 = 171.0, 298.5  # right container x bounds
L_CTR = (L_X0 + L_X1) / 2  # 99.75
R_CTR = (R_X0 + R_X1) / 2  # 234.75

# Paint DB over original content (y=206–263.5) in both containers
# to hide original yellow numbers + white labels
paint(p3, (L_X0 + 1, 206.0, L_X1 - 1, 263.5), DB)
paint(p3, (R_X0 + 1, 206.0, R_X1 - 1, 263.5), DB)

# Re-insert numbers (hebo 24pt, yellow) — centred in each container
for text, ctr in [("6", L_CTR), ("25", R_CTR)]:
    w = fitz.get_text_length(text, fontname='hebo', fontsize=24.0)
    p3.insert_text((ctr - w / 2, 221.2 + SHIFT),
                   text, fontname='hebo', fontsize=24.0, color=YL)

# Re-insert labels (helv 8pt, white) — centred in each container
for text, ctr, orig_y in [
    ("WEEKS OF STRUCTURED", L_CTR, 235.5),
    ("LEARNING",            L_CTR, 249.8),
    ("HOURS/WEEK ON-SITE",  R_CTR, 235.5),
]:
    w = fitz.get_text_length(text, fontname='helv', fontsize=8.0)
    p3.insert_text((ctr - w / 2, orig_y + SHIFT),
                   text, fontname='helv', fontsize=8.0, color=WH)

print(f"✓ Issue 1: metric cards shifted down {SHIFT}pt")
print(f"  '6' / '25' new baseline y={221.2 + SHIFT}")
print(f"  'LEARNING'  new baseline y={249.8 + SHIFT}  "
      f"(bottom ≈{249.8 + SHIFT + 2:.1f} vs container bottom 263.5 ✓)")

# ═══════════════════════════════════════════════════════════════════════════
# ISSUE 2 — Replace bullet section with full 5-bullet list
# ═══════════════════════════════════════════════════════════════════════════
# Orange bar: y=271.5–293.25  →  start paint at y=293.5 (0.25pt clearance)
# Impact box starts at y=396.75  →  stop paint at y=396.0

paint(p3, (36.0, 293.5, 300.0, 396.0), WH)   # wipe entire bullet area

BULLETS = [
    "Fresh perspectives and innovative ideas on real projects",
    "Expanded project capacity at no direct labor cost",
    "Early access to diverse NYC talent pipeline",
    "Strengthen community ties and corporate responsibility",
    "Mentor and support emerging talent",
]

# Original design: 3×3 dark-square markers; text baseline = marker-centre + 2.25pt
# Spacing = 15.75pt between markers (matches original 5-bullet layout)
# First marker y0 = 305.0  →  ~11.75pt gap below bar bottom (bar ends at 293.25)
MARKER_SZ   = 3.0
MARKER_STEP = 15.75
MARKER_X0   = 39.0
FIRST_MARKER_Y0 = 305.0

print("\n✓ Issue 2: 5-bullet list inserted")
for i, bullet_text in enumerate(BULLETS):
    marker_y0 = FIRST_MARKER_Y0 + i * MARKER_STEP
    marker_y1 = marker_y0 + MARKER_SZ
    text_y    = (marker_y0 + marker_y1) / 2 + 2.25   # baseline = marker-centre + 2.25

    # Dark square bullet marker
    paint(p3, (MARKER_X0, marker_y0, MARKER_X0 + MARKER_SZ, marker_y1), DR)

    # Bullet text
    p3.insert_text((49.5, text_y), bullet_text,
                   fontname='helv', fontsize=8.5, color=DK)

    w = fitz.get_text_length(bullet_text, fontname='helv', fontsize=8.5)
    print(f"  y={text_y:.1f}: {w:.1f}pt  {repr(bullet_text[:58])}")

# ─────────────────────────────────────────────────────────────────────────
doc.save(TMP, garbage=2, deflate=True)
doc.close()
os.replace(TMP, SRC)
print("\nDone.")
