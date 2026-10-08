# CampusIQ: Placement Interview & Technical Viva Guide

This comprehensive guide prepares you to explain every engineering decision, architectural choice, and machine learning concept in CampusIQ during technical interviews (e.g. for SDE, Full-Stack, and ML/AI roles).

---

## 1. System Overview & Problem Statement
**Q: What is CampusIQ and what problem does it solve?**
> "In most universities, academic data is siloed across separate departmental portals, ERPs, spreadsheets, and manual attendance registers. This fragmentation prevents institutions from identifying struggling students until semester results are already published—when it is too late for intervention.
> CampusIQ transforms raw academic records into an automated pipeline: **Data -> Analytics -> Insights -> Predictions -> Recommendations**. It offers role-based portals for Students, Faculty, and HODs, featuring an explainable ML Academic Risk Engine, What-If CGPA simulator, Placement Readiness scorecard, and a context-aware AI assistant."

---

## 2. Architecture & Backend Design
**Q: Why did you choose FastAPI over Flask or Django?**
> "1. **Asynchronous Throughput**: FastAPI is built on Starlette and ASGI, supporting high concurrency with Python `async`/`await`.
> 2. **Type Safety & Data Validation**: Built-in integration with Pydantic ensures automatic schema validation, serialized responses, and clear error responses with minimal boilerplate.
> 3. **Automatic OpenAPI/Swagger Docs**: Interactive API documentation at `/docs` speeds up frontend-backend integration and testing.
> 4. **Dependency Injection**: FastAPI's dependency injection system cleanly isolates database session lifecycles (`get_db`) and JWT role-based access checks (`require_role`)."

**Q: How is Authentication and Role-Based Access Control implemented?**
> "We implement OAuth2 Password Bearer flow with JWT (JSON Web Tokens). When a user logs in, their password is verified against a bcrypt salted hash. Upon successful verification, the backend generates an `HS256`-signed JWT containing the user's ID, role, and expiration timestamp.
> Protected API endpoints use FastAPI dependency injection (`Depends(require_role([...]))`) to intercept incoming requests, validate the token signature, and verify that the user's role is authorized before executing business logic."

---

## 3. Machine Learning & Explainability
**Q: Why did you choose Random Forest over Logistic Regression and Decision Trees?**
> "We evaluated all three algorithms on our academic failure dataset:
> 1. **Logistic Regression** achieved 84.7% accuracy. It assumes a linear relationship between features and log-odds of risk. However, academic risk involves complex feature interactions—for example, a student with borderline attendance (72%) who also has 2 uncleared backlogs exhibits compounded risk that linear hyperplanes underfit.
> 2. **Decision Trees** captured non-linear thresholds and achieved 92.3% accuracy, but suffered from high variance and was prone to overfitting on localized student data.
> 3. **Random Forest Classifier** achieved the highest performance: **94.7% accuracy with a 0.9498 Macro F1 score**. By aggregating 100 decorrelated decision trees trained on bootstrapped subsets, it suppresses variance, prevents overfitting, and outputs calibrated class probabilities.
> Most importantly, Random Forest natively yields **Gini Feature Importances** (Attendance: ~33.3%, Backlogs: ~24.5%, Previous CGPA: ~19.9%, Internal Marks: ~17.2%), which powers CampusIQ's Explainable AI diagnostics to clearly tell students and mentors *why* a risk tag was triggered."

**Q: How do you avoid ML being 'just for decoration'?**
> "In CampusIQ, the ML model is directly linked to actionable interventions. Rather than merely outputting a black-box label, the risk engine calculates specific driving factors (e.g., 'Attendance is below 65% university detention threshold in Database Systems') and immediately prescribes concrete steps (e.g., 'Requires attending next 12 consecutive hours to cross 75%'). This directly impacts faculty remarks and student study plans."

---

## 4. Artificial Intelligence & RAG
**Q: How does CampusAI work? Explain RAG.**
> "CampusAI acts as a personalized academic mentor. Rather than using a generic ChatGPT prompt, it employs Retrieval-Augmented Generation (RAG) principles:
> 1. **The Problem with Raw LLMs**: Standard foundation models do not know the student's real-time marks, attendance, or backlog count, and are prone to hallucinations.
> 2. **Context Construction & Retrieval**: When the student queries CampusAI, the backend pulls the authenticated student's real-time transcript, subject-wise attendance, risk factors, and placement breakdown, formulating a structured prompt context.
> 3. **Generation**: The augmented context is dispatched to the LLM (Google Gemini API), instructing it to provide empathetic, factual, and actionable guidance.
> 4. **Resilient Fallback**: If an API key is absent or offline, CampusIQ includes an internal expert system that parses intent and provides verified academic insights directly from the relational database."

**Q: What is the role of Vector Databases and Embeddings in RAG?**
> "In large-scale RAG systems with hundreds of syllabi and academic policy documents:
> - **Embeddings**: Text chunks are passed through an embedding model (e.g. `text-embedding-004`) to generate dense mathematical vectors in $n$-dimensional space where semantic similarity corresponds to geometric proximity.
> - **Vector Database**: Databases like ChromaDB, FAISS, or Pinecone index these vectors using indexing structures (like HNSW or IVF) for sub-millisecond retrieval.
> - **Similarity Search**: When a user submits a question, its vector is compared against document vectors using **Cosine Similarity**:
>   $$\text{Cosine Similarity} = \frac{A \cdot B}{\|A\| \|B\|}$$
> - The top-$k$ nearest document chunks are returned to augment the prompt."

---

## 5. Database & Full-Stack Engineering
**Q: How did you design the database schema?**
> "The database is structured in Third Normal Form (3NF) to eliminate redundancy:
> - A centralized `users` table handles authentication credentials and role flags.
> - Sub-tables `students` and `faculty` maintain 1-to-1 foreign key relationships to `users`.
> - `academic_records` creates a normalized associative entity linking `students` and `subjects`, recording continuous assessment (internals, assignments) and attendance.
> - Separate portfolio tables (`student_skills`, `student_projects`, `student_certifications`) allow 1-to-many scaling without inflating student entity records."

**Q: How did you develop the What-If Simulator?**
> "The simulator models real-world university credit weighting rules:
> $$\text{SGPA} = \frac{\sum (\text{Credits}_i \times \text{GradePoint}_i)}{\sum \text{Credits}_i}$$
> It allows students to test hypothetical scenarios—such as 'What if I score 85 in Python and 80 in DBMS?'—and projects the resulting cumulative CGPA. It also includes an attendance threshold solver that computes the minimum number of upcoming classes needed to hit the mandatory 75% cutoff."
