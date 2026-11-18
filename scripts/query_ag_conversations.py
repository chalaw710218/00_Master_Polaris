import sqlite3
import json

db_path = r"C:\Users\lenovo\.gemini\antigravity\conversation_summaries.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Get non-empty titles or previews
c.execute("""
SELECT conversation_id, title, preview, workspace_uris, last_modified_time 
FROM conversation_summaries 
ORDER BY last_modified_time DESC 
LIMIT 30
""")

rows = c.fetchall()
print(f"Total rows retrieved: {len(rows)}")
for r in rows:
    cid, title, prev, wss, lmt = r
    display_title = title if title else prev
    print(f"[{lmt[:10]}] Title: '{display_title}' | ID: {cid[:8]}... | WS: {wss[:60] if wss else ''}")

conn.close()
