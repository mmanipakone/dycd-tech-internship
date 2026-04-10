"""
fix_p1_cover.py
Page 1 cover fix — approved plan execution.
Photo: 241116_jca_inspiredu_1143_54365363760_l.jpg
"""
import fitz, os

SRC  = "revised_outputs/TechInternship_revised.pdf"
TMP  = SRC + ".tmp"

DB = (0.03920, 0.14510, 0.25100)
OR = (0.91000, 0.29410, 0.00000)
YL = (1.00000, 0.90200, 0.00000)
WH = (1.00000, 1.00000, 1.00000)

COVER = "studenttechpictures/241116_jca_inspiredu_1143_54365363760_l.jpg"
LOGO  = "Student Pathways Logos/PNG/NYCPS-Pathways-logo-color.png"

# apply_redactions integer constants (0=none, 1=remove)
IMG_REMOVE = 1
IMG_NONE   = 0
ART_NONE   = 0

doc = fitz.open(SRC)
p1  = doc[0]


def paint(rect, fill):
    s = p1.new_shape()
    s.draw_rect(fitz.Rect(*rect))
    s.finish(fill=fill, color=None)
    s.commit()


# ── Step 1: Remove old/broken image layers ────────────────────────────────────
# Removes the 3 stacked image XObjects (bboxes ending at y=352, 355, 394.5).
# LINE_ART_NONE preserves the DB full-page navy fill and all band vector fills.
p1.add_redact_annot(fitz.Rect(0, 0, 612, 355))
p1.apply_redactions(images=IMG_REMOVE, graphics=ART_NONE)
print("✓ Step 1: Old cover images removed (vector fills preserved)")


# ── Step 2: Insert new cover photo ────────────────────────────────────────────
# overlay=True places the image AFTER the DB fill in the stream → visible.
p1.insert_image(fitz.Rect(0, 0, 612, 350),
                filename=COVER,
                keep_proportion=False,
                overlay=True)
print("✓ Step 2: Cover image 1143 inserted at Rect(0,0,612,350)")


# ── Step 3: Semi-transparent navy overlay over photo ─────────────────────────
# PyMuPDF ExtGState fill_opacity — no PIL, no compositing.
s = p1.new_shape()
s.draw_rect(fitz.Rect(0, 0, 612, 350))
s.finish(fill=DB, fill_opacity=0.4, color=None)
s.commit()
print("✓ Step 3: Navy overlay 40% opacity applied (Rect 0,0,612,350)")


# ── Step 4: Remove band texts + HIGH SCHOOL in one batched text-only pass ─────
# Zone A (0,350,612,378): catches "D Y C D" (y=361–371) and
#   "Department of Youth..." (bbox_top=374.9) — stops before HIGH SCHOOL (383.6)
# Zone B (0,383,612,430): catches HIGH SCHOOL (bbox_top=383.6) —
#   stops before TECH INTERNSHIP (bbox_top=429.7)
# IMG_NONE + ART_NONE = text-only removal; all vector fills survive.
p1.add_redact_annot(fitz.Rect(0, 350, 612, 378))
p1.add_redact_annot(fitz.Rect(0, 383, 612, 430))
p1.apply_redactions(images=IMG_NONE, graphics=ART_NONE)
print("✓ Step 4: D Y C D, Dept text, and HIGH SCHOOL removed from stream")


# ── Step 5: Repaint yellow band + restore navy below band ────────────────────
# YL covers y=352–398 (full band, including white fills from step 4 redacts).
# DB covers y=398–430 (restores navy background behind HIGH SCHOOL text zone).
paint((0, 352, 612, 398), YL)
paint((0, 398, 612, 430), DB)
print("✓ Step 5: Yellow band repainted (352–398), navy restored (398–430)")


# ── Step 6: Remove old logo image, restore band at logo zone ─────────────────
p1.add_redact_annot(fitz.Rect(439, 355, 578, 395))
p1.apply_redactions(images=IMG_REMOVE, graphics=ART_NONE)
paint((439, 352, 578, 398), YL)   # restore band under new logo
print("✓ Step 6: Old logo removed, band restored at logo zone")


# ── Step 7: Insert department text (no D Y C D anywhere) ─────────────────────
p1.insert_text((43, 379),
               "Department of Youth and Community Development",
               fontname='helv', fontsize=8.5, color=WH)
print("✓ Step 7: Dept text inserted at (43, 379) — white, helv, 8.5pt")


# ── Step 8: Insert color Pathways logo ───────────────────────────────────────
p1.insert_image(fitz.Rect(440, 358, 576, 394),
                filename=LOGO,
                keep_proportion=True,
                overlay=True)
print("✓ Step 8: Color Pathways logo inserted at Rect(440,358,576,394)")


# ── Step 9: Reinsert HIGH SCHOOL (last in stream → renders on top of band) ───
# Exact original position: x=43, baseline y=420, sz=34, hebo, orange.
p1.insert_text((43, 420), "HIGH SCHOOL",
               fontname='hebo', fontsize=34, color=OR)
print("✓ Step 9: HIGH SCHOOL reinserted at x=43, baseline=420 (same position)")


# ── Save ──────────────────────────────────────────────────────────────────────
doc.save(TMP, garbage=4, deflate=True)
doc.close()
os.replace(TMP, SRC)
print(f"\n✅  Saved → {SRC}")
