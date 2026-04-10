# DYCD Tech Internship Playbook

> **DYCD Summer Youth Employment Program (SYEP) — High School Tech Internship**
> A complete employer toolkit for running a 6-week tech internship program for NYC high school students.

---

## What This Repository Contains

This repo holds all the assets needed to deliver, maintain, and continue building the DYCD Tech Internship Playbook. It was built using Claude Code (AI-assisted development) and can be continued from any terminal on any computer.

---

## Repository Structure

```
dycd-tech-internship/
├── playbook/
│   └── TechInternship_final.pdf          # The main employer playbook (6-week framework)
│
├── onboarding/
│   ├── Onboarding_Tools_for_High_School_Interns.pdf   # One-pager: checklist + orientation agenda
│   └── 1on1_CheckIn_Template.pdf                      # Weekly 1:1 meeting form
│
├── reference-docs/
│   ├── DYCD-Toolkit-Walkthrough-1hr.pdf               # 60-min training session guide
│   ├── Onboarding Tools for High School Interns (SYEP Focus).pdf
│   ├── NYC Student Pathways Logo Co-Branding-Guidelines.pdf
│   └── portrait-of-a-graduatenyc.pdf                  # NYC graduate framework reference
│
├── scripts/
│   ├── create_onboarding_tools.py         # Generates onboarding PDFs from scratch
│   ├── apply_all_revisions.py             # Master script: applies all content revisions
│   ├── fix_all_issues.py                  # Comprehensive fix script (layout, text, design)
│   ├── fix_v2.py / fix_v3.py             # Iterative fix passes
│   ├── add_scenario_d.py                  # Adds the 4th project scenario to playbook
│   ├── style_scenario_d.py                # Styles the Scenario D section
│   ├── fix_scenario_d.py                  # Fixes Scenario D content
│   ├── fix_p1_cover.py                    # Cover page redesign
│   ├── fix_p1_p3_p4.py                    # Pages 1, 3, 4 layout fixes
│   ├── fix_p1_redesign.py                 # Full cover redesign pass
│   ├── fix_p3_overflow.py                 # Page 3 text overflow fix
│   ├── fix_p3_para_p16_del.py             # Page 3 paragraph + page 16 deletion
│   ├── global_sentence_case.py            # Converts text to sentence case throughout
│   ├── multi_page_updates.py              # Multi-page content updates
│   ├── update_contacts.py                 # Updates contact section
│   ├── update_page6.py                    # Page 6 specific updates
│   ├── page3_cards_and_bullets.py         # Page 3 card/bullet layout
│   ├── fix_friction_log.py                # Friction log section fix
│   ├── apply_three_updates.py             # Applies three targeted updates
│   └── final_fixes.py                     # Final round of fixes before output
│
├── assets/
│   ├── logos/                             # NYC Student Pathways official logos (PNG + EPS)
│   └── photos/                            # Tech internship event photos (68 images)
│
└── feedback/
    ├── Generalfeedbackonscenariofeedbackfriction.pdf
    └── page*notes*.jpg                    # Annotated page-by-page feedback images
```

---

## The Toolkit: How Everything Works Together

Based on the **DYCD Toolkit Walkthrough (60-min session guide)**, here is how each resource connects:

| Resource | What It Does | Used By |
|----------|-------------|---------|
| **TechInternship_final.pdf** | Complete 6-week framework: journey, 4 project scenarios, compliance & supervision guide | Supervisors + CBOs |
| **Onboarding_Tools_for_High_School_Interns.pdf** | One-pager with checklist, orientation agenda, links to Week 1 resources | Supervisors |
| **1on1_CheckIn_Template.pdf** | Structured 20–30 min weekly meeting form: wins, blockers, skill self-rating, goals, feedback loop | Supervisors |
| **Learning Plan Template** | Week-by-week skill tracker (Explore → Launch phases), Common Core + Specialization rows | Supervisors + Interns |
| **Intern Reflection & Handoff Journal** | 6-week intern workbook: weekly reflection, career thinking, "For the Next Intern" handoff | Interns |

### The 6-Week Flow

```
Day 1 Onboarding → Week 1 Setup → Weekly 1:1s → Skill Tracking → Week 6 Final Presentations
```

Each week uses:
- **Supervisor:** Onboarding checklist → 1:1 check-in template → learning plan tracking
- **Intern:** Reflection journal → skill self-ratings → handoff notes

---

## How to Continue Building with Claude Code

