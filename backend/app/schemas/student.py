from pydantic import BaseModel
from typing import Optional, List

class SkillCreate(BaseModel):
    skill_name: str
    proficiency: str = "Intermediate"

class SkillResponse(BaseModel):
    id: int
    skill_name: str
    proficiency: str

    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    tech_stack: Optional[str] = None
    github_link: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    tech_stack: Optional[str] = None
    github_link: Optional[str] = None

    class Config:
        from_attributes = True

class CertificationCreate(BaseModel):
    title: str
    issuer: str
    issue_date: Optional[str] = None
    credential_url: Optional[str] = None

class CertificationResponse(BaseModel):
    id: int
    title: str
    issuer: str
    issue_date: Optional[str] = None
    credential_url: Optional[str] = None

    class Config:
        from_attributes = True

class StudentProfileResponse(BaseModel):
    id: int
    user_id: int
    name: str
    email: str
    roll_number: str
    department: str
    year: int
    semester: int
    section: str
    cgpa: float
    backlogs: int
    phone: Optional[str] = None
    skills: List[SkillResponse] = []
    projects: List[ProjectResponse] = []
    certifications: List[CertificationResponse] = []

    class Config:
        from_attributes = True
