"""
Phase 3 visual style fixes for Scenario D — page 16:
  1. Replace ✓ bullets with ✅ (Type3 font F100, glyph 0x0e)
  2. Replace ★ with ⚡ in Scope Note (Type3 font F28, glyph 0xdd)
  3. KLO section: plain text → yellow pill tags
  4. Clean up stray overflow fragments in right column
"""
import fitz, os

SRC = "revised_outputs/TechInternship_revised.pdf"
TMP = SRC + ".tmp"
AU  = '/Library/Fonts/Arial Unicode.ttf'

DB  = (0.03920, 0.14510, 0.25100)
OR  = (0.91000, 0.29410, 0.00000)
YL  = (1.00000, 0.90200, 0.00000)
WH  = (1.00000, 1.00000, 1.00000)
DK  = (26/255,  26/255,  26/255)

doc = fitz.open(SRC)
p16 = doc[15]

# ── helpers ───────────────────────────────────────────────────────────────────
def helv(pg, xy, txt, sz=8.5, clr=None):
    pg.insert_text(xy, txt, fontname='helv', fontsize=sz, color=clr or DK)

def hebo(pg, xy, txt, sz=8.5, clr=None):
    pg.insert_text(xy, txt, fontname='hebo', fontsize=sz, color=clr or DK)

def au(pg, xy, txt, sz=8.5, clr=None):
    pg.insert_text(xy, txt, fontname='arialuni', fontfile=AU, fontsize=sz, color=clr or DK)

def paint_white(pg, rect):
    shape = pg.new_shape()
    shape.draw_rect(fitz.Rect(*rect))
    shape.finish(fill=WH, color=None)
    shape.commit()

def inject_glyph(doc, page, x, y, font_name, font_size, glyph_byte):
    """Append a raw Type3 glyph command to the last content stream."""
    pdf_y = page.rect.height - y          # PyMuPDF y → PDF y (bottom-left origin)
    glyph_hex = format(glyph_byte, '02x')
    snippet = (
        f"\nq BT /{font_name} {font_size:.2f} Tf "
        f"1 0 0 1 {x:.3f} {pdf_y:.3f} Tm "
        f"<{glyph_hex}> Tj ET Q\n"
    ).encode('latin-1')

    xrefs = page.get_contents()
    if not xrefs:
        raise RuntimeError("Page has no content streams")
    last_xref = xrefs[-1]
    old_stream = doc.xref_stream(last_xref)
    doc.update_stream(last_xref, old_stream + snippet)

p16_xref = p16.xref

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Clean up KLO plain text + stray overflow fragments (right column)
# Covers y=463–605, x=311–576 (below KLO header, above Program Contacts)
# ═══════════════════════════════════════════════════════════════════════════════
paint_white(p16, (311.0, 463.0, 576.0, 605.0))
print("✓ KLO area painted white")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3 — Draw KLO yellow pill tags (mirrors page 14 Scenario C style)
# Pill: height=15pt, x-start=311.2, text-x-offset=6pt, text-y-offset=9pt
# Row spacing: 18.8pt; inter-pill gap: 5pt
# ═══════════════════════════════════════════════════════════════════════════════
KLO_ROWS = [
    ['PROBLEM SOLVING',        'USER RESEARCH'],
    ['PROCESS ANALYSIS',       'CRITICAL THINKING'],
    ['COMMUNICATION',          'DESIGN THINKING'],
    ['WORKPLACE COLLABORATION'],
]
PILL_H  = 15.0
PAD_X   = 6.0
TEXT_DY = 9.0
PILL_GAP   = 5.0
ROW_STEP   = 18.8
PILL_X0    = 311.2
PILL_MAX_X = 576.0

y_pill_top = 467.2   # matches page 14 pill-top reference

for row in KLO_ROWS:
    x_left = PILL_X0
    for label in row:
        tw = fitz.get_text_length(label, fontname='hebo', fontsize=7.0)
        pill_w = tw + 2 * PAD_X
        x_right = x_left + pill_w
        # clamp to right margin (shouldn't happen with these labels)
        if x_right > PILL_MAX_X:
            x_right = PILL_MAX_X
        # draw pill background
        shape = p16.new_shape()
        shape.draw_rect(fitz.Rect(x_left, y_pill_top, x_right, y_pill_top + PILL_H))
        shape.finish(fill=YL, color=None)
        shape.commit()
        # draw label
        hebo(p16, (x_left + PAD_X, y_pill_top + TEXT_DY), label, sz=7.0, clr=DB)
        x_left = x_right + PILL_GAP
    y_pill_top += ROW_STEP

