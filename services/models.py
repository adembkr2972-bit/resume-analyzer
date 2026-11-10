from pydantic import BaseModel


class ResumeChange(BaseModel):
    section: str
    original: str
    improved: str
    reason: str
    ats_impact: int


# ===========================
# Resume Models
# ===========================

class ContactInfo(BaseModel):
    email: str
    phone: str
    location: str
    linkedin: str
    website: str = ""


class Experience(BaseModel):
    job_title: str
    company: str
    dates: str
    location: str = ""
    bullets: list[str]


class Education(BaseModel):
    degree: str
    school: str
    dates: str


class Project(BaseModel):
    title: str
    bullets: list[str]


class StructuredResume(BaseModel):

    name: str

    title: str

    summary: str

    contact: ContactInfo

    skills: list[str]

    experience: list[Experience]

    education: list[Education]

    projects: list[Project] = []

    certifications: list[str] = []

    languages: list[str] = []


# ===========================
# AI Response
# ===========================

class ResumeAnalysis(BaseModel):

    ats_score: int
    improved_score: int

    overall_rating: str

    strengths: list[str]

    weaknesses: list[str]

    missing_skills: list[str]

    keywords_missing: list[str]

    changes: list[ResumeChange]

    optimized_resume: StructuredResume

    cover_letter: str

    interview_questions: list[str]

    hiring_decision: str

    reason: str