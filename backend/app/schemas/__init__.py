from app.schemas.auth import LoginRequest, TokenResponse, UserRegisterRequest, UserResponse
from app.schemas.student import StudentProfileResponse, SkillCreate, ProjectCreate, CertificationCreate
from app.schemas.faculty import UpdateMarksRequest, UpdateAttendanceRequest, FacultyRemarkCreate, FacultyRemarkResponse, FacultyProfileResponse
from app.schemas.academic import SubjectResponse, AcademicRecordResponse, SubjectPerformanceSummary
from app.schemas.ml_ai import (
    RiskPredictionRequest, RiskPredictionResponse,
    PlacementReadinessResponse, WhatIfRequest, WhatIfResponse,
    ChatQueryRequest, ChatQueryResponse
)

__all__ = [
    "LoginRequest", "TokenResponse", "UserRegisterRequest", "UserResponse",
    "StudentProfileResponse", "SkillCreate", "ProjectCreate", "CertificationCreate",
    "UpdateMarksRequest", "UpdateAttendanceRequest", "FacultyRemarkCreate", "FacultyRemarkResponse", "FacultyProfileResponse",
    "SubjectResponse", "AcademicRecordResponse", "SubjectPerformanceSummary",
    "RiskPredictionRequest", "RiskPredictionResponse",
    "PlacementReadinessResponse", "WhatIfRequest", "WhatIfResponse",
    "ChatQueryRequest", "ChatQueryResponse"
]
