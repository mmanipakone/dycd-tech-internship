"""
fix_p1_redesign.py — Page 1 final redesign.
Logo: Rect(400, 370, 580, 560)
Label: Rect(43, 350, 300, 380)  BLACK text, 9pt helv
Navy: Rect(0, 350, 612, 410)
"""
import fitz, os

SRC  = "revised_outputs/TechInternship_revised.pdf"
TMP  = SRC + ".tmp"

DB = (0.03920, 0.14510, 0.25100)
OR = (0.91000, 0.29410, 0.00000)
YL = (1.00000, 0.90200, 0.00000)
BK = (0.0,     0.0,     0.0   )

LOGO = "Student Pathways Logos/PNG/NYCPS-Pathways-logo-color.png"

doc = fitz.open(SRC)
p1  = doc[0]


def paint(rect, fill):
    s = p1.new_shape()
    s.draw_rect(fitz.Rect(*rect))
    s.finish(fill=fill, color=None)
    s.commit()


# ── Step 1: Remove old logo image from band zone ──────────────────────────────
# Rect(0,350,612,400) catches small logo (bbox 494,358–522,394) + any band images.
# graphics=0 preserves existing vector fills (we cover them with paint later).
p1.add_redact_annot(fitz.Rect(0, 350, 612, 400))
p1.apply_redactions(images=1, graphics=0)
print("✓ Step 1: Old logo image removed from band zone")


# ── Step 2: Remove old text (Dept text + HIGH SCHOOL) — text-only ─────────────
# Zone A: catches "Department of Youth..." (bbox_top=369.9 in [350,383))
# Zone B: catches HIGH SCHOOL (bbox_top=383.6 in [383,429))
#          stops before TECH INTERNSHIP (bbox_top=429.7 > 429)
p1.add_redact_annot(fitz.Rect(0,  350, 612, 383))   # Dept text zone
p1.add_redact_annot(fitz.Rect(43, 383, 285, 429))   # HIGH SCHOOL zone
p1.apply_redactions(images=0, graphics=0)
print("✓ Step 2: Old Dept text and HIGH SCHOOL removed from stream (text-only)")


# ── Step 3: Paint navy over entire ex-band zone + HIGH SCHOOL redact area ─────
# Rect(0,350,612,410): user-specified navy repaint, covers old band + white fills
# Rect(0,410,612,431): covers white fill from HIGH SCHOOL redact at y=410-429
#                       stops before TECH INTERNSHIP visible caps (~y=435)
paint((0, 350, 612, 410), DB)
paint((0, 410, 612, 431), DB)
print("✓ Step 3: Navy painted at y=350–410 (full width) and y=410–431 (patch)")


# ── Step 4: Yellow label bar (left-aligned tag) ───────────────────────────────
paint((43, 350, 300, 380), YL)
print("✓ Step 4: Yellow label painted at Rect(43, 350, 300, 380)")


# ── Step 5: Department text inside label (BLACK) ──────────────────────────────
# 12pt left padding (x=55), baseline y=368 (centered in 30pt bar)
p1.insert_text((55, 368),
               "Department of Youth and Community Development",
               fontname='helv', fontsize=9, color=BK)
print("✓ Step 5: Dept text inserted — black, helv 9pt, x=55, y=368")


# ── Step 6: Color Student Pathways logo (large, right column) ────────────────
# Rect(400,370,580,560): 180×190pt container. Logo PNG 578×751 (aspect 0.77).
# keep_proportion → actual render ~146×190pt, transparent bg floats on navy.
p1.insert_image(fitz.Rect(400, 370, 580, 560),
                filename=LOGO,
                keep_proportion=True,
                overlay=True)
print("✓ Step 6: Color logo inserted at Rect(400, 370, 580, 560)")


# ── Step 7: Reinsert HIGH SCHOOL last (renders on top of all fills) ───────────
# Exact original: x=43, baseline=420, sz=34, hebo, orange
p1.insert_text((43, 420), "HIGH SCHOOL",
               fontname='hebo', fontsize=34, color=OR)
print("✓ Step 7: HIGH SCHOOL reinserted at x=43, baseline=420 (same position)")


# ── Save ──────────────────────────────────────────────────────────────────────
doc.save(TMP, garbage=4, deflate=True)
doc.close()
os.replace(TMP, SRC)
print(f"\n✅  Saved → {SRC}")
