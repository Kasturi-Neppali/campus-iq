import math
from typing import Dict, Any, List, Optional

def marks_to_grade_point(marks: float) -> int:
    """Standard 10-point university absolute grading scale."""
    if marks >= 90:
        return 10
    elif marks >= 80:
        return 9
    elif marks >= 70:
        return 8
    elif marks >= 60:
        return 7
    elif marks >= 50:
        return 6
    elif marks >= 40:
        return 5
    else:
        return 0

class WhatIfSimulatorEngine:
    def simulate(
        self,
        current_cgpa: float,
        current_semester: int,
        subjects_with_credits_and_expected_marks: List[Dict[str, Any]],
        target_cgpa: Optional[float] = None,
        current_attendance_attended: Optional[int] = None,
        current_attendance_total: Optional[int] = None,
        additional_classes_attended: Optional[int] = None,
        additional_classes_total: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Calculates projected SGPA, updated CGPA, target feasibility, and attendance projection.
        """
        response: Dict[str, Any] = {}

        # 1. Subject marks -> Projected SGPA
        if subjects_with_credits_and_expected_marks:
            total_credits = 0
            weighted_points = 0.0
            for sub in subjects_with_credits_and_expected_marks:
                credits = sub.get("credits", 3)
                marks = sub.get("expected_marks", 75.0)
                grade_point = marks_to_grade_point(marks)
                total_credits += credits
                weighted_points += (credits * grade_point)

            projected_sgpa = round(weighted_points / total_credits, 2) if total_credits > 0 else 0.0
            response["projected_sgpa"] = projected_sgpa

            # Compute updated cumulative CGPA
            # Assuming ~20 credits per past semester
            past_semesters = max(current_semester - 1, 1)
            past_credits = past_semesters * 20
            new_total_credits = past_credits + total_credits
            projected_cgpa = round(((current_cgpa * past_credits) + (projected_sgpa * total_credits)) / new_total_credits, 2)
            response["projected_cgpa"] = projected_cgpa
        else:
            response["projected_sgpa"] = None
            response["projected_cgpa"] = None

        # 2. Target CGPA Solver
        if target_cgpa is not None:
            # Semesters remaining (assuming 8 total semesters in B.Tech)
            remaining_semesters = max(8 - current_semester + 1, 1)
            past_semesters = max(current_semester - 1, 0)
            past_credits = past_semesters * 20
            remaining_credits = remaining_semesters * 20
            total_btech_credits = past_credits + remaining_credits

            # Target formula: target_cgpa * total_credits = (current_cgpa * past_credits) + (req_sgpa * remaining_credits)
            required_total_points = (target_cgpa * total_btech_credits) - (current_cgpa * past_credits)
            required_sgpa = round(required_total_points / remaining_credits, 2)

            response["required_sgpa_for_target"] = required_sgpa

            if required_sgpa > 10.0:
                response["feasibility_message"] = (
                    f"A target CGPA of {target_cgpa} is mathematically unattainable in the remaining {remaining_semesters} "
                    f"semester(s), as it requires an average SGPA of {required_sgpa} (maximum possible is 10.0). "
                    f"Maximum achievable CGPA is {round(((current_cgpa * past_credits) + (10.0 * remaining_credits)) / total_btech_credits, 2)}."
                )
            elif required_sgpa < 0.0:
                response["feasibility_message"] = f"You have already securely exceeded the target CGPA of {target_cgpa}."
            elif required_sgpa >= 9.0:
                response["feasibility_message"] = (
                    f"Challenging but achievable! You need to maintain an average SGPA of {required_sgpa} across the "
                    f"remaining {remaining_semesters} semester(s). This requires mostly 'O' and 'A+' grades."
                )
            else:
                response["feasibility_message"] = (
                    f"Highly achievable! Maintaining an average SGPA of {required_sgpa} across the remaining "
                    f"{remaining_semesters} semester(s) will meet your target CGPA of {target_cgpa}."
                )
        else:
            response["required_sgpa_for_target"] = None
            if response["projected_cgpa"] is not None:
                diff = round(response["projected_cgpa"] - current_cgpa, 2)
                symbol = "+" if diff >= 0 else ""
                response["feasibility_message"] = f"Projected change in cumulative CGPA: {symbol}{diff} (New CGPA: {response['projected_cgpa']})."
            else:
                response["feasibility_message"] = "Enter expected marks or a target CGPA to simulate academic projections."

        # 3. Attendance Projection
        if current_attendance_attended is not None and current_attendance_total is not None and current_attendance_total > 0:
            addl_att = additional_classes_attended or 0
            addl_tot = additional_classes_total or 0
            new_att = current_attendance_attended + addl_att
            new_tot = current_attendance_total + addl_tot
            projected_attendance = round((new_att / new_tot) * 100.0, 2) if new_tot > 0 else 0.0
            response["projected_attendance_pct"] = projected_attendance

            # Classes needed to reach 75%
            curr_pct = (current_attendance_attended / current_attendance_total) * 100.0
            if curr_pct < 75.0:
                # (attended + k) / (total + k) >= 0.75  =>  k >= (0.75 * total - attended) / 0.25
                needed_classes = math.ceil(max(0, (0.75 * current_attendance_total - current_attendance_attended) / 0.25))
                response["classes_needed_for_75"] = needed_classes
            else:
                # Classes student can safely skip without dropping below 75%
                # (attended) / (total + m) >= 0.75  =>  total + m <= attended / 0.75 => m <= (attended / 0.75) - total
                safe_bunks = math.floor(max(0, (current_attendance_attended / 0.75) - current_attendance_total))
                response["classes_can_afford_to_miss"] = safe_bunks

        return response

simulator_engine = WhatIfSimulatorEngine()
