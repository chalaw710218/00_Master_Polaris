import os
import sys
import json
import time
import requests
from pathlib import Path

# 確保 Windows 終端機支援 Emoji 輸出
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 定位極星根目錄下的 .secrets.env
HUB_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_PATH = ROOT_DIR / ".secrets.env"
STATE_FILE = Path(__file__).resolve().parent / "replied_ids.json"

def load_env(env_path):
    if not env_path.exists():
        return {}
    env_vars = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                env_vars[key.strip()] = val.strip()
    return env_vars

ENV = load_env(ENV_PATH)
THREADS_USER_ID = ENV.get("THREADS_USER_ID")
THREADS_USERNAME = ENV.get("THREADS_USERNAME", "hellotaitung")
THREADS_ACCESS_TOKEN = ENV.get("THREADS_ACCESS_TOKEN")
API_BASE = "https://graph.threads.net/v1.0"

def load_replied_ids():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_replied_ids(replied_ids):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(replied_ids), f, ensure_ascii=False, indent=2)

def generate_meow_reply(comment_text, author_username="脆友"):
    """
    喵編專屬人格回覆生成邏輯：
    依據 01_Meow_Threads_Codex.md 之『三秒共情 ＋ 接梗幽默 ＋ 拋出新反問』
    """
    text_lower = comment_text.lower()
    
    # 規則 1：問哪裡買、多少錢、怎麼訂
    if any(k in text_lower for k in ["哪裡買", "怎麼買", "想吃", "多少錢", "價格", "連結", "+1"]):
        return "被你發現了喵！偷偷去個人檔案看傳送門~（小聲說：闆仔去送外送了，趁他不在快去逛逛，不要跟他說是我跟你說的喵🐱）"
    
    # 規則 2：抱怨煮飯累、下班很煩、吃外送
    elif any(k in text_lower for k in ["好累", "累死", "煮飯", "下班", "外送", "好難", "不知道煮什麼"]):
        return "拍拍！今天辛苦了喵~ 不想煮千萬不要勉強，去切兩片肉丟熱水燙一下淋醬油，剩下的時間留給沙發跟耍廢！明天的事明天再說喵🐾"
        
    # 規則 3：提到闆仔、貓咪、店貓
    elif any(k in text_lower for k in ["闆仔", "貓", "貓咪", "主子", "罐罐", "店貓"]):
        return "闆仔剛剛看報價單眉頭又皺起來了，我正準備去踩他的計算機鍵盤喵！快給我罐罐封口費~😼"

    # 通用親切接梗回覆
    else:
        return f"抓到了吼！感謝 @{author_username} 來留言取暖~ 喵編這就把你加入生活管家 VIP 偷懶名單喵✨！"

def get_latest_threads(limit=5):
    """獲取帳號最新的貼文清單"""
    url = f"{API_BASE}/{THREADS_USER_ID}/threads"
    params = {
        "access_token": THREADS_ACCESS_TOKEN,
        "fields": "id,text,timestamp",
        "limit": limit
    }
    r = requests.get(url, params=params)
    data = r.json()
    return data.get("data", [])

def get_thread_replies(thread_id):
    """取得指定貼文底下的所有留言回覆"""
    url = f"{API_BASE}/{thread_id}/conversation"
    params = {
        "access_token": THREADS_ACCESS_TOKEN,
        "fields": "id,text,username,timestamp"
    }
    r = requests.get(url, params=params)
    data = r.json()
    return data.get("data", [])

def reply_to_comment(reply_to_id, reply_text):
    """調用 Threads API 發表回覆"""
    # 1. 建立回覆容器
    url_container = f"{API_BASE}/{THREADS_USER_ID}/threads"
    payload = {
        "access_token": THREADS_ACCESS_TOKEN,
        "media_type": "TEXT",
        "text": reply_text,
        "reply_to_id": reply_to_id
    }
    r1 = requests.post(url_container, data=payload)
    res1 = r1.json()
    if "id" not in res1:
        print(f"❌ 建立回覆容器失敗: {res1}")
        return False
        
    creation_id = res1["id"]
    time.sleep(2)
    
    # 2. 正式發布回覆
    url_publish = f"{API_BASE}/{THREADS_USER_ID}/threads_publish"
    r2 = requests.post(url_publish, data={"access_token": THREADS_ACCESS_TOKEN, "creation_id": creation_id})
    res2 = r2.json()
    if "id" in res2:
        print(f"✅ 成功回覆留言 (Comment ID: {reply_to_id})！")
        return True
    else:
        print(f"❌ 發布回覆失敗: {res2}")
        return False

def run_replier_loop():
    """執行一次輪詢檢查與自動回覆"""
    if not THREADS_USER_ID or not THREADS_ACCESS_TOKEN:
        print("❌ 錯誤：尚未設定 THREADS_USER_ID 或 THREADS_ACCESS_TOKEN！")
        return

    replied_ids = load_replied_ids()
    print("🔍 [喵編雷達] 正在掃描 Threads 最新貼文留言...")

    threads = get_latest_threads(limit=3)
    new_replies_count = 0

    for t in threads:
        t_id = t["id"]
        replies = get_thread_replies(t_id)
        for rep in replies:
            rep_id = rep["id"]
            rep_text = rep.get("text", "")
            username = rep.get("username", "脆友")
            
            # 避免重複回覆自己或已回過的回覆
            if rep_id in replied_ids:
                continue

            # 避免回覆自己（生活管家/喵編官方帳號）
            if username == THREADS_USERNAME or username == "hellotaitung":
                replied_ids.add(rep_id)
                save_replied_ids(replied_ids)
                continue

            print(f"💬 發現新留言 [@{username}]: {rep_text}")
            reply_content = generate_meow_reply(rep_text, username)
            print(f"🐱 喵編準備回覆: {reply_content}")
            
            success = reply_to_comment(rep_id, reply_content)
            if success:
                replied_ids.add(rep_id)
                new_replies_count += 1
                save_replied_ids(replied_ids)
                time.sleep(3)

    if new_replies_count == 0:
        print("💤 目前沒有未回覆的新留言。")
    else:
        print(f"🎉 本次巡邏共完成了 {new_replies_count} 則自動接梗回覆！")

if __name__ == "__main__":
    run_replier_loop()
