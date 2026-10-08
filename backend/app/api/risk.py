from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.schemas.ml_ai import RiskPredictionRequest, RiskPredictionResponse
from app.services.risk_engine import risk_engine

router = APIRouter(prefix="/risk", tags=["Academic Risk ML"])

@router.post("/predict", response_model=RiskPredictionResponse)
def predict_academic_risk(
    payload: RiskPredictionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Predicts Academic Failure Risk (LOW, MEDIUM, HIGH) using the Scikit-Learn ML engine.
    Returns quantitative probability score and qualitative explainability factors.
    """
    prediction = risk_engine.predict_risk(
        attendance_pct=payload.attendance_pct,
        internal_pct=payload.internal_pct,
        assignment_pct=payload.assignment_pct,
        previous_cgpa=payload.previous_cgpa,
        backlogs=payload.backlogs
    )
    return RiskPredictionResponse(
        risk_level=prediction["risk_level"],
        risk_score=prediction["risk_score"],
        contributing_factors=prediction["contributing_factors"],
        recommendations=prediction["recommendations"]
    )
