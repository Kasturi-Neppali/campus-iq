from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class RiskPredictionRequest(BaseModel):
    attendance_pct: float
    internal_pct: float
    assignment_pct: float
    previous_cgpa: float
    backlogs: int

class RiskPredictionResponse(BaseModel):
    risk_level: str  # "LOW", "MEDIUM", "HIGH"
    risk_score: float # 0.0 - 100.0 probability
    contributing_factors: List[str]
    recommendations: List[str]

class PlacementReadinessResponse(BaseModel):
    overall_readiness: float
    dsa_score: float
    programming_score: float
    aptitude_score: float
    communication_score: float
    projects_score: float
    certifications_score: float
    leetcode_solved: int
    areas_to_improve: List[str]
    readiness_tier: str  # "Placement Ready", "Needs Polish", "High Priority Up-skilling Required"
    disclaimer: str = "This metric is an internal preparation indicator for self-evaluation and not an official placement guarantee."

class SubjectExpectation(BaseModel):
    subject_id: int
    subject_name: str
    expected_marks: float  # out of 100

class WhatIfRequest(BaseModel):
    expected_subject_marks: Optional[List[SubjectExpectation]] = None
    target_cgpa: Optional[float] = None
    additional_classes_to_attend: Optional[int] = None
    total_additional_classes: Optional[int] = None

class WhatIfResponse(BaseModel):
    projected_sgpa: Optional[float] = None
    projected_cgpa: Optional[float] = None
    projected_attendance_pct: Optional[float] = None
    required_sgpa_for_target: Optional[float] = None
    feasibility_message: str

class ChatMessage(BaseModel):
    sender: str  # "user" or "assistant"
    text: str

class ChatQueryRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

class ChatQueryResponse(BaseModel):
    reply: str
    student_context_applied: bool
    context_summary: Optional[Dict[str, Any]] = None
