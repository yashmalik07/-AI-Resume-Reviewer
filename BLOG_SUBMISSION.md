# Blog Post Submission: AI Resume Reviewer

**Category**: Task Submit  
**Title**: AI Resume Reviewer - DAS005423  
**Author**: Yash Malik (Student Code: `DAS005423`)  
**Task ID**: `AI-SS-004`  
**Domain**: Student Support & Internship Management NLP  
**Company**: Data Alcott Systems ([www.dataalcott.com](https://www.dataalcott.com))  

---

## 🔗 Project Links
- **GitHub Repository**: `https://github.com/your-username/ai-resume-reviewer` *(Replace with your actual GitHub repository URL)*
- **YouTube Video Demo**: `https://www.youtube.com/watch?v=your-video-id` *(Replace with your uploaded demo video link)*
- **Internship Platform**: [Free Internships](https://www.freeinternships.in/)

---

## 📖 Introduction & Overview
In today’s competitive job market, more than 75% of resumes are filtered out by automated **Applicant Tracking Systems (ATS)** before a recruiter ever reads them. Common pitfalls include non-standard section headers, vague passive descriptions without metrics, and poor alignment with target job requirements.

As part of my **Free Online AI & Data Science Internship at Data Alcott Systems**, I designed and built the **AI Resume Reviewer** (`Task ID: AI-SS-004`). This system uses Natural Language Processing (NLP) and Machine Learning to parse, analyze, and score resumes, providing actionable feedback and ATS diagnostics to help candidates land more interviews.

---

## 🛠️ Key Features Implemented

1. **Multi-Format Resume Ingestion**: Automatically parses text from PDF, DOCX, and TXT files.
2. **NLP Preprocessing & Segmentation**: Cleans text, tokenizes, performs lemmatization using NLTK `WordNetLemmatizer`, and segments sections (Experience, Education, Skills, Projects, Certifications).
3. **Hierarchical Skill Taxonomy**: Extracts technical skills across 6 domains (Programming, Data Science & AI, Web Development, Cloud & DevOps, Databases, Tools) alongside leadership and soft skills.
4. **Experience & Action Verb Engine**: Calculates tenure, identifies strong action verbs vs. passive phrases, and extracts quantified impact metrics (%, $, scale).
5. **Academic & Degree Classifier**: Classifies degrees (Ph.D., Master's, Bachelor's), majors, universities, and GPA.
6. **ATS Compatibility Diagnostic**: Audits contact details, standard header compliance, word count, and formatting hygiene.
7. **Job Description (JD) Alignment**: Employs Scikit-learn's **TF-IDF Vectorizer** and **Cosine Similarity** to match resumes against target job descriptions and highlight missing keywords.
8. **100-Point Composite Scoring Engine**: Provides transparent category-by-category scores and letter grades.
9. **Interactive Streamlit Web Dashboard & CLI**: Full graphical user interface with real-time score gauges, plotly charts, and batch processing CLI.

---

## 🏗️ Architecture & Pipeline Flow

```
Resume (PDF/DOCX/TXT) ➡️ Text Parser ➡️ NLP Cleaning & Segmentation
       ⬇️
  [ Skill Extractor ] + [ Experience Analyzer ] + [ Education Classifier ] + [ ATS Checker ]
       ⬇️
  [ TF-IDF Job Description Matcher (Cosine Similarity) ]
       ⬇️
  [ Composite Scoring Engine (0-100 Rubric) ]
       ⬇️
  [ Actionable Feedback & Prioritized Steps ]
       ⬇️
  [ Streamlit Web Dashboard & CLI Output ]
```

---

## 📸 Project Screenshots

*(Include 5+ screenshots here from your Streamlit dashboard and CLI demo)*

1. **Dashboard Overview & Score Breakdown**:
   ![Dashboard Overview](screenshots/dashboard_overview.png)

2. **Categorized Skills Extraction & Domain Distribution**:
   ![Skills Analysis](screenshots/skills_analysis.png)

3. **Experience, Action Verbs & Quantified Impact**:
   ![Experience Analysis](screenshots/experience_impact.png)

4. **ATS Compatibility & Hygiene Audit**:
   ![ATS Audit](screenshots/ats_audit.png)

5. **Job Description Alignment & TF-IDF Cosine Matcher**:
   ![JD Matcher](screenshots/jd_matcher.png)

6. **CLI Batch Processing Output**:
   ![CLI Terminal Output](screenshots/cli_terminal.png)

---

## 📊 Sample Analysis Results

Here is a summary of how the system evaluated sample resumes:

| Resume Profile | Overall Score | Letter Grade | ATS Score | Skills Detected | Seniority Level |
|---|:---:|:---:|:---:|:---:|:---:|
| **Senior Software Engineer** | **88.5 / 100** | A (Excellent) | 80 / 100 | 18 skills | Senior / Lead |
| **Entry-Level Data Scientist** | **82.0 / 100** | A (Excellent) | 82 / 100 | 16 skills | Entry-Level |
| **Mid-Level Product Manager** | **76.5 / 100** | B+ (Very Good) | 78 / 100 | 11 skills | Mid-Level |
| **Weak / Incomplete Resume** | **28.5 / 100** | F (Needs Overhaul) | 35 / 100 | 2 skills | Entry-Level |

---

## 💡 What I Learned During This Task
- How to structure NLP pipelines for unstructured resume text.
- Implementing n-gram matching with boundary conditions to avoid false-positive keyword matches.
- Using TF-IDF and Cosine Similarity for semantic matching between resumes and job specifications.
- Building interactive, responsive web applications with Streamlit and Plotly for real-time AI tools.
- Writing modular, test-driven Python code with automated `unittest` suites.

---

## 🚀 How to Run the Project Locally

```bash
# 1. Clone the repository
git clone https://github.com/your-username/ai-resume-reviewer.git
cd ai-resume-reviewer

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the Streamlit Web Application
streamlit run web_app.py

# 5. Run tests
python -m unittest tests/test_reviewer.py
```

---

## ✅ Submission Checklist
- [x] Complete resume analysis engine in Python
- [x] Skill extraction with multi-category taxonomy
- [x] Experience extraction & action verbs analysis
- [x] Education extraction & GPA detection
- [x] Resume scoring algorithm working
- [x] Actionable feedback generation implemented
- [x] Clean and documented codebase
- [x] GitHub Repository created with `README.md`
- [x] Project report written (`PROJECT_REPORT.md`)
- [x] Video demonstration script prepared
- [x] Blog post formatted for Task Submit category

