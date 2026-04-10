"""
fix_p1_p3_p4.py
Targeted fixes for Page 1 (cover), Page 3 (right column bullets), Page 4 (overflow line).
All removals use add_redact_annot + apply_redactions — no overlays.
"""
import fitz, os

SRC = "revised_outputs/TechInternship_revised.pdf"
TMP = SRC + ".tmp"
AU  = '/Library/Fonts/Arial Unicode.ttf'

DB  = (0.03920, 0.14510, 0.25100)
OR  = (0.91000, 0.29410, 0.00000)   # #E84B00
YL  = (1.00000, 0.90200, 0.00000)
WH  = (1.00000, 1.00000, 1.00000)
DK  = (26/255,  26/255,  26/255)

doc = fitz.open(SRC)


def redact(pg, rects):
    for r in rects:
        pg.add_redact_annot(fitz.Rect(*r))
    pg.apply_redactions()

def paint(pg, rect, fill):
    s = pg.new_shape()
    s.draw_rect(fitz.Rect(*rect))
    s.finish(fill=fill, color=None)
    s.commit()

def txt(pg, xy, text, sz=9.0, font='helv', clr=DK):
    pg.insert_text(xy, text, fontname=font, fontsize=sz, color=clr)

def au(pg, xy, text, sz=9.0, clr=DK):
    pg.insert_text(xy, text, fontname='arialuni', fontfile=AU,
                   fontsize=sz, color=clr)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Cover fixes
# ═══════════════════════════════════════════════════════════════════════════════
p1 = doc[0]

# Step 1: Redact cover photo zone and white logo
redact(p1, [
    (0,   0,   612, 354),   # cover photo area (and any image overlap into band)
    (439, 355, 578, 395),   # white logo
])

# Step 2: Restore the band portions that were cleared by the redactions
# y=352–354 strip (cleared by first redact)
paint(p1, (0,   352, 612, 354), YL)   # yellow strip
paint(p1, (0,   352, 142, 354), DB)   # dark-blue badge strip
# logo zone background (cleared by second redact)
paint(p1, (439, 355, 578, 395), YL)   # yellow under new logo

# Step 3: Insert new cover image (ends at y=352, above band)
cover = "studenttechpictures/241116_jca_inspiredu_1345_54365173654_l.jpg"
p1.insert_image(fitz.Rect(0, 0, 612, 352), filename=cover,
                keep_proportion=False, overlay=False)

# Step 4: Restore "HIGH SCHOOL" title (sz=34, bold, orange)
# Original bbox_top y=392 → baseline = 392 + 34*0.72 ≈ 416; user spec: ~420
txt(p1, (43, 420), "HIGH SCHOOL", sz=34, font='hebo', clr=OR)

# Step 5: Insert color Student Pathways logo
logo = "Student Pathways Logos/PNG/NYCPS-Pathways-logo-color.png"
p1.insert_image(fitz.Rect(440, 356, 576, 393), filename=logo,
                keep_proportion=True, overlay=True)

print("✓ P1: New cover image, HIGH SCHOOL restored, color logo inserted")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Right column bullet fixes only (x=312–576)
# Left column and all section headers untouched
# ═══════════════════════════════════════════════════════════════════════════════
p3 = doc[2]

# Step 1: Redact stray characters and all three bullet zones
redact(p3, [
    (313, 329, 315, 347),    # stray 't' (left of "What They Bring" header)
    (326, 243, 576, 310),    # Who They Are bullet zone (also covers stray 'ms' at x=516)
    (326, 354, 576, 420),    # What They Bring bullet zone
    (326, 452, 576, 535),    # What They Need bullet zone
])

# Step 2: Reinsert bullets — sz=9, color DK (#1a1a1a), ~15pt line spacing
# Baselines derived from original bbox_top positions + 7pt ascender offset

# ── Who They Are (4 bullets, first bbox_top=247) ─────────────────────────────
WHO_BASELINES = [254, 269, 285, 300]
WHO_BULLETS = [
    "NYC high school students, ages 16\u201321",
    "Enrolled in SYEP through DYCD-funded programs",
    "Curious, motivated, and eager to learn",
    "Bring varying levels of prior tech experience",
]
for y, line in zip(WHO_BASELINES, WHO_BULLETS):
    txt(p3, (327, y), line)

# ── What They Bring (4 bullets, first bbox_top=358) ──────────────────────────
BRING_BASELINES = [365, 381, 396, 412]
BRING_BULLETS = [
    "Curiosity and creativity in approaching new challenges",
    "Emerging critical thinking and problem-solving skills",
    "Developing communication skills across diverse environments",
    "Unique perspectives and lived experiences",
]
for y, line in zip(BRING_BASELINES, BRING_BULLETS):
    txt(p3, (327, y), line)

# ── What They Need (5 bullets, first bbox_top=456) ───────────────────────────
NEED_BASELINES = [463, 478, 493, 508, 523]
NEED_BULLETS = [
    "Clear structure, expectations, and onboarding",
    "A dedicated supervisor/mentor (1:1 weekly check-ins)",
    "Authentic, meaningful project work",
    "Regular feedback and encouragement",
    "Safe, professional, and inclusive environment",
]
for y, line in zip(NEED_BASELINES, NEED_BULLETS):
    txt(p3, (327, y), line)

print("✓ P3: Stray chars removed, all 13 bullets reinserted")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — Overflow line replacement
# ═══════════════════════════════════════════════════════════════════════════════
p4 = doc[3]

# Redact overflow line ("Iterate on assigned tasks based on feedback")
# bbox: x=236–415, y=272–284 → redact with small margin
redact(p4, [(235, 270, 416, 286)])

# Reinsert shorter version at same x, same baseline (y≈282 from bbox_top=272+10)
txt(p4, (236, 282), "Iterate on tasks using feedback")

print("✓ P4: Overflow line replaced")


# ═══════════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════════
doc.save(TMP, garbage=4, deflate=True)
doc.close()
os.replace(TMP, SRC)
print(f"\n✅  Saved → {SRC}")
