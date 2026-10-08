from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database import get_db
from app.api.auth import get_current_user, require_role
from app.models.user import User
from app.models.academic import AcademicRecord
from app.schemas.ml_ai import WhatIfRequest, WhatIfResponse
from app.services.simulator_engine import simulator_engine

router = APIRouter(prefix="/simulator", tags=["What-If Academic Simulator"])

@router.post("/simulate", response_model=WhatIfResponse)
def simulate_academic_trajectory(
    payload: WhatIfRequest,
    current_user: User = Depends(require_role(["student", "admin"])),
    db: Session = Depends(get_db)
):
    student = current_user.student_profile
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    records = db.query(AcademicRecord).filter(AcademicRecord.student_id == student.id).all()
    current_attended = sum(r.classes_attended for r in records)
    current_total = sum(r.total_classes for r in records)

    subjects_payload = []
    if payload.expected_subject_marks:
        for s in payload.expected_subject_marks:
            # Look up credits from record
            matched = next((r for r in records if r.subject_id == s.subject_id), None)
            credits = matched.subject.credits if (matched and matched.subject) else 3
            subjects_payload.append({
                "subject_id": s.subject_id,
                "credits": credits,
                "expected_marks": s.expected_marks
            })

    result = simulator_engine.simulate(
        current_cgpa=student.cgpa,
        current_semester=student.semester,
        subjects_with_credits_and_expected_marks=subjects_payload,
        target_cgpa=payload.target_cgpa,
        current_attendance_attended=current_attended,
        current_attendance_total=current_total,
        additional_classes_attended=payload.additional_classes_to_attend,
        additional_classes_total=payload.total_additional_classes
    )

    return WhatIfResponse(
        projected_sgpa=result.get("projected_sgpa"),
        projected_cgpa=result.get("projected_cgpa"),
        projected_attendance_pct=result.get("projected_attendance_pct"),
        required_sgpa_for_target=result.get("required_sgpa_for_target"),
        feasibility_message=result.get("feasibility_message", "")
    )
