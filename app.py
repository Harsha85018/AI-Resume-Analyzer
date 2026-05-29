import streamlit as st
import plotly.express as px

from src.extractor import extract_text_from_pdf
from src.preprocess import preprocess_text
from src.parser import extract_email, extract_phone, extract_skills, detect_sections
from src.semantic_matcher import calculate_semantic_similarity
from src.features import calculate_resume_score
from src.clustering import cluster_candidate
from src.predictor import predict_field
from src.recommender import recommend_skills, recommend_courses
from src.db import init_db, save_analysis, save_user_feedback, load_analyses, load_feedback
from src.ats_scorer import calculate_final_ats_score

init_db()

st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    h1, h2, h3 {
        color: #1f4e79;
    }

    .custom-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #e6e6e6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 18px;
    }

    .small-title {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 10px;
        color: #1f4e79;
    }

    .info-text {
        font-size: 16px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page",
    ["User", "Feedback", "About", "Admin"]
)

if page == "User":
    st.title("AI Resume Analyzer Pro")
    st.caption(
        "An AI-powered resume evaluation system using NLP, semantic similarity, "
        "feature engineering, ATS scoring, clustering, and recruiter-style recommendations."
    )

    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    job_description = st.text_area("Paste the job description here")

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("Analyze Resume", use_container_width=True):
        if not uploaded_file:
            st.warning("⚠️ Please upload a resume first.")
            st.stop()

        if not job_description.strip():
            st.warning("⚠️ Please paste a job description.")
            st.stop()

        with st.spinner("Analyzing your resume..."):
            raw_text = extract_text_from_pdf(uploaded_file)

            if not raw_text.strip():
                st.error("Could not extract text from the uploaded PDF.")
                st.stop()

            cleaned_text = preprocess_text(raw_text)

            email = extract_email(raw_text)
            phone = extract_phone(raw_text)
            skills = extract_skills(raw_text)
            sections = detect_sections(raw_text)

            predicted_field = predict_field(skills)
            recommended_skill_list = recommend_skills(predicted_field, skills)
            recommended_course_list = recommend_courses(predicted_field)

            semantic_score = calculate_semantic_similarity(cleaned_text, job_description)
            resume_score, feedback = calculate_resume_score(sections, skills)

            ats_result = calculate_final_ats_score(
                resume_text=raw_text,
                job_description=job_description,
                skills=skills,
                sections=sections,
                email=email,
                phone=phone,
                semantic_score=semantic_score,
                resume_score=resume_score
            )

            final_ats_score = ats_result["final_score"]
            candidate_class = cluster_candidate(final_ats_score, semantic_score)
            all_feedback = feedback + ats_result["feedback"]

            save_analysis(
                file_name=uploaded_file.name,
                email=email,
                phone=phone,
                predicted_field=predicted_field,
                skills=skills,
                recommended_skills=recommended_skill_list,
                recommended_courses=recommended_course_list,
                semantic_score=semantic_score,
                resume_score=final_ats_score,
                candidate_classification=candidate_class,
                feedback=all_feedback
            )

            st.markdown("## Analysis Overview")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.markdown('<div class="small-title">📄 Basic Information</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="info-text">📧 <b>Email:</b> {email}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="info-text">📞 <b>Phone:</b> {phone}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="info-text">🎯 <b>Predicted Field:</b> {predicted_field}</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="info-text">📂 <b>Sections Found:</b> '
                    f'{", ".join(sections) if sections else "No major sections detected"}</div>',
                    unsafe_allow_html=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.markdown('<div class="small-title">📊 Score Summary</div>', unsafe_allow_html=True)
                st.metric("Final ATS Score", f"{final_ats_score}/100")
                st.metric("Semantic Match", f"{semantic_score:.2f}%")
                st.metric("Resume Quality", f"{resume_score}/100")

                if candidate_class == "Strong Fit":
                    st.success(f"🧠 Candidate Classification: {candidate_class}")
                elif candidate_class == "Moderate Fit":
                    st.warning(f"🧠 Candidate Classification: {candidate_class}")
                else:
                    st.error(f"🧠 Candidate Classification: {candidate_class}")

                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("## Score Visualization")
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)

            st.write("Final ATS Score")
            ats_progress = float(max(0.0, min(final_ats_score / 100, 1.0)))
            st.progress(ats_progress)

            st.write("Semantic Match")
            match_progress = float(max(0.0, min(semantic_score / 100, 1.0)))
            st.progress(match_progress)

            st.write("Resume Quality")
            resume_progress = float(max(0.0, min(resume_score / 100, 1.0)))
            st.progress(resume_progress)

            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("## ATS Breakdown")
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)

            b1, b2, b3 = st.columns(3)

            with b1:
                st.metric("Keyword Match", f"{ats_result['keyword_score']}/100")
                st.metric("Skill Match", f"{ats_result['skill_score']}/100")

            with b2:
                st.metric("Action Verb Score", f"{ats_result['action_score']}/100")
                st.metric("Contact Score", f"{ats_result['contact_score']}/100")

            with b3:
                st.metric("Semantic Score", f"{ats_result['semantic_score']}/100")
                st.metric("Resume Quality", f"{ats_result['resume_score']}/100")

            st.markdown('</div>', unsafe_allow_html=True)

            if ats_result["missing_skills"]:
                st.markdown("## Missing Skills From Job Description")
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                for skill in ats_result["missing_skills"]:
                    st.warning(skill)
                st.markdown('</div>', unsafe_allow_html=True)

            if ats_result["missing_keywords"]:
                st.markdown("## Missing Keywords")
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.write(", ".join(ats_result["missing_keywords"]))
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("## Skills and Recommendations")
            col3, col4 = st.columns(2)

            with col3:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.markdown('<div class="small-title">🧠 Skills Detected</div>', unsafe_allow_html=True)
                if skills:
                    for skill in skills:
                        st.markdown(f"- {skill}")
                else:
                    st.write("No skills detected.")
                st.markdown('</div>', unsafe_allow_html=True)

            with col4:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.markdown('<div class="small-title">💡 Recommended Skills</div>', unsafe_allow_html=True)
                if recommended_skill_list:
                    for skill in recommended_skill_list:
                        st.markdown(f"- {skill}")
                else:
                    st.write("No additional recommendations.")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("## Recommended Courses")
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            if recommended_course_list:
                for course_name, course_link in recommended_course_list:
                    st.markdown(f"- [{course_name}]({course_link})")
            else:
                st.write("No course recommendations available.")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("## Resume Feedback and Suggestions")
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)

            if all_feedback:
                for item in all_feedback:
                    st.warning(item)
            else:
                st.success("Your resume already covers the major core sections well.")

            if final_ats_score < 50:
                st.info("This resume has low alignment with the job. Improve keywords, skills, and project relevance.")
            elif final_ats_score < 75:
                st.info("This resume has moderate alignment. Add missing skills and tailor experience bullets to the job.")
            else:
                st.success("This resume is strongly aligned with the target job description.")

            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("## Resume Text Details")
            with st.expander("Raw Text"):
                st.write(raw_text[:3000])

            with st.expander("Processed Text"):
                st.write(cleaned_text[:3000])

