"""
Part 1 — Page 6: Add Track D (Workplace Problem Solving & App Concept Design)
- Keep Tracks A–C at current positions (spacing already tight at ~10pt)
- Insert Track D header bar + body after Track C
- Shift Project Selection box and image downward to make room
"""
import fitz, os

SRC = "revised_outputs/TechInternship_revised.pdf"
TMP = SRC + ".tmp"
AU  = '/Library/Fonts/Arial Unicode.ttf'

DB  = (0.03920, 0.14510, 0.25100)
OR  = (0.91000, 0.29410, 0.00000)
WH  = (1.00000, 1.00000, 1.00000)
DK  = (26/255,  26/255,  26/255)

doc = fitz.open(SRC)
p6  = doc[5]

# ── helpers ───────────────────────────────────────────────────────────────────
def helv(pg, xy, txt, sz=8.5, clr=None):
    pg.insert_text(xy, txt, fontname='helv', fontsize=sz, color=clr or DK)

def hebo(pg, xy, txt, sz=8.5, clr=None):
    pg.insert_text(xy, txt, fontname='hebo', fontsize=sz, color=clr or DK)

def paint_white(pg, rect):
    shape = pg.new_shape()
    shape.draw_rect(fitz.Rect(*rect))
    shape.finish(fill=WH, color=None)
    shape.commit()

def draw_rect_fill(pg, rect, fill):
    shape = pg.new_shape()
    shape.draw_rect(fitz.Rect(*rect))
    shape.finish(fill=fill, color=None)
    shape.commit()

def inject_glyph(doc, page, x, y, font_name, font_size, glyph_byte):
    """Inject a Type3 glyph into the page's last content stream.
    Works for both new pages (standard CTM) and original pages (CTM at identity
    after all q…Q pairs are matched)."""
    pdf_y = page.rect.height - y
    glyph_hex = format(glyph_byte, '02x')
    snippet = (
        f"\nq BT /{font_name} {font_size:.2f} Tf "
        f"1 0 0 1 {x:.3f} {pdf_y:.3f} Tm "
        f"<{glyph_hex}> Tj ET Q\n"
    ).encode('latin-1')
    xrefs = page.get_contents()
    last_xref = xrefs[-1]
    doc.update_stream(last_xref, doc.xref_stream(last_xref) + snippet)

# ── Known page-6 measurements ─────────────────────────────────────────────────
# Track C body last baseline:
TC_BODY_LAST_Y  = 311.2   # "accessible tools." at y=311.2
# Original PS box: Rect(314.6, 322.5, 576.0, 375.8)
PS_BOX_OLD_TOP  = 322.5
PS_BOX_OLD_BOT  = 375.8
PS_BOX_H        = PS_BOX_OLD_BOT - PS_BOX_OLD_TOP   # 53.3
# Original image bbox (type=1 block): [312.8, 330.0, 576.0, 527.2]
IMG_OLD_TOP     = 330.0
IMG_OLD_BOT     = 527.2
IMG_XREF        = 55      # from get_images()
# PS box text offsets from box_top:
PS_ICON_OFFSET  = PS_BOX_OLD_TOP - PS_BOX_OLD_TOP  # 0 → we'll use 17.3 measured below
# measured from get_text: ⚡ y=339.8, PS_BOX_OLD_TOP=322.5 → delta=17.3
PS_TEXT_DY1     = 339.8 - PS_BOX_OLD_TOP  # 17.3  (icon / header row)
PS_TEXT_DY2     = 351.8 - PS_BOX_OLD_TOP  # 29.3  (body line 1)
PS_TEXT_DY3     = 363.0 - PS_BOX_OLD_TOP  # 40.5  (body line 2)
COL_RIGHT       = 576.0
COL_LEFT        = 312.8
COL_W           = COL_RIGHT - COL_LEFT    # 263.2

INTER_TRACK_GAP = 10.6    # gap from Track C body to Track D bar (matches A→B gap)
BAR_H           = 21.0    # orange bar height (matches Tracks A–C)
BAR_TO_BODY_DY  = 13.4    # from bar top to header text baseline
BODY_SPACING    = 13.6    # line spacing in body text

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Determine Track D body text lines (3 vs 4, depending on width)
# ═══════════════════════════════════════════════════════════════════════════════
BODY_3 = [
    "Example project: Interns may identify a real workplace challenge, conduct",
    "research with staff or customers, and design a technology-enabled solution",
    "(app, tool, or system) to improve how work gets done.",
]
BODY_4 = [
    "Example project: Interns may identify a real workplace challenge,",
    "conduct research with staff or customers, and design a",
    "technology-enabled solution (app, tool, or system) to improve",
    "how work gets done.",
]

body_lines = BODY_3
for ln in BODY_3:
    if fitz.get_text_length(ln, fontname='helv', fontsize=8.5) > COL_W - 1:
        body_lines = BODY_4
        break

n_body = len(body_lines)
print(f"Track D body: {n_body} lines")
for ln in body_lines:
    w = fitz.get_text_length(ln, fontname='helv', fontsize=8.5)
    print(f"  {w:.1f}pt  '{ln[:70]}'")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Calculate new y positions
# ═══════════════════════════════════════════════════════════════════════════════
TD_BAR_Y0   = TC_BODY_LAST_Y + INTER_TRACK_GAP       # Track D bar top
TD_BAR_Y1   = TD_BAR_Y0 + BAR_H                      # Track D bar bottom
TD_HDR_Y    = TD_BAR_Y0 + BAR_TO_BODY_DY             # header text baseline
TD_BODY_Y0  = TD_BAR_Y1 + BAR_TO_BODY_DY             # first body line baseline
TD_BODY_YS  = [TD_BODY_Y0 + i * BODY_SPACING for i in range(n_body)]

