import sqlite3
from typing import List, Tuple

DB_NAME = "plants.db"


def initialize_db() -> None:
    """Creates the plants table if it does not already exist."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_name TEXT NOT NULL,
            moisture INTEGER NOT NULL,
            status TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()


def save_data(name: str, moisture: int, status: str) -> None:
    """Safely inserts a new plant record into the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO plants (plant_name, moisture, status)
        VALUES (?, ?, ?)
        """, (name, moisture, status))
        conn.commit()


def fetch_data() -> List[Tuple]:
    """Retrieves all rows from the plants table."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM plants")
        return cursor.fetchall()


def fetch_unique_plants() -> List[str]:
    """Retrieves a list of all unique plant names saved in the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT plant_name FROM plants ORDER BY plant_name ASC")
        return [row[0] for row in cursor.fetchall() if row]


def fetch_filtered_data(plant_name: str) -> List[Tuple]:
    """Retrieves rows filtered by a specific plant name."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM plants WHERE plant_name = ?", (plant_name,))
        return cursor.fetchall()


def clear_all_records() -> None:
    """Deletes all plant tracking records from the database table."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM plants")
        conn.commit()
