from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    department = Column(String(100), nullable=False)
    semester = Column(Integer, nullable=False)
    credits = Column(Integer, default=3)
    faculty_id = Column(Integer, ForeignKey("faculty.id", ondelete="SET NULL"), nullable=True)

    faculty = relationship("Faculty", back_populates="subjects")
    academic_records = relationship("AcademicRecord", back_populates="subject", cascade="all, delete-orphan")

class AcademicRecord(Base):
    __tablename__ = "academic_records"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    semester = Column(Integer, nullable=False)
    classes_attended = Column(Integer, default=0)
    total_classes = Column(Integer, default=0)
    internal_marks = Column(Float, default=0.0)      # Out of 50
    assignment_marks = Column(Float, default=0.0)    # Out of 25
    final_exam_marks = Column(Float, default=0.0)    # Out of 100
    grade = Column(String(5), default="P")           # O, A+, A, B+, B, C, F

    student = relationship("Student", back_populates="academic_records")
    subject = relationship("Subject", back_populates="academic_records")

    @property
    def attendance_percentage(self) -> float:
        if self.total_classes and self.total_classes > 0:
            return round((self.classes_attended / self.total_classes) * 100.0, 2)
        return 0.0

    @property
    def total_score_percentage(self) -> float:
        """Calculates normalized score percentage: 40% internal (internal+assignment scaled) + 60% final."""
        internal_comp = ((self.internal_marks / 50.0) * 25.0) + self.assignment_marks  # max 50
        internal_pct = (internal_comp / 50.0) * 40.0
        final_pct = (self.final_exam_marks / 100.0) * 60.0
        return round(internal_pct + final_pct, 2)
