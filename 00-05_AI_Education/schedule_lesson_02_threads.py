import os
import sys
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SCRIPTS_DIR = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\scripts"
BIONIC_CORE_DIR = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-system\bionic_core"
if SCRIPTS_DIR not in sys.path:
    sys.path.append(SCRIPTS_DIR)
if BIONIC_CORE_DIR not in sys.path:
    sys.path.insert(0, BIONIC_CORE_DIR)

import enforce as bionic_enforce
from threads_publisher import upload_local_image_to_meta_cdn, create_media_container, publish_container

TZ_TW = timezone(timedelta(hours=8))

# ==========================================
# 貼文庫設定 (Threads 11/16 11:30 & 11/17 11:30)
# ==========================================
THREADS_SCHEDULE_QUEUE = [
    {
        "id": "2_blueprint",
        "name": "第 2 講連載 · 今天中午 11:30【全新自動化藍圖篇】",
        "target_dt": datetime(2026, 11, 16, 11, 30, 0, tzinfo=TZ_TW),
        "img_path": r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_02_Antigravity_Meta_Automation\FB_Lesson_02_Automation_Blueprint.png",
        "message": """很多人花一兩萬去上 AI 課，回到店裡還是天天手動複製貼上、半夜盯著手機回留言。
坦白說，那不是學會 AI，那是變成了 AI 文案的廉價打工仔。

週三下午第 2 講，我們要帶大家把最煩的雜事直接物理消滅：
串接 Meta 官方合法 API，資料夾丟入圖文，Python 3 秒自動排程發 FB 與 Threads，24 小時留言自動秒回。

外面顧問收三萬塊的系統，週三下午我坐在你身邊，親手盯著你在自己筆電跑通。
老朋友 0 元免單，新朋友單堂 $500。
依然是 6 席極致小班，自備筆電，做完專屬發射台才准走。

表單放第一則留言，週三見。""",
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
        "id": "3_final_call",
        "name": "第 2 講連載 · 明天中午 11:30【最後 24H 登機倒數篇】",
        "target_dt": datetime(2026, 11, 17, 11, 30, 0, tzinfo=TZ_TW),
        "fb_post_id": "110505444816362_1164717582903810",
        "img_path": r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_02_Antigravity_Meta_Automation\FB_L02_03_Final_Call_Tomorrow.png",
        "message": """最後 24 小時。明天下午 14:00，正氣北路家宅開練。

第 2 講主題：【把社群發射台交給 Python 與 Meta 官方 API】。
徹底消滅每天半夜手動複製貼上、盯著手機回訊息的折磨。

說到做到，客廳就 6 張椅子，多一張都不加，絕無線上同步。
帶著你的筆電來，現場坐在你身邊，沒親手把專屬發射台跑通、發出第一篇，當天不准下課。

老朋友 0 元免單，新夥伴單堂 $500。
正選 6 席即刻關門。想把時間買回來的在地朋友，第一則留言申請。明天家宅見。""",
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
    print(full_msg, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(full_msg + "\n")
            f.flush()
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

    # 強制通過 bionic_core 先讀後寫閘門 (Fail-Closed)
    for off in ("kage", "taylor"):
        ok_gate, v_gate = bionic_enforce.gate(off, task["message"])
        if not ok_gate:
            log_print(f"🛑 [bionic_core/{off} 閘門阻斷] 拒絕發射：{v_gate}")
            return False, None
    log_print("🟢 [bionic_core 閘門放行] 已通過 kage 與 taylor 現役規則與停機鎖檢核")
    
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

    # 🔗 連動補掛 Facebook 貼文留言（戴明安燈 Poka-Yoke）
    fb_post_id = task.get("fb_post_id")
    if fb_post_id:
        log_print(f"💬 [戴明連動] 正在自動補掛 Facebook 貼文第一則留言 ({fb_post_id})...")
        try:
            root = Path(r'c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris')
            env = {}
            for line in open(root / '.secrets.env', encoding='utf-8'):
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    env[k.strip()] = v.strip()
            fb_token = env.get('FB_PAGE_ACCESS_TOKEN')
            url = f'https://graph.facebook.com/v20.0/{fb_post_id}/comments'
            r = requests.post(url, data={'access_token': fb_token, 'message': task["comment"]}, timeout=15).json()
            fb_comment_id = r.get('id')
            if fb_comment_id:
                log_print(f"✅ Facebook 第一則留言補掛成功！Reply ID: {fb_comment_id}")
                state[task_id_str]["fb_comment_id"] = fb_comment_id
                save_state(state)
            else:
                log_print(f"⚠️ Facebook 留言回傳異常: {r}")
        except Exception as e:
            log_print(f"⚠️ Facebook 留言發布失敗: {e}")

    # 🐾 【影之完全體閉環】：文案發射後，自動啟動「去逛逛」(Autonomous Walk) 漫遊引擎！
    log_print("🐾 [影 · 社交漫遊啟動] 貼文落地！立即喚醒 execute_autonomous_walk_v3.py 執行六部曲去逛逛...")
    try:
        walk_script = SCRIPTS_DIR / "execute_autonomous_walk_v3.py"
        if walk_script.exists():
            import subprocess
            subprocess.Popen([sys.executable, str(walk_script), "--patrol-only"])
            log_print("✅ 已成功派出影出門『去逛逛』（看家門、訪鄰居、借光端茶引流）！")
        else:
            log_print(f"⚠️ 找不到漫遊腳本: {walk_script}")
    except Exception as w_err:
        log_print(f"⚠️ 啟動去逛逛漫遊失敗: {w_err}")
            
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
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        for t in THREADS_SCHEDULE_QUEUE:
            img_ok = Path(t["img_path"]).is_file()
            k_ok, k_v = bionic_enforce.gate("kage", t["message"])
            t_ok, t_v = bionic_enforce.gate("taylor", t["message"])
            print(f"[DRY-RUN] 篇號 {t['id']} ({t['name']}): 圖片存在={img_ok} | kage閘門={'PASS' if k_ok else k_v} | taylor閘門={'PASS' if t_ok else t_v}")
            if not (img_ok and k_ok and t_ok):
                sys.exit(1)
        print("🟢 排程佇列 02 & 03 篇全數通過 bionic_core 閘門與圖片實體核驗！")
        sys.exit(0)
    elif len(sys.argv) > 2 and sys.argv[1] == "--run-now":
        target_id = int(sys.argv[2])
        for t in THREADS_SCHEDULE_QUEUE:
            if t["id"] == target_id:
                publish_single_post(t)
                break
    else:
        run_daemon()
