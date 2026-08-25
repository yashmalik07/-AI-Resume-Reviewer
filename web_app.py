"""Interactive Web Dashboard for AI Resume Reviewer
Task ID: AI-SS-004 | Data Alcott Systems | Yash Malik (DAS005423)
Built with Streamlit and Plotly.
"""

import json
import os
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from app.analyzer import ResumeReviewer


# --- Page Configuration ---
st.set_page_config(
    page_title="AI Resume Reviewer | Data Alcott Systems",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #F8FAFC, #EDF2F7);
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #2563EB;
    }
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
    }
    .pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.82rem;
        font-weight: 600;
        margin: 3px;
    }
    .pill-tech {
        background-color: #DBEAFE;
        color: #1E40AF;
    }
    .pill-soft {
        background-color: #DCFCE7;
        color: #166534;
    }
    .pill-missing {
        background-color: #FEE2E2;
        color: #991B1B;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_reviewer():
    return ResumeReviewer()


reviewer = get_reviewer()

# --- Sidebar ---
st.sidebar.image("https://img.icons8.com/color/96/000000/resume.png", width=70)
st.sidebar.title("AI Resume Reviewer")
st.sidebar.caption("Free Online AI & Data Science Internship | Task AI-SS-004")

st.sidebar.markdown("---")
st.sidebar.markdown("**Student Information**")
st.sidebar.text("Student Name : Yash Malik")
st.sidebar.text("Student Code : DAS005423")
st.sidebar.text("Task ID      : AI-SS-004")
st.sidebar.text("Domain       : Student Support NLP")
st.sidebar.text("Company      : Data Alcott Systems")

st.sidebar.markdown("---")
st.sidebar.subheader("📥 Input Resume")

# Sample Resumes Selector
sample_dir = os.path.join(os.path.dirname(__file__), "sample_resumes")
sample_files = {}
if os.path.exists(sample_dir):
    for f in os.listdir(sample_dir):
        if f.endswith(".txt"):
            label = f.replace(".txt", "").replace("_", " ").title()
            sample_files[label] = os.path.join(sample_dir, f)

input_mode = st.sidebar.radio("Choose Input Method", ["Upload File (PDF/DOCX/TXT)", "Use Sample Resume", "Paste Text"])

resume_text_content = ""
uploaded_filename = ""

if input_mode == "Upload File (PDF/DOCX/TXT)":
    uploaded_file = st.sidebar.file_uploader("Upload Resume File", type=["pdf", "docx", "txt"])
    if uploaded_file:
        uploaded_filename = uploaded_file.name
        resume_text_content = uploaded_file

elif input_mode == "Use Sample Resume":
    if sample_files:
        chosen_sample = st.sidebar.selectbox("Select Sample Resume", list(sample_files.keys()))
        with open(sample_files[chosen_sample], "r", encoding="utf-8", errors="ignore") as sf:
            resume_text_content = sf.read()
            uploaded_filename = chosen_sample + ".txt"
    else:
        st.sidebar.warning("No sample resumes found.")

else:
    resume_text_content = st.sidebar.text_area("Paste Resume Text Here", height=250)
    uploaded_filename = "pasted_resume.txt"

# Optional Job Description
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Optional Job Description")
enable_jd = st.sidebar.checkbox("Compare with Job Description", value=False)
jd_text = ""
if enable_jd:
    jd_text = st.sidebar.text_area(
        "Paste Job Description / Requirements",
        placeholder="e.g. Seeking Senior Python Engineer with 4+ years of AWS, Docker, Kubernetes, and PostgreSQL experience...",
        height=150
    )


# --- Main Dashboard ---
st.markdown('<div class="main-header">📄 Intelligent AI Resume Reviewer & ATS Optimizer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated NLP and Machine Learning resume evaluation, scoring, and ATS diagnostics</div>', unsafe_allow_html=True)

if not resume_text_content:
    st.info("👈 Please upload a resume file (.pdf, .docx, .txt), select a sample resume, or paste text in the sidebar to run analysis.")
    st.stop()

# Run Analysis
with st.spinner("Analyzing resume using NLP pipeline..."):
    result = reviewer.analyze_resume(
        resume_text_content,
        job_description=jd_text if enable_jd else None,
        filename=uploaded_filename
    )

scoring = result["scoring"]
skills = result["skills"]
exp = result["experience"]
edu = result["education"]
ats = result["ats_compatibility"]
feedback = result["feedback"]
jd = result["job_match"]
stats = result["statistics"]

# --- Top KPI Summary Cards ---
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{scoring['total_score']} / 100</div>
        <div class="metric-label">Overall Score ({scoring['letter_grade'].split()[0]})</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{ats['ats_score']} / 100</div>
        <div class="metric-label">ATS Compatibility</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{skills['technical_count']}</div>
        <div class="metric-label">Tech Skills Found</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">~{exp['years']} Yrs</div>
        <div class="metric-label">Experience ({exp['seniority_level'].split()[0]})</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    if jd and jd.get("is_active"):
        jd_val = f"{jd['match_score']}%"
        jd_label = "JD Alignment"
    else:
        jd_val = f"{stats['word_count']}"
        jd_label = "Word Count"

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{jd_val}</div>
        <div class="metric-label">{jd_label}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Tabbed Navigation ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Overview & Scoring",
    "🛠️ Skills Analysis",
    "💼 Experience & Impact",
    "🎓 Education",
    "🤖 ATS Audit",
    "🎯 Job Matcher",
    "📄 Raw Text & JSON"
])

