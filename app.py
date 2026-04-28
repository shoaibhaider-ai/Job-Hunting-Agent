"""
CareerPrep Job-Hunting Agent
============================
A file-driven agent that helps students manage their job application workflow.

Reads job descriptions, resumes, and knowledge-base files from input folders
and generates tailored reports, interview questions, skill-gap analysis,
application tracking, and smart reminders.

Features:
  - Menu-based CLI interface           (Unique Feature 1)
  - Resume quality scoring             (Unique Feature 2)
  - Cover letter generator             (Unique Feature 3)
  - Project-to-job skill mapping       (Unique Feature 4)
  - Urgency-aware reminder engine      (Unique Feature 5)

Author  : CareerPrep Agent
Date    : April 28, 2026
Version : 1.0
"""

import os
import sys
import csv
import re
from datetime import datetime, date

# Force UTF-8 output so Unicode box-drawing characters render correctly on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ─── Directory Constants ───────────────────────────────────────────────────────
JOB_DIR     = "input_jobs"
RESUME_DIR  = "input_resumes"
KB_DIR      = "input_kb"
OUTPUT_DIR  = "outputs"
TRACKER_DIR = "tracker"
SAMPLES_DIR = "samples"

TRACKER_PATH = os.path.join(TRACKER_DIR, "applications.csv")

TRACKER_FIELDS = [
    "application_id", "company", "role", "source", "status",
    "applied_date", "interview_date", "follow_up_date", "next_action", "notes"
]

TODAY = date.today()

# ─── Categorised Skill / Keyword Dictionary ───────────────────────────────────
SKILL_CATEGORIES = {
    "Programming Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#",
        "r", "kotlin", "swift", "go", "rust", "php", "ruby", "scala"
    ],
    "AI & Machine Learning": [
        "machine learning", "deep learning", "neural network", "nlp",
        "computer vision", "scikit-learn", "tensorflow", "pytorch", "keras",
        "transformers", "langchain", "llm", "prompt engineering",
        "reinforcement learning", "data preprocessing", "feature engineering",
        "model training", "model evaluation", "hugging face", "openai",
        "generative ai", "rag", "vector database", "embeddings"
    ],
    "Data & Analytics": [
        "pandas", "numpy", "matplotlib", "seaborn", "sql", "mysql",
        "postgresql", "mongodb", "data analysis", "data visualization",
        "tableau", "power bi", "excel", "statistics"
    ],
    "Web & APIs": [
        "flask", "django", "fastapi", "rest api", "graphql", "html",
        "css", "react", "node.js", "streamlit", "web scraping", "api"
    ],
    "DevOps & Tools": [
        "git", "github", "docker", "kubernetes", "linux", "bash",
        "ci/cd", "aws", "azure", "gcp", "jupyter", "vscode"
    ],
    "Soft Skills": [
        "communication", "problem solving", "teamwork", "leadership",
        "time management", "critical thinking", "presentation",
        "collaboration", "adaptability"
    ],
    "Engineering Practices": [
        "oop", "agile", "scrum", "testing", "debugging",
        "documentation", "research", "project management", "database"
    ],
}

ALL_KEYWORDS = [kw for kws in SKILL_CATEGORIES.values() for kw in kws]


# ══════════════════════════════════════════════════════════════════════════════
#  UTILITY HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def sep(char="═", width=62):
    return char * width


def hdr(title):
    line = sep()
    return f"\n{line}\n  {title}\n{line}\n"


def ensure_folders():
    """Create all required project directories if they do not exist."""
    for folder in [JOB_DIR, RESUME_DIR, KB_DIR, OUTPUT_DIR, TRACKER_DIR, SAMPLES_DIR]:
        os.makedirs(folder, exist_ok=True)


def save_text(path, content):
    """Write text content to a file, creating parent directories as needed."""
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"    [Saved] {path}")


def read_text_files(folder):
    """
    Read every .txt file inside a folder.
    Returns (combined_text, file_count, list_of_filenames).
    """
    combined = ""
    filenames = []
    if not os.path.isdir(folder):
        return combined, 0, filenames
    for fname in sorted(os.listdir(folder)):
        if fname.lower().endswith(".txt"):
            fpath = os.path.join(folder, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                combined += f"\n\n--- FILE: {fname} ---\n" + f.read()
            filenames.append(fname)
    return combined, len(filenames), filenames


def parse_date(date_str):
    """Parse a date string (YYYY-MM-DD) to a date object; returns None on failure."""
    if not date_str or not date_str.strip():
        return None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_str.strip(), fmt).date()
        except ValueError:
            pass
    return None


