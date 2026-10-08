import os
import joblib
import numpy as np
from typing import Dict, Any, List

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml/risk_model.joblib"))

class AcademicRiskEngine:
    def __init__(self):
        self.model = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
            except Exception as e:
                print(f"[AcademicRiskEngine] Notice: Could not load model from {MODEL_PATH}: {e}")
                self.model = None

    def predict_risk(
        self,
        attendance_pct: float,
        internal_pct: float,
        assignment_pct: float,
        previous_cgpa: float,
        backlogs: int
    ) -> Dict[str, Any]:
        """
        Predicts Academic Risk (LOW, MEDIUM, HIGH) along with explainability factors and recommendations.
        Uses the trained Scikit-learn Random Forest model when available, with an ensemble rule safeguard.
        """
        # If model is loaded, use Random Forest prediction
        if self.model is not None:
            import pandas as pd
            features = pd.DataFrame([{
                "attendance_pct": attendance_pct,
                "internal_pct": internal_pct,
                "assignment_pct": assignment_pct,
                "previous_cgpa": previous_cgpa,
                "backlogs": backlogs
            }])
            predicted_class = self.model.predict(features)[0]
            probabilities = self.model.predict_proba(features)[0]
            risk_level = str(predicted_class)
            high_idx = list(self.model.classes_).index("HIGH") if "HIGH" in self.model.classes_ else -1
            risk_score = round(float(probabilities[high_idx] * 100.0) if high_idx >= 0 else 50.0, 1)
        else:
            # Deterministic academic heuristics baseline (mirroring collegiate risk matrix)
            score = 0.0
            if attendance_pct < 65.0:
                score += 35.0
            elif attendance_pct < 75.0:
                score += 15.0

            if internal_pct < 50.0:
                score += 30.0
            elif internal_pct < 65.0:
                score += 15.0

            if assignment_pct < 60.0:
                score += 10.0

            if backlogs >= 2:
                score += 30.0
            elif backlogs == 1:
                score += 15.0

            if previous_cgpa < 6.0:
                score += 20.0
            elif previous_cgpa < 7.0:
                score += 10.0

            risk_score = min(round(score, 1), 100.0)
            if risk_score >= 50.0 or backlogs >= 2 or (attendance_pct < 65.0 and internal_pct < 50.0):
                risk_level = "HIGH"
            elif risk_score >= 25.0 or backlogs == 1 or attendance_pct < 75.0 or internal_pct < 60.0:
                risk_level = "MEDIUM"
            else:
                risk_level = "LOW"

        # Explainability & Diagnostic Reasons
        contributing_factors = []
        recommendations = []

        if attendance_pct < 65.0:
            contributing_factors.append(f"Critical Attendance Deficit: Current attendance is {attendance_pct:.1f}% (below 65% university detention threshold).")
            recommendations.append("Prioritize attending all remaining lecture hours and labs to avoid exam hall ticket withholding.")
        elif attendance_pct < 75.0:
            contributing_factors.append(f"Borderline Attendance: Current attendance is {attendance_pct:.1f}% (below mandatory 75% eligibility).")
            recommendations.append("Maintain 100% attendance over the next 3 weeks to cross the 75% cutoff threshold.")

        if internal_pct < 50.0:
            contributing_factors.append(f"Low Internal Marks: Average internal score is {internal_pct:.1f}% (indicates struggle in mid-term evaluations).")
            recommendations.append("Schedule faculty doubts clearing sessions and solve previous 3 years mid-term question banks.")
        elif internal_pct < 65.0:
            contributing_factors.append(f"Average Internal Marks: Scoring {internal_pct:.1f}% leaves little buffer for semester end exams.")
            recommendations.append("Form study groups for problem-heavy concepts to boost unit-test performance.")

        if assignment_pct < 60.0:
            contributing_factors.append(f"Assignment Deficit: Assignment submission score is {assignment_pct:.1f}%.")
            recommendations.append("Ensure timely submission of all continuous assessment assignments and lab observation reports.")

        if backlogs >= 2:
            contributing_factors.append(f"Multiple Backlogs: {backlogs} uncleared courses create severe academic backlog pressure.")
            recommendations.append("Dedicate at least 1.5 hours daily specifically to backlog course syllabus revision.")
        elif backlogs == 1:
            contributing_factors.append(f"Active Backlog: 1 uncleared subject.")
            recommendations.append("Register for supplementary coaching and focus on scoring passing criteria in the upcoming supplementary cycle.")

        if previous_cgpa < 6.5:
            contributing_factors.append(f"Low Cumulative CGPA ({previous_cgpa:.2f}): Below most campus placement eligibility thresholds (typically 6.5-7.0).")
            recommendations.append("Target a minimum of 8.0 SGPA in current semester to lift overall CGPA above 7.0.")

        if not contributing_factors:
            contributing_factors.append("Consistent Academic Trajectory: Good attendance and solid internal scores.")
            recommendations.append("Maintain current study rhythm and focus on high-weightage final exam topics.")

        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "contributing_factors": contributing_factors,
            "recommendations": recommendations
        }

risk_engine = AcademicRiskEngine()
