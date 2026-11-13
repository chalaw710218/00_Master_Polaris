import os
import sys
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPTS_DIR = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\scripts"
if SCRIPTS_DIR not in sys.path:
    sys.path.append(SCRIPTS_DIR)

from threads_publisher import upload_local_image_to_meta_cdn, create_media_container, publish_container

TZ_TW = timezone(timedelta(hours=8))

# ==========================================
# 貼文庫設定 (Threads 02 & 03)
# ==========================================
THREADS_SCHEDULE_QUEUE = [
    {
        "id": 2,
        "name": "第 2 講連載 · 篇號 02【每年省下三萬塊月租費】",
        "target_dt": datetime(2026, 11, 15, 20, 30, 0, tzinfo=TZ_TW),
        "img_path": r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_02_Antigravity_Meta_Automation\FB_L02_02_Official_API_Security.png",
        "message": """外面幫你排程發文、自動回留言的行銷軟體，一個月收 2,000 塊，一年就是兩萬多。找來路不明的黑心外掛，又隨時會被官方封號。

11/18 週三第 2 講，我們教你走正道。
直接串接 Facebook 和 Threads 的官方合法 API，把文案照片丟進資料夾，Python 3 秒自動發射，金鑰安全隔離永不外洩。

這是外面顧問收三萬塊的系統，週三下午我坐在你身邊，親手盯著你在自己筆電跑通。

老朋友 0 元免單，新夥伴單堂 $500。
極限 6 席純實體，留言區申請。""",
        "comment": """🐾 2026 秋季《AI 家教實戰系列班 · 第 2 講極致小班須知》
⚠️ 堅持【100% 純實體現場教學】，絕無線上同步！導師手把手巡桌排錯到底！
全班極限 6 席深度陪伴，API 沒跑通不准走。

📅 時間：11/18 (週三) 14:00 - 16:00 ｜ 台東市正氣北路166巷90號（家宅）
🎯 主題：Antigravity 操作 ✕ Meta 官方自動發文串接 (FB / Threads API)
💰 費用：老學員（含第 1 講夥伴）0 元免單 ｜ 新朋友單堂 $500

📝 實體入席申請表：https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
💬 官方 LINE 諮詢：https://lin.ee/z83YSq6"""
    },
    {
        "id": 3,
        "name": "第 2 講連載 · 篇號 03【明天下午家宅見】",
        "target_dt": datetime(2026, 11, 17, 20, 30, 0, tzinfo=TZ_TW),
        "img_path": r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_02_Antigravity_Meta_Automation\FB_L02_03_Final_Call_Tomorrow.png",
        "message": """最後通報。明天下午 14:00 正氣北路家宅開練。

第 2 講：【Meta 官方自動發文與秒回】。
徹底消滅每天手動複製貼上、跟半夜盯著手機回訊息的焦慮。

說到做到，現場就 6 張椅子，多一張都不加，絕無線上同步。
帶著你的筆電來，現場把專屬發射台串通才放人下課。

正選名額即將全數鎖定，額滿表單立即關門。
想把時間買回來的小老闆，第一則留言自取。明天下午見。""",
        "comment": """🐾 2026 秋季《AI 家教實戰系列班 · 第 2 講極致小班須知》
⚠️ 堅持【100% 純實體現場教學】，絕無線上同步！導師手把手巡桌排錯到底！
全班極限 6 席深度陪伴，API 沒跑通不准走。

📅 時間：11/18 (週三) 14:00 - 16:00 ｜ 台東市正氣北路166巷90號（家宅）
🎯 主題：Antigravity 操作 ✕ Meta 官方自動發文串接 (FB / Threads API)
💰 費用：老學員（含第 1 講夥伴）0 元免單 ｜ 新朋友單堂 $500

📝 實體入席申請表：https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
💬 官方 LINE 諮詢：https://lin.ee/z83YSq6"""
    }
]

LOG_FILE = Path(__file__).parent / "schedule_lesson_02_threads.log"
STATE_FILE = Path(__file__).parent / "threads_lesson_02_state.json"

def get_state():
    if STATE_FILE.exists():
        try:
            import json
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_state(state):
    try:
        import json
        STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        log_print(f"⚠️ 儲存狀態檔失敗: {e}")

def log_print(msg: str):
    ts = datetime.now(TZ_TW).strftime("[%Y-%m-%d %H:%M:%S]")
    full_msg = f"{ts} {msg}"
    print(full_msg)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(full_msg + "\n")
    except Exception as e:
        pass

def publish_single_post(task):
    state = get_state()
    task_id_str = str(task["id"])
    if state.get(task_id_str, {}).get("published"):
        log_print(f"🛑 [戴明安燈防呆] 篇號 {task['id']} 過去已成功發布 (Post ID: {state[task_id_str].get('post_id')})，跳過重複發射！")
        return True, state[task_id_str].get("url")

    log_print("=" * 60)
    log_print(f"🚀 [Kage] 正在執行發射：{task['name']}")
    log_print("=" * 60)
    
    img_path = task["img_path"]
    cdn_url = upload_local_image_to_meta_cdn(img_path)
    
    creation_id = create_media_container(
        text=task["message"],
        image_url=cdn_url,
        topic_tag="生活服務"
    )
    if not creation_id:
        log_print("❌ 建立貼文容器失敗")
        return False, None
        
    time.sleep(3)
    post_id = publish_container(creation_id)
    if not post_id:
        log_print("❌ 主貼文發布失敗")
        return False, None
        
    th_url = f"https://www.threads.net/@hellotaitung/post/{post_id}"
    log_print(f"🎉 Threads 主貼文發布成功！ID: {post_id}")
    log_print(f"🔗 貼文網址: {th_url}")
    
    state[task_id_str] = {
        "published": True,
        "post_id": post_id,
        "url": th_url,
        "published_at": datetime.now(TZ_TW).strftime("%Y-%m-%d %H:%M:%S")
    }
    save_state(state)
    
    log_print("💬 正在自動補掛第一則置頂留言（表單）...")
    time.sleep(3)
    reply_creation_id = create_media_container(
        text=task["comment"],
        reply_to_id=post_id
    )
    if reply_creation_id:
        time.sleep(2)
        reply_id = publish_container(reply_creation_id)
        if reply_id:
            log_print(f"✅ 第一則留言發布成功！Reply ID: {reply_id}")
            state[task_id_str]["reply_id"] = reply_id
            save_state(state)
            
    return True, th_url

def run_daemon():
    log_print("🛰️ [Kage] 啟動 Threads 定時排程守衛 (Daemon)...")
    log_print("當前排程佇列：")
    for t in THREADS_SCHEDULE_QUEUE:
        log_print(f"• ID {t['id']}: {t['name']} ➔ 預計發布時間: {t['target_dt'].strftime('%Y-%m-%d %H:%M:%S (台灣時間)')}")
        
    executed_ids = set()
    while len(executed_ids) < len(THREADS_SCHEDULE_QUEUE):
        now = datetime.now(TZ_TW)
        for t in THREADS_SCHEDULE_QUEUE:
            if t["id"] not in executed_ids and now >= t["target_dt"]:
                log_print(f"⏰ 時間已到達！觸發發射：{t['name']}")
                ok, url = publish_single_post(t)
                executed_ids.add(t["id"])
        time.sleep(30)
    log_print("🏁 全部排程任務發射完畢，守衛任務圓滿收工！")

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--run-now":
        target_id = int(sys.argv[2])
        for t in THREADS_SCHEDULE_QUEUE:
            if t["id"] == target_id:
                publish_single_post(t)
                break
    else:
        run_daemon()
