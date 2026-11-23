# -*- coding: utf-8 -*-
"""
生活管家 · 第 3 講 行銷排程自動發射守護神 (Daemon Scheduler)
精準監控時間，時間一到自動執行發射腳本並記錄日誌。
"""
import os
import sys
import time
import datetime
import subprocess

SCRIPT_DIR = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_03_Data_Architecture_Persona_Engineering"
LOG_FILE = os.path.join(SCRIPT_DIR, "scheduler_execution.log")
STATE_FILE = os.path.join(SCRIPT_DIR, "scheduler_state.json")

def log(msg):
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now_str}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# 定義三大發布任務目標時間
TASKS = [
    {
        "id": "post_02",
        "name": "第 2 篇【去塑料三刀法】",
        "target_time": "2026-11-24 08:30:00",
        "script": "publish_post02.py"
    },
    {
        "id": "post_03",
        "name": "第 3 篇【倒數 18 小時】",
        "target_time": "2026-11-24 19:30:00",
        "script": "publish_post03.py"
    },
    {
        "id": "post_04",
        "name": "第 4 篇【今天下午見】",
        "target_time": "2026-11-25 09:30:00",
        "script": "publish_post04.py"
    }
]

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                import json
                return json.load(f)
        except:
            return {}
    return {}

def save_state(state):
    import json
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def main():
    log("==========================================")
    log("🚀 生活管家自動發射守護神已啟動！")
    for t in TASKS:
        log(f"📌 排定任務: {t['name']} ➔ 目標時間: {t['target_time']}")
    log("==========================================")
    
    while True:
        state = load_state()
        now = datetime.datetime.now()
        
        all_done = True
        for task in TASKS:
            t_id = task["id"]
            if state.get(t_id, {}).get("status") == "DONE":
                continue
            
            all_done = False
            target_dt = datetime.datetime.strptime(task["target_time"], "%Y-%m-%d %H:%M:%S")
            
            if now >= target_dt:
                log(f"⏰ 觸發時間到達！開始執行: {task['name']} ({task['script']})")
                script_path = os.path.join(SCRIPT_DIR, task["script"])
                try:
                    res = subprocess.run([sys.executable, script_path], capture_output=True, text=True, encoding="utf-8")
                    log(f"執行輸出: {res.stdout}")
                    if res.returncode == 0:
                        log(f"✅ {task['name']} 發射成功！")
                        state[t_id] = {"status": "DONE", "executed_at": now.strftime("%Y-%m-%d %H:%M:%S")}
                        save_state(state)
                    else:
                        log(f"❌ {task['name']} 執行出錯: {res.stderr}")
                except Exception as e:
                    log(f"💥 執行異常: {str(e)}")
        
        if all_done:
            log("🎉 所有排程任務皆已圓滿執行完畢，守護神平穩退場！")
            break
            
        time.sleep(30)

if __name__ == "__main__":
    main()
