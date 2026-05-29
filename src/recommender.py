from data.field_config import FIELD_KEYWORDS
from data.courses import COURSES


def recommend_skills(predicted_field, current_skills):
    current_skills = set(skill.lower() for skill in current_skills)
    target_skills = FIELD_KEYWORDS.get(predicted_field, {}).get("recommended_skills", [])
    return [skill for skill in target_skills if skill.lower() not in current_skills]


def recommend_courses(predicted_field, limit=3):
    return COURSES.get(predicted_field, COURSES["General Software"])[:limit]