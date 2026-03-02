
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def create_user_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            name VARCHAR(100),
            gender VARCHAR(20),
            password VARCHAR(100)
        )
    """)

    conn.commit()
    conn.close()


def register_user(username, name, gender, password):

    conn = get_connection()
    cursor = conn.cursor()

    # Check if username exists
    cursor.execute(
        "SELECT id FROM users WHERE username=%s",
        (username,)
    )

    existing = cursor.fetchone()

    if existing:
        conn.close()
        return False   # username exists

    # Insert new user
    cursor.execute(
        "INSERT INTO users (username, name, gender, password) VALUES (%s, %s, %s, %s)",
        (username, name, gender, password)
    )

    conn.commit()
    conn.close()

    return True   # success


def login_user(username , password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    return user