print(f"✓ KLO pills drawn (final y_top = {y_pill_top:.1f})")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4 — Replace ✓ (arialuni) with ✅ (F100 glyph 0x0e) in deliverables
# Six bullet positions: y = 476.2, 505.5, 534.8, 564.1, 593.4, 622.7  x = 49.5
# ═══════════════════════════════════════════════════════════════════════════════
CHECK_YS = [476.2, 505.5, 534.8, 564.1, 593.4, 622.7]

# Redact the plain ✓ glyphs
for y in CHECK_YS:
    p16.add_redact_annot(fitz.Rect(44.0, y - 10.5, 59.5, y + 3.0), fill=None)
p16.apply_redactions(images=0, graphics=0, text=0)

# Inject ✅ via content stream
for y in CHECK_YS:
    inject_glyph(doc, p16, 49.5, y, 'F100', 9.0, 0x0e)

print("✓ Deliverable checkmarks replaced with ✅")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5 — Replace ★ with ⚡ in Scope Note box + update text
# Box: DB fill Rect(37.875, 645.75, 299.25, 706.5), YL accent Rect(36,645.75,39.75,706.5)
# Current text at y=663.75 (★ x=51.8), y=675.75, y=687.75
# New text: ⚡ Prototype Scope Note: Interns are not expected
#           to build a working app or deploy a live system.
#           A researched concept or prototype is sufficient.
# ═══════════════════════════════════════════════════════════════════════════════
# Redact existing scope note text (inside box, excluding yellow accent strip)
p16.add_redact_annot(fitz.Rect(40.0, 646.0, 299.25, 706.5), fill=None)
p16.apply_redactions(images=0, graphics=0, text=0)

# Inject ⚡ (F28 glyph 0xdd = 221)
inject_glyph(doc, p16, 51.8, 663.75, 'F28', 8.5, 0xdd)

# Re-insert scope note text
# Line 1: bold header on same line as ⚡
hebo(p16, (62.2, 663.75), ' Prototype Scope Note:', sz=8.5, clr=YL)
# Calculate where body text starts on line 1
header_w = fitz.get_text_length(' Prototype Scope Note:', fontname='hebo', fontsize=8.5)
body_x = 62.2 + header_w
body_line1 = ' Interns are not expected'
body_line1_w = fitz.get_text_length(body_line1, fontname='helv', fontsize=8.5)

if body_x + body_line1_w <= 299.0:
    helv(p16, (body_x,  663.75), body_line1,                                     sz=8.5, clr=WH)
    helv(p16, (51.8,    675.75), 'to build a working app or deploy a live system.', sz=8.5, clr=WH)
    helv(p16, (51.8,    687.75), 'A researched concept or prototype is sufficient.',sz=8.5, clr=WH)
else:
    # Header alone on line 1, body wraps from line 2
    helv(p16, (51.8,    675.75), 'Interns are not expected to build a working app or', sz=8.5, clr=WH)
    helv(p16, (51.8,    687.75), 'deploy a live system. A researched concept or prototype is sufficient.',
         sz=8.5, clr=WH)

print("✓ Scope note updated with ⚡")

print(f"\nScope note line-1 header width: {header_w:.1f}pt  "
      f"body_x={body_x:.1f}  body_line1 width={body_line1_w:.1f}  "
      f"total={body_x+body_line1_w:.1f} (limit 299)")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 6 — Add F100/F28 to page 16 resources LAST (after all apply_redactions)
# Must be after apply_redactions so it isn't rebuilt/stripped.
# Save with garbage=2 (removes orphaned xrefs but preserves explicit inline dicts)
# ═══════════════════════════════════════════════════════════════════════════════
doc.xref_set_key(
    p16_xref, "Resources",
    "<</Font<</arialuni 2122 0 R/hebo 2120 0 R/helv 2121 0 R"
    "/F100 86 0 R/F28 26 0 R>>>>"
)
print("✓ F100 and F28 added to page 16 resources")

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE  (garbage=2 — removes orphaned objects but preserves explicit dicts)
# ═══════════════════════════════════════════════════════════════════════════════
doc.save(TMP, garbage=2, deflate=True)
doc.close()
os.replace(TMP, SRC)
print("\nDone — page 16 Phase 3 style applied.")
