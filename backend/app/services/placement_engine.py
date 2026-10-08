import json
from typing import Dict, Any, List

class PlacementReadinessEngine:
    def calculate_readiness(
        self,
        cgpa: float,
        dsa_score: float,
        programming_score: float,
        aptitude_score: float,
        communication_score: float,
        projects_count: int,
        certifications_count: int,
        leetcode_solved: int
    ) -> Dict[str, Any]:
        """
        Calculates holistic Placement Readiness score and surfaces priority areas to improve.
        Formula weights:
        - DSA & Problem Solving: 25%
        - Core Programming / Coding: 20%
        - Aptitude & Logical Reasoning: 15%
        - Communication & Soft Skills: 15%
        - Practical Projects & Certifications: 15%
        - Academic CGPA (normalized): 10%
        """
        cgpa_normalized = min(max((cgpa / 10.0) * 100.0, 0.0), 100.0)
        
        # Calculate projects score based on count and depth
        projects_score = min(projects_count * 30.0 + (10.0 if projects_count >= 2 else 0.0), 100.0)
        certifications_score = min(certifications_count * 35.0, 100.0)
        practical_score = (projects_score * 0.7) + (certifications_score * 0.3)

        overall = (
            (dsa_score * 0.25) +
            (programming_score * 0.20) +
            (aptitude_score * 0.15) +
            (communication_score * 0.15) +
            (practical_score * 0.15) +
            (cgpa_normalized * 0.10)
        )
        overall_score = round(overall, 1)

        # Areas to Improve
        areas_to_improve = []
        if dsa_score < 70.0 or leetcode_solved < 150:
            areas_to_improve.append(f"DSA & Problem Solving ({dsa_score:.0f}%): Practice Trees, Graphs, DP and target 150+ solved problems.")
        if programming_score < 75.0:
            areas_to_improve.append(f"Programming Fundamentals ({programming_score:.0f}%): Strengthen OOP, SQL indexing, and concurrency.")
        if aptitude_score < 70.0:
            areas_to_improve.append(f"Aptitude & Quantitative ({aptitude_score:.0f}%): Practice speed-math, Permutation/Combination, and Logical reasoning.")
        if communication_score < 75.0:
            areas_to_improve.append(f"Communication & Interview Polish ({communication_score:.0f}%): Conduct mock HR and behavioral STAR-method interviews.")
        if projects_count < 2:
            areas_to_improve.append("Industry Projects: Add at least 2 full-stack / AI-driven projects with live demos and clean GitHub repositories.")
        if cgpa < 7.0:
            areas_to_improve.append(f"CGPA ({cgpa:.2f}): Lift CGPA above 7.0/7.5 to unlock top-tier product company shortlisting criteria.")

        if not areas_to_improve:
            areas_to_improve.append("Profile is well balanced! Practice advanced system design and mock coding rounds.")

        # Determine Readiness Tier
        if overall_score >= 80.0:
            tier = "Placement Ready (Product / Tier-1 Focus)"
        elif overall_score >= 65.0:
            tier = "Competitive (Service & Mid-tier Product Focus)"
        else:
            tier = "High Priority Up-skilling Required"

        return {
            "overall_readiness": overall_score,
            "dsa_score": round(dsa_score, 1),
            "programming_score": round(programming_score, 1),
            "aptitude_score": round(aptitude_score, 1),
            "communication_score": round(communication_score, 1),
            "projects_score": round(projects_score, 1),
            "certifications_score": round(certifications_score, 1),
            "leetcode_solved": leetcode_solved,
            "areas_to_improve": areas_to_improve,
            "readiness_tier": tier,
            "disclaimer": "This readiness indicator is an internal self-assessment metric based on institutional placement benchmarks and does NOT guarantee placement offers."
        }

placement_engine = PlacementReadinessEngine()
