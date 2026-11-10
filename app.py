import streamlit as st
from services.cover_letter_generator import create_cover_letter
from services.pdf_utils import extract_text
from prompts import resume_prompt
from services.ai import analyze_resume
from components.resume_renderer import render_resume

# ===========================================
# PAGE CONFIG
# ===========================================

st.set_page_config(
    page_title="ResumeAI Pro",
    page_icon="🚀",
    layout="wide"
)

# ===========================================
# SESSION STATE
# ===========================================

defaults = {
    "analysis_result": None,
    "resume_text": "",
    "current_resume": "",
    "job_description": "",
    "accepted_changes": []}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ===========================================
# SIDEBAR
# ===========================================

with st.sidebar:

    st.title("🚀 ResumeAI Pro")

    st.markdown("---")

    st.markdown("""
### Features

✅ ATS Analysis

✅ Resume Rewrite

✅ Missing Skills

✅ Missing Keywords

✅ Cover Letter

✅ Interview Questions

✅ Hiring Decision

✅ DOCX Export

🔜 PDF Export

🔜 LinkedIn Optimizer
""")

    st.markdown("---")

    st.caption("Version 2.0")

# ===========================================
# HEADER
# ===========================================

st.title("🚀 ResumeAI Pro")

st.subheader("AI-Powered ATS Resume Optimizer")

st.write("""
Upload your resume, paste a job description,
and let AI analyze, improve and optimize your CV.
""")

# ===========================================
# FILE UPLOAD
# ===========================================

uploaded_file = st.file_uploader(
    "📄 Upload Resume (PDF)",
    type=["pdf"]
)

# ===========================================
# JOB DESCRIPTION
# ===========================================

job_description = st.text_area(
    "💼 Job Description",
    value=st.session_state.job_description,
    height=220
)

st.session_state.job_description = job_description

# ===========================================
# READ RESUME
# ===========================================

if uploaded_file:

    resume_text = extract_text(uploaded_file)

    st.session_state.resume_text = resume_text

    st.success("✅ Resume uploaded successfully!")

    with st.expander("Resume Preview"):

        render_resume(
            st.session_state.current_resume,
            "Modern"
    )

# ===========================================
# ANALYZE BUTTON
# ===========================================

analyze_clicked = st.button(
    "🚀 Analyze Resume",
    use_container_width=True
)

if analyze_clicked:

    if uploaded_file is None:

        st.warning("Please upload a resume.")

        st.stop()

    if not job_description.strip():

        st.warning("Please paste a job description.")

        st.stop()

    with st.spinner("🤖 AI is analyzing your resume..."):

        prompt = resume_prompt(
            st.session_state.resume_text,
            st.session_state.job_description
        )

        try:

            result = analyze_resume(prompt)

            st.session_state.analysis_result = result
            st.session_state.current_resume = result.optimized_resume

            st.session_state.accepted_changes = []

        except Exception as e:

            st.error(f"❌ {e}")

            st.stop()

# ===========================================
# SHOW RESULTS
# ===========================================

