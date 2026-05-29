def calculate_resume_score(sections, skills):
    score = 0
    feedback = []

    # Section weights
    section_weights = {
        "summary": 8,
        "education": 12,
        "experience": 16,
        "projects": 18,
        "skills": 10,
        "certifications": 8,
        "achievements": 8
    }

    for section, weight in section_weights.items():
        if section in sections:
            score += weight
        else:
            feedback.append(f"Consider adding '{section}' section")

    # Skill strength
    if len(skills) >= 10:
        score += 10
    elif len(skills) >= 5:
        score += 5
    else:
        feedback.append("Add more technical skills")

    return min(score, 100), feedback