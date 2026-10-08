from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class PlacementProfile(Base):
    __tablename__ = "placement_profiles"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), unique=True, nullable=False)
    dsa_score = Column(Float, default=70.0)           # 0 to 100
    programming_score = Column(Float, default=75.0)   # 0 to 100
    aptitude_score = Column(Float, default=65.0)      # 0 to 100
    communication_score = Column(Float, default=70.0) # 0 to 100
    leetcode_solved = Column(Integer, default=120)
    github_url = Column(String(255), nullable=True)
    linkedin_url = Column(String(255), nullable=True)
    readiness_score = Column(Float, default=72.0)     # Calculated overall readiness
    areas_to_improve = Column(Text, nullable=True)     # JSON string array of topics e.g. ["Dynamic Programming", "Quantitative Aptitude"]

    student = relationship("Student", back_populates="placement_profile")