# ══════════════════════════════════════════════════════════════════════════════
#  EXTRACTION
# ══════════════════════════════════════════════════════════════════════════════

def extract_skills(text):
    """
    Scan text for known skills and return them grouped by category.
    Uses word-boundary regex for precise matching.
    """
    text_lower = text.lower()
    found = {}
    for category, keywords in SKILL_CATEGORIES.items():
        hits = [
            kw for kw in keywords
            if re.search(r"\b" + re.escape(kw) + r"\b", text_lower)
        ]
        if hits:
            found[category] = hits
    return found


def flatten(skill_dict):
    """Convert {category: [skills]} dict into a flat list."""
    return [s for skills in skill_dict.values() for s in skills]


def extract_projects(resume_text):
    """
    Heuristic: pull lines from resume that describe projects.
    Looks for action-oriented verbs as signals.
    """
    signals = ["project", "built", "developed", "created", "designed",
               "implemented", "deployed", "trained", "automated"]
    results = []
    for line in resume_text.splitlines():
        line = line.strip()
        if len(line) > 25 and any(s in line.lower() for s in signals):
            results.append(line[:220])
    return results[:10]


# ══════════════════════════════════════════════════════════════════════════════
#  ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

def compare_skills(job_flat, resume_flat):
    """Return (matched, missing, score_percent)."""
    matched = [s for s in job_flat if s in resume_flat]
    missing = [s for s in job_flat if s not in resume_flat]
    score = 0.0 if not job_flat else round(len(matched) / len(job_flat) * 100, 1)
    return matched, missing, score


