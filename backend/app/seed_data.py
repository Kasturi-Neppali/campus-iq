import os
import sys

# Ensure backend root is in Python module search path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import Base, engine, SessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.models.student import Student, StudentSkill, StudentProject, StudentCertification
from app.models.faculty import Faculty, FacultyRemark
from app.models.academic import Subject, AcademicRecord
from app.models.placement import PlacementProfile
from app.models.risk import RiskAssessment

def seed_database():
    print("=" * 60)
    print(" CampusIQ: Seeding Relational Database with Realistic College Data")
    print("=" * 60)

    # Recreate all tables cleanly
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 1. Create Admin
        admin_user = User(
            email="admin@campusiq.edu",
            hashed_password=hash_password("Admin@123"),
            name="Dr. K. S. Murthy (Dean & HOD)",
            role="admin"
        )
        db.add(admin_user)

        # 2. Create Faculty
        fac1_user = User(
            email="hod.cse@campusiq.edu",
            hashed_password=hash_password("Faculty@123"),
            name="Dr. Rajesh Sharma",
            role="faculty"
        )
        fac2_user = User(
            email="faculty.menon@campusiq.edu",
            hashed_password=hash_password("Faculty@123"),
            name="Prof. Priya Menon",
            role="faculty"
        )
        fac3_user = User(
            email="faculty.patel@campusiq.edu",
            hashed_password=hash_password("Faculty@123"),
            name="Prof. Amit Patel",
            role="faculty"
        )
        db.add_all([fac1_user, fac2_user, fac3_user])
        db.flush()

        fac1 = Faculty(user_id=fac1_user.id, employee_id="FAC-CSE-001", department="Computer Science & Engineering", designation="Professor & HOD")
        fac2 = Faculty(user_id=fac2_user.id, employee_id="FAC-CSE-008", department="Computer Science & Engineering", designation="Associate Professor")
        fac3 = Faculty(user_id=fac3_user.id, employee_id="FAC-CSE-015", department="Computer Science & Engineering", designation="Assistant Professor")
        db.add_all([fac1, fac2, fac3])
        db.flush()

        # 3. Create Core Subjects (Semester 7 CSE)
        s1 = Subject(name="Python Programming & Scripting", code="CS701", department="Computer Science & Engineering", semester=7, credits=4, faculty_id=fac1.id)
        s2 = Subject(name="Database Management Systems", code="CS702", department="Computer Science & Engineering", semester=7, credits=4, faculty_id=fac2.id)
        s3 = Subject(name="Operating Systems & Architecture", code="CS703", department="Computer Science & Engineering", semester=7, credits=3, faculty_id=fac2.id)
        s4 = Subject(name="Machine Learning & Deep Neural Nets", code="CS704", department="Computer Science & Engineering", semester=7, credits=4, faculty_id=fac3.id)
        s5 = Subject(name="Computer Networks & Security", code="CS705", department="Computer Science & Engineering", semester=7, credits=3, faculty_id=fac1.id)
        db.add_all([s1, s2, s3, s4, s5])
        db.flush()

        subjects_list = [s1, s2, s3, s4, s5]

        # 4. Create Kasturi (Primary Student Persona)
        kasturi_user = User(
            email="kasturi@campusiq.edu",
            hashed_password=hash_password("Student@123"),
            name="Kasturi Neppali",
            role="student"
        )
        db.add(kasturi_user)
        db.flush()

        kasturi = Student(
            user_id=kasturi_user.id,
            roll_number="21CSE042",
            department="Computer Science & Engineering",
            year=4,
            semester=7,
            section="A",
            cgpa=8.10,
            backlogs=0,
            phone="+91 98765 43210"
        )
        db.add(kasturi)
        db.flush()

        # Kasturi Academic Records
        # Python: 82%, DBMS: 68%, OS: 74%, ML: 85%, CN: 78%
        k_records = [
            AcademicRecord(student_id=kasturi.id, subject_id=s1.id, semester=7, classes_attended=38, total_classes=44, internal_marks=42.0, assignment_marks=22.0, final_exam_marks=80.0, grade="A+"),
            AcademicRecord(student_id=kasturi.id, subject_id=s2.id, semester=7, classes_attended=34, total_classes=44, internal_marks=34.0, assignment_marks=17.0, final_exam_marks=66.0, grade="B+"),
            AcademicRecord(student_id=kasturi.id, subject_id=s3.id, semester=7, classes_attended=35, total_classes=42, internal_marks=37.0, assignment_marks=19.0, final_exam_marks=72.0, grade="A"),
            AcademicRecord(student_id=kasturi.id, subject_id=s4.id, semester=7, classes_attended=39, total_classes=44, internal_marks=44.0, assignment_marks=23.0, final_exam_marks=84.0, grade="A+"),
            AcademicRecord(student_id=kasturi.id, subject_id=s5.id, semester=7, classes_attended=36, total_classes=42, internal_marks=39.0, assignment_marks=20.0, final_exam_marks=76.0, grade="A"),
        ]
        db.add_all(k_records)

        # Kasturi Placement Profile & Portfolio
        k_placement = PlacementProfile(
            student_id=kasturi.id,
            dsa_score=70.0,
            programming_score=80.0,
            aptitude_score=65.0,
            communication_score=75.0,
            leetcode_solved=185,
            github_url="https://github.com/kasturi-neppali",
            linkedin_url="https://linkedin.com/in/kasturi-neppali",
            readiness_score=78.0,
            areas_to_improve="Quantitative Aptitude, Advanced Tree / Graph DP Algorithms"
        )
        db.add(k_placement)

        # Kasturi Skills
        skills = [
            StudentSkill(student_id=kasturi.id, skill_name="Python", proficiency="Advanced"),
            StudentSkill(student_id=kasturi.id, skill_name="FastAPI & REST APIs", proficiency="Advanced"),
            StudentSkill(student_id=kasturi.id, skill_name="React.js", proficiency="Intermediate"),
            StudentSkill(student_id=kasturi.id, skill_name="SQL & Database Design", proficiency="Intermediate"),
            StudentSkill(student_id=kasturi.id, skill_name="Data Structures & Algorithms", proficiency="Intermediate"),
            StudentSkill(student_id=kasturi.id, skill_name="Scikit-Learn & Machine Learning", proficiency="Intermediate"),
        ]
        db.add_all(skills)

        # Kasturi Projects
        projects = [
            StudentProject(
                student_id=kasturi.id,
                title="CampusIQ – Academic Intelligence & Student Success Platform",
                description="Engineered full-stack intelligence portal integrating Scikit-Learn ML risk prediction, What-If academic simulator, and CampusAI contextual advisor.",
                tech_stack="FastAPI, React, SQLite/PostgreSQL, Scikit-Learn, Tailwind CSS",
                github_link="https://github.com/kasturi/campusiq"
            ),
            StudentProject(
                student_id=kasturi.id,
                title="FoodHub – Full Stack Online Food Ordering Engine",
                description="Designed high-throughput ordering workflow with state management, basket calculations, and real-time tracking.",
                tech_stack="React, Node.js, Express, MongoDB",
                github_link="https://github.com/kasturi/foodhub"
            ),
            StudentProject(
                student_id=kasturi.id,
                title="EV Charge & Range Analytics Dashboard",
                description="Interactive visualization portal analyzing real-time EV telemetry, battery degradation, and charge station loads.",
                tech_stack="Python, Pandas, Plotly, Streamlit",
                github_link="https://github.com/kasturi/ev-analytics"
            )
        ]
        db.add_all(projects)

        # Kasturi Certifications
        certs = [
            StudentCertification(
                student_id=kasturi.id,
                title="NPTEL Certified in Artificial Intelligence Search Methods",
                issuer="NPTEL & IIT Madras",
                issue_date="Nov 2025",
                credential_url="https://nptel.ac.in/noc/Ecertificate/?q=NPTEL25CS101"
            ),
            StudentCertification(
                student_id=kasturi.id,
                title="Full Stack Software Development Specialization",
                issuer="NxtWave Academy",
                issue_date="May 2026",
                credential_url="https://certificates.ccbp.in/nxtwave"
            )
        ]
        db.add_all(certs)

        # Kasturi Faculty Remarks
        rem1 = FacultyRemark(faculty_id=fac2.id, student_id=kasturi.id, subject_id=s2.id, remark="Good engagement in DBMS lab sessions. Recommended to practice normalization decomposition and SQL query indexing for upcoming finals.")
        rem2 = FacultyRemark(faculty_id=fac3.id, student_id=kasturi.id, subject_id=s4.id, remark="Strong understanding of ML algorithms and model evaluation. Keep up the high standard!")
        db.add_all([rem1, rem2])

        # 5. Create Cohort Students (Varying risk & placement levels)
        cohort_data = [
            ("Rahul Varma", "rahul@campusiq.edu", "21CSE088", 4, 7, "A", 5.8, 3, 58.0, 48.0, 52.0, 45.0, 50.0, 45, "Needs immediate intervention on Operating Systems and attendance."),
            ("Sneha Reddy", "sneha@campusiq.edu", "21CSE015", 4, 7, "B", 6.8, 1, 72.0, 68.0, 70.0, 62.0, 65.0, 110, "Satisfactory performance, focus on clearing the 3rd sem backlog."),
            ("Aditya Krishna", "aditya@campusiq.edu", "21CSE003", 4, 7, "A", 9.2, 0, 94.0, 92.0, 90.0, 88.0, 92.0, 320, "Outstanding academic performance and coding problem solver."),
            ("Ananya Das", "ananya@campusiq.edu", "21CSE027", 4, 7, "A", 7.9, 0, 84.0, 78.0, 75.0, 72.0, 80.0, 160, "Solid aptitude and communication skills."),
            ("Vikram Singh", "vikram@campusiq.edu", "21CSE095", 4, 7, "B", 6.2, 2, 63.0, 54.0, 58.0, 50.0, 60.0, 65, "At academic risk due to low lab attendance."),
            ("Divya Nair", "divya@campusiq.edu", "21CSE034", 4, 7, "B", 8.4, 0, 89.0, 82.0, 84.0, 80.0, 85.0, 210, "Great leadership skills in technical team projects."),
            ("Karthik Subramanian", "karthik@campusiq.edu", "21CSE055", 4, 7, "A", 7.4, 0, 78.0, 74.0, 72.0, 70.0, 75.0, 140, "Good analytical mindset."),
            ("Meera Joshi", "meera@campusiq.edu", "21CSE062", 4, 7, "B", 6.9, 1, 74.0, 66.0, 68.0, 64.0, 70.0, 95, "Focus on completing coding rounds efficiently."),
            ("Siddharth Roy", "siddharth@campusiq.edu", "21CSE079", 4, 7, "A", 8.7, 0, 91.0, 86.0, 88.0, 82.0, 88.0, 260, "Excellent candidate for product tier-1 drives."),
            ("Pooja Hegde", "pooja@campusiq.edu", "21CSE071", 4, 7, "B", 5.9, 2, 61.0, 52.0, 50.0, 55.0, 58.0, 50, "Needs special remedial classes in Networks.")
        ]

        for (name, email, roll, yr, sem, sec, cg, bg, att, dsa, prog, apt, comm, lc, remark_txt) in cohort_data:
            u = User(email=email, hashed_password=hash_password("Student@123"), name=name, role="student")
            db.add(u)
            db.flush()

            stu = Student(
                user_id=u.id,
                roll_number=roll,
                department="Computer Science & Engineering",
                year=yr,
                semester=sem,
                section=sec,
                cgpa=cg,
                backlogs=bg,
                phone="+91 98700 12345"
            )
            db.add(stu)
            db.flush()

            # Add Academic records for each subject
            for s in subjects_list:
                tot_cls = 44
                att_cls = int(tot_cls * (att / 100.0))
                # Add realistic variation
                intl_marks = round(max(15.0, min(48.0, (cg / 10.0) * 45.0 + (att_cls / tot_cls) * 5.0 - 2.0)), 1)
                asg_marks = round(max(10.0, min(24.0, (intl_marks / 50.0) * 23.0)), 1)
                final_marks = round(max(35.0, min(95.0, (intl_marks / 50.0) * 88.0)), 1)

                grade = "A" if final_marks >= 75 else ("B+" if final_marks >= 65 else ("C" if final_marks >= 50 else "F"))

                rec = AcademicRecord(
                    student_id=stu.id,
                    subject_id=s.id,
                    semester=sem,
                    classes_attended=att_cls,
                    total_classes=tot_cls,
                    internal_marks=intl_marks,
                    assignment_marks=asg_marks,
                    final_exam_marks=final_marks,
                    grade=grade
                )
                db.add(rec)

            # Placement profile
            pl = PlacementProfile(
                student_id=stu.id,
                dsa_score=dsa,
                programming_score=prog,
                aptitude_score=apt,
                communication_score=comm,
                leetcode_solved=lc,
                readiness_score=round((dsa * 0.25 + prog * 0.20 + apt * 0.15 + comm * 0.15 + (cg * 10) * 0.15 + 10.0), 1),
                areas_to_improve="Core Technical Depth, Practice Speed-Coding"
            )
            db.add(pl)

            # Remarks
            if remark_txt:
                r = FacultyRemark(faculty_id=fac1.id, student_id=stu.id, subject_id=s1.id, remark=remark_txt)
                db.add(r)

        db.commit()
        print("[OK] Successfully seeded 1 Admin, 3 Faculty, 5 Core Subjects, and 11 Engineering Students!")
        print("[OK] Kasturi profile initialized with 8.1 CGPA, 5 subjects, projects, skills, and placement records.")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Seeding failed: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
