"""
Part 2 — Global Program Contacts update (pages 14 and 16):
  REMOVE: Urban Assembly (UA) and The Knowledge House (TKH)
  KEEP:   DYCD Program Coordinator | DYCD Main Office
"""
import fitz, os

SRC = "revised_outputs/TechInternship_revised.pdf"
TMP = SRC + ".tmp"
AU  = '/Library/Fonts/Arial Unicode.ttf'

DB  = (0.03920, 0.14510, 0.25100)
WH  = (1.00000, 1.00000, 1.00000)
DK  = (26/255,  26/255,  26/255)

doc = fitz.open(SRC)

def hebo(pg, xy, txt, sz=8.5, clr=None):
    pg.insert_text(xy, txt, fontname='hebo', fontsize=sz, color=clr or DK)

def au_txt(pg, xy, txt, sz=8.5, clr=None):
    pg.insert_text(xy, txt, fontname='arialuni', fontfile=AU, fontsize=sz, color=clr or DK)

def paint_rect(pg, rect, fill):
    shape = pg.new_shape()
    shape.draw_rect(fitz.Rect(*rect))
    shape.finish(fill=fill, color=None)
    shape.commit()

def update_contacts_box(page, pg_num,
                        box_rect,           # existing dark-blue box rect
                        coord_ref,          # (x_left, y_header) reference
                        y_coordinator,      # y of "DYCD Program Coordinator" line
                        y_ua,               # y of UA line  (to remove)
                        y_tkh,              # y of TKH line (to remove)
                        y_main_old,         # y of DYCD Main Office (old position)
                        line_spacing=13.5): # line spacing in box
    """
    Remove UA and TKH lines, move DYCD Main Office up to where UA was,
    then shrink the box by painting white over the vacated bottom space.
    """
    x_left = coord_ref[0]
    box_x0, box_y0, box_x1, box_y1 = box_rect

    # ── Redact UA, TKH, and old DYCD Main Office lines ─────────────────────
    for y_line in (y_ua, y_tkh, y_main_old):
        page.add_redact_annot(
            fitz.Rect(box_x0, y_line - 9.5, box_x1, y_line + 3.5), fill=None)
    page.apply_redactions(images=0, graphics=0, text=0)

    # ── Reinsert DYCD Main Office at position where UA was ──────────────────
    y_main_new = y_ua   # move DYCD Main Office up to UA's old y
    label = "DYCD Main Office"
    hebo(page, (x_left, y_main_new), label, sz=8.0, clr=WH)
    label_w = fitz.get_text_length(label, fontname='hebo', fontsize=8.0)
    au_txt(page, (x_left + label_w, y_main_new), " \u2014 dycd.nyc.gov", sz=8.0, clr=WH)

    # ── Shrink box visually: paint white below new last line ─────────────────
    # New box bottom = y_main_new + enough margin below text
    new_box_bot = y_main_new + line_spacing + 1.5
    # Paint over extra dark-blue space at the bottom of the old box
    if new_box_bot < box_y1:
        paint_rect(page, (box_x0, new_box_bot, box_x1 + 1, box_y1 + 1), WH)

    print(f"  Page {pg_num}: DYCD Main Office moved to y={y_main_new:.1f}  "
          f"box now y={box_y0:.1f}–{new_box_bot:.1f}")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 14
# Box: Rect(311.2, 603.8, 576.0, 702.8)
# Header (📞): y=619.5, x=321.8
# Intro:       y=637.5, x=321.8
# Coordinator: y=651.0, x=321.8   ← KEEP
# UA:          y=664.5, x=321.8   ← REMOVE
# TKH:         y=678.0, x=321.8   ← REMOVE
# DYCD Main:   y=691.5, x=321.8   ← KEEP, move to y=664.5
# ═══════════════════════════════════════════════════════════════════════════════
p14 = doc[13]
update_contacts_box(
    page         = p14,
    pg_num       = 14,
    box_rect     = (311.2, 603.8, 576.0, 702.8),
    coord_ref    = (321.8, 619.5),
    y_coordinator= 651.0,
    y_ua         = 664.5,
    y_tkh        = 678.0,
    y_main_old   = 691.5,
    line_spacing = 13.5,
)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 16
# Box: Rect(312.8, 607.5, 576.0, 706.5)
# Header (☎): y=625.5, x=321.8
# Intro:       y=643.5, x=321.8
# Coordinator: y=657.0, x=321.8   ← KEEP
# UA:          y=670.5, x=321.8   ← REMOVE
# TKH:         y=684.0, x=321.8   ← REMOVE
# DYCD Main:   y=697.5, x=321.8   ← KEEP, move to y=670.5
# ═══════════════════════════════════════════════════════════════════════════════
p16 = doc[15]
update_contacts_box(
    page         = p16,
    pg_num       = 16,
    box_rect     = (312.8, 607.5, 576.0, 706.5),
    coord_ref    = (321.8, 625.5),
    y_coordinator= 657.0,
    y_ua         = 670.5,
    y_tkh        = 684.0,
    y_main_old   = 697.5,
    line_spacing = 13.5,
)

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE — add F100/F28 back to page 16 resources (apply_redactions may clear them)
# ═══════════════════════════════════════════════════════════════════════════════
p16_xref = p16.xref
doc.xref_set_key(
    p16_xref, "Resources",
    "<</Font<</arialuni 2122 0 R/hebo 2120 0 R/helv 2121 0 R"
    "/F100 86 0 R/F28 26 0 R>>>>"
)

doc.save(TMP, garbage=2, deflate=True)
doc.close()
os.replace(TMP, SRC)
print("\nDone — contacts updated on pages 14 and 16.")
