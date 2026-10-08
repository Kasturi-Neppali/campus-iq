from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database import get_db
from app.api.auth import get_current_user, require_role
from app.models.user import User
from app.models.placement import PlacementProfile
from app.schemas.ml_ai import PlacementReadinessResponse
from app.services.placement_engine import placement_engine

router = APIRouter(prefix="/placement", tags=["Placement Readiness"])

@router.get("/readiness", response_model=PlacementReadinessResponse)
def get_placement_readiness(
    current_user: User = Depends(require_role(["student", "admin"])),
    db: Session = Depends(get_db)
):
    student = current_user.student_profile
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    p = student.placement_profile
    dsa = p.dsa_score if p else 70.0
    prog = p.programming_score if p else 75.0
    apt = p.aptitude_score if p else 65.0
    comm = p.communication_score if p else 70.0
    leetcode = p.leetcode_solved if p else 120

    res = placement_engine.calculate_readiness(
        cgpa=student.cgpa,
        dsa_score=dsa,
        programming_score=prog,
        aptitude_score=apt,
        communication_score=comm,
        projects_count=len(student.projects),
        certifications_count=len(student.certifications),
        leetcode_solved=leetcode
    )
    return PlacementReadinessResponse(**res)
