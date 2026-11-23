"""
極星 AI 數位店長 · 每日子夜零點全自動巡檢與回覆排程器 (Midnight Autopilot)
執行時間：每日 00:00
職能：
1. 自動續期 Google Business Profile API 憑證
2. 掃描「職人食堂」全量 Google 地圖評論
3. 識別未回覆評論，嚴格遵循品碩兩大鐵律自動生成高情商回覆並即時推送上線
4. 截取每日營運指標快照（評分、總評論數、新增數），存檔於 data/daily_metrics.jsonl
"""

import os
import sys
import json
import urllib.request
from datetime import datetime
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

BASE_DIR = Path(__file__).resolve().parent
TOKEN_FILE = BASE_DIR / "token.json"
CLIENT_SECRET_FILE = BASE_DIR / "client_secret.json"
CLIENT_DATA_DIR = BASE_DIR / "clients" / "01_Taitung_Shokunin_Diner" / "data"
LOG_FILE = CLIENT_DATA_DIR / "autopilot_execution.log"
METRICS_FILE = CLIENT_DATA_DIR / "daily_metrics.jsonl"
REPLIES_LOG = CLIENT_DATA_DIR / "autopilot_replies.jsonl"

ACCOUNT_ID = "112884798662846885062"
LOCATION_ID = "1774177451467087781"

CLIENT_DATA_DIR.mkdir(parents=True, exist_ok=True)

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def get_valid_credentials():
    if not TOKEN_FILE.exists():
        log("❌ 找不到 token.json，請先執行 run_auth.bat 進行初始授權！")
        return None
    try:
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))
        if creds.expired and creds.refresh_token:
            log("🔄 憑證過期，正在以 Refresh Token 自動續期...")
            creds.refresh(Request())
            with open(TOKEN_FILE, "w", encoding="utf-8") as f:
                f.write(creds.to_json())
            log("✅ 憑證續期成功！")
        return creds
    except Exception as e:
        log(f"❌ 憑證刷新失敗: {e}")
        return None

def generate_reply_for_review(comment, star_rating, reviewer_name):
    """
    遵循創辦人（品碩）兩大鐵律生成高情商回覆：
    1. 負評不找藉口辯解、不長篇大論、虛心收下
    2. 絕不給予承諾、不承諾折扣或補償
    """
    c_lower = (comment or "").lower()
    
    # 判斷是否為外語
    has_foreign = any(c in c_lower for c in ['delicious', 'good', 'dumpling', 'great', 'super', 'lecker', 'danke', 'nice'])
    
    if star_rating in ['ONE', 'TWO', 'THREE'] or any(k in c_lower for k in ['態度', '差', '等很久', '貴', '生氣', '慢', '鹹', '油']):
        # 負評/抱怨處理
        return f"非常感謝 {reviewer_name} 撥空留下真實的反饋。對於這次未能帶給您滿意的用餐體驗，我們虛心收下您的提醒並銘記在心，我們會持續檢討並調整現場的各項細節。感謝您的指教與包涵。"
    
    if has_foreign:
        return f"非常感謝 {reviewer_name} 的支持與推薦！很高興您喜歡我們的現蒸手作料理，祝您在台東有美好的一天！\n(Thank you so much {reviewer_name} for your kind review! We are delighted that you enjoyed our freshly handmade dishes. Wishing you a wonderful time in Taitung!)"
    
    # 一般好評
    return f"感謝 {reviewer_name} 的溫暖肯定與喜愛！很高興現蒸的點心與熱騰騰的料理能合您的口味，老闆與闆娘會繼續堅持手作初衷，歡迎下次來安慶街再坐坐！"

def run_midnight_sync():
    log("=== 🌙 啟動子夜零點自動化巡檢任務 ===")
    creds = get_valid_credentials()
    if not creds:
        return

    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }

    # 1. 抓取最新評論
    url = f"https://mybusiness.googleapis.com/v4/accounts/{ACCOUNT_ID}/locations/{LOCATION_ID}/reviews"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        log(f"❌ 抓取評論失敗: {e}")
        return

    reviews = data.get('reviews', [])
    avg_rating = data.get('averageRating', 0)
    total_count = data.get('totalReviewCount', len(reviews))
    log(f"📊 當前總評論數: {total_count} | 平均評分: {avg_rating} 星")

    # 紀錄每日指標快照
    today_str = datetime.now().strftime("%Y-%m-%d")
    metrics_record = {
        "date": today_str,
        "timestamp": datetime.now().isoformat(),
        "total_reviews": total_count,
        "average_rating": avg_rating,
        "active_location": "職人食堂"
    }
    with open(METRICS_FILE, "a", encoding="utf-8") as mf:
        mf.write(json.dumps(metrics_record, ensure_ascii=False) + "\n")

    # 2. 檢測未回覆評論並自動發送
    unreplied = [r for r in reviews if not r.get('reviewReply')]
    log(f"🔍 掃描到 {len(unreplied)} 則待回覆評論")

    for r in unreplied:
        r_id = r.get('reviewId')
        name = r.get('reviewer', {}).get('displayName', '訪客')
        star = r.get('starRating', 'FIVE')
        comm = r.get('comment', '')
        
        reply_content = generate_reply_for_review(comm, star, name)
        reply_url = f"https://mybusiness.googleapis.com/v4/accounts/{ACCOUNT_ID}/locations/{LOCATION_ID}/reviews/{r_id}/reply"
        body = json.dumps({"comment": reply_content}).encode('utf-8')
        
        try:
            r_req = urllib.request.Request(reply_url, data=body, method='PUT')
            r_req.add_header("Authorization", f"Bearer {creds.token}")
            r_req.add_header("Content-Type", "application/json")
            with urllib.request.urlopen(r_req, timeout=10) as r_resp:
                log(f"✅ 成功自動回覆 [{name}] (星等: {star})")
                log_item = {
                    "timestamp": datetime.now().isoformat(),
                    "reviewId": r_id,
                    "reviewer": name,
                    "rating": star,
                    "comment": comm,
                    "reply": reply_content
                }
                with open(REPLIES_LOG, "a", encoding="utf-8") as rf:
                    rf.write(json.dumps(log_item, ensure_ascii=False) + "\n")
        except Exception as e:
            log(f"❌ 回覆 [{name}] 失敗: {e}")

    log("=== 🌙 子夜巡檢任務執行完成 ===")

if __name__ == '__main__':
    run_midnight_sync()
