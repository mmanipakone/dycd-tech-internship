"""
Three targeted PDF updates:
  1. Page 13 — change "Team Size: 4–5 Interns" → "Team Size: 1–5 Interns"
  2. Standalone 1on1_CheckIn_Template.pdf — remove "09" page numbers (header + footer)
  3. Cover page (page 1) — replace "D Y C D" with "Department of Youth and Community Development"
"""
import fitz
import os

# ─────────────────────────────────────────────────────────────────────────────
MAIN_SRC = "revised_outputs/TechInternship_revised.pdf"
MAIN_TMP = MAIN_SRC + ".tmp"
T_SRC    = "revised_outputs/1on1_CheckIn_Template.pdf"
T_TMP    = T_SRC + ".tmp"

DB = (0.03920, 0.14510, 0.25100)
WH = (1.0,     1.0,     1.0)
YL = (1.0,     0.902,   0.0)

def paint_rect(pg, rect, fill):
    shape = pg.new_shape()
    shape.draw_rect(fitz.Rect(*rect))
    shape.finish(fill=fill, color=None)
    shape.commit()

# ═══════════════════════════════════════════════════════════════════════════
# PART 1 — Page 13: "Team Size: 4–5 Interns" → "Team Size: 1–5 Interns"
# Subheader bar: DB Rect(0, 0, 612, 74.25)
# "4–5" word bbox: (380.97, 50.35, 395.99, 60.41), span baseline y=58.5
# "4" and "1" both measure 5.0pt at 9pt helv — zero layout impact
# ═══════════════════════════════════════════════════════════════════════════
doc_main = fitz.open(MAIN_SRC)
p13 = doc_main[12]

# Paint DB over the "4" character only (x=380.97, width≈5pt)
paint_rect(p13, (380.5, 49.5, 386.5, 61.5), DB)

# Reinsert "1" at exact same position, same style (ArialMT≈helv, 9pt white)
p13.insert_text((380.97, 58.5), "1", fontname='helv', fontsize=9.0, color=WH)

print("✓ Part 1: Page 13 Team Size updated: 4–5 → 1–5")

# ═══════════════════════════════════════════════════════════════════════════
# PART 3 — Cover page: "D Y C D" → "Department of Youth and Community Development"
# Yellow bar: Rect(43.5, 361.5, 332.25, 379.5)
# "D Y C D" text: font Arial-BoldMT≈hebo, size=7.5, color=DB, baseline y=372.8
# New text width at 7.5pt hebo: 182.1pt — fits comfortably (available ~278pt)
# ═══════════════════════════════════════════════════════════════════════════
p1 = doc_main[0]

# Paint yellow over the old "D Y C D" area (x=53.7 to ~82, full bar height)
paint_rect(p1, (53.0, 361.5, 120.0, 379.5), YL)

# Insert full name at same baseline and x-start
new_cover_text = "Department of Youth and Community Development"
p1.insert_text((53.7, 372.8), new_cover_text,
               fontname='hebo', fontsize=7.5, color=DB)

# Verify width fits
w_new = fitz.get_text_length(new_cover_text, fontname='hebo', fontsize=7.5)
print(f"✓ Part 3: Cover page DYCD replaced  (text width={w_new:.1f}pt, bar available≈278pt)")

# Save main document
doc_main.save(MAIN_TMP, garbage=2, deflate=True)
doc_main.close()
os.replace(MAIN_TMP, MAIN_SRC)
print("  Main document saved.\n")

# ═══════════════════════════════════════════════════════════════════════════
# PART 2 — 1:1 Check-In Template: remove "09" page numbers
# Header bar: DB Rect(0, 0, 612, 40.5)  — "09" at x=567.1, baseline y=22.5, sz=8, white
# Footer bar: DB Rect(0, 769.5, 612, 792) — "09" at x=566.9, baseline y=783.0, sz=7.5, yellow
# Paint DB over both "09" areas — no replacement text (standalone doc needs no page number)
# ═══════════════════════════════════════════════════════════════════════════
doc_t = fitz.open(T_SRC)
pt = doc_t[0]

# Remove header "09"  (width of "09" at 8pt ≈ 11pt; add generous margin)
paint_rect(pt, (560.0, 13.0, 598.0, 33.0), DB)

# Remove footer "09"  (width of "09" at 7.5pt ≈ 10pt)
paint_rect(pt, (560.0, 773.0, 598.0, 790.0), DB)

print("✓ Part 2: 1:1 template page numbers removed (header + footer)")

doc_t.save(T_TMP, garbage=2, deflate=True)
doc_t.close()
os.replace(T_TMP, T_SRC)
print("  Standalone template saved.")
