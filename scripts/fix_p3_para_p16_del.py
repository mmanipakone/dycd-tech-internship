"""
Fix two issues from multi_page_updates.py:
  1. Page 3 paragraph — 5 correct lines with proper AU em-dash on line 2
  2. Page 16 deliverables — fix "Final Presentation" spacing + re-inject ✅ cleanly
"""
import fitz, os

SRC = "revised_outputs/TechInternship_revised.pdf"
TMP = SRC + ".tmp"
AU  = '/Library/Fonts/Arial Unicode.ttf'

WH = (1.0, 1.0, 1.0)
DK = (26/255, 26/255, 26/255)

doc = fitz.open(SRC)

def paint(pg, rect, fill):
    s = pg.new_shape()
    s.draw_rect(fitz.Rect(*rect))
    s.finish(fill=fill, color=None)
    s.commit()

def inject_glyph(doc, page, x, y, font_name, font_size, glyph_byte):
    pdf_y = page.rect.height - y
    snippet = (
        f"\nq BT /{font_name} {font_size:.2f} Tf "
        f"1 0 0 1 {x:.3f} {pdf_y:.3f} Tm "
        f"<{format(glyph_byte,'02x')}> Tj ET Q\n"
    ).encode('latin-1')
    xrefs = page.get_contents()
    last  = xrefs[-1]
    doc.update_stream(last, doc.xref_stream(last) + snippet)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 3 — 5-line paragraph with proper AU em-dash on line 2
# White paint covers y=123–205, x=35–310 (all 5 lines + padding)
# Line 2: "experience " (helv) + "—" (arialuni) + rest (helv) — all within 263pt
# ═══════════════════════════════════════════════════════════════════════════
p3 = doc[2]

paint(p3, (35.0, 123.0, 310.0, 205.0), WH)

SZ = 9.5
X  = 36.0

# Line 1 — plain helv
p3.insert_text((X, 131.2),
    "Hosting a SYEP tech intern creates a mutually beneficial",
    fontname='helv', fontsize=SZ, color=DK)

# Line 2 — three segments: helv + AU em-dash + helv
pre_text  = "experience "
post_text = " interns gain real-world skills aligned to the"
w_pre  = fitz.get_text_length(pre_text, fontname='helv', fontsize=SZ)
# AU em-dash width estimated at 6.5pt; we chain x positions to avoid gap/overlap
p3.insert_text((X, 146.2), pre_text,
               fontname='helv', fontsize=SZ, color=DK)
x_dash = X + w_pre
p3.insert_text((x_dash, 146.2), "\u2014",
               fontname='arialuni', fontfile=AU, fontsize=SZ, color=DK)
# We don't know exact AU em-dash advance, so use helv proxy width + 3.86pt correction
w_dash_helv = fitz.get_text_length("\u2014", fontname='helv', fontsize=SZ)  # 2.64pt
x_post = x_dash + w_dash_helv + 3.86   # approximate AU em-dash advance
p3.insert_text((x_post, 146.2), post_text,
               fontname='helv', fontsize=SZ, color=DK)

# Lines 3–5 — plain helv
for y, text in [
    (161.2, "Portrait of a Graduate, while employers gain fresh"),
    (176.2, "perspectives, expanded capacity, and a pipeline of diverse"),
    (191.2, "future talent."),
]:
    p3.insert_text((X, y), text, fontname='helv', fontsize=SZ, color=DK)

# Verify widths
print("Page 3 paragraph line widths:")
checks = [
    "Hosting a SYEP tech intern creates a mutually beneficial",
    "experience  \u2014 interns gain real-world skills aligned to the",  # approx
    "Portrait of a Graduate, while employers gain fresh",
    "perspectives, expanded capacity, and a pipeline of diverse",
    "future talent.",
]
for c in checks:
    w = fitz.get_text_length(c.replace('\u2014',''), fontname='helv', fontsize=SZ)
    print(f"  {w:.1f}pt  {repr(c[:60])}")
print()

# ═══════════════════════════════════════════════════════════════════════════
# PAGE 16 — fix deliverables: redo all 6 with correct spacing and text
# Paint white over the area (covers all previous injections/text)
# Then re-inject ✅ and text cleanly
# ═══════════════════════════════════════════════════════════════════════════
p16      = doc[15]
p16_xref = p16.xref

paint(p16, (36.0, 468.0, 300.0, 570.0), WH)

DELIVS = [
    ("Problem Statement",       " \u2014 clearly defined challenge"),
    ("Research Summary",        " \u2014 interviews, observations, insights"),
    ("Workflow Map",            " \u2014 current process visualization"),
    ("Solution Concept",        " \u2014 app/tool/system design"),
    ("Before/After Comparison", " \u2014 time saved or impact"),
    ("Final Presentation",      " \u2014 10\u201315 slides"),   # note: space after em-dash
]

Y_START = 476.2
Y_STEP  = 16.0

for i, (label, body) in enumerate(DELIVS):
    y = Y_START + i * Y_STEP
    inject_glyph(doc, p16, 49.5, y, 'F100', 9.0, 0x0e)   # ✅
    p16.insert_text((63.3, y), label,
                    fontname='hebo', fontsize=9.0, color=DK)
    lw = fitz.get_text_length(label, fontname='hebo', fontsize=9.0)
    p16.insert_text((63.3 + lw, y), body,
                    fontname='arialuni', fontfile=AU, fontsize=9.0, color=DK)

# Preserve F100/F28 resources
doc.xref_set_key(
    p16_xref, "Resources",
    "<</Font<</arialuni 2122 0 R/hebo 2120 0 R/helv 2121 0 R"
    "/F100 86 0 R/F28 26 0 R>>>>"
)
print(f"Page 16 deliverables: {len(DELIVS)} items at y={Y_START:.1f}–{Y_START+(len(DELIVS)-1)*Y_STEP:.1f}")

doc.save(TMP, garbage=2, deflate=True)
doc.close()
os.replace(TMP, SRC)
print("Done.")
