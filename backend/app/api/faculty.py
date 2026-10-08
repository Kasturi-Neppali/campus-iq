from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.core.database import get_db
from app.api.auth import get_current_user, require_role
from app.models.user import User
from app.models.faculty import Faculty, FacultyRemark
from app.models.student import Student
from app.models.academic import Subject, AcademicRecord
from app.schemas.faculty import UpdateMarksRequest, UpdateAttendanceRequest, FacultyRemarkCreate
from app.services.risk_engine import risk_engine

router = APIRouter(prefix="/faculty", tags=["Faculty"])

def _get_faculty(current_user: User, db: Session) -> Faculty:
    faculty = current_user.faculty_profile
    if not faculty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Faculty profile not found for this user")
    return faculty

@router.get("/dashboard")
def get_faculty_dashboard(
    current_user: User = Depends(require_role(["faculty", "admin"])),
    db: Session = Depends(get_db)
):
    faculty = _get_faculty(current_user, db)
    subjects = db.query(Subject).filter(Subject.faculty_id == faculty.id).all()
    subject_ids = [s.id for s in subjects]

    # Gather records across all taught subjects
    records = db.query(AcademicRecord).filter(AcademicRecord.subject_id.in_(subject_ids)).all() if subject_ids else []

    total_records = len(records)
    total_attendance = 0.0
    total_internal = 0.0
    low_attendance_count = 0
    low_marks_count = 0
    at_risk_students_set = set()

    for r in records:
        att = r.attendance_percentage
        int_pct = (r.internal_marks / 50.0) * 100.0
        total_attendance += att
        total_internal += int_pct

        if att < 75.0:
            low_attendance_count += 1
        if int_pct < 50.0:
            low_marks_count += 1
        if att < 65.0 or int_pct < 50.0:
            at_risk_students_set.add(r.student_id)

    avg_attendance = round(total_attendance / total_records, 1) if total_records > 0 else 0.0
    avg_marks = round(total_internal / total_records, 1) if total_records > 0 else 0.0

    return {
        "faculty": {
            "id": faculty.id,
            "name": current_user.name,
            "email": current_user.email,
            "employee_id": faculty.employee_id,
            "department": faculty.department,
            "designation": faculty.designation
        },
        "stats": {
            "assigned_subjects_count": len(subjects),
            "total_enrolled_students": total_records,
            "class_average_attendance": avg_attendance,
            "class_average_internal_marks": avg_marks,
            "low_attendance_alerts": low_attendance_count,
            "low_marks_alerts": low_marks_count,
            "at_risk_students_count": len(at_risk_students_set)
        },
        "subjects": [
            {
                "id": s.id,
                "name": s.name,
                "code": s.code,
                "department": s.department,
                "semester": s.semester,
                "credits": s.credits,
                "student_count": len(s.academic_records)
            }
            for s in subjects
        ]
    }

@router.get("/subject/{subject_id}/students")
def get_subject_students(
    subject_id: int,
    current_user: User = Depends(require_role(["faculty", "admin"])),
    db: Session = Depends(get_db)
):
    faculty = _get_faculty(current_user, db)
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    records = db.query(AcademicRecord).filter(AcademicRecord.subject_id == subject_id).all()
    students_data = []

    for r in records:
        stu = r.student
        stu_name = stu.user.name if stu and stu.user else "Unknown"
        att_pct = r.attendance_percentage
        int_pct = round((r.internal_marks / 50.0) * 100.0, 1)
        asg_pct = round((r.assignment_marks / 25.0) * 100.0, 1)

        # Quick risk check
        risk_tag = "LOW"
        if att_pct < 65.0 or int_pct < 50.0 or stu.backlogs >= 2:
            risk_tag = "HIGH"
        elif att_pct < 75.0 or int_pct < 60.0 or stu.backlogs == 1:
            risk_tag = "MEDIUM"

        students_data.append({
            "record_id": r.id,
            "student_id": stu.id,
            "name": stu_name,
            "roll_number": stu.roll_number,
            "section": stu.section,
            "cgpa": stu.cgpa,
            "backlogs": stu.backlogs,
            "classes_attended": r.classes_attended,
            "total_classes": r.total_classes,
            "attendance_percentage": att_pct,
            "internal_marks": r.internal_marks,
            "assignment_marks": r.assignment_marks,
            "final_exam_marks": r.final_exam_marks,
            "grade": r.grade,
            "risk_tag": risk_tag
        })

    return {
        "subject": {
            "id": subject.id,
            "name": subject.name,
            "code": subject.code,
            "semester": subject.semester
        },
        "students": students_data
    }

@router.put("/record/{record_id}/marks")
def update_marks(
    record_id: int,
    payload: UpdateMarksRequest,
    current_user: User = Depends(require_role(["faculty", "admin"])),
    db: Session = Depends(get_db)
):
    record = db.query(AcademicRecord).filter(AcademicRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Academic record not found")

    if payload.internal_marks is not None:
        record.internal_marks = max(0.0, min(payload.internal_marks, 50.0))
    if payload.assignment_marks is not None:
        record.assignment_marks = max(0.0, min(payload.assignment_marks, 25.0))
    if payload.final_exam_marks is not None:
        record.final_exam_marks = max(0.0, min(payload.final_exam_marks, 100.0))
    if payload.grade is not None:
        record.grade = payload.grade

    db.commit()
    return {"message": "Marks updated successfully", "record_id": record.id}

@router.put("/record/{record_id}/attendance")
def update_attendance(
    record_id: int,
    payload: UpdateAttendanceRequest,
    current_user: User = Depends(require_role(["faculty", "admin"])),
    db: Session = Depends(get_db)
):
    record = db.query(AcademicRecord).filter(AcademicRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Academic record not found")

    record.classes_attended = max(0, payload.classes_attended)
    record.total_classes = max(1, payload.total_classes)
    db.commit()
    return {"message": "Attendance updated successfully", "attendance_percentage": record.attendance_percentage}

@router.post("/remarks")
def add_faculty_remark(
    payload: FacultyRemarkCreate,
    current_user: User = Depends(require_role(["faculty", "admin"])),
    db: Session = Depends(get_db)
):
    faculty = _get_faculty(current_user, db)
    remark = FacultyRemark(
        faculty_id=faculty.id,
        student_id=payload.student_id,
        subject_id=payload.subject_id,
        remark=payload.remark.strip()
    )
    db.add(remark)
    db.commit()
    db.refresh(remark)
    return {"message": "Remark added successfully", "remark_id": remark.id}
