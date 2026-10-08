import json
import requests
from typing import Dict, Any, List, Optional
from app.core.config import settings

class CampusAIEngine:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY

    def ask(
        self,
        student_context: Dict[str, Any],
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Processes student academic advisory queries.
        Uses Google Gemini LLM API if key is available; otherwise leverages the deterministic
        context-aware academic expert system.
        """
        # Attempt Gemini API call if key is present
        if self.api_key:
            try:
                gemini_reply = self._call_gemini_api(student_context, user_message, conversation_history)
                if gemini_reply:
                    return {
                        "reply": gemini_reply,
                        "student_context_applied": True,
                        "context_summary": self._extract_summary(student_context)
                    }
            except Exception as e:
                print(f"[CampusAIEngine] Gemini API fallback triggered due to: {e}")

        # Intelligent Contextual Academic Advisor (Guaranteed Offline / Interview Ready)
        advisor_reply = self._generate_contextual_advisory(student_context, user_message)
        return {
            "reply": advisor_reply,
            "student_context_applied": True,
            "context_summary": self._extract_summary(student_context)
        }

    def _extract_summary(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "name": context.get("name"),
            "cgpa": context.get("cgpa"),
            "attendance": context.get("overall_attendance"),
            "risk_level": context.get("risk_level"),
            "placement_readiness": context.get("placement_readiness"),
            "backlogs": context.get("backlogs")
        }

    def _call_gemini_api(
        self,
        student_context: Dict[str, Any],
        user_message: str,
        history: Optional[List[Dict[str, str]]]
    ) -> Optional[str]:
        system_prompt = (
            "You are CampusAI, an elite academic and career mentor for college students. "
            "Use the provided student academic context to give specific, empathetic, and actionable advice. "
            "Context:\n" + json.dumps(student_context, indent=2)
        )
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": f"System Context:\n{system_prompt}\n\nStudent Query: {user_message}"}]
                }
            ],
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 800
            }
        }
        resp = requests.post(url, json=payload, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        return None

    def _generate_contextual_advisory(self, ctx: Dict[str, Any], message: str) -> str:
        q = message.lower()
        name = ctx.get("name", "Student")
        cgpa = ctx.get("cgpa", 0.0)
        attendance = ctx.get("overall_attendance", 0.0)
        backlogs = ctx.get("backlogs", 0)
        risk = ctx.get("risk_level", "LOW")
        placement_score = ctx.get("placement_readiness", 70.0)
        subjects = ctx.get("subjects", [])
        weak_subjects = [s for s in subjects if s.get("internal_percentage", 100) < 60 or s.get("attendance_percentage", 100) < 75]
        areas_to_improve = ctx.get("areas_to_improve", [])

        # 1. Weak subjects / Where to focus
        if "focus" in q or "weak" in q or "subject" in q:
            if weak_subjects:
                weak_list = "\n".join([f"- **{s['name']}**: Internal Marks: {s.get('internal_percentage', 0)}%, Attendance: {s.get('attendance_percentage', 0)}%" for s in weak_subjects])
                return (
                    f"Hello {name}! Based on your current semester evaluations, here are the subjects requiring immediate focus:\n\n"
                    f"{weak_list}\n\n"
                    f"### Recommended Action Plan:\n"
                    f"1. **Attend all upcoming classes** in these subjects to pull attendance above the university 75% threshold.\n"
                    f"2. **Midterm & Assignment Review**: Revisit topics where marks were lost in the first internal exam.\n"
                    f"3. **Faculty Office Hours**: Consult your course instructors to clarify doubts before the semester-end examination."
                )
            else:
                return (
                    f"Great news, {name}! Your performance across all enrolled subjects is steady. "
                    f"None of your subjects currently fall into the critical performance zone. "
                    f"Continue revising unit summaries weekly and prioritize your placement DSA preparation."
                )

        # 2. Academic Risk diagnostics
        if "risk" in q or "why" in q and "academic" in q:
            factors = ctx.get("contributing_factors", [])
            recs = ctx.get("recommendations", [])
            factors_text = "\n".join([f"- {f}" for f in factors]) if factors else "- No high-risk indicators detected."
            recs_text = "\n".join([f"1. {r}" for r in recs]) if recs else "1. Maintain your steady study schedule."
            return (
                f"### Academic Risk Assessment: **{risk} RISK**\n\n"
                f"Hello {name}, our predictive model analyzed your academic factors:\n"
                f"- **Current CGPA**: {cgpa:.2f}\n"
                f"- **Overall Attendance**: {attendance:.1f}%\n"
                f"- **Uncleared Backlogs**: {backlogs}\n\n"
                f"#### Primary Contributing Factors:\n{factors_text}\n\n"
                f"#### Prescribed Next Steps:\n{recs_text}"
            )

        # 3. Study plan
        if "study plan" in q or "timetable" in q or "schedule" in q or "plan" in q:
            weak_names = ", ".join([s['name'] for s in weak_subjects]) if weak_subjects else "Core Technical Subjects"
            return (
                f"### Personalized 4-Week Study Plan for {name}\n\n"
                f"**Target Areas**: {weak_names} | Backlogs: {backlogs} | Current CGPA: {cgpa}\n\n"
                f"| Time Slot | Monday – Thursday | Friday – Saturday | Sunday |\n"
                f"| :--- | :--- | :--- | :--- |\n"
                f"| **5:30 PM - 7:00 PM** | {weak_names} syllabus revision | Placement DSA (Arrays, Trees, DP) | Mock Assessment Test |\n"
                f"| **7:30 PM - 8:30 PM** | Continuous Lab & Assignment work | Quantitative Aptitude & Reasoning | Project / GitHub Portfolio |\n"
                f"| **9:00 PM - 10:00 PM** | Previous Year University Papers | Faculty Remarks review | Rest & Week Planning |\n\n"
                f"> **Tip**: High attendance directly correlates with higher internal scores. Avoid unexcused leaves over the next 4 weeks."
            )

        # 4. Placement Readiness
        if "placement" in q or "interview" in q or "job" in q or "readiness" in q:
            areas_text = "\n".join([f"- {a}" for a in areas_to_improve]) if areas_to_improve else "- Strong profile balance across metrics."
            return (
                f"### Placement Readiness Report for {name}\n\n"
                f"**Overall Readiness Score**: **{placement_score:.1f}%**\n\n"
                f"#### Core Breakdown:\n"
                f"- **DSA & Coding**: {ctx.get('dsa_score', 70)}%\n"
                f"- **Core Programming**: {ctx.get('programming_score', 75)}%\n"
                f"- **Aptitude**: {ctx.get('aptitude_score', 65)}%\n"
                f"- **Communication**: {ctx.get('communication_score', 70)}%\n"
                f"- **Verified Projects**: {ctx.get('projects_count', 2)} project(s)\n\n"
                f"#### Priority Areas to Polish:\n{areas_text}\n\n"
                f"*Note: This is an internal preparation benchmark to guide your prep schedule before campus placement drives.*"
            )

        # 5. RAG / Vector DB / Placement technical explainer
        if "rag" in q or "vector" in q or "embedding" in q:
            return (
                f"### Technical Concept: Retrieval-Augmented Generation (RAG)\n\n"
                f"Here is how RAG operates in systems like **CampusIQ** (ideal for placement interview answers!):\n\n"
                f"1. **Why RAG?**: LLMs have static training cutoffs and lack private enterprise data (such as your college transcript). RAG dynamically grounds the LLM in private, real-time facts without retraining.\n"
                f"2. **Embeddings**: Text chunks (e.g., student marks, syllabus, policies) are converted into dense numerical vectors (e.g. 768 or 1536 dimensions) using models like `text-embedding-004`.\n"
                f"3. **Vector Database**: High-dimensional vectors are indexed in vector databases (e.g. ChromaDB, FAISS, Pinecone) using Approximate Nearest Neighbor (ANN) search algorithms.\n"
                f"4. **Retrieval**: When a student asks a query, the query vector is compared against document vectors using **Cosine Similarity** to retrieve top-k relevant context chunks.\n"
                f"5. **Augmented Generation**: The retrieved context + user prompt are combined and fed into the LLM, synthesizing a hallucination-free, contextual response."
            )

        # 6. Default general advisor response
        return (
            f"Hello {name}! I am **CampusAI**, your intelligent academic and placement mentor.\n\n"
            f"Here is a quick snapshot of your status:\n"
            f"- **CGPA**: {cgpa:.2f} | **Attendance**: {attendance:.1f}%\n"
            f"- **Academic Risk**: **{risk}**\n"
            f"- **Placement Readiness**: **{placement_score:.1f}%**\n\n"
            f"You can ask me:\n"
            f"- *'Which subjects should I focus on?'*\n"
            f"- *'Why is my academic risk {risk}?'*\n"
            f"- *'Create a study plan for me.'*\n"
            f"- *'How can I improve my placement readiness?'*\n"
            f"- *'Explain RAG and vector databases for my interview.'*"
        )

ai_engine = CampusAIEngine()
