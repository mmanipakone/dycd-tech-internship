"""
Fix Pages 15 & 16 — Scenario D: text density, overflow, and formatting improvements.
Matches Scenario C layout conventions.
"""
import fitz
import os

SRC = "revised_outputs/TechInternship_revised.pdf"
TMP = SRC + ".tmp"
AU  = '/Library/Fonts/Arial Unicode.ttf'

DB  = (0.03920, 0.14510, 0.25100)
OR  = (0.91000, 0.29410, 0.00000)
YL  = (1.00000, 0.90200, 0.00000)
WH  = (1.00000, 1.00000, 1.00000)
DK  = (26/255,  26/255,  26/255 )

doc = fitz.open(SRC)
p15 = doc[14]
p16 = doc[15]

# ── helpers ──────────────────────────────────────────────────────────────────
def helv(pg, xy, txt, sz=8.5, clr=None):
    pg.insert_text(xy, txt, fontname='helv', fontsize=sz, color=clr or DK)

def hebo(pg, xy, txt, sz=8.5, clr=None):
    pg.insert_text(xy, txt, fontname='hebo', fontsize=sz, color=clr or DK)

def au(pg, xy, txt, sz=8.5, clr=None):
    pg.insert_text(xy, txt, fontname='arialuni', fontfile=AU, fontsize=sz,
                   color=clr or DK)

def redact(pg, rect):
    pg.add_redact_annot(fitz.Rect(*rect), fill=None)

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  PAGE 15 — FIXES                                                         ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# ── 1. Company Background body (shorten ~20%) ────────────────────────────────
redact(p15, (36, 133, 299.25, 262))

# ── 2. THE CHALLENGE body (clean single-line bullets) ────────────────────────
redact(p15, (36, 281, 299.25, 375))

# ── 3. SOLUTION OUTPUT — header text (extend to include NO CODING REQUIRED) ─
redact(p15, (312.75, 334, 576, 352))

# ── 4. SOLUTION OUTPUT — body (restructure: items + tools section) ───────────
redact(p15, (312.75, 355, 576, 483))

# ── 5. SAMPLE OUTPUT — body (shorten to ~3 lines) ────────────────────────────
redact(p15, (312.75, 513, 576, 601))

p15.apply_redactions(images=0, graphics=0, text=0)

# ── 1. Company Background — reinsert ─────────────────────────────────────────
cb = [
    "Your organization operates in a fast-paced environment where",
    "staff face real challenges, from customer service issues to",
    "operational inefficiencies, that often go unaddressed.",
    "",   # paragraph break
    "Your intern team will identify a real problem, research its",
    "causes, and design a technology-enabled solution, supervised",
    "by employer staff with DYCD-funded SYEP provider support.",
]
y = 140.2
for line in cb:
    if line:
        helv(p15, (36.0, y), line)
    y += 13.5

# ── 2. THE CHALLENGE — reinsert (brief intro + 4 single-line bullets) ────────
tc = [
    "Every workplace has problems better systems could address.",
    "Your intern team will:",
    "- Identify a real workplace challenge",
    "- Conduct structured research",
    "- Design a solution (app/tool/system concept)",
    "- Present a clear proposal",
]
y = 288.0
for line in tc:
    helv(p15, (36.0, y), line)
    y += 13.5

# ── 3. SOLUTION OUTPUT — new header ──────────────────────────────────────────
hebo(p15, (312.75, 341.5), 'SOLUTION OUTPUT (NO CODING REQUIRED)', sz=11.0, clr=OR)

# ── 4. SOLUTION OUTPUT — restructured body ───────────────────────────────────
# Solution type items
so = [
    (374.0, "Mobile app concept"),
    (387.5, "Digital workflow or tracking tool"),
    (401.0, "Communication or scheduling system"),
    (414.5, "Operations dashboard"),
]
for y_, txt in so:
    helv(p15, (319.5, y_), txt)

# Tools sub-header (bold, with visual gap)
hebo(p15, (319.5, 431.5), 'Tools (no coding required):')

