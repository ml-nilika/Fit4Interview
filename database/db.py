import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def connect():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interviews (
        id INT AUTO_INCREMENT PRIMARY KEY,
        candidate_name VARCHAR(255),
        role VARCHAR(255),
        question TEXT,
        answer TEXT,
        content_score FLOAT,
        voice_score FLOAT,
        final_score FLOAT,
        mode VARCHAR(50),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_interview(data):
    conn = connect()
    cursor = conn.cursor()

    query = """
    INSERT INTO interviews (
        candidate_name,
        role,
        question,
        answer,
        content_score,
        voice_score,
        final_score,
        mode
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data["name"],
        data["role"],
        data["question"],
        data["answer"],
        data["content"],
        data["voice"],
        data["final"],
        data["mode"]
    )

    cursor.execute(query, values)

    conn.commit()
    conn.close()