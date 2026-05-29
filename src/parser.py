import re


def extract_email(text):
    matches = re.findall(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+", text)
    return matches[0] if matches else "Not found"


def extract_phone(text):
    matches = re.findall(r"\+?\d[\d\s\-()]{8,15}\d", text)
    return matches[0] if matches else "Not found"


def extract_skills(text):
    skills_db = [
        "python", "java", "c++", "sql", "machine learning",
        "deep learning", "nlp", "data analysis", "pandas",
        "numpy", "tensorflow", "pytorch", "excel", "power bi",
        "tableau", "flask", "streamlit", "aws", "docker",
        "spark", "hadoop", "mongodb", "postgresql", "mysql",
        "bigquery", "snowflake", "kafka", "databricks",
        "scikit-learn", "matplotlib", "seaborn", "plotly",
        "react", "django", "javascript"
    ]

    text_lower = text.lower()
    found_skills = []

    for skill in skills_db:
        if skill in text_lower:
            found_skills.append(skill)

    return list(set(found_skills))


def detect_sections(text):
    sections = {
        "summary": ["summary", "objective", "profile"],
        "education": ["education", "academic"],
        "experience": ["experience", "work experience"],
        "projects": ["projects", "project"],
        "skills": ["skills"],
        "certifications": ["certifications", "certification"],
        "achievements": ["achievements", "awards"]
    }

    text_lower = text.lower()
    found_sections = []

    for section, keywords in sections.items():
        for word in keywords:
            if word in text_lower:
                found_sections.append(section)
                break

    return found_sections