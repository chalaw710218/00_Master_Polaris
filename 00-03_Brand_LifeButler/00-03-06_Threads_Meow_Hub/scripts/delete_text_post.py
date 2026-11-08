import sys
import requests
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.append("scripts")
from threads_publisher import THREADS_ACCESS_TOKEN, API_BASE

post_id = "18170516911472750"
del_url = f"{API_BASE}/{post_id}?access_token={THREADS_ACCESS_TOKEN}"
try:
    r = requests.delete(del_url, timeout=10)
    print("API DELETE 狀態碼:", r.status_code, "回應:", r.text)
except Exception as e:
    print("API DELETE 異常:", e)
