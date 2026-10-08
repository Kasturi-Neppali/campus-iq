from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database import get_db
from app.api.auth import get_current_user, require_role
from app.models.user import User
from app.models.academic import AcademicRecord
from app.schemas.ml_ai import ChatQueryRequest, ChatQueryResponse
from app.services.ai_engine import ai_engine
from app.services.risk_engine import risk_engine
from app.services.placement_engine import placement_engine

router = APIRouter(prefix="/ai", tags=["CampusAI Assistant"])

@router.post("/chat", response_model=ChatQueryResponse)
def chat_with_campus_ai(
    payload: ChatQueryRequest,
    current_user: User = Depends(require_role(["student", "faculty", "admin"])),
    db: Session = Depends(get_db)
):
    student = current_user.student_profile
    student_context: Dict[str, Any] = {
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }

    if student:
        records = db.query(AcademicRecord).filter(AcademicRecord.student_id == student.id).all()
        total_att = sum(r.classes_attended for r in records)
        total_cls = sum(r.total_classes for r in records)
        overall_attendance = round((total_att / total_cls * 100.0), 2) if total_cls > 0 else 0.0

        subjects_summary = []
        for r in records:
            sub_name = r.subject.name if r.subject else "Subject"
            subjects_summary.append({
                "name": sub_name,
                "attendance_percentage": r.attendance_percentage,
                "internal_percentage": round((r.internal_marks / 50.0) * 100.0, 1)
            })

        # Calculate risk and placement metrics
        risk_res = risk_engine.predict_risk(
            attendance_pct=overall_attendance,
            internal_pct=round(sum(s["internal_percentage"] for s in subjects_summary) / max(len(subjects_summary), 1), 1),
            assignment_pct=75.0,
            previous_cgpa=student.cgpa,
            backlogs=student.backlogs
        )

        p = student.placement_profile
        placement_res = placement_engine.calculate_readiness(
            cgpa=student.cgpa,
            dsa_score=p.dsa_score if p else 70.0,
            programming_score=p.programming_score if p else 75.0,
            aptitude_score=p.aptitude_score if p else 65.0,
            communication_score=p.communication_score if p else 70.0,
            projects_count=len(student.projects),
            certifications_count=len(student.certifications),
            leetcode_solved=p.leetcode_solved if p else 120
        )

        student_context.update({
            "roll_number": student.roll_number,
            "department": student.department,
            "semester": student.semester,
            "cgpa": student.cgpa,
            "backlogs": student.backlogs,
            "overall_attendance": overall_attendance,
            "subjects": subjects_summary,
            "risk_level": risk_res["risk_level"],
            "contributing_factors": risk_res["contributing_factors"],
            "recommendations": risk_res["recommendations"],
            "placement_readiness": placement_res["overall_readiness"],
            "dsa_score": placement_res["dsa_score"],
            "programming_score": placement_res["programming_score"],
            "aptitude_score": placement_res["aptitude_score"],
            "communication_score": placement_res["communication_score"],
            "projects_count": len(student.projects),
            "areas_to_improve": placement_res["areas_to_improve"]
        })

    conv_history = [{"sender": msg.sender, "text": msg.text} for msg in (payload.history or [])]
    ai_result = ai_engine.ask(
        student_context=student_context,
        user_message=payload.message,
        conversation_history=conv_history
    )

    return ChatQueryResponse(
        reply=ai_result["reply"],
        student_context_applied=ai_result["student_context_applied"],
        context_summary=ai_result.get("context_summary")
    )