Anyone picking this up can continue exactly where it left off. Here's how:

### Step 1: Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

Or download the Claude Code desktop app at [claude.ai/code](https://claude.ai/code).

### Step 2: Clone This Repo

```bash
git clone https://github.com/mmanipakone/dycd-tech-internship.git
cd dycd-tech-internship
```

### Step 3: Install Python Dependencies

The scripts use the `reportlab` library to generate and modify PDFs:

```bash
pip3 install reportlab PyPDF2
```

### Step 4: Open Claude Code in the Project Directory

```bash
claude
```

Or open the Claude Code desktop app and point it to the `dycd-tech-internship/` folder.

### Step 5: Give Claude Context

When you start a new session, paste this into Claude Code to orient it:

> "I'm working on the DYCD Tech Internship Playbook for the NYC Summer Youth Employment Program (SYEP). This is a 6-week employer toolkit for high school tech interns. The main deliverable is `playbook/TechInternship_final.pdf`. The scripts in `scripts/` use reportlab to modify the PDF. The feedback in `feedback/` shows annotated notes from reviewers. The onboarding tools are in `onboarding/`. Use the `reference-docs/DYCD-Toolkit-Walkthrough-1hr.pdf` to understand how all the pieces connect."

### Step 6: Common Tasks You Can Ask Claude Code to Do

```
"Add a new section to the playbook covering [topic]"
"Fix the layout on page [X] of the playbook"
"Update the contact information in the playbook"
"Generate a new version of the onboarding one-pager"
"Apply the feedback from the feedback/ folder to the playbook"
"Create a new project scenario for [type of tech work]"
```

---

## How the Scripts Work

All scripts in `scripts/` take the existing PDF and generate a modified version. The general pattern is:

```python
# Input: existing PDF (usually TechInternship_final.pdf or an intermediate version)
# Process: modify using reportlab (draw new elements, replace text, fix layout)
# Output: new PDF saved to revised_outputs/ or overwriting the input
```

**To run any script:**

```bash
cd scripts/
python3 fix_all_issues.py
```

**Recommended order if rebuilding from scratch:**

1. `create_onboarding_tools.py` — generates the onboarding PDFs
2. `apply_all_revisions.py` — master revision script
3. `add_scenario_d.py` → `style_scenario_d.py` → `fix_scenario_d.py` — builds Scenario D
4. `fix_all_issues.py` — comprehensive fixes
5. `fix_v2.py` → `fix_v3.py` — iterative polish passes
6. `final_fixes.py` — final cleanup before publishing

---

## Playbook Content Overview

The **TechInternship_final.pdf** covers:

- **Cover + Introduction:** Program overview, who it's for, DYCD/SYEP context
- **6-Week Journey Map:** Week-by-week guide from onboarding to final presentations
- **4 Project Scenarios:**
  - Scenario A: Web/App Design
  - Scenario B: Data & Research
  - Scenario C: IT Support & Infrastructure
  - Scenario D: Digital Media & Content Creation
- **Supervision Best Practices:** How to run effective 1:1s, give feedback, track progress
- **Compliance Essentials:** SYEP requirements, documentation, reporting
- **Onboarding Resources:** Checklist, orientation agenda, learning plan setup

---

## Assets

### Logos (`assets/logos/`)
Official **NYC Student Pathways** logos in PNG and EPS format. Use per the branding guidelines in `reference-docs/NYC Student Pathways Logo Co-Branding-Guidelines.pdf`.

### Photos (`assets/photos/`)
68 photos from InspirED/JCA tech internship events (November 2024). These are available for use in presentations, marketing materials, and the playbook itself.

---

## Feedback & Revision History

The `feedback/` folder contains:
- Annotated page screenshots (`page1notes.jpg` through `page7comments.jpg`) — reviewer markup on the original playbook
- `Generalfeedbackonscenariofeedbackfriction.pdf` — consolidated written feedback on scenario sections

These were the basis for all revisions applied by the scripts.

---

## Contributing / Continuing the Work

1. Always work from the latest `playbook/TechInternship_final.pdf` as your base
2. Create a new script for each major change (keeps history clean and reversible)
3. Name scripts descriptively: `fix_[what].py` or `add_[what].py`
4. After making changes, test by opening the output PDF and reviewing visually
5. Commit your updated PDF and script together

---

## Questions?

This project was built for the NYC Department of Youth and Community Development (DYCD) as part of the Summer Youth Employment Program (SYEP) Tech Internship initiative.
