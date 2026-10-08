from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UpdateMarksRequest(BaseModel):
    internal_marks: Optional[float] = None
    assignment_marks: Optional[float] = None
    final_exam_marks: Optional[float] = None
    grade: Optional[str] = None

class UpdateAttendanceRequest(BaseModel):
    classes_attended: int
    total_classes: int

class FacultyRemarkCreate(BaseModel):
    student_id: int
    subject_id: Optional[int] = None
    remark: str

class FacultyRemarkResponse(BaseModel):
    id: int
    student_id: int
    student_name: Optional[str] = None
    subject_name: Optional[str] = None
    remark: str
    created_at: datetime

    class Config:
        from_attributes = True

class FacultyProfileResponse(BaseModel):
    id: int
    user_id: int
    name: str
    email: str
    employee_id: str
    department: str
    designation: str

    class Config:
        from_attributes = True
