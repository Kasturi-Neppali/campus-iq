from app.core.database import Base
from app.models.user import User
from app.models.student import Student, StudentSkill, StudentProject, StudentCertification
from app.models.faculty import Faculty, FacultyRemark
from app.models.academic import Subject, AcademicRecord
from app.models.placement import PlacementProfile
from app.models.risk import RiskAssessment

__all__ = [
    "Base",
    "User",
    "Student",
    "StudentSkill",
    "StudentProject",
    "StudentCertification",
    "Faculty",
    "FacultyRemark",
    "Subject",
    "AcademicRecord",
    "PlacementProfile",
    "RiskAssessment"
]
