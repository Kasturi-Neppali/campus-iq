from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    roll_number = Column(String(50), unique=True, index=True, nullable=False)
    department = Column(String(100), nullable=False)  # e.g., "Computer Science & Engineering"
    year = Column(Integer, nullable=False)            # 1, 2, 3, 4
    semester = Column(Integer, nullable=False)        # 1 to 8
    section = Column(String(10), nullable=False)      # A, B, C
    cgpa = Column(Float, default=0.0)
    backlogs = Column(Integer, default=0)
    phone = Column(String(20), nullable=True)

    # Relationships
    user = relationship("User", back_populates="student_profile")
    academic_records = relationship("AcademicRecord", back_populates="student", cascade="all, delete-orphan")
    skills = relationship("StudentSkill", back_populates="student", cascade="all, delete-orphan")
    projects = relationship("StudentProject", back_populates="student", cascade="all, delete-orphan")
    certifications = relationship("StudentCertification", back_populates="student", cascade="all, delete-orphan")
    placement_profile = relationship("PlacementProfile", back_populates="student", uselist=False, cascade="all, delete-orphan")
    risk_assessment = relationship("RiskAssessment", back_populates="student", uselist=False, cascade="all, delete-orphan")
    remarks = relationship("FacultyRemark", back_populates="student", cascade="all, delete-orphan")

class StudentSkill(Base):
    __tablename__ = "student_skills"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(100), nullable=False)
    proficiency = Column(String(50), default="Intermediate")  # Beginner, Intermediate, Advanced

    student = relationship("Student", back_populates="skills")

class StudentProject(Base):
    __tablename__ = "student_projects"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)
    tech_stack = Column(String(200), nullable=True)
    github_link = Column(String(255), nullable=True)

    student = relationship("Student", back_populates="projects")

class StudentCertification(Base):
    __tablename__ = "student_certifications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(150), nullable=False)
    issuer = Column(String(150), nullable=False)
    issue_date = Column(String(50), nullable=True)
    credential_url = Column(String(255), nullable=True)

    student = relationship("Student", back_populates="certifications")
