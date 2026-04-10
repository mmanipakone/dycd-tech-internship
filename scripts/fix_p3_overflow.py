"""
fix_p3_overflow.py
Erase text-overflow artifacts in the column-gutter zone (x=298–313.5) on page 3.

Root cause: all prior white paints in the left column stopped at x=300.
Old paragraph lines (y=123–205) and old bullet text (y=293–396) that
extended slightly past x=300 were never covered — leaving partial
character fragments ("nt", "ns", etc.) visible in the gutter.

Fix: two narrow white-paint strips covering x=298–313.5 for each y range.
Right column content (bars at x=313.5, text at x=322.5+) is untouched.
"""
import fitz, os

SRC = "revised_outputs/TechInternship_revised.pdf"
TMP = SRC + ".tmp"

WH = (1.0, 1.0, 1.0)

doc = fitz.open(SRC)
p3  = doc[2]

def paint(pg, rect, fill):
    s = pg.new_shape()
    s.draw_rect(fitz.Rect(*rect))
    s.finish(fill=fill, color=None)
    s.commit()

# ── Strip 1: paragraph zone (old multi-line paragraphs had long lines) ────
# Old paragraph versions at y=123–205 extended up to ~x=326 originally,
# with only x=35–310 white-painted. Cover x=298–313.5 for that y range.
paint(p3, (298.0, 120.0, 313.5, 207.0), WH)
print("✓ Strip 1: x=298–313.5, y=120–207 (paragraph gutter) cleared")

# ── Strip 2: bullet zone (old bullets: "Opportunity…emerging talent" etc.) ─
# Bullets starting at x=49.5 with widths up to ~255pt end around x=305.
# Prior bullet white paints covered x=36–300 only.
paint(p3, (298.0, 293.0, 313.5, 400.0), WH)
print("✓ Strip 2: x=298–313.5, y=293–400 (bullet gutter) cleared")

doc.save(TMP, garbage=2, deflate=True)
doc.close()
os.replace(TMP, SRC)
print("Done.")
