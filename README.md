# CampusIQ – College Academic Intelligence & Student Success Platform

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?style=flat)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **CampusIQ** transitions conventional academic college management from static record-keeping into an intelligent, data-driven student success ecosystem:  
> **DATA &rarr; ANALYTICS &rarr; INSIGHTS &rarr; PREDICTIONS &rarr; RECOMMENDATIONS**

---

## 1. Problem Statement & Motivation
Universities generate enormous volumes of academic telemetry—attendance patterns, continuous internal assessments, assignment submissions, semester GPAs, backlog counts, and technical placement skills. However, this critical data is traditionally siloed across disjointed spreadsheets and ERP portals.

Institutions typically identify academic failures and student attrition **retrospectively**, after semester-end exams when remedial intervention is impossible. Furthermore, students lack quantitative visibility into their placement readiness and cumulative GPA trajectories.

**CampusIQ** solves this institutional challenge by unifying collegiate records into an intelligent full-stack portal featuring:
- **ML Early Risk Intervention**: Predicting academic failure probability before exams using Random Forest classification.
- **Explainable AI (XAI)**: Diagnosing driving risk factors and prescribing customized remedial actions.
- **Credit-Weighted What-If Simulator**: Projecting semester SGPA, cumulative CGPA, and minimum attendance thresholds.
- **Placement Readiness Scorecard**: Multi-metric benchmarking across DSA, coding, aptitude, communication, and verified projects.
- **CampusAI Assistant**: RAG-inspired contextual mentor providing personalized academic advice based on real-time transcripts.

---

## 2. High-Level System Architecture

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

## 3. Core Features by Role

### 🎓 Student Portal (Persona: Kasturi - Final Year CSE)
- **Academic KPI Cards**: Real-time display of CGPA (8.10), Attendance (84.3%), Backlogs (0), Academic Risk Badge, and Placement Readiness (78%).
- **Subject-Wise Analytics**: Continuous tracking of internal marks (out of 50), assignments (out of 25), and final exams across enrolled courses (Python, DBMS, OS, ML, Networks).
- **Weak Subject Diagnostics**: Automated alerts identifying courses with internal marks below 50% or attendance below 75%.
- **What-If Academic Simulator**:
  - Interactive simulator modeling projected SGPA and cumulative CGPA based on expected exam scores.
  - Target CGPA solver calculating the exact SGPA needed across remaining semesters.
  - Attendance threshold calculator determining consecutive classes needed to cross the mandatory 75% cutoff.
- **Placement Readiness Scorecard**: Multi-criteria radar chart evaluating DSA (70%), Programming (80%), Aptitude (65%), Communication (75%), and Verified Projects (90%) with targeted deficit diagnostics.
- **Portfolio Management**: CRUD operations for technical skills, verified GitHub projects, and certifications.
- **Faculty Remarks**: Real-time feed of qualitative mentorship feedback from professors.

### 👨‍🏫 Faculty Portal (Persona: Prof. Priya Menon - DBMS & OS)
- **Subject Management**: Overview of assigned courses, total enrolled students, and class averages.
- **Early Warning Metrics**: Automated alerts for students with attendance below 75% or internal marks below 50%.
- **Class Roster & Evaluation Console**: Inline editing of internal marks, assignments, final marks, and attendance records.
- **At-Risk Radar**: Instant identification of students categorized as HIGH or MEDIUM risk.
- **Qualitative Mentorship**: Direct submission of academic remarks linked to student profiles.

### 🏛️ Executive Admin / HOD Portal (Persona: Dr. K. S. Murthy - Dean & HOD)
- **Institutional Analytics**: College-wide mean CGPA, attendance averages, pass percentages, and total students at risk.
- **Department Benchmarking**: Cross-departmental comparisons across CSE, IT, and ECE.
- **Risk Distribution Heatmap**: Real-time donut chart visualizing Low vs. Medium vs. High risk student proportions.
- **Comprehensive Student Directory**: Searchable, filterable student roster with risk classification and placement indicators.

---

## 4. Machine Learning: Academic Risk Prediction

### Problem Formulation
Multiclass classification predicting student academic risk: `LOW`, `MEDIUM`, or `HIGH` based on 5 features:
1. `attendance_pct` (35% - 99%)
2. `internal_pct` (20% - 98%)
3. `assignment_pct` (25% - 100%)
4. `previous_cgpa` (4.0 - 9.9)
5. `backlogs` (0 - 6 uncleared courses)

