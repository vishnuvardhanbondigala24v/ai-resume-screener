import streamlit as st
from resume_parser import extract_resume_text
from job_parser import extract_keywords
from matcher import match_resume_to_job
import os
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="AI Resume Screener", layout="wide")

# Optional logo
# st.image("logo.png", width=120)

st.title("📄 AI Resume Screener")
st.markdown("Use this tool to compare your resume against a job description and get smart suggestions to improve your match.")

# Sidebar
st.sidebar.header("📂 Upload Your Files")
resume_file = st.sidebar.file_uploader("Resume (PDF)", type=["pdf"])
job_file = st.sidebar.file_uploader("Job Description (PDF)", type=["pdf"])

if resume_file and job_file:
    resume_path = os.path.join("uploads", resume_file.name)
    job_path = os.path.join("uploads", job_file.name)
    with open(resume_path, "wb") as f:
        f.write(resume_file.getbuffer())
    with open(job_path, "wb") as f:
        f.write(job_file.getbuffer())

    resume_text = extract_resume_text(resume_path)
    job_text = extract_resume_text(job_path)

    score = match_resume_to_job(resume_text, job_text)
    st.header("📊 Match Score")
    st.success(f"Your resume matches the job description by **{score}%**")

    job_keywords = extract_keywords(job_text)
    matched_keywords = [kw for kw in job_keywords if kw in resume_text.lower()]
    unmatched_keywords = [kw for kw in job_keywords if kw not in resume_text.lower()]

    st.header("🔍 Keyword Match Summary")
    col1, col2 = st.columns(2)
    col1.metric("Matched Keywords", len(matched_keywords))
    col2.metric("Unmatched Keywords", len(unmatched_keywords))

    fig, ax = plt.subplots()
    ax.bar(["Matched", "Unmatched"], [len(matched_keywords), len(unmatched_keywords)], color=["green", "red"])
    ax.set_ylabel("Number of Keywords")
    ax.set_title("Resume vs Job Keyword Match")
    st.pyplot(fig)

    with st.expander("✅ Matched Keywords"):
        st.write(", ".join(matched_keywords))
    with st.expander("❌ Unmatched Keywords"):
        st.write(", ".join(unmatched_keywords))

    st.header("💡 Smart Suggestions to Improve Your Resume")
    if unmatched_keywords:
        st.write("Consider adding these keywords or skills to better match the job description:")
        for kw in unmatched_keywords[:10]:
            st.markdown(f"- **{kw}**")
        st.write("You can include these in your resume sections like:")
        st.markdown("- **Skills**")
        st.markdown("- **Summary**")
        st.markdown("- **Experience bullet points**")
    else:
        st.success("Your resume already covers all the key terms from the job description. Great job!")

    with st.expander("📄 See Resume Text"):
        st.write(resume_text)
    with st.expander("📄 See Job Description Text"):
        st.write(job_text)

st.markdown("---")