# Tool items — 11.5 pt spacing to fit before SAMPLE OUTPUT at y=490
tools = [
    (443.5, "Paper sketches"),
    (455.0, "Google Slides"),
    (466.5, "Canva"),
    (478.0, "Figma (optional)"),
]
for y_, txt in tools:
    helv(p15, (319.5, y_), txt)

# ── 5. SAMPLE OUTPUT — reinsert (3 lines max) ────────────────────────────────
hebo(p15, (319.5, 521.0), 'Example Outcome:')
au(p15,   (319.5, 534.5),
   'Retail store interns found employees spent 15\u201320 min/shift')
helv(p15, (319.5, 548.0),
   'tracking inventory manually. Their app concept cut this')
helv(p15, (319.5, 561.5),
   'to under 5 minutes, improving accuracy across teams.')


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  PAGE 16 — FIXES                                                         ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# ── 6. 6-week table — shorten Activities text ────────────────────────────────
# Redact all activity cells (ACTS col x=129–418.5, but stop before DEL col)
week_row_bounds = [
    (115.5, 168.5),   # W1
    (168.5, 221.5),   # W2
    (221.5, 274.5),   # W3
    (274.5, 327.5),   # W4
    (327.5, 380.5),   # W5
    (380.5, 433.5),   # W6
]
for y0, y1 in week_row_bounds:
    redact(p16, (129.0, y0, 418.0, y1))

# ── 7. Deliverables — redact all entries ─────────────────────────────────────
redact(p16, (36, 469, 299.25, 641))

p16.apply_redactions(images=0, graphics=0, text=0)

# ── 6. Activities — reinsert concise text ────────────────────────────────────
#  Row text baseline = row_top + 12.7; L2 = +11.3
weeks_acts = [
    # (row_top, phase_lines, act_lines)
    (115.5, ['Explore'],
     ['Observe company operations; identify potential challenges;',
      'assign team roles; set up project plan']),
    (168.5, ['Explore', '+', 'Build'],
     ['Interview staff; conduct surveys; analyze findings; draft',
      'problem statement; select focus area']),
    (221.5, ['Build'],
     ['Map current workflow; identify inefficiencies; brainstorm',
      'solution ideas; select concept with supervisor']),
    (274.5, ['Build +', 'Apply'],
     ['Design solution concept; define key features;',
      'gather staff feedback; mid-program check-in']),
    (327.5, ['Apply'],
     ['Refine solution; build before/after comparison;',
      'create presentation deck; practice with supervisor']),
    (380.5, ['Launch', '+', 'Reflect'],
     ['Present to employer (10\u201315 min); receive feedback;',
      'complete exit survey; team debrief; reflect on learning']),
]
for row_top, phase, acts in weeks_acts:
    y0 = row_top + 12.7
    for i, a in enumerate(acts):
        if '\u2013' in a:
            au(p16, (136.0, y0 + i*11.3), a, sz=8.0)
        else:
            helv(p16, (136.0, y0 + i*11.3), a, sz=8.0)

# ── 7. Deliverables — reinsert tight checkmark bullets ───────────────────────
deliverables = [
    ("Problem Statement",       " \u2014 clearly defined challenge"),
    ("Research Summary",        " \u2014 interviews, observations, insights"),
    ("Workflow Map",            " \u2014 current process visualization"),
    ("Solution Concept",        " \u2014 app/tool/system design"),
    ("Before/After Comparison", " \u2014 time saved or impact"),
    ("Final Presentation",      " \u2014 10\u201315 slides"),
]
y_del = 476.2
for label, body in deliverables:
    au(p16,   (49.5, y_del),  '\u2713', sz=9.0)
    helv(p16, (60.8, y_del),  ' ',      sz=9.0)
    hebo(p16, (63.3, y_del),  label,    sz=9.0)
    label_w = fitz.get_text_length(label, fontname='hebo', fontsize=9.0)
    au(p16,   (63.3 + label_w, y_del), body, sz=9.0)
    y_del += 29.3

# ── SAVE ─────────────────────────────────────────────────────────────────────
doc.save(TMP, garbage=4, deflate=True)
doc.close()
os.replace(TMP, SRC)
print("Done — pages 15 & 16 updated.")
