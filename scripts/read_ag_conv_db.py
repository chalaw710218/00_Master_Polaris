import sqlite3
import os

db_path = r"C:\Users\lenovo\.gemini\antigravity\conversation_summaries.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = c.fetchall()
print("Tables in conversation_summaries.db:", tables)

for t in tables:
    t_name = t[0]
    print(f"--- Table: {t_name} ---")
    c.execute(f"PRAGMA table_info({t_name})")
    cols = [col[1] for col in c.fetchall()]
    print("Columns:", cols)
    c.execute(f"SELECT * FROM {t_name} LIMIT 10")
    for r in c.fetchall():
        print(r)

conn.close()
