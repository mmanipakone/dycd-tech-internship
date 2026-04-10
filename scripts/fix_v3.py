"""
fix_v3.py — Round 3 targeted fixes.
Pages: 3 (missing header line + stat numbers), 6 (truncated right-column header),
       15 (paragraph bleed fix + Research Lead row)
"""
import fitz, os

SRC = "revised_outputs/TechInternship_revised.pdf"
TMP = SRC + ".tmp"

AB  = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
AU  = "/Library/Fonts/Arial Unicode.ttf"

DB  = (0.03920, 0.14510, 0.25100)
OR  = (0.91000, 0.29410, 0.00000)
WH  = (1.00000, 1.00000, 1.00000)
DK  = (26/255,  26/255,  26/255)
LB  = (0.969,   0.973,   0.980)

doc = fitz.open(SRC)


def paint(pg, rect, fill):
    s = pg.new_shape()
    s.draw_rect(fitz.Rect(*rect))
    s.finish(fill=fill, color=None)
    s.commit()

def ab(pg, xy, text, sz, clr=WH):
    pg.insert_text(xy, text, fontname='arialbold', fontfile=AB, fontsize=sz, color=clr)

def hebo(pg, xy, text, sz, clr=WH):
    pg.insert_text(xy, text, fontname='hebo', fontsize=sz, color=clr)

def helv(pg, xy, text, sz, clr=DK):
    pg.insert_text(xy, text, fontname='helv', fontsize=sz, color=clr)

def bl(y_top, sz, r=0.91):
    return y_top + sz * r


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 (doc[2]) — Fix A: Missing second header line "SYEP tech intern"
#
# global_sentence_case.py redacted zone (36,64,300,86) covering both header
# lines ("WHY HOST A" + "SYEP TECH INTERN"), but only re-inserted "Why host a".
# The second line was lost. Body text starts at y=119.9 — ~17pt clearance.
#
# Fix: INSERT second line at bl(88.4, 16) using Arial-BoldMT, OR, sz=16.
# No redaction needed — the space is blank (existing insert can only add).
# ═══════════════════════════════════════════════════════════════════════════════
p3 = doc[2]

ab(p3, (36, bl(88.4, 16)), "SYEP tech intern", 16, OR)
# bl(88.4, 16) = 88.4 + 14.56 = 102.96

print("✓ P3 Fix A: Second header line 'SYEP tech intern' inserted at bl(88.4,16)=103")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 (doc[2]) — Fix B: Missing stat numbers "6" and "25"
#
# global_sentence_case.py painted DB fills over the entire stat box area
# (y=207–264), covering the original large-number glyphs. Labels were
# reinserted but numbers were not.
#
# Box geometry (from get_drawings):
#   Box 1: rect=[37.0, 207.0, 162.5, 264.0], center_x=99.75
#   Box 2: rect=[172.0, 207.0, 297.5, 264.0], center_x=234.75
# Labels at y=233.1 — numbers sit above them at y_top≈209.
#
# Fix: INSERT "6" and "25" centered above labels using hebo WH sz=20.
#   "6"  is ~1 char wide; at sz=20 approx 11pt → x = center_x - 5.5 = 94.25
#   "25" is ~2 chars wide; at sz=20 approx 22pt → x = center_x - 11 = 223.75
# ═══════════════════════════════════════════════════════════════════════════════

hebo(p3, (94,  bl(209, 20)), "6",  20, WH)
hebo(p3, (222, bl(209, 20)), "25", 20, WH)
# bl(209, 20) = 209 + 18.2 = 227.2 → baseline≈227, bbox_top≈209, gap to labels ≈6pt

print("✓ P3 Fix B: Stat numbers '6' and '25' inserted centered in DB boxes")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6 (doc[5]) — Restore "Example Project Tracks & Applications" header
#
# global_sentence_case.py redact zone (36,65,360,82) cut through the right-
# column header. Chars "Exampl" (bbox_left < 362) were redacted; only the
# fragment "e Project Tracks & Applications" (bbox_left=362.6) survived.
#
# Fix:
#   1. Redact stray fragment rect (360,68,578,91)
#   2. Repaint nav/header background if needed (original was WH background —
#      redact white fill matches, no repaint required)
#   3. INSERT full header "Example Project Tracks & Applications" at x=313.5
#      using hebo, OR, sz=14 — matches original font/color audit
# ═══════════════════════════════════════════════════════════════════════════════
p6 = doc[5]

p6.add_redact_annot(fitz.Rect(360, 68, 578, 91))
p6.apply_redactions(images=0, graphics=0)

