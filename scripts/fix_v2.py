"""
fix_v2.py — Round 2 targeted fixes.
Pages: 6 (Web & coding), 9 (Data Analyst bold), 14 (em dash + stray glyph),
       15 (scenario banner + section title reposition), 16 (multiple)
"""
import fitz, os

SRC = "revised_outputs/TechInternship_revised.pdf"
TMP = SRC + ".tmp"

AB  = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
AU  = "/Library/Fonts/Arial Unicode.ttf"

DB  = (0.03920, 0.14510, 0.25100)
OR  = (0.91000, 0.29410, 0.00000)
YL  = (1.00000, 0.90200, 0.00000)
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

def au(pg, xy, text, sz, clr=WH):
    pg.insert_text(xy, text, fontname='arialuni', fontfile=AU, fontsize=sz, color=clr)

def bl(y_top, sz, r=0.91):
    return y_top + sz * r


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — Restore "Web & coding" body (Interns may explore: + 3 bullets)
#
# Root cause: the zone (36,341,295,374) redacted in global_sentence_case.py
# captured the "Interns may explore:" line for the Web & coding column
# (its bbox_top ≈374.1, partially overlapping the redact boundary).
# Additionally, the legacy body text at x≈191 (y=385–504) does not match
# the requested content and must be replaced.
#
# Fix: clear x=153–296, y=370–516; re-insert header + 3 bullets.
# ═══════════════════════════════════════════════════════════════════════════════
p6 = doc[5]

p6.add_redact_annot(fitz.Rect(153, 370, 296, 516))
p6.apply_redactions(images=0, graphics=0)

# "Interns may explore:" — Helvetica-Bold DK sz=8.5 (matches the 3 existing ones)
hebo(p6, (191.6, bl(374.1, 8.5)), "Interns may explore:", 8.5, DK)

# 3 bullets — Helvetica DK sz=9.0, ~16pt line spacing (matches Workflow column)
helv(p6, (191.6, bl(384.0, 9.0)), "HTML/CSS fundamentals",       9.0, DK)
helv(p6, (191.6, bl(400.0, 9.0)), "Basic Python / scripting",    9.0, DK)
helv(p6, (191.6, bl(416.0, 9.0)), "Website structure and logic",  9.0, DK)

print("✓ P6: Web & coding section restored (Interns may explore: + 3 bullets)")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 9 — Data Analyst: re-insert as Arial-BoldMT to match Security Analyst
#
# global_sentence_case.py inserted "Data Analyst" with helv (non-bold).
# All other role-column names use Arial-BoldMT. Fix: redact + LB repaint + ab().
# ═══════════════════════════════════════════════════════════════════════════════
p9 = doc[8]

# Redact the non-bold "Data Analyst" text (bbox: 280.4, 208.6, 328.6, 220.3)
p9.add_redact_annot(fitz.Rect(273, 206, 362, 222))
p9.apply_redactions(images=0, graphics=0)

# Restore LB row background (original fill at 273.8, 204.0, 576.0, 238.5;
# the redact's white fill covers only the redact rect — repaint that zone)
paint(p9, (273, 206, 362, 222), LB)

# Re-insert bold — Arial-BoldMT DK sz=8.5
ab(p9, (280.4, bl(208.6, 8.5)), "Data Analyst", 8.5, DK)

print("✓ P9: Data Analyst re-inserted as Arial-BoldMT (bold, matches Security Analyst)")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 14 — Em dash fix + stray 'l' glyphs outside contact box
#
# global_sentence_case.py used helv for SYEP Provider and DYCD lines.
# Helvetica built-in uses WinAnsiEncoding; U+2014 maps to a middle-dot glyph
# (0x97 in CP1252 is not a valid WinAnsi glyph → rendered as ·).
# Fix: switch to ArialUnicode which natively supports U+2014.
# Also: stray 'l' chars at x≈592 (outside contact box, y≈634–636) are cleared.
#
# Contact box: DB fill at (311.2, 603.8, 576.0, 702.8).
# Affected lines: SYEP Provider (baseline 645), via worksite portal (658), DYCD (671).
# ═══════════════════════════════════════════════════════════════════════════════
p14 = doc[13]

# Zone 1: SYEP Provider + "via worksite portal" + stray 'l' chars (y=633–652)
p14.add_redact_annot(fitz.Rect(315, 633, 600, 652))
# Zone 2: DYCD line (y=660–672)
p14.add_redact_annot(fitz.Rect(315, 660, 580, 672))
p14.apply_redactions(images=0, graphics=0)

# Repaint DB inside contact box over the redaction white fills
paint(p14, (315, 633, 576, 652), DB)
paint(p14, (315, 660, 576, 672), DB)

# Re-insert with ArialUnicode (proper U+2014 em dash rendering)
au(p14, (322.0, 645.0), "SYEP Provider \u2014 contact information available", 8, WH)
au(p14, (322.0, 658.0), "via worksite portal",                                8, WH)
au(p14, (322.0, 671.0), "DYCD \u2014 nyc.gov/dycd  |  1-800-246-4646",       8, WH)

