import re


def extract_keywords(text):
    words = re.findall(r"\b[a-zA-Z][a-zA-Z+#.-]{2,}\b", text.lower())

    stopwords = {
        "the", "and", "for", "with", "this", "that", "are", "you", "your",
        "will", "from", "have", "has", "was", "were", "our", "their",
        "using", "such", "like", "into", "about", "role", "work", "team",
        "experience", "skills", "required", "preferred", "responsibilities"
    }

    return set(word for word in words if word not in stopwords)


def calculate_keyword_score(resume_text, job_description):
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)

    if not job_keywords:
        return 0, []

    matched_keywords = resume_keywords.intersection(job_keywords)
    keyword_score = round((len(matched_keywords) / len(job_keywords)) * 100)

    missing_keywords = list(job_keywords - resume_keywords)
    return min(keyword_score, 100), missing_keywords[:12]


def calculate_skill_match_score(skills, job_description):
    job_text = job_description.lower()
    resume_skills = set(skill.lower() for skill in skills)

    required_skill_bank = {
        "python", "java", "javascript", "typescript", "c++", "sql",
        "machine learning", "deep learning", "nlp", "pandas", "numpy",
        "scikit-learn", "tensorflow", "pytorch", "react", "node.js",
        "flask", "django", "aws", "gcp", "azure", "docker", "kubernetes",
        "spark", "hadoop", "kafka", "airflow", "mongodb", "postgresql",
        "mysql", "tableau", "power bi", "excel", "figma", "swift",
        "kotlin", "firebase"
    }

    jd_skills = {skill for skill in required_skill_bank if skill in job_text}

    if not jd_skills:
        return 50, []

    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills

    score = round((len(matched) / len(jd_skills)) * 100)
    return min(score, 100), sorted(list(missing))


def calculate_action_score(resume_text):
    action_words = {
        "developed", "built", "created", "designed", "implemented",
        "deployed", "optimized", "improved", "automated", "analyzed",
        "engineered", "led", "managed", "reduced", "increased",
        "collaborated", "delivered", "trained", "evaluated", "integrated"
    }

    text = resume_text.lower()
    count = sum(1 for word in action_words if word in text)

    return min(count * 10, 100)


def calculate_final_ats_score(
    resume_text,
    job_description,
    skills,
    sections,
    email,
    phone,
    semantic_score,
    resume_score
):
    keyword_score, missing_keywords = calculate_keyword_score(resume_text, job_description)
    skill_score, missing_skills = calculate_skill_match_score(skills, job_description)
    action_score = calculate_action_score(resume_text)

    contact_score = 100 if email != "Not found" and phone != "Not found" else 60

    section_score = resume_score

    final_score = (
        0.40 * float(semantic_score) +
        0.20 * keyword_score +
        0.20 * skill_score +
        0.10 * section_score +
        0.05 * action_score +
        0.05 * contact_score
    )

    feedback = []

    if keyword_score < 50:
        feedback.append("Add more role-specific keywords from the job description.")

    if skill_score < 60:
        feedback.append("Highlight more required technical skills from the job description.")

    if semantic_score < 50:
        feedback.append("Your resume content is not strongly aligned with the target role. Tailor your projects and experience more closely.")

    if resume_score < 70:
        feedback.append("Improve resume structure by adding missing core sections.")

    if action_score < 50:
        feedback.append("Use stronger action verbs such as developed, deployed, optimized, automated, and improved.")

    if contact_score < 100:
        feedback.append("Make sure your email and phone number are clearly visible.")

    final_score = round(max(30, min(final_score, 100)), 2)

    return {
        "final_score": final_score,
        "keyword_score": keyword_score,
        "skill_score": skill_score,
        "semantic_score": round(float(semantic_score), 2),
        "resume_score": resume_score,
        "action_score": action_score,
        "contact_score": contact_score,
        "missing_keywords": missing_keywords,
        "missing_skills": missing_skills,
        "feedback": feedback
    }