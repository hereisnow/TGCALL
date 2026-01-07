import sqlite3
import os

# Определяем путь к базе в корне проекта, чтобы её видели и бот, и сервер
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
    # Используем переменную db_path для сохранения в правильный файл
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO user_tokens (tg_id, refresh_token) VALUES (?, ?)", (tg_id, refresh_token))
    conn.commit()
    conn.close()
