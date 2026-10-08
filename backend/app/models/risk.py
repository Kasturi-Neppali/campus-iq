from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), unique=True, nullable=False)
    risk_level = Column(String(20), default="LOW")  # "LOW", "MEDIUM", "HIGH"
    risk_score = Column(Float, default=20.0)        # 0.0 to 100.0 (probability of failure/attrition)
    contributing_factors = Column(Text, nullable=True) # JSON array of explainability strings
    recommendations = Column(Text, nullable=True)      # JSON array of actionable recommendation strings
    calculated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    student = relationship("Student", back_populates="risk_assessment")