def resume_quality_score(resume_text, resume_skills_flat):
    """
    UNIQUE FEATURE 2 — Score the resume on four dimensions.
    Returns {"scores": {dim: pct}, "feedback": [tips]}.
    """
    scores = {}
    feedback = []

    # 1. Skill breadth
    n = len(resume_skills_flat)
    scores["Skill Breadth"] = min(100, n * 9)
    if n < 5:
        feedback.append("Add more technical skills — aim for at least 8–10 relevant keywords.")
    elif n >= 10:
        feedback.append("Good skill variety. Ensure every skill is backed by project evidence.")

    # 2. Content length
    words = len(resume_text.split())
    scores["Length & Detail"] = min(100, max(0, 100 - abs(words - 400) // 4))
    if words < 150:
        feedback.append("Resume is too short. Add project descriptions and experiences.")
    elif words > 750:
        feedback.append("Resume may be too long. Keep it to one page for student roles.")

    # 3. Action verbs
    action_verbs = [
        "developed", "designed", "implemented", "built", "created",
        "analyzed", "managed", "led", "achieved", "optimized",
        "deployed", "collaborated", "researched", "presented", "automated"
    ]
    verb_hits = sum(1 for v in action_verbs if v in resume_text.lower())
    scores["Action Verbs"] = min(100, verb_hits * 12)
    if verb_hits < 3:
        feedback.append("Use more action verbs: Developed, Implemented, Deployed, Automated…")

    # 4. Contact information
    has_email   = bool(re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", resume_text))
    has_github  = "github" in resume_text.lower()
    has_linkedin = "linkedin" in resume_text.lower()
    scores["Contact & Links"] = (34 if has_email else 0) + (33 if has_github else 0) + (33 if has_linkedin else 0)
    if not has_email:
        feedback.append("Add your email address.")
    if not has_github:
        feedback.append("Add your GitHub profile link to showcase code.")
    if not has_linkedin:
        feedback.append("Add your LinkedIn profile link.")

    scores["Overall"] = round(sum(scores.values()) / len(scores), 1)
    return {"scores": scores, "feedback": feedback}


# ══════════════════════════════════════════════════════════════════════════════
#  REPORT GENERATORS
# ══════════════════════════════════════════════════════════════════════════════

def generate_job_analysis(job_text, job_skill_dict, filenames):
    report  = hdr("JOB ANALYSIS REPORT")
    report += f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    report += f"Files read: {', '.join(filenames)}\n\n"

    report += "SKILLS & KEYWORDS FOUND IN JOB DESCRIPTIONS\n"
    report += sep("-", 48) + "\n"
    for cat, skills in job_skill_dict.items():
        report += f"\n  [{cat}]\n"
        for s in skills:
            report += f"    •  {s}\n"

    total = len(flatten(job_skill_dict))
    report += f"\n  Total skill areas identified: {total}\n"

    report += "\nKEY ROLE INDICATORS (extracted from job text)\n"
    report += sep("-", 48) + "\n"
    role_kw = ["role:", "position:", "job title:", "title:", "company:", "responsibilities:", "requirements:"]
    for line in job_text.splitlines():
        stripped = line.strip()
        if 8 < len(stripped) < 130 and any(kw in stripped.lower() for kw in role_kw):
            report += f"  →  {stripped}\n"

    return report


def generate_skill_gap_report(job_skill_dict, resume_skill_dict, matched, missing, score):
    report  = hdr("SKILL GAP REPORT")
    report += f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

    filled = int(score / 5)
    bar    = "█" * filled + "░" * (20 - filled)
    report += f"  MATCH SCORE :  {score}%\n"
    report += f"  Progress    : [{bar}]\n\n"

    report += f"MATCHED SKILLS  ({len(matched)} found in your resume)\n"
    report += sep("-", 48) + "\n"
    for s in matched:
        report += f"  ✔  {s}\n"
    if not matched:
        report += "  None matched yet — start by adding core skills to your resume.\n"

    report += f"\nMISSING SKILLS  ({len(missing)} gaps to close)\n"
    report += sep("-", 48) + "\n"
    for s in missing:
        report += f"  ✘  {s}\n"
    if not missing:
        report += "  🎉  No gaps! Your resume matches all job requirements.\n"

    # Priority learning order by category importance
    priority_order = {
        "AI & Machine Learning": 1, "Programming Languages": 2,
        "Data & Analytics": 3, "Web & APIs": 4,
        "DevOps & Tools": 5, "Engineering Practices": 6, "Soft Skills": 7,
    }
    missing_by_cat = {}
    for cat, cat_skills in SKILL_CATEGORIES.items():
        gaps = [s for s in cat_skills if s in missing]
        if gaps:
            missing_by_cat[cat] = gaps
    sorted_cats = sorted(missing_by_cat.items(), key=lambda x: priority_order.get(x[0], 99))

    if sorted_cats:
        report += "\nPRIORITY LEARNING ROADMAP\n" + sep("-", 48) + "\n"
        for i, (cat, skills) in enumerate(sorted_cats, 1):
            report += f"  {i}. [{cat}]:  {', '.join(skills)}\n"

    return report


def generate_resume_suggestions(job_skill_dict, missing, resume_text, quality):
    report  = hdr("TAILORED RESUME SUGGESTIONS")
    report += f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

    # Quality score grid
    report += "RESUME QUALITY SCORECARD\n" + sep("-", 48) + "\n"
    for dim, val in quality["scores"].items():
        bar = "█" * int(val / 10) + "░" * (10 - int(val / 10))
        report += f"  {dim:<22} [{bar}]  {val}%\n"

    report += "\nIMPROVEMENT FEEDBACK\n" + sep("-", 48) + "\n"
    for tip in quality["feedback"]:
        report += f"  ⚠  {tip}\n"
    if not quality["feedback"]:
        report += "  ✔  Resume quality looks strong!\n"

    # Category-specific bullet point suggestions
    bullet_map = {
        "AI & Machine Learning": [
            "Trained a classification model using scikit-learn with 93% test accuracy.",
            "Built an NLP pipeline for text classification using Hugging Face transformers.",
            "Designed a prompt-engineering workflow with LangChain to automate document Q&A.",
        ],
        "Programming Languages": [
            "Wrote modular, OOP-based Python scripts for data extraction and analysis.",
            "Implemented a command-line tool in Python to automate repetitive workflows.",
        ],
        "Data & Analytics": [
            "Analyzed a 50,000-row dataset with Pandas and NumPy; identified 3 key trends.",
            "Created interactive Matplotlib dashboards to visualize model performance.",
        ],
        "Web & APIs": [
            "Built a REST API with Flask to serve ML model predictions to a React frontend.",
            "Developed a Streamlit dashboard for real-time data exploration and filtering.",
        ],
        "DevOps & Tools": [
            "Managed all projects on GitHub with structured branches, commits, and README files.",
            "Used Docker to containerize a Flask application for consistent deployment.",
        ],
    }

    report += "\nSUGGESTED RESUME BULLET POINTS\n" + sep("-", 48) + "\n"
    for cat, skills in job_skill_dict.items():
        bullets = bullet_map.get(cat, [])
        if bullets:
            report += f"\n  [{cat}]\n"
            for b in bullets:
                report += f"    •  {b}\n"

    # Skills-to-acquire section with resources
    if missing:
        resources = {
            "machine learning"   : "Coursera — Machine Learning Specialization (Andrew Ng)",
            "deep learning"      : "fast.ai — Practical Deep Learning for Coders",
            "python"             : "python.org — Official Python Tutorial",
            "sql"                : "SQLZoo.net — Interactive SQL exercises",
            "git"                : "GitHub Learning Lab — Git & GitHub",
            "docker"             : "docs.docker.com — Docker Get Started",
            "streamlit"          : "docs.streamlit.io — Streamlit documentation",
            "flask"              : "Flask Mega-Tutorial by Miguel Grinberg",
            "prompt engineering": "DeepLearning.AI — Prompt Engineering for Developers",
            "tensorflow"         : "tensorflow.org/tutorials",
            "pytorch"            : "pytorch.org/tutorials",
            "pandas"             : "pandas.pydata.org/docs/getting_started",
        }
        report += "\nSKILLS TO ACQUIRE (with learning resources)\n" + sep("-", 48) + "\n"
        for skill in missing:
            resource = resources.get(skill, f"Search: '{skill} tutorial for beginners'")
            report += f"  •  {skill:<28}  →  {resource}\n"

    return report


def generate_interview_questions(job_skill_dict, kb_text, job_text):
    report  = hdr("INTERVIEW QUESTIONS")
    report += f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

    tech_questions = {
        "AI & Machine Learning": [
            "What is the difference between supervised, unsupervised, and reinforcement learning?",
            "How do you handle overfitting in a machine learning model?",
            "Explain the bias-variance tradeoff with an example.",
            "What evaluation metric would you choose for an imbalanced classification dataset and why?",
            "Describe the steps in a typical ML pipeline from raw data to deployment.",
        ],
        "Programming Languages": [
            "What are Python decorators and why would you use them?",
            "Explain OOP concepts: inheritance, polymorphism, and encapsulation.",
            "What is the difference between a list, tuple, set, and dictionary in Python?",
            "How does Python handle memory management and garbage collection?",
        ],
        "Data & Analytics": [
            "How do you handle missing values in a real-world dataset?",
            "What is the difference between INNER JOIN, LEFT JOIN, and FULL OUTER JOIN in SQL?",
            "How would you detect and handle outliers in a dataset?",
            "Describe a data analysis project you have worked on end-to-end.",
        ],
        "Web & APIs": [
            "What is a REST API and how does it differ from GraphQL?",
            "How would you secure a REST API endpoint against unauthorized access?",
            "Explain HTTP status codes 200, 400, 401, 403, 404, and 500.",
        ],
        "DevOps & Tools": [
            "What is the difference between git merge and git rebase?",
            "What is Docker and what problem does it solve?",
            "Describe your GitHub workflow when collaborating on a team project.",
        ],
    }

    q_num = 1
    report += "TECHNICAL QUESTIONS (BY SKILL AREA)\n" + sep("-", 48) + "\n"
    for cat, skills in job_skill_dict.items():
        prepared = tech_questions.get(cat, [])
        if prepared or skills:
            report += f"\n  [{cat}]\n"
            for q in prepared:
                report += f"  Q{q_num:02d}. {q}\n"
                q_num += 1
            for skill in skills:
                report += f"  Q{q_num:02d}. How have you applied '{skill}' in a project or academic task?\n"
                q_num += 1

    report += "\n\nHR & BEHAVIOURAL QUESTIONS\n" + sep("-", 48) + "\n"
    hr_qs = [
        "Tell me about yourself and your career goals.",
        "Why are you interested in this specific role and company?",
        "Describe your most challenging project experience and how you handled it.",
        "How do you manage your time when working under multiple deadlines?",
        "Tell me about a time you worked effectively in a team.",
        "What are your greatest strengths and areas you want to improve?",
        "Where do you see yourself in 3–5 years?",
        "Why should we select you over other candidates?",
        "How do you keep up to date with new developments in AI and technology?",
        "Describe a project you are most proud of and explain your contribution.",
    ]
    for q in hr_qs:
        report += f"  Q{q_num:02d}. {q}\n"
        q_num += 1

    report += "\n\nQUESTIONS DERIVED FROM KNOWLEDGE BASE\n" + sep("-", 48) + "\n"
    kb_lines = [
        line.strip().lstrip("-•→").strip()
        for line in kb_text.splitlines()
        if len(line.strip()) > 35
    ]
    report += "  (Based on your uploaded KB files — study these carefully)\n\n"
    for line in kb_lines[:15]:
        report += f"  Q{q_num:02d}. Explain the following concept and give a practical example:\n"
        report += f"       \"{line[:120]}\"\n"
        q_num += 1

    return report


# ══════════════════════════════════════════════════════════════════════════════
#  UNIQUE FEATURE 3 — COVER LETTER GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

def generate_cover_letter(company, role, resume_text, matched_skills):
    """Generate a personalised cover letter draft based on matched skills."""
    today_str   = TODAY.strftime("%B %d, %Y")
    skills_str  = ", ".join(matched_skills[:6]) if matched_skills else "relevant technical skills"

    letter  = hdr("COVER LETTER DRAFT")
    letter += f"Date: {today_str}\n\n"
    letter += f"Hiring Manager\n{company}\n\n"
    letter += f"Subject: Application for the {role} Position\n\n"
    letter += "Dear Hiring Manager,\n\n"
    letter += (
        f"I am writing to express my strong interest in the {role} position at {company}. "
        f"As a motivated computer science student with hands-on experience in {skills_str}, "
        f"I am confident that I can make a meaningful contribution to your team.\n\n"
        f"Throughout my academic journey I have worked on several projects that required me to "
        f"apply theoretical knowledge to real-world problems. I thrive in collaborative environments, "
        f"consistently deliver quality work under deadlines, and am passionate about leveraging "
        f"technology to solve meaningful challenges.\n\n"
        f"I have carefully reviewed the requirements for this role and I am excited by the "
        f"opportunity to apply my skills in {skills_str} in a professional setting. I am a "
        f"fast learner and I am committed to growing alongside the talented team at {company}.\n\n"
        f"I would welcome the opportunity to discuss how my background and enthusiasm align "
        f"with your team's goals. My resume is attached for your review.\n\n"
        f"Thank you for your time and consideration.\n\n"
        f"Sincerely,\n"
        f"[Your Full Name]\n"
        f"[Your Email Address]  |  [Your Phone Number]\n"
        f"[GitHub Profile URL]  |  [LinkedIn Profile URL]\n"
    )
    return letter


# ══════════════════════════════════════════════════════════════════════════════
#  UNIQUE FEATURE 4 — PROJECT-TO-JOB MAPPING
# ══════════════════════════════════════════════════════════════════════════════

def map_projects_to_jobs(resume_text, job_skill_dict):
    """Map resume project lines to relevant job skill requirements."""
    report  = hdr("PROJECT-TO-JOB SKILL MAPPING")
    report += f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    report += "This section shows which of your projects cover the required job skills.\n\n"

    projects    = extract_projects(resume_text)
    job_flat    = flatten(job_skill_dict)

    if not projects:
        report += "  No project descriptions detected in your resume.\n"
        report += "  Tip: Add project entries starting with action verbs (e.g., 'Developed a…').\n"
        return report

    for i, proj in enumerate(projects, 1):
        covered = [s for s in job_flat if s in proj.lower()]
        label   = proj[:100] + "…" if len(proj) > 100 else proj
        report += f"  PROJECT {i}: {label}\n"
        if covered:
            report += f"    → Job skills covered: {', '.join(covered)}\n"
        else:
            report += "    → No direct skill match. Add relevant keywords to this entry.\n"
        report += "\n"

    return report


# ══════════════════════════════════════════════════════════════════════════════
#  TRACKER
# ══════════════════════════════════════════════════════════════════════════════

def load_tracker():
    """Load all applications from the CSV tracker."""
    if not os.path.exists(TRACKER_PATH):
        return []
    with open(TRACKER_PATH, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def save_tracker(records):
    """Persist the tracker records back to CSV."""
    os.makedirs(TRACKER_DIR, exist_ok=True)
    with open(TRACKER_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=TRACKER_FIELDS)
        writer.writeheader()
        writer.writerows(records)


def create_sample_tracker():
    """Populate tracker with realistic sample entries if it does not yet exist."""
    if os.path.exists(TRACKER_PATH):
        return
    sample = [
        {
            "application_id" : "APP-001",
            "company"        : "ABC Tech Solutions",
            "role"           : "Junior AI Engineer Intern",
            "source"         : "LinkedIn",
            "status"         : "Interview Scheduled",
            "applied_date"   : "2026-04-20",
            "interview_date" : "2026-05-03",
            "follow_up_date" : "2026-05-06",
            "next_action"    : "Revise Python & ML concepts; prepare project explanations",
            "notes"          : "Resume tailored; cover letter submitted",
        },
        {
            "application_id" : "APP-002",
            "company"        : "DataVision Analytics",
            "role"           : "Data Science Intern",
            "source"         : "Rozee.pk",
            "status"         : "Applied",
            "applied_date"   : "2026-04-22",
            "interview_date" : "",
            "follow_up_date" : "2026-05-02",
            "next_action"    : "Send follow-up email if no response by May 2",
            "notes"          : "Applied via online portal; confirmation email received",
        },
        {
            "application_id" : "APP-003",
            "company"        : "CloudBase Systems",
            "role"           : "Python Developer Trainee",
            "source"         : "Company Website",
            "status"         : "Not Applied",
            "applied_date"   : "",
            "interview_date" : "",
            "follow_up_date" : "",
            "next_action"    : "Tailor resume for Flask/Django; apply by April 30",
            "notes"          : "Strong Flask and REST API requirement",
        },
        {
            "application_id" : "APP-004",
            "company"        : "NeuralEdge AI",
            "role"           : "ML Research Assistant",
            "source"         : "University Job Portal",
            "status"         : "Shortlisted",
            "applied_date"   : "2026-04-15",
            "interview_date" : "2026-05-10",
            "follow_up_date" : "2026-05-12",
            "next_action"    : "Prepare research presentation; study deep learning concepts",
            "notes"          : "Shortlisted from 80 applicants; strong ML background required",
        },
        {
            "application_id" : "APP-005",
            "company"        : "TechStart Innovations",
            "role"           : "Software Engineering Intern",
            "source"         : "WhatsApp / Referral",
            "status"         : "Rejected",
            "applied_date"   : "2026-04-10",
            "interview_date" : "",
            "follow_up_date" : "",
            "next_action"    : "Request feedback; improve GitHub portfolio projects",
            "notes"          : "Rejected at initial screening; work on project quality",
        },
    ]
    save_tracker(sample)
    print(f"    [Created] {TRACKER_PATH} with {len(sample)} sample entries")


def add_application():
    """Interactive: add a new application row to the tracker."""
    records = load_tracker()
    new_id  = f"APP-{len(records) + 1:03d}"
    print(f"\n  Adding new application [{new_id}]\n")
    record  = {"application_id": new_id}
    fields  = {
        "company"        : "Company name: ",
        "role"           : "Role / Position: ",
        "source"         : "Source (LinkedIn / Rozee / Referral / etc.): ",
        "status"         : "Status (Not Applied / Applied / Interview Scheduled / Shortlisted / Rejected / Offered): ",
        "applied_date"   : "Applied date (YYYY-MM-DD or leave blank): ",
        "interview_date" : "Interview date (YYYY-MM-DD or leave blank): ",
        "follow_up_date" : "Follow-up date (YYYY-MM-DD or leave blank): ",
        "next_action"    : "Next action: ",
        "notes"          : "Notes: ",
    }
    for field, prompt in fields.items():
        record[field] = input(f"    {prompt}").strip()
    records.append(record)
    save_tracker(records)
    print(f"\n    [Added] Application {new_id} saved successfully.")


def view_tracker():
    """Print the tracker as a formatted table."""
    records = load_tracker()
    if not records:
        print("\n  Tracker is empty. Run the agent first or add applications manually.\n")
        return
    print(f"\n  {'ID':<10} {'Company':<24} {'Role':<28} {'Status':<22} {'Interview':<12}")
    print("  " + sep("-", 97))
    for r in records:
        print(
            f"  {r.get('application_id',''):<10} "
            f"{r.get('company','')[:22]:<24} "
            f"{r.get('role','')[:26]:<28} "
            f"{r.get('status','')[:20]:<22} "
            f"{r.get('interview_date',''):<12}"
        )
    print()


# ══════════════════════════════════════════════════════════════════════════════
#  UNIQUE FEATURE 5 — URGENCY-AWARE REMINDER ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def generate_reminders():
    """
    Build reminder text from tracker.
    Classifies each reminder as URGENT / UPCOMING / GENERAL.
    """
    records   = load_tracker()
    reminders = hdr("APPLICATION REMINDERS")
    reminders += f"Generated  : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    reminders += f"Today      : {TODAY.strftime('%A, %B %d, %Y')}\n\n"

    if not records:
        return reminders + "  No applications in tracker.\n"

    urgent   = []
    upcoming = []
    general  = []

    for row in records:
        app_id         = row.get("application_id", "")
        company        = row.get("company", "")
        role           = row.get("role", "")
        status         = row.get("status", "").strip().lower()
        interview_date = parse_date(row.get("interview_date", ""))
        follow_up_date = parse_date(row.get("follow_up_date", ""))
        next_action    = row.get("next_action", "N/A")

        if status in ("interview scheduled", "shortlisted"):
            if interview_date:
                days = (interview_date - TODAY).days
                if days < 0:
                    tag   = "🔴 OVERDUE"
                    entry = (f"  {tag}  — {app_id} | {company} | {role}\n"
                             f"    Interview was {interview_date} ({abs(days)} days ago). Update status.\n"
                             f"    Next action : {next_action}\n")
                    urgent.append(entry)
                elif days == 0:
                    tag   = "🔴 TODAY"
                    entry = (f"  {tag}    — {app_id} | {company} | {role}\n"
                             f"    Interview is TODAY ({interview_date}). Be prepared!\n"
                             f"    Next action : {next_action}\n")
                    urgent.append(entry)
                elif days <= 3:
                    tag   = "🟠 IN {d} DAYS".format(d=days)
                    entry = (f"  {tag} — {app_id} | {company} | {role}\n"
                             f"    Interview : {interview_date}  ({days} days away)\n"
                             f"    Next action : {next_action}\n")
                    urgent.append(entry)
                elif days <= 7:
                    entry = (f"  🟡 THIS WEEK — {app_id} | {company} | {role}\n"
                             f"    Interview : {interview_date}  ({days} days away)\n"
                             f"    Next action : {next_action}\n")
                    upcoming.append(entry)
                else:
                    entry = (f"  🟢 PLANNED   — {app_id} | {company} | {role}\n"
                             f"    Interview : {interview_date}  ({days} days away)\n"
                             f"    Next action : {next_action}\n")
                    general.append(entry)
            else:
                general.append(
                    f"  📅 {app_id} | {company} — Interview date not set. Confirm with recruiter.\n"
                )

        elif status == "applied":
            if follow_up_date:
                days = (follow_up_date - TODAY).days
                entry = (f"  📬 {app_id} | {company} | {role} — Application submitted.\n"
                         f"    Follow-up  : {follow_up_date}  ({days} days away)\n"
                         f"    Next action: {next_action}\n")
                if days <= 0:
                    urgent.append(entry)
                elif days <= 5:
                    upcoming.append(entry)
                else:
                    general.append(entry)
            else:
                general.append(f"  📬 {app_id} | {company} — Applied. Set a follow-up date.\n")

        elif status == "not applied":
            general.append(
                f"  📝 {app_id} | {company} | {role} — Not applied yet!\n"
                f"    Next action: {next_action}\n"
            )

        elif status == "rejected":
            general.append(
                f"  ❌ {app_id} | {company} | {role} — Rejected.\n"
                f"    Next action: {next_action}\n"
            )

        elif status == "offered":
            urgent.append(
                f"  🎉 OFFER RECEIVED — {app_id} | {company} | {role}\n"
                f"    Respond promptly! Review offer terms carefully.\n"
            )

    sections = [("🔴  URGENT — ACTION REQUIRED NOW", urgent),
                ("🟡  UPCOMING — THIS WEEK",          upcoming),
                ("🟢  GENERAL REMINDERS",             general)]

    for title, items in sections:
        if items:
            reminders += f"{title}\n" + sep("-", 48) + "\n"
            for item in items:
                reminders += item + "\n"

    return reminders


# ══════════════════════════════════════════════════════════════════════════════
#  FULL PIPELINE RUNNER
# ══════════════════════════════════════════════════════════════════════════════

def run_agent():
    """Execute the complete CareerPrep pipeline and save all output files."""
    print(hdr("CAREERPREP JOB-HUNTING AGENT — FULL RUN"))
    print("  Reading input files…\n")

    job_text,    job_count,    job_files    = read_text_files(JOB_DIR)
    resume_text, resume_count, resume_files = read_text_files(RESUME_DIR)
    kb_text,     kb_count,     kb_files     = read_text_files(KB_DIR)

    print(f"  Job files    : {job_count}  →  {job_files}")
    print(f"  Resume files : {resume_count}  →  {resume_files}")
    print(f"  KB files     : {kb_count}  →  {kb_files}\n")

    if job_count == 0 or resume_count == 0 or kb_count == 0:
        print("  ✘  Please add at least one .txt file to each input folder before running.\n")
        return

    # ── Extraction & analysis ──────────────────────────────────────────────
    job_skill_dict    = extract_skills(job_text)
    resume_skill_dict = extract_skills(resume_text)
    job_flat          = flatten(job_skill_dict)
    resume_flat       = flatten(resume_skill_dict)
    matched, missing, score = compare_skills(job_flat, resume_flat)
    quality           = resume_quality_score(resume_text, resume_flat)

    print(f"  Match Score    : {score}%")
    print(f"  Skills matched : {len(matched)}")
    print(f"  Skills missing : {len(missing)}")
    print(f"  Resume quality : {quality['scores']['Overall']}%\n")

    # ── Generate all reports ───────────────────────────────────────────────
    print("  Generating reports…")
    job_report         = generate_job_analysis(job_text, job_skill_dict, job_files)
    gap_report         = generate_skill_gap_report(job_skill_dict, resume_skill_dict, matched, missing, score)
    resume_suggestions = generate_resume_suggestions(job_skill_dict, missing, resume_text, quality)
    interview_qs       = generate_interview_questions(job_skill_dict, kb_text, job_text)
    project_map        = map_projects_to_jobs(resume_text, job_skill_dict)

    records     = load_tracker()
    company     = records[0]["company"] if records else "Target Company"
    role        = records[0]["role"]    if records else "Target Role"
    cover_letter = generate_cover_letter(company, role, resume_text, matched)
    reminders    = generate_reminders()

    final_report  = hdr("CAREERPREP FINAL REPORT")
    final_report += f"Generated on : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    final_report += f"Match Score  : {score}%  |  Matched: {len(matched)}  |  Gaps: {len(missing)}\n"
    final_report += f"Resume Score : {quality['scores']['Overall']}%\n"
    final_report += sep() + "\n\n"
    final_report += job_report + gap_report + resume_suggestions + interview_qs
    final_report += project_map + cover_letter + reminders

    # ── Save all outputs ───────────────────────────────────────────────────
    print("\n  Saving output files…")
    save_text(os.path.join(OUTPUT_DIR, "job_analysis_report.txt"),       job_report)
    save_text(os.path.join(OUTPUT_DIR, "skill_gap_report.txt"),          gap_report)
    save_text(os.path.join(OUTPUT_DIR, "tailored_resume_suggestions.txt"), resume_suggestions)
    save_text(os.path.join(OUTPUT_DIR, "interview_questions.txt"),       interview_qs)
    save_text(os.path.join(OUTPUT_DIR, "project_mapping.txt"),           project_map)
    save_text(os.path.join(OUTPUT_DIR, "cover_letter.txt"),              cover_letter)
    save_text(os.path.join(OUTPUT_DIR, "final_agent_report.txt"),        final_report)
    save_text(os.path.join(TRACKER_DIR, "reminders.txt"),                reminders)

    print(f"\n  ✔  All reports saved in '{OUTPUT_DIR}/' and '{TRACKER_DIR}/'")
    print("  ✔  Agent completed successfully.\n")


# ══════════════════════════════════════════════════════════════════════════════
#  UNIQUE FEATURE 1 — MENU-BASED CLI
# ══════════════════════════════════════════════════════════════════════════════

def print_banner():
    print("\n" + "═" * 62)
    print("   CareerPrep Job-Hunting Agent   v1.0")
    print("   File-Driven  •  AI-Powered  •  GitHub-Ready")
    print("═" * 62)


def main_menu():
    """Entry point: interactive menu for the agent."""
    ensure_folders()
    create_sample_tracker()
    print_banner()

    while True:
        print("\n  MAIN MENU")
        print("  " + sep("-", 44))
        print("  1.  Run Full Agent  (generate all reports)")
        print("  2.  View Application Tracker")
        print("  3.  Add New Application")
        print("  4.  View Reminders")
        print("  5.  Generate Cover Letter  (pick application)")
        print("  6.  Exit")
        print("  " + sep("-", 44))
        choice = input("  Enter choice [1–6]: ").strip()

        if choice == "1":
            run_agent()

        elif choice == "2":
            view_tracker()

        elif choice == "3":
            add_application()

        elif choice == "4":
            r = generate_reminders()
            print("\n" + r)
            save_text(os.path.join(TRACKER_DIR, "reminders.txt"), r)

        elif choice == "5":
            records = load_tracker()
            if not records:
                print("  No applications found. Add one first (option 3).")
                continue
            print("\n  Available applications:")
            for rec in records:
                print(f"    {rec['application_id']}: {rec['company']} — {rec['role']}")
            app_id = input("  Enter Application ID: ").strip().upper()
            rec = next((r for r in records if r["application_id"] == app_id), None)
            if not rec:
                print("  Application ID not found.")
                continue
            resume_text, _, _ = read_text_files(RESUME_DIR)
            resume_flat = flatten(extract_skills(resume_text))
            letter      = generate_cover_letter(rec["company"], rec["role"], resume_text, resume_flat)
            out_path    = os.path.join(OUTPUT_DIR, f"cover_letter_{app_id}.txt")
            save_text(out_path, letter)
            print(letter)

        elif choice == "6":
            print("\n  Goodbye! Good luck with your job search! 🚀\n")
            break

        else:
            print("  Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main_menu()
