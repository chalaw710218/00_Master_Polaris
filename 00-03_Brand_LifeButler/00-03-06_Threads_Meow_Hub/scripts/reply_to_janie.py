import sys
import json
import requests
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.append("scripts")
from threads_publisher import THREADS_ACCESS_TOKEN, API_BASE

reply_text = "真的，把熱茶喝透、好好睡上一覺，今天開工腳步就不會慌。祝你在台中新的一週元氣滿滿，今天如果忙累了，記得深呼吸休息一下喔！🍵✨"
parent_comment_id = "18471136852190485"

url = f"{API_BASE}/me/threads"
params = {
    "media_type": "TEXT",
    "text": reply_text,
    "reply_to_id": parent_comment_id,
    "access_token": THREADS_ACCESS_TOKEN
}

res = requests.post(url, data=params).json()
print("建立回覆容器:", res)
creation_id = res.get("id")

if creation_id:
    pub_url = f"{API_BASE}/me/threads_publish"
    pub_res = requests.post(pub_url, data={"creation_id": creation_id, "access_token": THREADS_ACCESS_TOKEN}).json()
    print("公開發布回覆結果:", pub_res)
    
    # 更新 replied_ids.json
    state_file = Path("scripts/replied_ids.json")
    ids = []
    if state_file.exists():
        ids = json.load(open(state_file, encoding='utf-8'))
    if parent_comment_id not in ids:
        ids.append(parent_comment_id)
    with open(state_file, "w", encoding='utf-8') as f:
        json.dump(ids, f, ensure_ascii=False, indent=2)
    print("✅ 已成功回覆並記入 replied_ids.json！")
else:
    print("❌ 建立回覆容器失敗:", res)