# --- TAB 1: Overview & Scoring ---
with tab1:
    col_chart, col_feed = st.columns([1, 1.2])

    with col_chart:
        st.subheader("Category Scoring Rubric")
        categories_data = scoring["categories"]
        cat_names = [k.replace("_", " ").title() for k in categories_data.keys()]
        cat_scores = [v["score"] for v in categories_data.values()]
        cat_maxes = [v["max"] for v in categories_data.values()]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=cat_names,
            x=cat_scores,
            orientation='h',
            name='Earned Points',
            marker=dict(color='#2563EB', opacity=0.85),
            text=[f"{s}/{m}" for s, m in zip(cat_scores, cat_maxes)],
            textposition='auto'
        ))
        fig.update_layout(
            title="Score Breakdown by Evaluation Pillar",
            xaxis=dict(title="Points Earned", range=[0, 35]),
            yaxis=dict(autorange="reversed"),
            height=340,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_feed:
        st.subheader("Actionable Recommendations")
        
        st.markdown("##### 🚀 Top 3 Prioritized Next Steps:")
        for idx, step in enumerate(feedback["prioritized_next_steps"], 1):
            st.info(f"**Step {idx}:** {step}")

        st.markdown("##### 🌟 Key Strengths Identified:")
        for s in feedback["strengths"]:
            st.success(s)

        if feedback["areas_for_improvement"]:
            st.markdown("##### ⚠️ Areas for Improvement:")
            for imp in feedback["areas_for_improvement"]:
                st.warning(imp)

# --- TAB 2: Skills Analysis ---
with tab2:
    st.subheader("🛠️ Technical & Soft Skills Extraction")

    col_s1, col_s2 = st.columns([1.5, 1])

    with col_s1:
        st.markdown("#### Categorized Technical Competencies")
        categorized = skills["categorized_technical"]
        for cat, items in categorized.items():
            if items:
                st.markdown(f"**{cat.replace('_', ' ').title()}:**")
                pills_html = " ".join([f'<span class="pill pill-tech">{item}</span>' for item in items])
                st.markdown(pills_html, unsafe_allow_html=True)
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        st.markdown("#### Soft & Leadership Skills")
        if skills["soft_skills"]:
            soft_pills = " ".join([f'<span class="pill pill-soft">{s}</span>' for s in skills["soft_skills"]])
            st.markdown(soft_pills, unsafe_allow_html=True)
        else:
            st.info("No explicit soft skills detected. Consider adding communication, leadership, or teamwork.")

    with col_s2:
        st.markdown("#### Domain Coverage Distribution")
        coverage = skills["category_coverage"]
        df_cov = pd.DataFrame(list(coverage.items()), columns=["Category", "Count"])
        df_cov["Category"] = df_cov["Category"].str.replace("_", " ").str.title()
        
        fig_pie = px.pie(
            df_cov,
            values="Count",
            names="Category",
            hole=0.4,
            title="Skill Domain Diversity"
        )
        fig_pie.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

# --- TAB 3: Experience & Impact ---
with tab3:
    st.subheader("💼 Experience, Impact & Verb Strength")

    col_e1, col_e2 = st.columns(2)

    with col_e1:
        st.markdown("#### Career Timeline & Seniority")
        st.write(f"**Estimated Tenure:** ~{exp['years']} Years")
        st.write(f"**Assessed Level:** {exp['seniority_level']}")
        st.write(f"**Work History Signals:** {'✅ Detected' if exp['has_experience'] else '❌ Missing'}")

        st.markdown("#### 📈 Quantified Achievements Detected")
        if exp["quantified_metrics"]:
            for metric in exp["quantified_metrics"]:
                st.write(f"• `{metric}`")
        else:
            st.warning("No quantified metrics (%, $, numbers) detected. Add measurable results!")

    with col_e2:
        st.markdown("#### ⚡ Action Verbs Analysis")
        verbs = exp["action_verbs"]
        st.metric("Strong Action Verbs Found", verbs["strong_verbs_count"])
        if verbs["strong_verbs"]:
            st.write(f"**Strong Verbs Used:** {', '.join(verbs['strong_verbs'])}")
        
        if verbs["weak_phrases"]:
            st.error(f"**Passive/Weak Phrases Detected:** {', '.join(verbs['weak_phrases'])}")
            st.caption("Replace passive duties with powerful action verbs.")

# --- TAB 4: Education ---
with tab4:
    st.subheader("🎓 Educational Qualifications")
    st.write(f"**Highest Degree Level Detected:** {edu['highest_degree_level'].replace('_', ' ').title()}")
    
    if edu["majors_found"]:
        st.write(f"**Field of Study / Major:** {', '.join(edu['majors_found'])}")
    if edu["institutions_found"]:
        st.write(f"**Institutions Identified:** {', '.join(edu['institutions_found'])}")
    if edu["gpa_or_grade"]:
        st.write(f"**Academic Grade / GPA:** {edu['gpa_or_grade']}")

    if not edu["has_education"]:
        st.error("No formal education information was detected. Ensure degree and university names are listed.")

# --- TAB 5: ATS Audit ---
with tab5:
    st.subheader("🤖 Applicant Tracking System (ATS) Diagnostic")
    
    col_a1, col_a2 = st.columns(2)

    with col_a1:
        st.markdown("#### 📇 Contact Information Verification")
        contact = ats["contact_info"]
        st.write(f"• **Email Address:** {'✅ ' + contact['email'] if contact['has_email'] else '❌ Missing'}")
        st.write(f"• **Phone Number:** {'✅ ' + contact['phone'] if contact['has_phone'] else '❌ Missing'}")
        st.write(f"• **LinkedIn Profile:** {'✅ ' + contact['linkedin'] if contact['has_linkedin'] else '❌ Missing'}")
        st.write(f"• **GitHub / Portfolio:** {'✅ ' + contact['github'] if contact['has_github'] else '❌ Missing'}")

        st.markdown("#### 📑 Standard Section Headers")
        sections_audit = ats["section_audit"]
        st.write(f"**Present Sections:** {', '.join([s.title() for s in sections_audit['present_sections']])}")
        if sections_audit["missing_required"]:
            st.error(f"**Missing Required Sections:** {', '.join([s.title() for s in sections_audit['missing_required']])}")

    with col_a2:
        st.markdown("#### 📏 Length & Formatting Hygiene")
        formatting = ats["formatting_audit"]
        st.write(f"• **Word Count:** {stats['word_count']} words")
        st.write(f"• **Bullet Points:** {formatting['bullet_count']} bullet items detected")
        
        for s in formatting["formatting_strengths"]:
            st.success(s)
        for issue in formatting["formatting_issues"]:
            st.warning(issue)

# --- TAB 6: Job Matcher ---
with tab6:
    st.subheader("🎯 Job Description Alignment & TF-IDF Cosine Similarity")
    
    if jd and jd.get("is_active"):
        col_j1, col_j2 = st.columns([1, 1.5])
        with col_j1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=jd["match_score"],
                title={'text': "Job Alignment Score"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#2563EB"},
                    'steps': [
                        {'range': [0, 50], 'color': "#FEE2E2"},
                        {'range': [50, 75], 'color': "#FEF3C7"},
                        {'range': [75, 100], 'color': "#DCFCE7"}
                    ]
                }
            ))
            fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col_j2:
            st.write(f"**Match Status:** {jd['match_level']}")
            st.write(f"**TF-IDF Cosine Similarity:** {jd['cosine_similarity']}%")
            st.write(f"**Target Keyword Coverage:** {jd['keyword_coverage']}%")

            st.markdown("##### ✅ Matched Job Keywords:")
            matched_html = " ".join([f'<span class="pill pill-tech">{kw}</span>' for kw in jd["matched_keywords"]])
            st.markdown(matched_html, unsafe_allow_html=True)

            st.markdown("##### ❌ Missing / Recommended Target Keywords:")
            missing_html = " ".join([f'<span class="pill pill-missing">{kw}</span>' for kw in jd["missing_keywords"]])
            st.markdown(missing_html, unsafe_allow_html=True)
    else:
        st.info("ℹ️ To check job description compatibility, enable 'Compare with Job Description' in the sidebar and paste target job requirements.")

# --- TAB 7: Raw Text & JSON Export ---
with tab7:
    st.subheader("📄 Raw Data & Exportable Report")
    
    json_export = json.dumps(result, indent=2)
    st.download_button(
        label="💾 Download Full Analysis Report (JSON)",
        data=json_export,
        file_name="resume_analysis_report.json",
        mime="application/json"
    )

    with st.expander("View Clean Extracted Text"):
        st.text(result["raw_text"])

    with st.expander("View Full Raw JSON Response"):
        st.json(result)