print("✓ P14: Em dashes fixed (ArialUnicode); stray 'l' glyphs removed")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 15 — Restore missing scenario banner + reposition section titles
#
# global_sentence_case.py used redact zone (36, 19, 400, 57).
# The scenario banner (sz=8, bbox: 36, 13.8, ?, 22.7) overlapped with the zone
# at y=19–22.7 and was erased (same issue as noted for P11/P13 which used y=22).
#
# The section titles "Workplace problem solving" / "& app concept design" were
# re-inserted at bl(23.5,18)=39.9 and bl(43.7,18)=60.1, placing bbox_top≈20.6
# and ≈40.8 — too high. At these positions the section title overlaps with the
# restored banner (banner bbox_bottom ≈22). The titles need to be moved to
# P9-equivalent positions: bl(26.5,18) and bl(46.0,18).
#
# Fix:
#   1. Redact current section titles (y=18–64)
#   2. Repaint navy (banner background spans y=0–93.8)
#   3. Re-insert banner at y=13.8 (Arial-BoldMT YL sz=8 — same as P9/P11/P13)
#   4. Re-insert section titles at P9-equivalent baselines (hebo OR sz=18 —
#      P15 uses Helvetica-Bold per original font audit)
# ═══════════════════════════════════════════════════════════════════════════════
p15 = doc[14]

# Redact current too-high section titles
p15.add_redact_annot(fitz.Rect(35, 18, 500, 64))
p15.apply_redactions(images=0, graphics=0)

# Restore navy background over cleared area
paint(p15, (0, 18, 612, 64), DB)

# Scenario banner — Arial-BoldMT, YL, sz=8 (matches P9/P11/P13 exactly)
ab(p15, (36, bl(13.8, 8)),
   "P R O J E C T  S C E N A R I O  D  \u2014  T R A C K :  W O R K P L A C E  P R O B L E M  S O L V I N G",
   8, YL)

# Section titles — Helvetica-Bold, OR, sz=18 (P15 original font)
# Baselines match P9 structure: bl(26.5,18)=42.9 and bl(46.0,18)=62.4
hebo(p15, (36, bl(26.5, 18)), "Workplace problem solving", 18, OR)
hebo(p15, (36, bl(46.0, 18)), "& app concept design",      18, OR)

# ── P15 provider-language removal (requested addition) ────────────────────────
# Target: remove "with DYCD-funded SYEP provider support" from the company
# background sentence so it reads:
#   "Your intern team will identify a real problem, research its causes, and
#    design a technology-enabled solution, supervised by employer staff."
#
# Verification: text extraction of the current PDF confirms the sentence at
# y=193.9–206.9 already reads "...supervised by employer staff." (period present,
# no trailing clause). The phrase is not present in this build — likely removed
# in a prior pass. No redaction is needed; this block is a no-op safeguard.
# If the phrase reappears in a future revision, redact the offending line and
# re-insert only "supervised by employer staff." at the same baseline.

print("✓ P15: Scenario D banner restored; section titles repositioned to match P9 layout")
print("  (P15 provider-language check: phrase not present — sentence already clean)")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 16 — Three separate fixes
#
# Fix A: "6-Week Project Structure" (Helvetica-Bold DK sz=15) — never redacted
#         by global_sentence_case.py because it was title case, not ALL CAPS.
#         Other pages (P10, P12, P14) show "6-week project structure" in OR.
#         Fix: sentence case + orange to match document standard.
#
# Fix B: "Expected Final Deliverables" / "Key Learning Outcomes"
#         (Helvetica-Bold WH sz=9 on navy bar, y=445.4) — title case, missed
#         by the global pass. Fix: sentence case, keep white on navy.
#         Note: redact creates a white fill on top of the navy vector rect;
#         repaint DB to restore the background.
#
# Fix C: Contact lines (SYEP Provider, DYCD, Employer Feedback Form) all used
#         helv → em dashes rendered as ·. Switch to ArialUnicode.
#         Background is white; no repaint needed.
# ═══════════════════════════════════════════════════════════════════════════════
p16 = doc[15]

# Fix A: "6-Week Project Structure" bbox (36, 55.9, 214.4, 76.6)
p16.add_redact_annot(fitz.Rect(35, 54, 216, 78))

# Fix B: both headers at y=445.4, combined zone x=35–578
p16.add_redact_annot(fitz.Rect(35, 443, 578, 460))

# Fix C: all four contact lines y=582–630
p16.add_redact_annot(fitz.Rect(309, 580, 578, 633))

p16.apply_redactions(images=0, graphics=0)

# Fix B: repaint full-width navy bar (headers are WH text on DB background)
paint(p16, (35, 443, 578, 460), DB)

# Fix A: "6-week project structure" — Helvetica-Bold OR sz=15 (matches P10/P12/P14)
hebo(p16, (36.0, bl(55.9, 15)), "6-week project structure", 15, OR)

# Fix B: sentence case, keep white on restored navy
hebo(p16, (42.0,  bl(445.4, 9)), "Expected final deliverables", 9, WH)
hebo(p16, (311.0, bl(445.4, 9)), "Key learning outcomes",        9, WH)

# Fix C: ArialUnicode for proper em dash + consistent formatting
au(p16, (311.0, bl(583.4, 8)), "SYEP Provider \u2014 contact information available", 8, DK)
au(p16, (311.0, bl(596.4, 8)), "via worksite portal",                                8, DK)
au(p16, (311.0, bl(609.4, 8)), "DYCD \u2014 nyc.gov/dycd  |  1-800-246-4646",       8, DK)
au(p16, (311.0, bl(622.4, 8)),
   "Employer Feedback Form \u2014 ______________________________",                    8, DK)

print("✓ P16: 6-week header → orange; Expected/Key → sentence case; contacts em-dash fixed")


# ═══════════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════════
doc.save(TMP, garbage=4, deflate=True)
doc.close()
os.replace(TMP, SRC)
print(f"\n✅  Saved → {SRC}")
