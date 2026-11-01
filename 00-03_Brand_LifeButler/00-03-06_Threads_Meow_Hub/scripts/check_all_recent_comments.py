import requests
import json
from pathlib import Path

def load_env(env_path):
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env_vars[k.strip()] = v.strip()
    return env_vars

ROOT_DIR = Path(__file__).resolve().parents[3]
ENV = load_env(ROOT_DIR / '.secrets.env')
TOKEN = ENV.get('THREADS_ACCESS_TOKEN')
USER_ID = ENV.get('THREADS_USER_ID')
API_BASE = 'https://graph.threads.net/v1.0'

url = f'{API_BASE}/me/threads?fields=id,text,permalink,timestamp&limit=25&access_token={TOKEN}'
res = requests.get(url).json()
posts = res.get('data', [])
print(f'Total posts fetched: {len(posts)}')

all_comments = []
for p in posts:
    pid = p['id']
    curl = f'{API_BASE}/{pid}/conversation?fields=id,text,timestamp,username,permalink&access_token={TOKEN}'
    cres = requests.get(curl).json()
    cdata = cres.get('data', [])
    for c in cdata:
        if c.get('username') != 'hellotaitung':
            all_comments.append({'post': p, 'comment': c})

print(f'\nFound {len(all_comments)} comments from other users:')
for item in all_comments:
    p_text = item['post'].get('text', '')[:30].replace('\n', ' ')
    c_user = item['comment'].get('username')
    c_text = item['comment'].get('text')
    c_id = item['comment'].get('id')
    p_id = item['post'].get('id')
    print(f"- Post {p_id} [{p_text}]:")
    print(f"  From @{c_user}: {c_text} (ID: {c_id})")

with open(Path(__file__).parent / 'all_comments_scan.json', 'w', encoding='utf-8') as f:
    json.dump(all_comments, f, ensure_ascii=False, indent=2)
