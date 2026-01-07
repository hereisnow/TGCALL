import sqlite3
import os

# Это гарантирует, что база всегда будет в корне проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")

def init_db():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_tokens (
            tg_id TEXT PRIMARY KEY,
            refresh_token TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_token(tg_id, refresh_token):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO user_tokens (tg_id, refresh_token) VALUES (?, ?)", (tg_id, refresh_token))
    conn.commit()
    conn.close()
