"""
Page 17 — How to Use AI to Customize Your Internship Scenario
Single-page PDF addition to the DYCD Tech Internship Playbook (Page 17)
Matches playbook design: navy/orange/white, Arial-equivalent fonts, clean hierarchy
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white

OUT = '/Users/manipakone/Documents/dycd-tech-internship/playbook/page17_ai_guide.pdf'

# ── Colors ────────────────────────────────────────────────────────────────────
NAVY   = HexColor('#0A2540')
ORANGE = HexColor('#E84B00')
YELLOW = HexColor('#FFE600')
DARK   = HexColor('#1A1A1A')
GRAY   = HexColor('#666666')
STRIPE = HexColor('#F2F5F9')
LNAVY  = HexColor('#143A63')

W, H = letter   # 612 × 792 points (8.5 × 11 in)
LM   = 36       # left margin
RM   = 36       # right margin
CW   = W-LM-RM  # 540pt content width

# Two-column widths
C1W  = 250
GAP  = 12
C2X  = LM + C1W + GAP   # 298
C2W  = W - C2X - RM     # 278

# ── Utility: word-wrap ────────────────────────────────────────────────────────
def wrap(cv, text, font, size, max_w):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if cv.stringWidth(test, font, size) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or ['']

# ── Section bar helpers ───────────────────────────────────────────────────────
def navy_bar(cv, x, y, w, text, h=18):
    """Navy bar with yellow text. Returns y below bar."""
    cv.setFillColor(NAVY)
    cv.rect(x, y-h, w, h, fill=1, stroke=0)
    cv.setFont('Helvetica-Bold', 9)
    cv.setFillColor(YELLOW)
    cv.drawString(x+6, y-h+6, text)
    return y-h

def orange_bar(cv, x, y, w, text, h=18):
    """Orange bar with white text. Returns y below bar."""
    cv.setFillColor(ORANGE)
    cv.rect(x, y-h, w, h, fill=1, stroke=0)
    cv.setFont('Helvetica-Bold', 9)
    cv.setFillColor(white)
    cv.drawString(x+6, y-h+6, text)
    return y-h

# ── Build page ────────────────────────────────────────────────────────────────
cv = canvas.Canvas(OUT, pagesize=letter)
cv.setTitle('How to Use AI to Customize Your Internship Scenario — Page 17')

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
HDR_H = 28
cv.setFillColor(NAVY)
cv.rect(0, H-HDR_H, W, HDR_H, fill=1, stroke=0)
cv.setFont('Helvetica-Bold', 9)
cv.setFillColor(YELLOW)
cv.drawString(LM, H-HDR_H+10, 'AI PROMPTING GUIDE')
cv.setFillColor(white)
cv.drawRightString(W-RM, H-HDR_H+10, '17')

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
FTR_H = 20
cv.setFillColor(NAVY)
cv.rect(0, 0, W, FTR_H, fill=1, stroke=0)
cv.setFont('Helvetica', 7)
cv.setFillColor(white)
cv.drawCentredString(W/2, 7, 'NYC DYCD \u2014 High School Tech Internship Framework \u00b7 17')

# ─────────────────────────────────────────────────────────────────────────────
# PAGE TITLE + SUBTITLE
# ─────────────────────────────────────────────────────────────────────────────
y = H - HDR_H - 14

cv.setFont('Helvetica-Bold', 14)
cv.setFillColor(ORANGE)
cv.drawString(LM, y, 'How to Use AI to Customize Your Internship Scenario')
y -= 16

cv.setFont('Helvetica', 9)
cv.setFillColor(GRAY)
cv.drawString(LM, y, 'Use AI as a tool to adapt existing scenarios to your organization\u2019s real work')
y -= 10

cv.setStrokeColor(ORANGE)
cv.setLineWidth(1)
cv.line(LM, y, W-RM, y)
y -= 14

# ─────────────────────────────────────────────────────────────────────────────
# TWO-COLUMN SECTION
# Left: Section 1 — Start with what already exists
# Right: Section 2 — Use AI as a work partner
# ─────────────────────────────────────────────────────────────────────────────
ly = y
ry = y

# ── LEFT: Section 1 ───────────────────────────────────────────────────────────
ly = navy_bar(cv, LM, ly, C1W, 'Start with what already exists')
ly -= 8

s1_items = [
    'Review the 4 project scenarios in this playbook',
    'Choose the scenario closest to your organization\u2019s work',
    'Identify where interns could contribute to real tasks',
    'Do NOT start from scratch \u2014 adapt what already works',
]
for item in s1_items:
    cv.setFont('Helvetica', 9)
    cv.setFillColor(DARK)
    lines = wrap(cv, item, 'Helvetica', 9, C1W - 20)
    cv.drawString(LM+5, ly, '\u2022')
    for i, line in enumerate(lines):
        cv.drawString(LM+16, ly - i*14, line)
    ly -= len(lines)*14 + 3

ly -= 7

# Tip note in shaded box
tip = ('The 4 scenarios on pages 9\u201316 are your starting points. '
       'Adapt them to fit your organization \u2014 don\u2019t rebuild from scratch.')
tip_lines = wrap(cv, tip, 'Helvetica-Oblique', 7.5, C1W - 14)
tip_h = len(tip_lines)*11 + 10
cv.setFillColor(STRIPE)
cv.rect(LM, ly-tip_h, C1W, tip_h, fill=1, stroke=0)
cv.setFont('Helvetica-Oblique', 7.5)
cv.setFillColor(GRAY)
ty = ly - 7
for line in tip_lines:
    cv.drawString(LM+6, ty, line)
    ty -= 11
ly -= tip_h

# ── RIGHT: Section 2 ──────────────────────────────────────────────────────────
ry = navy_bar(cv, C2X, ry, C2W, 'Use AI as a work partner, not a replacement')
ry -= 8

cv.setFont('Helvetica', 8.5)
cv.setFillColor(DARK)
cv.drawString(C2X, ry, 'Different tools are useful for different parts of the process:')
ry -= 15

tools = [
    ('NotebookLM',      'Reviewing documents, datasets, or internal materials'),
    ('ChatGPT',         'Brainstorming and refining ideas'),
    ('Claude',          'Generating structured outputs: project plans, deliverables'),
    ('Advanced tools',  'Prototyping or technical builds (e.g., coding assistants)'),
]

for name, desc in tools:
    cv.setFont('Helvetica-Bold', 9)
    cv.setFillColor(NAVY)
    cv.drawString(C2X+5, ry, f'\u2022  {name}')
    ry -= 13
    cv.setFont('Helvetica', 8)
    cv.setFillColor(GRAY)
    desc_lines = wrap(cv, desc, 'Helvetica', 8, C2W - 18)
    for line in desc_lines:
        cv.drawString(C2X+17, ry, line)
        ry -= 12
    ry -= 4

# Advance main y past both columns
y = min(ly, ry) - 16

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — A simple workflow (4 numbered steps in 2×2 grid)
# ─────────────────────────────────────────────────────────────────────────────
y = orange_bar(cv, LM, y, CW, 'A simple workflow \u2014 4 steps')
y -= 10

STEP_W = (CW - 10) / 2   # ~265pt per box
STEP_H = 98               # height of each step box
ROW_GAP = 8

steps = [
    ('1', 'Choose a scenario',
     'Select the project track that best matches your organization.',
     []),
    ('2', 'Ground it in your work',
     'Identify real tasks, problems, or workflows interns can support.',
     []),
    ('3', 'Give AI context',
     'Provide details so the output fits your real environment:',
     ['What your organization does',
      'Tools your team uses',
      'Example tasks or data']),
    ('4', 'Generate and refine',
     'Use AI to adapt the scenario. Revise until it\u2019s realistic for 6 weeks, 25 hours per week.',
     []),
]

for i, (num, title, desc, subs) in enumerate(steps):
    col = i % 2
    row = i // 2
    sx  = LM + col * (STEP_W + 10)
    sy  = y - row * (STEP_H + ROW_GAP)

    # Box background
    cv.setFillColor(STRIPE)
    cv.rect(sx, sy-STEP_H, STEP_W, STEP_H, fill=1, stroke=0)
    # Orange left accent
    cv.setFillColor(ORANGE)
    cv.rect(sx, sy-STEP_H, 4, STEP_H, fill=1, stroke=0)

    # Navy number circle
    cx = sx + 21
    cy_circ = sy - 19
    cv.setFillColor(NAVY)
    cv.circle(cx, cy_circ, 12, fill=1, stroke=0)
    cv.setFont('Helvetica-Bold', 11)
    cv.setFillColor(white)
    cv.drawCentredString(cx, cy_circ-4, num)

    # Step title
    cv.setFont('Helvetica-Bold', 10)
    cv.setFillColor(NAVY)
    cv.drawString(sx+40, sy-15, title)

    # Description
    cv.setFont('Helvetica', 8.5)
    cv.setFillColor(DARK)
    desc_lines = wrap(cv, desc, 'Helvetica', 8.5, STEP_W - 18)
    dy = sy - 34
    for line in desc_lines:
        cv.drawString(sx+10, dy, line)
        dy -= 13

    # Sub-bullets (Step 3)
    if subs:
        cv.setFont('Helvetica', 8)
        cv.setFillColor(GRAY)
        for sb in subs:
            cv.drawString(sx+16, dy, f'\u2013  {sb}')
            dy -= 12

# Advance y past both rows of step boxes
y -= 2*(STEP_H + ROW_GAP) + 10

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — Example prompts (shaded box with left accent)
# ─────────────────────────────────────────────────────────────────────────────
y = orange_bar(cv, LM, y, CW, 'Example prompts')
y -= 8

prompts = [
    ('Prompt 1',
     '\u201cHere is a sample internship scenario. Adapt it for a [type of organization] that does [X], '
     'using [tools]. Make it realistic for high school interns.\u201d'),
    ('Prompt 2',
     '\u201cHere is a draft internship project. Improve it so it is realistic for a 6-week program '
     'with 1\u20135 high school students.\u201d'),
    ('Prompt 3',
     '\u201cCreate a simple week-by-week plan and deliverables based on this project idea.\u201d'),
]

PFONT = 8.5
PLH   = 13
PPAD  = 10

# Calculate total box height
box_h = 2 * PPAD
for label, text in prompts:
    box_h += 14                                                          # label line
    box_h += len(wrap(cv, text, 'Helvetica', PFONT, CW-2*PPAD-8))*PLH  # body
    box_h += 6                                                           # gap after

# Draw prompt box
cv.setFillColor(STRIPE)
cv.rect(LM, y-box_h, CW, box_h, fill=1, stroke=0)
cv.setFillColor(NAVY)
cv.rect(LM, y-box_h, 4, box_h, fill=1, stroke=0)   # left navy accent

py = y - PPAD - PFONT
for label, text in prompts:
    cv.setFont('Helvetica-Bold', PFONT)
    cv.setFillColor(NAVY)
    cv.drawString(LM+8, py, label)
    py -= 14

    cv.setFont('Helvetica', PFONT)
    cv.setFillColor(DARK)
    for line in wrap(cv, text, 'Helvetica', PFONT, CW-2*PPAD-8):
        cv.drawString(LM+12, py, line)
        py -= PLH
    py -= 6

y -= box_h + 12

# ─────────────────────────────────────────────────────────────────────────────
# FINAL CALLOUT BOX — navy, full width
# ─────────────────────────────────────────────────────────────────────────────
CBOX_H = 62
cv.setFillColor(NAVY)
cv.rect(LM, y-CBOX_H, CW, CBOX_H, fill=1, stroke=0)

# Yellow label
cv.setFont('Helvetica-Bold', 9)
cv.setFillColor(YELLOW)
cv.drawString(LM+8, y-16, 'A note on AI')

# Body lines
cv.setFont('Helvetica', 8.5)
cv.setFillColor(white)
cv.drawString(LM+8, y-31, 'AI helps you customize \u2014 not replace \u2014 your internship design.')
body2 = 'The strongest projects are grounded in your organization\u2019s real work and needs.'
for j, line in enumerate(wrap(cv, body2, 'Helvetica', 8.5, CW-20)):
    cv.drawString(LM+8, y-44-j*13, line)

# ─────────────────────────────────────────────────────────────────────────────
cv.save()
print(f'Saved: {OUT}')
print(f'Bottom of callout box: y = {y-CBOX_H:.0f}pt (footer top = {FTR_H}pt)')