hebo(p6, (313.5, bl(69.8, 14)), "Example Project Tracks & Applications", 14, OR)
# bl(69.8, 14) = 69.8 + 12.74 = 82.54

print("✓ P6: Stray fragment removed; full 'Example Project Tracks & Applications' restored")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 15 (doc[14]) — Fix A: Paragraph bleed fix
#
# Current state:
#   Line 1: bbox=[36.0,193.9,330.3,205.5] — bleeds 17pt past right col boundary (x=313)
#   Line 2: ends with "supervised by employer staff." (correct, no additions)
#
# The original 2 lines must be cleared and rewrapped into 3 short lines that
# stay within the 277pt left column (x=36–313). Line 3 baseline = bl(220.9,8.5)
# = 228.6 → bbox_bottom ≈231 — redact zone extended to y=232 to fully clear
# the 3-line range and ensure no legacy text survives under line 3.
#
# Fix:
#   1. Redact full 3-line zone in left column (y=192–232)
#   2. Redact bleed overhang into right column (x=313–335, y=192–232)
#   3. Repaint LB over white fills that landed in the right column
#   4. Reinsert 3 constrained lines — all within x=36–313 left column
#      Line 1: "Your intern team will identify a real problem, research its"
#      Line 2: "causes, and design a technology-enabled solution, supervised"
#      Line 3: "by employer staff."
# ═══════════════════════════════════════════════════════════════════════════════
p15 = doc[14]

# Redact full 3-line zone (y=192–232 covers all 3 new baselines + descenders)
p15.add_redact_annot(fitz.Rect(36,  192, 315, 232))   # left col, 3-line zone
p15.add_redact_annot(fitz.Rect(315, 192, 335, 232))   # bleed overhang into right col
p15.apply_redactions(images=0, graphics=0)

# Restore LB background in right column over white redaction fills
paint(p15, (312.8, 192, 576, 232), LB)

# Reinsert 3-line paragraph — all constrained to left column (x=36, width≤277pt)
helv(p15, (36, bl(193.9, 8.5)), "Your intern team will identify a real problem, research its", 8.5, DK)
helv(p15, (36, bl(207.4, 8.5)), "causes, and design a technology-enabled solution, supervised", 8.5, DK)
helv(p15, (36, bl(220.9, 8.5)), "by employer staff.",                                          8.5, DK)

print("✓ P15 Fix A: Paragraph bleed fixed; 3 lines reinserted within left column")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 15 (doc[14]) — Fix B: Research Lead row text missing
#
# The LB background rect at y=184.5–218.2 exists (confirmed via get_drawings),
# but no text was ever inserted for the Research Lead row.
#
# Table column geometry (from Project Manager / Process Analyst rows):
#   Role column:           x=319.5  (left-aligned within right col)
#   Responsibilities col:  x=393.9  (second column start)
#   Full row width:        x=313.5–576
#
# Row 2 LB: y=184.5–218.2, center_y=201.35
# Baseline: bl(189.6, 8.5) = 189.6 + 7.735 = 197.3
#   — matches Project Manager row spacing (baseline sits ~12pt from row top)
#
# Fix:
#   1. Redact full text area of row (x=313.5–576, y=184.5–218.2), graphics=0
#      so the underlying LB vector rect is preserved in the content stream
#   2. Repaint LB over the white fill that apply_redactions appends —
#      exact same LB=(0.969,0.973,0.980) constant used by Solution Designer
#      row (row 4) ensuring pixel-perfect match with adjacent alternating rows
#   3. INSERT role (hebo DK) and responsibilities (helv DK) at that baseline
# ═══════════════════════════════════════════════════════════════════════════════

# Step 1: Targeted redact — text-only, vector LB rect survives in stream
p15.add_redact_annot(fitz.Rect(313.5, 184.5, 576, 218.2))
p15.apply_redactions(images=0, graphics=0)

# Step 2: Repaint LB over white fill — full row width, exact row bounds
paint(p15, (313.5, 184.5, 576, 218.2), LB)

# Step 3: Insert role and responsibilities
hebo(p15, (319.5, bl(189.6, 8.5)), "Research Lead",                                   8.5, DK)
helv(p15, (393.9, bl(189.6, 8.5)), "Conducts interviews/surveys; documents findings", 8.5, DK)
# bl(189.6, 8.5) = 197.3

print("✓ P15 Fix B: Research Lead row redacted, LB repainted, text inserted (y=184.5–218.2)")


# ═══════════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════════
doc.save(TMP, garbage=4, deflate=True)
doc.close()
os.replace(TMP, SRC)
print(f"\n✅  Saved → {SRC}")
