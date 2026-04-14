"""
Job Recommendation System - Core Engine
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import math


# ─────────────────────────────────────────────
#  DATA STRUCTURES
# ─────────────────────────────────────────────

@dataclass
class Job:
    title: str
    domain: str
    required_skills: List[str]
    nice_to_have: List[str]
    experience_level: str          # "fresher" | "mid" | "senior"
    salary_range: Tuple[int, int]  # in LPA (lakhs per annum)
    description: str
    growth_path: str


@dataclass
class RecommendationResult:
    job: Job
    match_score: float             # 0–100
    matched_required: List[str]
    matched_nice: List[str]
    missing_skills: List[str]
    experience_match: bool


# ─────────────────────────────────────────────
#  JOB DATABASE  (30 jobs across 8 domains)
# ─────────────────────────────────────────────

JOB_DATABASE: List[Job] = [

    # ── TECHNOLOGY ──────────────────────────────
    Job(
        title="Software Engineer",
        domain="Technology",
        required_skills=["python", "data structures", "algorithms", "git"],
        nice_to_have=["java", "docker", "system design", "rest api"],
        experience_level="fresher",
        salary_range=(6, 14),
        description="Build and maintain scalable software systems. Work on backend services, APIs, and internal tooling.",
        growth_path="Senior SWE → Tech Lead → Engineering Manager",
    ),
    Job(
        title="Senior Software Engineer",
        domain="Technology",
        required_skills=["python", "system design", "rest api", "docker", "sql"],
        nice_to_have=["kubernetes", "microservices", "aws", "ci/cd"],
        experience_level="senior",
        salary_range=(20, 45),
        description="Lead feature development, mentor junior devs, drive architecture decisions.",
        growth_path="Staff Engineer → Principal Engineer → CTO",
    ),
    Job(
        title="DevOps Engineer",
        domain="Technology",
        required_skills=["docker", "kubernetes", "linux", "ci/cd", "git"],
        nice_to_have=["aws", "terraform", "ansible", "python", "monitoring"],
        experience_level="mid",
        salary_range=(12, 28),
        description="Automate deployment pipelines, manage cloud infrastructure, ensure system reliability.",
        growth_path="Senior DevOps → Site Reliability Engineer → Infrastructure Architect",
    ),
    Job(
        title="Mobile Developer (Android)",
        domain="Technology",
        required_skills=["java", "android", "kotlin", "rest api"],
        nice_to_have=["firebase", "git", "ui/ux", "room database"],
        experience_level="fresher",
        salary_range=(5, 13),
        description="Develop Android applications, integrate APIs, optimise performance.",
        growth_path="Senior Android Dev → Mobile Architect → Product Manager",
    ),
    Job(
        title="Mobile Developer (iOS)",
        domain="Technology",
        required_skills=["swift", "xcode", "rest api", "git"],
        nice_to_have=["objective-c", "core data", "swiftui", "firebase"],
        experience_level="fresher",
        salary_range=(6, 14),
        description="Build iPhone/iPad apps, work with Apple APIs, publish to App Store.",
        growth_path="Senior iOS Dev → Mobile Lead → Tech Lead",
    ),
    Job(
        title="Embedded Systems Engineer",
        domain="Technology",
        required_skills=["c", "c++", "microcontrollers", "rtos"],
        nice_to_have=["python", "linux", "arm", "can bus"],
        experience_level="mid",
        salary_range=(8, 20),
        description="Programme firmware for IoT devices, automotive systems, and industrial hardware.",
        growth_path="Senior Embedded → Hardware Architect → CTO (Hardware)",
    ),

    # ── DATA & AI ────────────────────────────────
    Job(
        title="Data Scientist",
        domain="Data & AI",
        required_skills=["python", "machine learning", "statistics", "pandas", "numpy"],
        nice_to_have=["deep learning", "sql", "tableau", "scikit-learn", "r"],
        experience_level="mid",
        salary_range=(10, 25),
        description="Build predictive models, perform A/B tests, extract actionable insights from data.",
        growth_path="Senior Data Scientist → Lead DS → Head of Data",
    ),
    Job(
        title="Machine Learning Engineer",
        domain="Data & AI",
        required_skills=["python", "machine learning", "deep learning", "tensorflow", "docker"],
        nice_to_have=["mlops", "kubernetes", "aws", "spark", "feature engineering"],
        experience_level="mid",
        salary_range=(15, 35),
        description="Deploy and scale ML models to production, optimise inference pipelines.",
        growth_path="Senior MLE → ML Architect → Head of ML",
    ),
    Job(
        title="AI Engineer",
        domain="Data & AI",
        required_skills=["python", "deep learning", "nlp", "transformers", "pytorch"],
        nice_to_have=["llm", "langchain", "vector databases", "rag", "mlops"],
        experience_level="mid",
        salary_range=(18, 40),
        description="Design and productionise AI systems, LLM-powered apps, and agentic workflows.",
        growth_path="Senior AI Engineer → AI Research Scientist → AI Architect",
    ),
    Job(
        title="Data Analyst",
        domain="Data & AI",
        required_skills=["sql", "excel", "data visualisation", "statistics"],
        nice_to_have=["python", "tableau", "power bi", "pandas", "r"],
        experience_level="fresher",
        salary_range=(4, 10),
        description="Analyse business data, create dashboards and reports for stakeholders.",
        growth_path="Senior Analyst → Analytics Manager → Head of Analytics",
    ),
    Job(
        title="Data Engineer",
        domain="Data & AI",
        required_skills=["python", "sql", "spark", "etl", "data warehousing"],
        nice_to_have=["airflow", "kafka", "aws", "dbt", "snowflake"],
        experience_level="mid",
        salary_range=(12, 28),
        description="Build and maintain data pipelines, warehouses, and streaming infrastructure.",
        growth_path="Senior DE → Data Architect → Head of Data Engineering",
    ),
    Job(
        title="NLP Engineer",
        domain="Data & AI",
        required_skills=["python", "nlp", "transformers", "pytorch", "text processing"],
        nice_to_have=["llm", "hugging face", "spacy", "bert", "summarisation"],
        experience_level="mid",
        salary_range=(14, 32),
        description="Build natural language processing models for chatbots, search, and text analytics.",
        growth_path="Senior NLP → Research Scientist → AI Research Lead",
    ),

    # ── WEB DEVELOPMENT ──────────────────────────
    Job(
        title="Frontend Developer",
        domain="Web Development",
        required_skills=["html", "css", "javascript", "react"],
        nice_to_have=["typescript", "tailwind css", "next.js", "git", "figma"],
        experience_level="fresher",
        salary_range=(4, 12),
        description="Build responsive web UIs, implement designs, ensure cross-browser compatibility.",
        growth_path="Senior Frontend → UI Tech Lead → Frontend Architect",
    ),
    Job(
        title="Backend Developer",
        domain="Web Development",
        required_skills=["python", "rest api", "sql", "git"],
        nice_to_have=["django", "fastapi", "docker", "redis", "postgresql"],
        experience_level="fresher",
        salary_range=(5, 14),
        description="Develop server-side logic, APIs, and database schemas.",
        growth_path="Senior Backend → Backend Architect → CTO",
    ),
    Job(
        title="Full Stack Developer",
        domain="Web Development",
        required_skills=["html", "css", "javascript", "python", "sql", "git"],
        nice_to_have=["react", "node.js", "docker", "aws", "rest api"],
        experience_level="mid",
        salary_range=(8, 22),
        description="Build end-to-end web features covering frontend, backend, and database.",
        growth_path="Senior Fullstack → Tech Lead → CTO",
    ),

    # ── DESIGN ───────────────────────────────────
    Job(
        title="UI/UX Designer",
        domain="Design",
        required_skills=["figma", "ui/ux", "wireframing", "user research"],
        nice_to_have=["adobe xd", "prototyping", "css", "html", "usability testing"],
        experience_level="fresher",
        salary_range=(4, 10),
        description="Design intuitive digital interfaces, create wireframes and prototypes, conduct user research.",
        growth_path="Senior Designer → Design Lead → Head of Design / CPO",
    ),
    Job(
        title="Product Designer",
        domain="Design",
        required_skills=["figma", "ui/ux", "prototyping", "user research", "design systems"],
        nice_to_have=["motion design", "accessibility", "data driven design", "agile"],
        experience_level="mid",
        salary_range=(10, 24),
        description="Own the end-to-end design process for products from discovery to launch.",
        growth_path="Principal Designer → Head of Design → CPO",
    ),

    # ── FINANCE ──────────────────────────────────
    Job(
        title="Financial Analyst",
        domain="Finance",
        required_skills=["excel", "financial modelling", "accounting", "statistics"],
        nice_to_have=["python", "sql", "power bi", "valuation", "bloomberg terminal"],
        experience_level="fresher",
        salary_range=(5, 12),
        description="Analyse financial data, build models, and support investment or business decisions.",
        growth_path="Senior Analyst → Finance Manager → CFO",
    ),
    Job(
        title="Quantitative Analyst",
        domain="Finance",
        required_skills=["python", "statistics", "mathematics", "financial modelling", "r"],
        nice_to_have=["machine learning", "sql", "c++", "derivatives pricing", "risk management"],
        experience_level="senior",
        salary_range=(25, 60),
        description="Build mathematical models for trading strategies, risk management, and pricing.",
        growth_path="Senior Quant → Quant Researcher → Head of Quant",
    ),
    Job(
        title="Risk Analyst",
        domain="Finance",
        required_skills=["statistics", "excel", "risk management", "financial modelling"],
        nice_to_have=["python", "sql", "r", "var", "basel iii"],
        experience_level="mid",
        salary_range=(8, 18),
        description="Identify and assess financial risks, build risk models, ensure regulatory compliance.",
        growth_path="Senior Risk Analyst → Risk Manager → Chief Risk Officer",
    ),

    # ── MARKETING ────────────────────────────────
    Job(
        title="Digital Marketing Analyst",
        domain="Marketing",
        required_skills=["google analytics", "seo", "social media marketing", "excel"],
        nice_to_have=["python", "sql", "google ads", "content marketing", "a/b testing"],
        experience_level="fresher",
        salary_range=(3, 8),
        description="Analyse marketing campaigns, track KPIs, run SEO and paid media strategy.",
        growth_path="Senior Analyst → Marketing Manager → CMO",
    ),
    Job(
        title="Growth Hacker",
        domain="Marketing",
        required_skills=["a/b testing", "google analytics", "seo", "data analysis", "python"],
        nice_to_have=["sql", "product analytics", "retention", "email marketing", "funnel optimisation"],
        experience_level="mid",
        salary_range=(8, 20),
        description="Drive user acquisition and retention through data-driven experiments at scale.",
        growth_path="Head of Growth → VP Marketing → CMO",
    ),

    # ── HEALTHCARE & BIOTECH ──────────────────────
    Job(
        title="Bioinformatics Analyst",
        domain="Healthcare & Biotech",
        required_skills=["python", "r", "bioinformatics", "statistics", "linux"],
        nice_to_have=["machine learning", "sql", "genomics", "biopython", "nextflow"],
        experience_level="mid",
        salary_range=(8, 20),
        description="Analyse genomic and clinical datasets to support drug discovery and precision medicine.",
        growth_path="Senior Bioinformatician → Computational Biology Lead → Research Director",
    ),
    Job(
        title="Health Data Scientist",
        domain="Healthcare & Biotech",
        required_skills=["python", "machine learning", "statistics", "sql", "data visualisation"],
        nice_to_have=["r", "nlp", "ehr systems", "clinical trials", "tableau"],
        experience_level="mid",
        salary_range=(10, 22),
        description="Apply ML to healthcare data—clinical records, imaging, genomics—to improve patient outcomes.",
        growth_path="Senior HDS → Head of Clinical AI → Chief Medical Data Officer",
    ),

    # ── LEGAL & COMPLIANCE ────────────────────────
    Job(
        title="Legal Tech Analyst",
        domain="Legal & Compliance",
        required_skills=["legal research", "microsoft office", "contract review", "compliance"],
        nice_to_have=["python", "nlp", "e-discovery tools", "legaltech platforms", "data analysis"],
        experience_level="fresher",
        salary_range=(5, 12),
        description="Assist with contract analysis, legal research, and compliance monitoring using technology.",
        growth_path="Senior Legal Analyst → Legal Manager → General Counsel",
    ),

    # ── OPERATIONS ────────────────────────────────
    Job(
        title="Business Analyst",
        domain="Operations",
        required_skills=["excel", "sql", "business analysis", "requirements gathering", "data visualisation"],
        nice_to_have=["python", "power bi", "agile", "process mapping", "tableau"],
        experience_level="fresher",
        salary_range=(4, 10),
        description="Bridge the gap between business needs and technical solutions; write requirements, analyse processes.",
        growth_path="Senior BA → Product Manager → Director of Product",
    ),
    Job(
        title="Product Manager",
        domain="Operations",
        required_skills=["product strategy", "agile", "user research", "data analysis", "stakeholder management"],
        nice_to_have=["sql", "a/b testing", "figma", "roadmapping", "go to market"],
        experience_level="mid",
        salary_range=(12, 30),
        description="Own product vision and roadmap, prioritise features, work with engineering and design.",
        growth_path="Senior PM → Group PM → CPO",
    ),
    Job(
        title="Supply Chain Analyst",
        domain="Operations",
        required_skills=["excel", "sql", "supply chain management", "data analysis", "logistics"],
        nice_to_have=["python", "erp systems", "power bi", "forecasting", "inventory management"],
        experience_level="fresher",
        salary_range=(4, 9),
        description="Analyse supply chain data, optimise inventory levels, track supplier KPIs.",
        growth_path="Senior SC Analyst → Supply Chain Manager → VP Operations",
    ),
    Job(
        title="Cybersecurity Analyst",
        domain="Technology",
        required_skills=["networking", "linux", "cybersecurity", "firewalls", "siem"],
        nice_to_have=["python", "ethical hacking", "penetration testing", "splunk", "incident response"],
        experience_level="mid",
        salary_range=(10, 25),
        description="Monitor, detect and respond to security threats, conduct vulnerability assessments.",
        growth_path="Senior Security Analyst → Security Architect → CISO",
    ),
    Job(
        title="Cloud Architect",
        domain="Technology",
        required_skills=["aws", "system design", "docker", "kubernetes", "terraform"],
        nice_to_have=["azure", "gcp", "networking", "security", "cost optimisation"],
        experience_level="senior",
        salary_range=(25, 55),
        description="Design and govern cloud infrastructure for large-scale distributed systems.",
        growth_path="Principal Cloud Architect → VP Engineering → CTO",
    ),
]


# ─────────────────────────────────────────────
#  RECOMMENDATION ENGINE
# ─────────────────────────────────────────────

EXPERIENCE_MAP = {
    "fresher": 0,
    "mid": 1,
    "senior": 2,
}

EXPERIENCE_LABELS = {
    "fresher": "0–2 years",
    "mid": "2–5 years",
    "senior": "5+ years",
}


def _compute_score(job: Job, user_skills: List[str]) -> float:
    """
    Weighted match score (0–100).
    Required skills carry 70% weight, nice-to-have 30%.
    Within each group we use a TF-IDF-inspired rarity bonus:
    rarer skills (fewer jobs require them) are worth more.
    """
    skill_frequency: Dict[str, int] = {}
    for j in JOB_DATABASE:
        for s in j.required_skills + j.nice_to_have:
            skill_frequency[s] = skill_frequency.get(s, 0) + 1

    def idf(skill: str) -> float:
        freq = skill_frequency.get(skill, 1)
        return math.log(len(JOB_DATABASE) / freq + 1)

    def weighted_match(pool: List[str]) -> Tuple[float, float]:
        total_weight = sum(idf(s) for s in pool) or 1
        matched_weight = sum(idf(s) for s in pool if s in user_skills)
        return matched_weight, total_weight

    req_matched, req_total = weighted_match(job.required_skills)
    nice_matched, nice_total = weighted_match(job.nice_to_have)

    req_score = (req_matched / req_total) * 70 if req_total else 0
    nice_score = (nice_matched / nice_total) * 30 if nice_total else 0

    return round(req_score + nice_score, 2)


def recommend(
    user_skills_raw: List[str],
    experience_level: str = "fresher",
    preferred_domains: List[str] = None,
    top_n: int = 5,
    min_score: float = 10.0,
) -> List[RecommendationResult]:
    """
    Returns top_n job recommendations sorted by match score.

    Parameters
    ----------
    user_skills_raw    : list of skills as entered by the user
    experience_level   : "fresher" | "mid" | "senior"
    preferred_domains  : optional filter (e.g. ["Data & AI", "Technology"])
    top_n              : number of results to return
    min_score          : minimum score threshold (0–100)
    """
    user_skills = [s.strip().lower() for s in user_skills_raw]
    user_exp = EXPERIENCE_MAP.get(experience_level, 0)

    results: List[RecommendationResult] = []

    for job in JOB_DATABASE:
        # Domain filter
        if preferred_domains and job.domain not in preferred_domains:
            continue

        score = _compute_score(job, user_skills)
        if score < min_score:
            continue

        job_exp = EXPERIENCE_MAP.get(job.experience_level, 0)
        exp_match = abs(user_exp - job_exp) <= 1  # adjacent levels are fine

        matched_req = [s for s in job.required_skills if s in user_skills]
        matched_nice = [s for s in job.nice_to_have if s in user_skills]
        missing = [s for s in job.required_skills if s not in user_skills]

        results.append(RecommendationResult(
            job=job,
            match_score=score,
            matched_required=matched_req,
            matched_nice=matched_nice,
            missing_skills=missing,
            experience_match=exp_match,
        ))

    results.sort(key=lambda r: (r.match_score, r.experience_match), reverse=True)
    return results[:top_n]


def get_all_domains() -> List[str]:
    return sorted(set(j.domain for j in JOB_DATABASE))


def get_all_skills() -> List[str]:
    skills = set()
    for j in JOB_DATABASE:
        skills.update(j.required_skills)
        skills.update(j.nice_to_have)
    return sorted(skills)
