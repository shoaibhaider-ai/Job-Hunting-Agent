# Reflection — CareerPrep Job-Hunting Agent

**Course:** Agentic AI / AI Agents
**Activity:** File-Driven Job-Hunting Agent
**Date:** April 28, 2026

---

## 1. What I Built

I built the **CareerPrep Job-Hunting Agent** — a fully file-driven Python application
that helps a student manage their job search workflow from a single command-line interface.

The agent reads real job descriptions, my own resume, and course/interview knowledge-base
notes from organised input folders, then performs automated analysis and generates a complete
set of career-preparation outputs.

### Core Capabilities Implemented

| Capability | How It Works |
|---|---|
| File Reading | Reads all `.txt` files from `input_jobs/`, `input_resumes/`, and `input_kb/` dynamically |
| Skill Extraction | Uses regex word-boundary matching against a categorised dictionary of 80+ keywords |
| Job Analysis | Extracts required skills and role indicators from job descriptions |
| Resume Analysis | Identifies skills present in the resume by category |
| Skill-Gap Report | Computes a match score (%) and lists matched vs. missing skills with a learning roadmap |
| Resume Tailoring | Generates improvement feedback, category-specific bullet points, and learning resources |
| Interview Questions | Generates technical question banks, HR questions, and KB-derived questions |
| Application Tracker | CSV-based tracker with 10 fields: status, dates, actions, and notes |
| Reminder Engine | Classifies reminders as Overdue, Today, This Week, or Planned based on real dates |

### Unique Features Added

1. **Resume Quality Score** — Rates the resume on four dimensions (skill breadth, content length,
   action verb usage, and contact/links) and produces specific improvement tips.

2. **Cover Letter Generator** — Produces a personalised cover-letter draft tailored to the
   specific company and role, incorporating matched skills from the resume.

3. **Project-to-Job Mapping** — Scans resume project descriptions and maps each project to the
   job skills it covers, helping identify which experience to emphasise in applications.

4. **Urgency-Aware Reminder Engine** — Goes beyond basic reminders by comparing dates with today
   and classifying each reminder with urgency labels (Overdue, Today, In N Days, This Week, Planned).

5. **Menu-Based CLI Interface** — Provides a clean interactive menu so the agent can be used
   without editing any code — useful for non-technical users.

---

## 2. How I Designed It (GAME Framework)

**Goal:** Help a student convert scattered job-search materials into an organised, actionable
workflow covering analysis, preparation, tracking, and reminders.

**Actions:**
- Read files → extract skills → compare → generate reports → track → remind

**Memory:**
- Current job skill set extracted from job posters
- Resume skills and quality score
- KB notes for question generation
- Application history in `tracker/applications.csv`

**Environment:**
- Local project folders (input/output/tracker)
- GitHub repository for version control and submission

---

## 3. Challenges Faced

**Challenge 1: Keyword Matching Accuracy**
Initially I used simple string containment (`keyword in text`), which produced false positives
(e.g., "r" matching anywhere in text). I resolved this by switching to regex with
`\b` word-boundary anchors, which ensures only whole-word matches are counted.

**Challenge 2: Meaningful Text Extraction**
Extracting "project descriptions" from resume text heuristically is imprecise.
I used action-verb signals (developed, built, deployed, etc.) as proxies, which works
well for properly formatted resumes but may miss projects written in other styles.
A future improvement would be to use an NLP library like spaCy for entity recognition.

**Challenge 3: Date-Based Reminder Logic**
Comparing dates correctly required careful handling of empty fields, invalid formats,
and edge cases (overdue vs. today vs. upcoming). I implemented a `parse_date()` helper
that tries multiple date formats before returning None.

**Challenge 4: Keeping Code Modular**
With 10+ features, keeping functions small and single-purpose was a deliberate discipline.
I organised the code into clear sections: utilities, extraction, analysis, report generators,
tracker, reminders, and the CLI — which also makes each part independently testable.

---

## 4. What I Would Improve with More Time

- **PDF Reading:** Use `pypdf` or `pdfplumber` to read job posters and resumes directly as PDFs,
  without requiring manual conversion to text.

- **LLM Integration:** Connect to the OpenAI API or a local LLM to generate truly personalised
  resume bullets and cover letters rather than template-based ones.

- **Streamlit Dashboard:** Replace the CLI with a Streamlit web interface showing charts for
  match score, application status breakdown, and an interactive tracker table.

- **Reminder Notifications:** Send actual email reminders using Python's `smtplib` when an
  interview date is approaching.

- **DOCX Resume Support:** Use the `python-docx` library to read `.docx` resume files directly.

- **Spacy NLP:** Use spaCy for more accurate entity extraction from job descriptions and resumes
  (organisations, roles, skills, dates).

---

## 5. What I Learned

- How to design a practical agentic AI system using the GAME framework.
- How to build clean, modular Python programs with clear separation of concerns.
- How to use regex for precise keyword extraction from unstructured text.
- How to read, write, and manage CSV files programmatically for application tracking.
- How to handle date logic for reminder systems in real-world scenarios.
- The importance of folder-based file management for file-driven agent workflows.
- How to write professional documentation (README, reflection, code comments).

---

## 6. LLM / Copilot Usage

GitHub Copilot was used to assist with boilerplate code generation and code completion.
All agent design decisions, logic structure, keyword dictionaries, report formats,
and feature ideas were my own. I reviewed and understood every line of code before
including it in the final submission.

---

## 7. Testing Evidence

- Placed 2 job posters in `input_jobs/`, 1 resume in `input_resumes/`, 2 KB files in `input_kb/`.
- Ran `python app.py` and selected option 1 (Full Run).
- Verified all 7 output files were created in `outputs/` and `tracker/`.
- Checked skill extraction accuracy manually by comparing extracted keywords to source files.
- Tested the reminder engine with different status values and date combinations.
- Verified the cover letter generator produces output for a selected application.
- Tested edge case: empty input folder — agent prints error message and exits cleanly.

---

*I confirm that I built and tested this agent myself and understand all submitted code.*

**Student Signature:** ___________________
**Date:** April 28, 2026
