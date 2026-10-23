import os
import sqlite3
from pathlib import Path

import psycopg
from psycopg.rows import dict_row


# Locate the project root directory.
BASE_DIR = Path(__file__).resolve().parent.parent

# Use PostgreSQL when DATABASE_URL is configured.
DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    if DATABASE_URL:
        connection = psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row,
        )
        return connection

    # Local development: use SQLite.
    database_path = BASE_DIR / "portfolio.db"

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    return connection


def create_tables():
    connection = get_connection()

    try:
        if DATABASE_URL:
            # PostgreSQL tables
            connection.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    technologies TEXT NOT NULL,
                    github_url TEXT,
                    demo_url TEXT,
                    status TEXT NOT NULL
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS contact_messages (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

        else:
            # SQLite tables
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

            connection.execute("""
                CREATE TABLE IF NOT EXISTS contact_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

        connection.commit()

    finally:
        connection.close()
        