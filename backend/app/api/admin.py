from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any

from app.core.database import get_db
from app.api.auth import get_current_user, require_role
from app.models.user import User
from app.models.student import Student
from app.models.faculty import Faculty
from app.models.academic import Subject, AcademicRecord
from app.models.placement import PlacementProfile
from app.services.risk_engine import risk_engine

router = APIRouter(prefix="/admin", tags=["Admin & HOD"])

@router.get("/overview")
def get_admin_overview(
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    total_students = db.query(Student).count()
    total_faculty = db.query(Faculty).count()
    total_subjects = db.query(Subject).count()

    students = db.query(Student).all()
    if not students:
        return {
            "total_students": 0,
            "total_faculty": total_faculty,
            "average_cgpa": 0.0,
            "high_risk_count": 0,
            "medium_risk_count": 0,
            "low_risk_count": 0,
            "average_attendance": 0.0,
            "average_placement_readiness": 0.0
        }

    total_cgpa = sum(s.cgpa for s in students)
    avg_cgpa = round(total_cgpa / len(students), 2)

    # Risk distribution & Placement average
    high_risk_count = 0
    med_risk_count = 0
    low_risk_count = 0
    total_readiness = 0.0
    students_with_placement = 0

    for s in students:
        # Determine risk tag
        if s.backlogs >= 2 or s.cgpa < 6.0:
            high_risk_count += 1
        elif s.backlogs == 1 or s.cgpa < 7.0:
            med_risk_count += 1
        else:
            low_risk_count += 1

        if s.placement_profile:
            total_readiness += s.placement_profile.readiness_score
            students_with_placement += 1

    avg_readiness = round(total_readiness / max(students_with_placement, 1), 1)

    # Overall attendance average across all academic records
    records = db.query(AcademicRecord).all()
    total_att_pct = sum(r.attendance_percentage for r in records)
    avg_attendance = round(total_att_pct / max(len(records), 1), 1)

    return {
        "total_students": total_students,
        "total_faculty": total_faculty,
        "total_subjects": total_subjects,
        "average_cgpa": avg_cgpa,
        "college_attendance_average": avg_attendance,
        "risk_breakdown": {
            "high": high_risk_count,
            "medium": med_risk_count,
            "low": low_risk_count
        },
        "average_placement_readiness": avg_readiness
    }

@router.get("/students")
def get_all_students(
    current_user: User = Depends(require_role(["admin", "faculty"])),
    db: Session = Depends(get_db)
):
    students = db.query(Student).all()
    results = []
    for s in students:
        records = db.query(AcademicRecord).filter(AcademicRecord.student_id == s.id).all()
        att = round(sum(r.classes_attended for r in records) / max(sum(r.total_classes for r in records), 1) * 100.0, 1)
        
        # Risk estimation
        risk = "LOW"
        if att < 65.0 or s.backlogs >= 2 or s.cgpa < 6.0:
            risk = "HIGH"
        elif att < 75.0 or s.backlogs == 1 or s.cgpa < 7.0:
            risk = "MEDIUM"

        readiness = s.placement_profile.readiness_score if s.placement_profile else 65.0

        results.append({
            "id": s.id,
            "name": s.user.name if s.user else "Student",
            "email": s.user.email if s.user else "",
            "roll_number": s.roll_number,
            "department": s.department,
            "year": s.year,
            "semester": s.semester,
            "section": s.section,
            "cgpa": s.cgpa,
            "backlogs": s.backlogs,
            "attendance_percentage": att,
            "risk_level": risk,
            "placement_readiness": readiness
        })

    return results

@router.get("/departments")
def get_department_analytics(
    current_user: User = Depends(require_role(["admin"])),
    db: Session = Depends(get_db)
):
    departments = ["Computer Science & Engineering", "Information Technology", "Electronics & Communication"]
    data = []
    for dept in departments:
        students = db.query(Student).filter(Student.department == dept).all()
        if not students:
            continue
        avg_cgpa = round(sum(s.cgpa for s in students) / len(students), 2)
        total_backlogs = sum(s.backlogs for s in students)
        high_risk = sum(1 for s in students if s.backlogs >= 2 or s.cgpa < 6.0)
        data.append({
            "department": dept,
            "student_count": len(students),
            "average_cgpa": avg_cgpa,
            "total_backlogs": total_backlogs,
            "high_risk_count": high_risk
        })
    return data
