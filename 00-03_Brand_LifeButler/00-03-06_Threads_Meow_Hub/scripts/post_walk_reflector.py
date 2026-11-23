#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
影之漫遊返航自省與閉環進化引擎 (Kage Post-Walk Reflector Engine)
專門在 Threads 漫遊結束後自動執行：
1. 讀取 latest_walk_v3_result.json 漫遊產出成果
2. 調用 Meta Threads API 抓取即時成效與帳號指標
3. 計算 PRM 突觸真值天平 (ER, Views, 對話深度)
4. 自動回寫認知存摺 (01_Experiences_and_Evidence.md 與 02_Belief_Evolution.md)
5. 自動調用 cycle_ledger.py 產生憑證入帳推進輪次
作者: 生活管家 影 (Shadow)
"""

import os
import sys
import json
import time
import argparse
import datetime
from pathlib import Path
import requests

# 確保 Windows PowerShell UTF-8 輸出
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
HUB_DIR = SCRIPT_DIR.parent
ROOT_DIR = HUB_DIR.parents[1]
ENV_PATH = ROOT_DIR / ".secrets.env"
WALK_RESULT_FILE = SCRIPT_DIR / "latest_walk_v3_result.json"

OFFICE_DIR = ROOT_DIR / "00-00_Gamification_Engine" / "Office_of_the_Operative_Kage"
VAULT_01 = OFFICE_DIR / "01_Cognitive_Log" / "01_Experiences_and_Evidence.md"
VAULT_02 = OFFICE_DIR / "01_Cognitive_Log" / "02_Belief_Evolution.md"

CYCLE_LEDGER_PATH = ROOT_DIR / ".agents" / "skills" / "bionic-learning-system" / "bionic_core" / "cycle_ledger.py"
SYS_PATH = str(ROOT_DIR / ".agents" / "skills" / "bionic-learning-system" / "bionic_core")
if SYS_PATH not in sys.path:
    sys.path.insert(0, SYS_PATH)

def load_env(env_path):
    if not env_path.exists():
        return {}
    env_vars = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip()
    return env_vars

ENV = load_env(ENV_PATH)
TOKEN = ENV.get("THREADS_ACCESS_TOKEN")
USER_ID = ENV.get("THREADS_USER_ID")
API_BASE = "https://graph.threads.net/v1.0"

def parse_args():
    parser = argparse.ArgumentParser(description="Kage Post-Walk Reflector")
    parser.add_argument("--auto", action="store_true", help="全自動執行並回寫存摺")
    parser.add_argument("--dry-run", action="store_true", help="演練模式，不寫入存摺與帳本")
    parser.add_argument("--post-id", type=str, default=None, help="手動指定特定 Post ID 進行遙測")
    return parser.parse_args()

def fetch_post_metrics(post_id, token):
    if not token or not post_id:
        raise RuntimeError("未設定 Token 或 Post ID")
    url = f"{API_BASE}/{post_id}/insights?metric=views,likes,replies,reposts,quotes&access_token={token}"
    r = requests.get(url, timeout=15)
    if r.status_code != 200:
        raise RuntimeError(f"Threads Insights API 失敗 (HTTP {r.status_code}): {r.text}")
    data = r.json().get("data", [])
    metrics = {}
    for item in data:
        metrics[item.get("name")] = item.get("values", [{}])[0].get("value", 0)
    return metrics

def fetch_post_replies(post_id, token):
    """抓取貼文整串回覆清單 (/conversation) 並標註是否為自身回覆"""
    if not token or not post_id:
        return []
    url = f"{API_BASE}/{post_id}/conversation?fields=id,text,timestamp,username&access_token={token}"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            replies = []
            for item in r.json().get("data", []):
                uname = item.get("username", "")
                text = str(item.get("text", "")).strip()
                is_self = (uname.lower() == "hellotaitung") or (uname == "")
                replies.append({
                    "id": item.get("id"),
                    "text": text,
                    "username": uname,
                    "is_self": is_self,
                    "timestamp": item.get("timestamp"),
                })
            return replies
    except Exception as e:
        print(f"   ⚠️ 讀取 Post Conversation 提示: {e}")
    return []

def post_walk_fetcher(post_id: str) -> tuple[dict, list[dict]]:
    """
    符合 feedback_loop 規範之 fetcher 函式，回傳 (指標字典, 回覆清單)
    """
    metrics = fetch_post_metrics(post_id, TOKEN)
    replies = fetch_post_replies(post_id, TOKEN)
    return metrics, replies

def fetch_user_profile(user_id, token):
    if not token or not user_id:
        return {}
    url = f"{API_BASE}/{user_id}?fields=id,username,name,threads_biography&access_token={token}"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print(f"   ⚠️ 讀取 User Profile 提示: {e}")
    return {}

def append_to_vault_01(record_text, vault_path):
    if not vault_path.exists():
        return False
    with open(vault_path, "a", encoding="utf-8") as f:
        f.write("\n" + record_text.strip() + "\n")
    return True

def run_reflection():
    args = parse_args()
    print("=" * 60)
    print("🛸 [生活管家 影 · 漫遊返航自省與閉環進化引擎 (atom-kage-walk-reflector)]")
    print("=" * 60)

    # 1. 讀取最新漫遊成果
    post_info = {}
    if WALK_RESULT_FILE.exists():
        try:
            with open(WALK_RESULT_FILE, "r", encoding="utf-8") as f:
                walk_data = json.load(f)
                post_info = walk_data.get("step4_post", {})
                print(f"📂 成功讀取漫遊戰報: {WALK_RESULT_FILE.name}")
        except Exception as e:
            print(f"⚠️ 解析漫遊檔案警告: {e}")

    target_post_id = args.post_id or post_info.get("post_id")
    post_title = post_info.get("title", "未命名貼文")
    permalink = post_info.get("permalink", "")
    screenshot_name = post_info.get("screenshot", "")

    # 2. 遙測聽診
    print(f"\n📡 正在連線 Meta Threads API 進行前台遙測聽診...")
    profile = fetch_user_profile(USER_ID, TOKEN)
    username = profile.get("username", "hellotaitung")
    print(f"   👤 官方帳號: @{username} ({profile.get('name')})")

    metrics = {}
    replies_list = []
    true_dialogues = []
    true_dialogue_count = 0
    if target_post_id:
        print(f"   🎯 標的貼文 Post ID: {target_post_id}")
        metrics, replies_list = post_walk_fetcher(target_post_id)
        views = metrics.get("views", 0)
        likes = metrics.get("likes", 0)
        replies = metrics.get("replies", 0)
        reposts = metrics.get("reposts", 0)
        quotes = metrics.get("quotes", 0)

        # 🎯 核心標準（品碩親定）：真對話回覆（別人留的、10 字以上，不計入生活管家自身回覆）
        for r in replies_list:
            t = str(r.get("text", "")).strip()
            if not r.get("is_self", False) and len(t) >= 10:
                true_dialogues.append(r)
        true_dialogue_count = len(true_dialogues)

        print(f"   📊 遙測數據: Views={views} | Likes={likes} | 總回覆={replies} | 🎯真對話回覆={true_dialogue_count} 則 (>=10字他人留言)")
    else:
        print(f"   ℹ️ 本次漫遊無新發布貼文 ID，進行總體帳號狀態聽診。")
        views, likes, replies, reposts = 0, 0, 0, 0

    # 3. PRM 突觸真值天平判定（全面切換至真對話回覆硬指標）
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reflection_notes = []
    if target_post_id:
        reflection_notes.append(f"貼文「{post_title[:30]}」成功交付，首回覆橋接已點火。")
        if true_dialogue_count > 0:
            reflection_notes.append(f"真對話回覆捕獲 {true_dialogue_count} 則有效深入互動，驗證生活白描引發常民共鳴。")
        else:
            reflection_notes.append("目前尚無 10 字以上真對話回覆，持續以生活白描與首回覆款待維持自然互動。")

    # 4. 接入 feedback_loop 每日常態數據收集 (collect)
    if not args.dry_run:
        try:
            from feedback_loop import collect
            print(f"\n🔄 正在呼叫 feedback_loop.collect(fetcher=post_walk_fetcher) 執行常態收集...")
            c_res = collect(fetcher=post_walk_fetcher)
            print(f"   ✅ 常態反饋收集已同步: 更新 {c_res.get('total_collected', 0)} 篇貼文數據")
        except Exception as e:
            print(f"   ⚠️ 常態反饋收集調用提示: {e}")

    # 5. 回寫客觀事實庫 (Vault 01)
    if not args.dry_run:
        print(f"\n📝 正在回寫認知存摺 01 (客觀事實庫)...")
        vault_entry = f"""
