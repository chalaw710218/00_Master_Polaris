import sys
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.append("scripts")
from threads_publisher import THREADS_ACCESS_TOKEN, API_BASE

wrong_post_id = "18054790760816401"
del_url = f"{API_BASE}/{wrong_post_id}?access_token={THREADS_ACCESS_TOKEN}"
r = requests.delete(del_url, timeout=10)
print("刪除錯圖貼文結果:", r.status_code, r.text)
