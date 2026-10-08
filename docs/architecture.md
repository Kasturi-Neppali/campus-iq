# CampusIQ – System Architecture & Technical Specifications

CampusIQ is an enterprise College Academic Intelligence & Student Success Platform designed to convert scattered institutional data into predictive interventions and placement readiness insights.

---

## 1. High-Level System Architecture

```
                                  +---------------------------------------+
                                  |            React 18 + Vite            |
                                  |   Tailwind CSS / Lucide / Recharts    |
                                  +-------------------+-------------------+
                                                      |
                                                      | HTTPS / REST API
                                                      | (Bearer JWT Auth)
                                                      v
                                  +---------------------------------------+
                                  |          FastAPI REST Engine          |
                                  |    (Uvicorn / Pydantic v2 / CORS)     |
                                  +---+---------------+---------------+---+
                                      |               |               |
           +--------------------------+   +-----------+--+     +------+------------------+
           |                              |              |     |                         |
           v                              v              v     v                         v
+--------------------+        +---------------+   +-------------------+    +--------------------+
| SQLAlchemy 2.0 ORM |        | Scikit-Learn  |   | What-If Simulator |    | CampusAI Assistant |
| Relational Storage |        | Random Forest |   | Credit-Weighted   |    | Contextual RAG /   |
| (SQLite / Postgres)|        | Risk Engine   |   | SGPA & CGPA Calc  |    | Gemini API Fallback|
+--------------------+        +---------------+   +-------------------+    +--------------------+
```

---

## 2. Core Subsystems

### A. Authentication & Role-Based Access Control (RBAC)
- **Token Format**: Standard RFC 7519 JSON Web Tokens (JWT) signed using HMAC-SHA256 (`HS256`).
- **Roles**:
  - `student`: Access to personal academic records, What-If simulator, placement readiness, portfolio manager, and CampusAI assistant.
  - `faculty`: Access to assigned courses, class rosters, marks entry, attendance updates, at-risk student tracking, and remarks.
  - `admin` (Dean / HOD): Institutional-level analytics, department comparisons, pass percentage heatmaps, college-wide student & faculty directories.

### B. Machine Learning Academic Risk Engine
- **Objective**: Identify students at risk of semester-end failure, low attendance detention, or graduation delay.
- **Model Comparison & Benchmark**:
  - *Logistic Regression*: 84.67% accuracy. Linear hyperplane fails to capture compound interactions (e.g., high marks compensating for borderline attendance).
  - *Decision Tree*: 92.33% accuracy. Interpretable thresholds but sensitive to data variance.
  - *Random Forest Classifier (Selected)*: **94.67% accuracy, 0.9498 Macro F1**. Ensembles 100 decorrelated decision trees, mitigating overfitting.
- **Explainability**: Natively surfaces Gini feature importances (`attendance_pct: 33.3%`, `backlogs: 24.5%`, `previous_cgpa: 19.9%`, `internal_pct: 17.2%`) and maps risk levels to targeted remediation steps.

### C. What-If CGPA & Academic Simulator
- **University Credit Weighting Formula**:
  $$\text{SGPA} = \frac{\sum (\text{Credits}_i \times \text{GradePoint}_i)}{\sum \text{Credits}_i}$$
  $$\text{CGPA}_{\text{new}} = \frac{(\text{CGPA}_{\text{prev}} \times \text{Credits}_{\text{prev}}) + (\text{SGPA}_{\text{proj}} \times \text{Credits}_{\text{curr}})}{\text{Credits}_{\text{prev}} + \text{Credits}_{\text{curr}}}$$
- **Target Feasibility Solver**: Computes minimum required SGPA across remaining semesters to reach a target CGPA. Flags mathematically impossible targets when required SGPA exceeds 10.0.
- **Attendance Threshold Projection**: Solves minimum consecutive classes needed to cross the mandatory 75% cutoff:
  $$k = \lceil \frac{0.75 \times T - A}{0.25} \rceil$$

### D. CampusAI Contextual Advisor & RAG
- **Dynamic Context Injection**: Grounds the LLM by pulling the student's real-time transcript, backlogs, weak subjects, and placement scores.
- **Dual-Mode Engine**: Connects to Google Gemini API when configured, with an offline-deterministic expert system fallback for zero-downtime interview demos.
