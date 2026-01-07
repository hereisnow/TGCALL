import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
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
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO user_tokens (tg_id, refresh_token) VALUES (?, ?)", (tg_id, refresh_token))
    conn.commit()
    conn.close()
