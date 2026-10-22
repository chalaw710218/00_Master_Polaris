import sys
import json
import time
import requests
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

cur = Path.cwd()
env_file = None
for p in [cur] + list(cur.parents):
    candidate = p / ".secrets.env"
    if candidate.exists():
        env_file = candidate
        break

env_vars = {}
with open(env_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip()

token = env_vars.get("THREADS_ACCESS_TOKEN")
user_id = env_vars.get("THREADS_USER_ID")
API_BASE = "https://graph.threads.net/v1.0"

reply_to_id = "18489576688104058"
reply_text = "綠島蘭嶼下午先放了～至於我們生活管家……闆仔剛剛才從外頭歷劫歸來，回報山西路上甚至有『會飛的鐵捲門』出沒！😱\n\n小編立刻強制勒令他回房喝熱茶放颱風假，現在由小編跟喵編接管防颱守夜！外頭風大雨大，大家今晚也千萬待在室內躲好、平平安安最重要喵～🌪️🏠✨"

print(f"🚀 準備回覆 @a828603 (Comment ID: {reply_to_id})...")
print(f"回覆內容:\n{reply_text}")

# 1. 建立回覆容器
url_container = f"{API_BASE}/{user_id}/threads"
payload = {
    "access_token": token,
    "media_type": "TEXT",
    "text": reply_text,
    "reply_to_id": reply_to_id
}
r1 = requests.post(url_container, data=payload)
res1 = r1.json()
print("容器回應:", res1)
creation_id = res1.get("id")

if creation_id:
    time.sleep(2)
    # 2. 正式發布
    url_publish = f"{API_BASE}/{user_id}/threads_publish"
    r2 = requests.post(url_publish, data={"access_token": token, "creation_id": creation_id})
    res2 = r2.json()
    print("發布回應:", res2)
    pub_id = res2.get("id")
    if pub_id:
        print(f"🎉 成功發布回覆！Post ID: {pub_id}")
        
        # 寫入 replied_ids.json
        state_file = Path("scripts/replied_ids.json")
        replied = []
        if state_file.exists():
            with open(state_file, "r", encoding="utf-8") as f:
                replied = json.load(f)
        if reply_to_id not in replied:
            replied.append(reply_to_id)
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(replied, f, ensure_ascii=False, indent=2)
            print("📝 已更新 replied_ids.json")
else:
    print("❌ 建立容器失敗")
