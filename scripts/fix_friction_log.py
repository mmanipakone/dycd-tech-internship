"""
Fix Page 9 friction log guidance text:
- White-paint over the 3 overflowing lines (y=555–605, right column)
- Reinsert 5 clean lines with 13pt spacing and a blank-line gap
"""
import fitz, os

SRC = "revised_outputs/TechInternship_revised.pdf"
TMP = SRC + ".tmp"

WH = (1.0, 1.0, 1.0)
DK = (26/255, 26/255, 26/255)   # 0x1a1a1a

doc = fitz.open(SRC)
p9  = doc[8]

# ── Paint white over the 3 old lines ──────────────────────────────────────
# Covers x=273.6–576, y=555–605 (generous padding around baselines 566/579/592)
shape = p9.new_shape()
shape.draw_rect(fitz.Rect(273.0, 554.0, 577.0, 606.0))
shape.finish(fill=WH, color=None)
shape.commit()

# ── Insert replacement lines ───────────────────────────────────────────────
X   = 273.6
SZ  = 8.5

lines = [
    (566.0, "Use the friction log to record events and identify patterns."),
    # blank line gap at y=579 (no text inserted)
    (592.0, "Consider:"),
    (605.0, "What were you expecting?"),
    (618.0, "What patterns or anomalies stand out?"),
    (631.0, "What would you flag or investigate next?"),
]

for y, text in lines:
    p9.insert_text((X, y), text, fontname='helv', fontsize=SZ, color=DK)

# ── Save ──────────────────────────────────────────────────────────────────
doc.save(TMP, garbage=2, deflate=True)
doc.close()
os.replace(TMP, SRC)
print("Done — friction log text fixed on page 9.")