# New Project Selection box — same gap below Track D body as between A→B
NEW_PS_TOP  = TD_BODY_YS[-1] + INTER_TRACK_GAP
NEW_PS_BOT  = NEW_PS_TOP + PS_BOX_H

# New image position — preserve same relative offset from PS box top
IMG_OFFSET  = IMG_OLD_TOP - PS_BOX_OLD_TOP   # originally 7.5pt
NEW_IMG_TOP = NEW_PS_TOP + IMG_OFFSET
NEW_IMG_BOT = NEW_IMG_TOP + (IMG_OLD_BOT - IMG_OLD_TOP)

SHIFT = NEW_PS_TOP - PS_BOX_OLD_TOP
print(f"\nShift: {SHIFT:.1f}pt")
print(f"Track D bar: y={TD_BAR_Y0:.1f}–{TD_BAR_Y1:.1f}")
print(f"Track D body: y={TD_BODY_YS[0]:.1f}–{TD_BODY_YS[-1]:.1f}")
print(f"New PS box: y={NEW_PS_TOP:.1f}–{NEW_PS_BOT:.1f}")
print(f"New image: y={NEW_IMG_TOP:.1f}–{NEW_IMG_BOT:.1f}")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3 — Paint white over old PS box and old image area
# ═══════════════════════════════════════════════════════════════════════════════
# Cover from Track C body bottom (slightly above PS box start) to image bottom
COVER_TOP = TC_BODY_LAST_Y + INTER_TRACK_GAP - 2  # just above old PS top
COVER_BOT = IMG_OLD_BOT + 2
paint_white(p6, (COL_LEFT - 1, COVER_TOP, COL_RIGHT + 1, COVER_BOT))
print(f"\n✓ White painted over y={COVER_TOP:.0f}–{COVER_BOT:.0f}")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4 — Draw Track D orange header bar + text
# ═══════════════════════════════════════════════════════════════════════════════
draw_rect_fill(p6, (312.7, TD_BAR_Y0, 576.0, TD_BAR_Y1), OR)

# Header text — split at em-dash because hebo lacks U+2014
td_pre   = 'Track D '
td_dash  = '\u2014'
td_post  = ' Workplace Problem Solving & App Concept Design'
w_pre    = fitz.get_text_length(td_pre,  fontname='hebo',     fontsize=8.5)
w_dash   = 6.5   # em-dash advance width in arialuni at 8.5pt (approx)
hebo(p6, (321.8,              TD_HDR_Y), td_pre,  sz=8.5, clr=WH)
p6.insert_text((321.8 + w_pre, TD_HDR_Y), td_dash,
               fontname='arialuni', fontfile=AU, fontsize=8.5, color=WH)
hebo(p6, (321.8 + w_pre + w_dash, TD_HDR_Y), td_post, sz=8.5, clr=WH)
print(f"✓ Track D bar drawn  y={TD_BAR_Y0:.1f}–{TD_BAR_Y1:.1f}")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5 — Insert Track D body text
# ═══════════════════════════════════════════════════════════════════════════════
for y, line in zip(TD_BODY_YS, body_lines):
    helv(p6, (COL_LEFT, y), line, sz=8.5)
print(f"✓ Track D body inserted ({n_body} lines)")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 6 — Draw new Project Selection box (dark blue)
# ═══════════════════════════════════════════════════════════════════════════════
draw_rect_fill(p6, (314.6, NEW_PS_TOP, 576.0, NEW_PS_BOT), DB)
print(f"✓ New PS box drawn  y={NEW_PS_TOP:.1f}–{NEW_PS_BOT:.1f}")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 7 — Reinsert Project Selection content
# F59 (xref=48) is already in page 6 resources; ⚡ = glyph 0xdd at sz=8.0
# ═══════════════════════════════════════════════════════════════════════════════
PS_Y1 = NEW_PS_TOP + PS_TEXT_DY1   # icon / header baseline
PS_Y2 = NEW_PS_TOP + PS_TEXT_DY2   # body line 1
PS_Y3 = NEW_PS_TOP + PS_TEXT_DY3   # body line 2

# ⚡ glyph
inject_glyph(doc, p6, 328.5, PS_Y1, 'F59', 8.0, 0xdd)

# Bold label " Project Selection"
PS_BOLD = " Project Selection"
hebo(p6, (338.2, PS_Y1), PS_BOLD, sz=8.0, clr=WH)

# Regular text on same line: " Employers are encouraged to design"
ps_bold_w = fitz.get_text_length(PS_BOLD, fontname='hebo', fontsize=8.0)
helv(p6, (338.2 + ps_bold_w, PS_Y1),
     " Employers are encouraged to design", sz=8.0, clr=WH)

# Body lines
helv(p6, (328.5, PS_Y2), "projects and tasks that align with their organization's work,",
     sz=8.0, clr=WH)
helv(p6, (328.5, PS_Y3), "using these examples as a starting point.",
     sz=8.0, clr=WH)

print(f"✓ PS content reinserted  y={PS_Y1:.1f}, {PS_Y2:.1f}, {PS_Y3:.1f}")

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 8 — Reinsert image at new position
# ═══════════════════════════════════════════════════════════════════════════════
new_img_rect = fitz.Rect(COL_LEFT, NEW_IMG_TOP, COL_RIGHT, NEW_IMG_BOT)
p6.insert_image(new_img_rect, xref=IMG_XREF)
print(f"✓ Image reinserted  y={NEW_IMG_TOP:.1f}–{NEW_IMG_BOT:.1f}")

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════════
doc.save(TMP, garbage=2, deflate=True)
doc.close()
os.replace(TMP, SRC)
print("\nDone — page 6 updated with Track D.")