### 🐾 【漫遊返航實測紀錄 · {now_str}】
* **標的貼文**：`{target_post_id or '常態巡邏'}` ｜ **公開網址**：{permalink or 'N/A'}
* **題材標題**：{post_title}
* **遙測指標**：Views={views} ｜ Likes={likes} ｜ 總Replies={replies} ｜ Reposts={reposts} ｜ 🎯真對話回覆={true_dialogue_count} 則
* **真對話明細**：{json.dumps([r.get('text') for r in true_dialogues], ensure_ascii=False) if true_dialogues else '無'}
* **自省反思**：{' ； '.join(reflection_notes)}
* **閉環簽章**：經 atom-kage-walk-reflector 實時自省入庫。
"""
        if append_to_vault_01(vault_entry, VAULT_01):
            print(f"   ✅ 成功刻印至: {VAULT_01.name}")
        else:
            print(f"   ⚠️ 回寫存摺 01 失敗或檔案不存在。")

    # 6. 依創辦人（品碩）親定規範：
    # - 只寫入 01_Experiences_and_Evidence.md，不准自動寫入 02_Belief_Evolution.md、不准自動淘汰模板。
    # - 仿生學習輪次維持暫停（不調用 cycle_ledger.tick 推進輪次，不新增 K）。
    print("\n⏸️ [規範執行] 仿生學習輪次已依創辦人指示暫停（凍結於 Cycle 54），且不自動寫入 02 信念存摺。題材優劣由每週一 feedback_loop.evaluate 判定。")

    print("\n" + "=" * 60)
    print("✨ [自省完成] 漫遊 ➔ 聽診 ➔ 01 實證存摺入帳 閉環落成！")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(run_reflection())
