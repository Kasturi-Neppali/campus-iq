from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.core.database import get_db
from app.api.auth import get_current_user, require_role
from app.models.user import User
from app.models.student import Student, StudentSkill, StudentProject, StudentCertification
from app.models.academic import AcademicRecord, Subject
from app.models.faculty import FacultyRemark
from app.models.placement import PlacementProfile
from app.models.risk import RiskAssessment
from app.schemas.student import SkillCreate, ProjectCreate, CertificationCreate
from app.services.risk_engine import risk_engine
from app.services.placement_engine import placement_engine

router = APIRouter(prefix="/student", tags=["Student"])

def _get_student(current_user: User, db: Session) -> Student:
    student = current_user.student_profile
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found for this user")
    return student

@router.get("/dashboard")
def get_student_dashboard(
    current_user: User = Depends(require_role(["student", "admin"])),
    db: Session = Depends(get_db)
):
    student = _get_student(current_user, db)

    # 1. Academic records & Subject performance
    records = db.query(AcademicRecord).filter(AcademicRecord.student_id == student.id).all()
    
    total_attended = sum(r.classes_attended for r in records)
    total_classes = sum(r.total_classes for r in records)
    overall_attendance = round((total_attended / total_classes * 100.0), 2) if total_classes > 0 else 0.0

    subjects_data = []
    weak_subjects = []
    total_internal = 0.0
    total_assignment = 0.0

    for r in records:
        sub_name = r.subject.name if r.subject else "Subject"
        sub_code = r.subject.code if r.subject else "SUB"
        credits = r.subject.credits if r.subject else 3
        att_pct = r.attendance_percentage
        # Internal marks out of 50 -> percentage
        int_pct = round((r.internal_marks / 50.0) * 100.0, 1)
        asg_pct = round((r.assignment_marks / 25.0) * 100.0, 1)
        total_internal += int_pct
        total_assignment += asg_pct

        status_flag = "Strong"
        if int_pct < 50.0 or att_pct < 65.0:
            status_flag = "Critical"
            weak_subjects.append({"name": sub_name, "code": sub_code, "reason": "Low internal score or attendance"})
        elif int_pct < 65.0 or att_pct < 75.0:
            status_flag = "Average"
            weak_subjects.append({"name": sub_name, "code": sub_code, "reason": "Borderline performance"})

        subjects_data.append({
            "record_id": r.id,
            "subject_id": r.subject_id,
            "name": sub_name,
            "code": sub_code,
            "credits": credits,
            "classes_attended": r.classes_attended,
            "total_classes": r.total_classes,
            "attendance_percentage": att_pct,
            "internal_marks": r.internal_marks,
            "internal_percentage": int_pct,
            "assignment_marks": r.assignment_marks,
            "assignment_percentage": asg_pct,
            "final_exam_marks": r.final_exam_marks,
            "grade": r.grade,
            "status": status_flag
        })

    num_records = len(records) if records else 1
    avg_internal_pct = round(total_internal / num_records, 1)
    avg_assignment_pct = round(total_assignment / num_records, 1)

    # 2. Risk Assessment calculation
    risk_info = risk_engine.predict_risk(
        attendance_pct=overall_attendance,
        internal_pct=avg_internal_pct,
        assignment_pct=avg_assignment_pct,
        previous_cgpa=student.cgpa,
        backlogs=student.backlogs
    )

    # 3. Placement Readiness calculation
    p_profile = student.placement_profile
    if not p_profile:
        # Default starter values if not initialized
        dsa = 70.0
        prog = 75.0
        apt = 65.0
        comm = 70.0
        leetcode = 120
    else:
        dsa = p_profile.dsa_score
        prog = p_profile.programming_score
        apt = p_profile.aptitude_score
        comm = p_profile.communication_score
        leetcode = p_profile.leetcode_solved

    placement_info = placement_engine.calculate_readiness(
        cgpa=student.cgpa,
        dsa_score=dsa,
        programming_score=prog,
        aptitude_score=apt,
        communication_score=comm,
        projects_count=len(student.projects),
        certifications_count=len(student.certifications),
        leetcode_solved=leetcode
    )

    return {
        "student": {
            "id": student.id,
            "name": current_user.name,
            "email": current_user.email,
            "roll_number": student.roll_number,
            "department": student.department,
            "year": student.year,
            "semester": student.semester,
            "section": student.section,
            "cgpa": student.cgpa,
            "backlogs": student.backlogs
        },
        "stats": {
            "cgpa": student.cgpa,
            "attendance_pct": overall_attendance,
            "backlogs": student.backlogs,
            "risk_level": risk_info["risk_level"],
            "risk_score": risk_info["risk_score"],
            "placement_readiness": placement_info["overall_readiness"],
            "total_subjects": len(records),
            "weak_subjects_count": len(weak_subjects)
        },
        "subjects": subjects_data,
        "weak_subjects": weak_subjects,
        "risk_details": risk_info,
        "placement_details": placement_info,
        "portfolio": {
            "skills": [{"id": s.id, "skill_name": s.skill_name, "proficiency": s.proficiency} for s in student.skills],
            "projects": [{"id": p.id, "title": p.title, "description": p.description, "tech_stack": p.tech_stack, "github_link": p.github_link} for p in student.projects],
            "certifications": [{"id": c.id, "title": c.title, "issuer": c.issuer, "issue_date": c.issue_date, "credential_url": c.credential_url} for c in student.certifications]
        }
    }