elif page == "Feedback":
    st.title("Feedback")
    st.caption("Help improve the app by sharing your feedback.")

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    with st.form("feedback_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        rating = st.slider("Rate this app", 1, 5, 4)
        comments = st.text_area("Comments")
        submitted = st.form_submit_button("Submit Feedback", use_container_width=True)

        if submitted:
            save_user_feedback(name, email, rating, comments)
            st.success("Thank you! Your feedback has been saved.")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "About":
    st.title("About")
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.write(
        "AI Resume Analyzer Pro is a resume evaluation system built using NLP, "
        "semantic similarity scoring, ATS scoring, feature engineering, clustering, "
        "and recommendation techniques."
    )
    st.write(
        "It analyzes resumes, predicts likely domains, recommends skills and courses, "
        "scores resume strength, identifies skill gaps, and classifies candidate fit."
    )
    st.write(
        "This version is inspired by the original AI Resume Analyzer project, but rebuilt "
        "with a cleaner, more modern, and more advanced AI workflow."
    )
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Admin":
    st.title("Admin Dashboard")
    st.caption("View saved resume analyses and user feedback.")

    analyses_df = load_analyses()
    feedback_df = load_feedback()

    st.markdown("## Summary Metrics")
    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("Total Analyses", len(analyses_df))

    with m2:
        if not analyses_df.empty:
            st.metric("Avg ATS Score", round(analyses_df["resume_score"].mean(), 2))
        else:
            st.metric("Avg ATS Score", "0")

    with m3:
        st.metric("Total Feedback Entries", len(feedback_df))

    st.markdown("## Saved Resume Analyses")
    if not analyses_df.empty:
        st.dataframe(analyses_df, use_container_width=True)

        st.markdown("## Analytics")
        c1, c2 = st.columns(2)

        with c1:
            fig1 = px.pie(
                analyses_df,
                names="predicted_field",
                title="Predicted Field Distribution"
            )
            st.plotly_chart(fig1, use_container_width=True)

        with c2:
            fig2 = px.pie(
                analyses_df,
                names="candidate_classification",
                title="Candidate Classification Distribution"
            )
            st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.histogram(
            analyses_df,
            x="resume_score",
            nbins=10,
            title="ATS Score Distribution"
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No analysis records found yet.")

    st.markdown("## User Feedback")
    if not feedback_df.empty:
        st.dataframe(feedback_df, use_container_width=True)

        fig4 = px.pie(
            feedback_df,
            names="rating",
            title="Feedback Rating Distribution"
        )
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("No feedback records found yet.")