# CareerPrep Job-Hunting Agent

> A file-driven AI agent that helps students manage their entire job application workflow — from resume tailoring and interview preparation to application tracking and smart reminders.

---

## Features

| Feature | Description |
|---|---|
| **Job Description Analysis** | Reads job posters and extracts required skills by category |
| **Resume Analysis** | Reads your resume and identifies matched vs. missing skills |
| **Skill-Gap Report** | Visual match score with prioritised learning roadmap |
| **Resume Tailoring** | Actionable bullet points and improvement suggestions per skill area |
| **Interview Questions** | Technical, HR, and KB-derived questions tailored to each job |
| **Application Tracker** | CSV-based tracker with status, dates, and next actions |
| **Smart Reminders** | Urgency-aware reminders (Overdue / Today / This Week / Planned) |
| **Cover Letter Generator** ⭐ | Personalised cover letter draft per application |
| **Resume Quality Score** ⭐ | Scores your resume on 4 dimensions with specific feedback |
| **Project-to-Job Mapping** ⭐ | Maps your resume projects to job skill requirements |
| **Menu-based CLI** ⭐ | Interactive command-line interface — no code editing needed |

---

## Project Structure

```
job-hunting-agent/
│
├── app.py                  ← Main agent (run this)
├── requirements.txt        ← Python dependencies
├── README.md               ← This file
├── reflection.md           ← What was built and learned
│
├── input_jobs/             ← Place job posters here (.txt)
│   ├── job_poster_01.txt
│   └── job_poster_02.txt
│
├── input_resumes/          ← Place your resume here (.txt)
│   └── my_resume.txt
│
├── input_kb/               ← Place course/KB notes here (.txt)
│   ├── interview_prep_notes.txt
│   └── job_fair_slides.txt
│
├── outputs/                ← Generated reports (auto-created)
│   ├── job_analysis_report.txt
│   ├── skill_gap_report.txt
│   ├── tailored_resume_suggestions.txt
│   ├── interview_questions.txt
│   ├── project_mapping.txt
│   ├── cover_letter.txt
│   └── final_agent_report.txt
│
├── tracker/                ← Application tracker (auto-created)
│   ├── applications.csv
│   └── reminders.txt
│
└── samples/                ← Example input files for reference
    ├── sample_job_poster.txt
    ├── sample_resume.txt
    └── sample_kb.txt
```

---

## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shoaibhaider-ai/job-hunting-agent.git
cd job-hunting-agent
```

### 2. Create a Virtual Environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare Your Input Files

| Folder | What to add |
|---|---|
| `input_jobs/` | Copy-paste job descriptions as `.txt` files |
| `input_resumes/` | Paste your resume text into `my_resume.txt` |
| `input_kb/` | Add course slides, notes, or job-prep material as `.txt` files |

> **Tip:** Sample files are provided in `samples/` — you can copy them as a starting point.

### 5. Run the Agent

```bash
python app.py
```

You will see a menu:

```
══════════════════════════════════════════════════════════════
   CareerPrep Job-Hunting Agent   v1.0
   File-Driven  •  AI-Powered  •  GitHub-Ready
══════════════════════════════════════════════════════════════

  MAIN MENU
  ─────────────────────────────────────────────
  1.  Run Full Agent  (generate all reports)
  2.  View Application Tracker
  3.  Add New Application
  4.  View Reminders
  5.  Generate Cover Letter  (pick application)
  6.  Exit
```

---

## Application Tracker Fields

| Field | Description | Example |
|---|---|---|
| `application_id` | Unique ID | APP-001 |
| `company` | Company name | ABC Tech Solutions |
| `role` | Job title | Junior AI Engineer Intern |
| `source` | Where found | LinkedIn |
| `status` | Current status | Interview Scheduled |
| `applied_date` | Date applied | 2026-04-20 |
| `interview_date` | Interview date | 2026-05-03 |
| `follow_up_date` | Follow-up deadline | 2026-05-06 |
| `next_action` | What to do next | Revise ML concepts |
| `notes` | Extra notes | Cover letter submitted |

---

## Output Files Generated

| File | Description |
|---|---|
| `outputs/job_analysis_report.txt` | Skills extracted from job descriptions |
| `outputs/skill_gap_report.txt` | Match score, matched skills, gaps + learning roadmap |
| `outputs/tailored_resume_suggestions.txt` | Resume quality score + bullet point suggestions |
| `outputs/interview_questions.txt` | Technical, HR, and KB-based questions |
| `outputs/project_mapping.txt` | Which projects cover which job skills |
| `outputs/cover_letter.txt` | Personalised cover letter draft |
| `outputs/final_agent_report.txt` | Complete consolidated report |
| `tracker/applications.csv` | Application tracker |
| `tracker/reminders.txt` | Urgency-aware reminders |

---

## Unique Features (Extra Marks)

1. **Resume Quality Score** — Rates your resume on Skill Breadth, Content Length, Action Verbs, and Contact/Links
2. **Cover Letter Generator** — Generates a personalised, editable cover letter per application
3. **Project-to-Job Mapping** — Shows which of your resume projects satisfy job requirements
4. **Urgency-Aware Reminder Engine** — Classifies reminders as Overdue / Today / This Week / Planned
5. **Menu-based CLI** — Interactive interface; no code changes needed to use the agent

---

## Technologies Used

- **Python 3.10+** — Core language
- **csv** — Application tracker read/write
- **re** — Keyword extraction with word-boundary matching
- **datetime** — Date-based reminder logic
- **os** — File and folder management

No paid APIs or external services required.

---

## Submission Checklist

- [x] GitHub repository created
- [x] `input_jobs/` contains at least 2 job poster files
- [x] `input_resumes/` contains resume file
- [x] `input_kb/` contains at least 2 KB files
- [x] Agent reads files dynamically from folders
- [x] All 7 output reports generated
- [x] `tracker/applications.csv` populated with real-like entries
- [x] `tracker/reminders.txt` generated
- [x] `README.md` complete
- [x] `reflection.md` complete
- [x] At least 3 unique features implemented

---

## Author

**[Muhammad Shoaib Haider]**    
GitHub: [shoaibhaider-ai]  
Date: April 28, 2026
