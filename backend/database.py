
import sqlite3
from pathlib import Path

# Locate the project root directory.
BASE_DIR = Path(__file__).resolve().parent.parent

# Store the database in the project root.
DATABASE_PATH = BASE_DIR / "portfolio.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()

    try:
        # Table for portfolio projects.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                technologies TEXT NOT NULL,
                github_url TEXT,
                demo_url TEXT,
                status TEXT NOT NULL
            )
        """)

        # Table for contact form submissions.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()

    finally:
        connection.close()
