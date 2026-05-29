from data.field_config import FIELD_KEYWORDS


def predict_field(skills):
    skill_set = set(skill.lower() for skill in skills)

    scores = {}

    for field, config in FIELD_KEYWORDS.items():
        scores[field] = len(skill_set.intersection(config["keywords"]))

    # Tie-breaker boosts
    if skill_set.intersection({"java", "javascript", "react", "django", "flask", "typescript"}):
        scores["Software Development"] += 2

    if skill_set.intersection({"machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "nlp"}):
        scores["Data Science"] += 2

    if skill_set.intersection({"spark", "kafka", "airflow", "databricks", "snowflake", "bigquery"}):
        scores["Data Engineering"] += 2

    if skill_set.intersection({"docker", "kubernetes", "aws", "gcp", "azure", "terraform"}):
        scores["Cloud / DevOps"] += 2

    if skill_set.intersection({"swift", "kotlin", "flutter", "firebase", "android", "ios"}):
        scores["Mobile App Development"] += 2

    best_field = max(scores, key=scores.get)

    if scores[best_field] == 0:
        return "General Software"

    return best_field