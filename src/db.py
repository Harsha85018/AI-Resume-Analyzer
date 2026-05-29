import sqlite3
import pandas as pd

DB_NAME = "resume_analyzer.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            email TEXT,
            phone TEXT,
            predicted_field TEXT,
            skills TEXT,
            recommended_skills TEXT,
            recommended_courses TEXT,
            semantic_score REAL,
            resume_score INTEGER,
            candidate_classification TEXT,
            feedback TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            rating INTEGER,
            comments TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_analysis(
    file_name,
    email,
    phone,
    predicted_field,
    skills,
    recommended_skills,
    recommended_courses,
    semantic_score,
    resume_score,
    candidate_classification,
    feedback
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analyses (
            file_name, email, phone, predicted_field, skills,
            recommended_skills, recommended_courses,
            semantic_score, resume_score, candidate_classification, feedback
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        file_name,
        email,
        phone,
        predicted_field,
        ", ".join(skills),
        ", ".join(recommended_skills),
        " | ".join([course[0] for course in recommended_courses]),
        semantic_score,
        resume_score,
        candidate_classification,
        " | ".join(feedback)
    ))

    conn.commit()
    conn.close()


def save_user_feedback(name, email, rating, comments):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_feedback (name, email, rating, comments)
        VALUES (?, ?, ?, ?)
    """, (name, email, rating, comments))

    conn.commit()
    conn.close()


def load_analyses():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM analyses", conn)
    conn.close()
    return df


def load_feedback():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM user_feedback", conn)
    conn.close()
    return df