### Model Comparison & Justification
| Model | Test Accuracy | Macro F1-Score | Architectural Justification |
| :--- | :---: | :---: | :--- |
| **Logistic Regression** | 84.67% | 0.8466 | Linear hyperplane underfits compound non-linear risk interactions. |
| **Decision Tree** | 92.33% | 0.9266 | Interpretable split rules, but exhibits high variance on smaller cohorts. |
| **Random Forest (Selected)** | **94.67%** | **0.9498** | Ensembles 100 decorrelated trees; optimal generalization & Gini explainability. |

### Explainable AI (Gini Feature Importances)
- **Attendance Percentage**: **33.31%** (Primary driver of exam eligibility & detentions)
- **Active Backlogs**: **24.52%** (Compounding factor for academic overload)
- **Previous CGPA**: **19.86%** (Baseline academic capability indicator)
- **Internal Assessment**: **17.17%** (Midterm exam mastery)
- **Assignment Submissions**: **5.15%** (Continuous lab & coursework engagement)

---

## 5. Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, Vite, Tailwind CSS, Lucide Icons, Recharts |
| **Backend** | Python 3.11+, FastAPI, Pydantic v2, Uvicorn, ASGI |
| **Database & ORM**| SQLite (Development) / PostgreSQL (Production), SQLAlchemy 2.0 |
| **Security & Auth** | OAuth2 Password Bearer, JWT (`HS256`), Bcrypt salted hashing |
| **Machine Learning**| Scikit-learn, Pandas, NumPy, Joblib |
| **GenAI / LLM** | Google Gemini API with intelligent context injection & offline fallback |

---

## 6. Quick Start & Local Setup

### Prerequisites
- Python 3.10+ installed
- Node.js v18+ and npm installed

### 1. Clone the Repository
```bash
git clone https://github.com/kasturi-neppali/CampusIQ.git
cd CampusIQ
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Seed database with realistic collegiate records
python app/seed_data.py

# Train and benchmark ML Risk Model
python ../ml/train_risk_model.py

# Launch FastAPI Server
uvicorn main:app --reload --port 8000
```
*Backend API documentation will be accessible at: `http://127.0.0.1:8000/docs`*

### 3. Frontend Setup
```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install npm dependencies
npm install

# Start Vite Development Server
npm run dev
```
*Frontend application will be accessible at: `http://localhost:5173`*

---

## 7. Demo Credentials

For zero-friction demonstration during placement interviews, one-click demo logins are available on the login page:

| Role | Email | Password | Persona Details |
| :--- | :--- | :--- | :--- |
| **Student** | `kasturi@campusiq.edu` | `Student@123` | Kasturi Neppali (8.1 CGPA, 0 Backlogs, CSE Final Year) |
| **Faculty** | `faculty.menon@campusiq.edu` | `Faculty@123` | Prof. Priya Menon (Associate Professor, DBMS & OS) |
| **Admin / HOD**| `admin@campusiq.edu` | `Admin@123` | Dr. K. S. Murthy (Dean of Academics & HOD) |

---

## 8. REST API Reference

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/login` | Public | Authenticates credentials and returns JWT bearer token |
| `GET` | `/api/student/dashboard` | Student, Admin | Retrieves student KPI metrics, subject records, risk & placement scores |
| `POST` | `/api/student/skills` | Student | Adds verified skill to student portfolio |
| `GET` | `/api/faculty/dashboard` | Faculty, Admin | Retrieves class averages, low attendance alerts, and assigned subjects |
| `GET` | `/api/faculty/subject/{id}/students` | Faculty, Admin | Returns enrolled student roster with marks and attendance |
| `PUT` | `/api/faculty/record/{id}/marks` | Faculty, Admin | Updates continuous assessment or final exam marks |
| `GET` | `/api/admin/overview` | Admin | Returns college-wide enrollment, CGPA, and risk distribution |
| `POST` | `/api/risk/predict` | Authenticated | Runs Scikit-learn Random Forest model inference with explainability |
| `POST` | `/api/simulator/simulate` | Student, Admin | Runs credit-weighted SGPA/CGPA and attendance threshold solver |
| `POST` | `/api/ai/chat` | Authenticated | Dispatches student query to CampusAI contextual advisor |

---

## 9. Placement Viva & Interview Resources
Comprehensive documentation has been prepared to help you excel in technical interviews:
- [`docs/architecture.md`](docs/architecture.md): Full technical architecture and system component diagrams.
- [`docs/interview_preparation.md`](docs/interview_preparation.md): Placement viva cheat sheet covering ML model selection, RAG vs. Fine-Tuning, database normalization, and security design.
- [`docs/resume_bullet_points.md`](docs/resume_bullet_points.md): Tailored resume descriptions for SDE, Full-Stack, and ML roles.

---

## 10. License
This project is open-source and licensed under the [MIT License](LICENSE).
