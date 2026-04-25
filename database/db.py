import sqlite3
import os
from datetime import datetime

DB_PATH = "travel_data.db"

def init_db():
    """Initialize the database and create tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Searches table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            response TEXT NOT NULL,
            search_type TEXT DEFAULT 'general',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Itineraries table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itineraries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination TEXT NOT NULL,
            duration_days INTEGER NOT NULL,
            itinerary TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized!")

def save_search(query: str, response: str, search_type: str = "general"):
    """Save a search to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO searches (query, response, search_type) VALUES (?, ?, ?)",
            (query, response, search_type)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB save error: {e}")

def get_recent_searches(limit: int = 5):
    """Get recent searches from database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT query, search_type, timestamp FROM searches ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(f"DB fetch error: {e}")
        return []

def save_itinerary(destination: str, duration_days: int, itinerary: str):
    """Save an itinerary to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO itineraries (destination, duration_days, itinerary) VALUES (?, ?, ?)",
            (destination, duration_days, itinerary)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB save error: {e}")

def get_saved_itineraries():
    """Get all saved itineraries."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT destination, duration_days, itinerary, timestamp FROM itineraries ORDER BY timestamp DESC"
        )
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(f"DB fetch error: {e}")
        return []