@router.get("/profile")
def get_student_profile(
    current_user: User = Depends(require_role(["student"])),
    db: Session = Depends(get_db)
):
    student = _get_student(current_user, db)
    return {
        "id": student.id,
        "name": current_user.name,
        "email": current_user.email,
        "roll_number": student.roll_number,
        "department": student.department,
        "year": student.year,
        "semester": student.semester,
        "section": student.section,
        "cgpa": student.cgpa,
        "backlogs": student.backlogs,
        "phone": student.phone,
        "skills": [{"id": s.id, "skill_name": s.skill_name, "proficiency": s.proficiency} for s in student.skills],
        "projects": [{"id": p.id, "title": p.title, "description": p.description, "tech_stack": p.tech_stack, "github_link": p.github_link} for p in student.projects],
        "certifications": [{"id": c.id, "title": c.title, "issuer": c.issuer, "issue_date": c.issue_date, "credential_url": c.credential_url} for c in student.certifications]
    }

@router.post("/skills")
def add_skill(
    payload: SkillCreate,
    current_user: User = Depends(require_role(["student"])),
    db: Session = Depends(get_db)
):
    student = _get_student(current_user, db)
    new_skill = StudentSkill(student_id=student.id, skill_name=payload.skill_name, proficiency=payload.proficiency)
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return {"message": "Skill added successfully", "skill": {"id": new_skill.id, "skill_name": new_skill.skill_name, "proficiency": new_skill.proficiency}}

@router.delete("/skills/{skill_id}")
def delete_skill(
    skill_id: int,
    current_user: User = Depends(require_role(["student"])),
    db: Session = Depends(get_db)
):
    student = _get_student(current_user, db)
    skill = db.query(StudentSkill).filter(StudentSkill.id == skill_id, StudentSkill.student_id == student.id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(skill)
    db.commit()
    return {"message": "Skill deleted successfully"}

@router.post("/projects")
def add_project(
    payload: ProjectCreate,
    current_user: User = Depends(require_role(["student"])),
    db: Session = Depends(get_db)
):
    student = _get_student(current_user, db)
    project = StudentProject(
        student_id=student.id,
        title=payload.title,
        description=payload.description,
        tech_stack=payload.tech_stack,
        github_link=payload.github_link
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"message": "Project added successfully", "project": {"id": project.id, "title": project.title}}

@router.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    current_user: User = Depends(require_role(["student"])),
    db: Session = Depends(get_db)
):
    student = _get_student(current_user, db)
    project = db.query(StudentProject).filter(StudentProject.id == project_id, StudentProject.student_id == student.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}

@router.post("/certifications")
def add_certification(
    payload: CertificationCreate,
    current_user: User = Depends(require_role(["student"])),
    db: Session = Depends(get_db)
):
    student = _get_student(current_user, db)
    cert = StudentCertification(
        student_id=student.id,
        title=payload.title,
        issuer=payload.issuer,
        issue_date=payload.issue_date,
        credential_url=payload.credential_url
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return {"message": "Certification added successfully", "certification": {"id": cert.id, "title": cert.title}}

@router.delete("/certifications/{cert_id}")
def delete_certification(
    cert_id: int,
    current_user: User = Depends(require_role(["student"])),
    db: Session = Depends(get_db)
):
    student = _get_student(current_user, db)
    cert = db.query(StudentCertification).filter(StudentCertification.id == cert_id, StudentCertification.student_id == student.id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    db.delete(cert)
    db.commit()
    return {"message": "Certification deleted successfully"}

@router.get("/remarks")
def get_student_remarks(
    current_user: User = Depends(require_role(["student"])),
    db: Session = Depends(get_db)
):
    student = _get_student(current_user, db)
    remarks = db.query(FacultyRemark).filter(FacultyRemark.student_id == student.id).order_by(FacultyRemark.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "faculty_name": r.faculty.user.name if r.faculty and r.faculty.user else "Faculty",
            "subject_name": r.subject.name if r.subject else "General",
            "remark": r.remark,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else ""
        }
        for r in remarks
    ]