if st.session_state.analysis_result:

    result = st.session_state.analysis_result

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 ATS Dashboard",
        "📄 Resume Studio",
        "💌 Cover Letter",
        "🎤 Interview",
        "📥 Downloads"
    ]
)

    st.success("✅ Analysis Completed!")

    # ===========================================
    # ATS DASHBOARD
    # ===========================================

    with tab1:
        st.divider()

        st.header("📊 ATS Dashboard")

        accepted = len(st.session_state.accepted_changes)
        total = len(result.changes)

        progress = accepted / total if total else 0

        live_score = int(
            result.ats_score +
            (result.improved_score - result.ats_score) * progress
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Current ATS Score",
                f"{live_score}%"
            )

        with col2:
            st.metric(
                "Potential ATS Score",
                f"{result.improved_score}%"
            )

        with col3:
            st.metric(
                "Overall Rating",
                result.overall_rating
            )

        st.progress(live_score / 100)

        st.divider()

        # ===========================================
        # STRENGTHS
        # ===========================================

        st.subheader("💪 Strengths")

        if result.strengths:
            for strength in result.strengths:
                st.success(strength)
        else:
            st.info("No strengths were identified.")

        # ===========================================
        # WEAKNESSES
        # ===========================================

        st.subheader("⚠️ Weaknesses")

        if result.weaknesses:
            for weakness in result.weaknesses:
                st.warning(weakness)
        else:
            st.success("No major weaknesses detected.")

        # ===========================================
        # MISSING SKILLS
        # ===========================================

        st.subheader("❌ Missing Skills")

        if result.missing_skills:
            for skill in result.missing_skills:
                st.error(skill)
        else:
            st.success("No missing skills detected.")

        # ===========================================
        # MISSING KEYWORDS
        # ===========================================

        st.subheader("🔑 Missing Keywords")

        if result.keywords_missing:
            for keyword in result.keywords_missing:
                st.info(keyword)
        else:
            st.success("No important keywords are missing.")

    # ===========================================
    # AI SUGGESTED IMPROVEMENTS
    # ===========================================

    st.divider()

    st.header("✨ AI Suggested Improvements")

    st.divider()

    st.header("✨ AI Suggested Improvements")

    remaining = len(result.changes) - len(st.session_state.accepted_changes)

    progress = (
        len(st.session_state.accepted_changes) / len(result.changes)
        if result.changes else 0
    )

    st.progress(progress)

    st.caption(
        f"{len(st.session_state.accepted_changes)} of {len(result.changes)} improvements applied"
    )

    for index, change in enumerate(result.changes):

        if index in st.session_state.accepted_changes:
            continue

        with st.expander(f"🟡 {change.section}"):

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("### 📄 Original")
                st.code(change.original)

            with col2:

                st.markdown("### ✨ AI Suggestion")
                st.code(change.improved)

            st.markdown("### 🤖 Why this change?")
            st.write(change.reason)

            st.metric(
                "Estimated ATS Improvement",
                f"+{change.ats_impact}%"
            )

            if st.button(
                "✅ Approve",
                key=f"approve_{index}"
            ):

                st.session_state.current_resume = (
                    st.session_state.current_resume.replace(
                        change.original,
                        change.improved
                    )
                )

                st.session_state.accepted_changes.append(index)

                st.rerun()

    remaining = len(result.changes) - len(st.session_state.accepted_changes)

    st.info(f"📌 Remaining Suggestions: {remaining}")

    if remaining == 0:

        st.success("🎉 Resume fully optimized!")

        st.balloons()
        
    
    st.divider()

    st.header("✨ Optimized Resume")

    st.header("✨ Optimized Resume")

    render_resume(
        result.optimized_resume,
        "Modern"
    )

    from doc_generator import create_resume_doc

    doc_path = create_resume_doc(
        result.optimized_resume
    )

    with open(doc_path, "rb") as file:

        st.download_button(
            "📄 Download Optimized Resume",
            file.read(),
            "Optimized_Resume.docx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
    st.divider()

    with tab2:      
        st.header("💌 Cover Letter")

        st.text_area(
            "",
            result.cover_letter,
            height=300
        )
    
        cover_path = create_cover_letter(
        result.cover_letter
        )

        with open(cover_path, "rb") as file:

            st.download_button(
                "💌 Download Cover Letter",
                file.read(),
                "Cover_Letter.docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

    with tab3:        
        st.divider()

        st.header("🎤 Interview Questions")

        for i, question in enumerate(result.interview_questions, start=1):

            st.markdown(f"**{i}.** {question}")

        st.divider()

        st.header("🧑‍💼 Hiring Decision")

        if result.hiring_decision.lower() == "yes":

            st.success(result.reason)

        else:

            st.error(result.reason)

        with tab5:

            st.header("📥 Downloads")    