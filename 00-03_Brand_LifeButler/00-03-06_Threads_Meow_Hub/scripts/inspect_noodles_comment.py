import sys
import requests
import json
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

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

url = f'{API_BASE}/18092766425241454/conversation?fields=id,text,timestamp,username,permalink&access_token={TOKEN}'
res = requests.get(url).json()
print("Comments on Post 18092766425241454:")
print(json.dumps(res, ensure_ascii=False, indent=2))
