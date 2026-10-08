from pydantic import BaseModel
from typing import Optional, List

class SubjectBase(BaseModel):
    name: str
    code: str
    department: str
    semester: int
    credits: int

class SubjectResponse(SubjectBase):
    id: int
    faculty_id: Optional[int] = None
    faculty_name: Optional[str] = None

    class Config:
        from_attributes = True

class AcademicRecordResponse(BaseModel):
    id: int
    student_id: int
    subject_id: int
    subject_name: str
    subject_code: str
    credits: int
    semester: int
    classes_attended: int
    total_classes: int
    attendance_percentage: float
    internal_marks: float
    assignment_marks: float
    final_exam_marks: float
    grade: str
    total_score_percentage: float

    class Config:
        from_attributes = True

class SubjectPerformanceSummary(BaseModel):
    subject_id: int
    subject_name: str
    subject_code: str
    credits: int
    internal_percentage: float
    attendance_percentage: float
    status: str  # "Strong", "Average", "Critical"
