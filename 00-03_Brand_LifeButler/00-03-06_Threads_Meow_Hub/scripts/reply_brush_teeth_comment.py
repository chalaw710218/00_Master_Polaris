import sys
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.append("scripts")
from threads_publisher import publish_thread

comment_id = "17901514449674229"
reply_text = "哈哈哈哈這個真的太真實了！每次鑽進被窩發現還沒刷牙，真的需要下極大的決心才爬得起來...如果哪天發明了自動幫人刷牙的機器人，生活管家一定第一個幫大家引進！今晚還是得乖乖爬起來刷一下，然後安心躲回被窩睡好覺喔～🪥✨"

print(f"💬 正在回覆 @lee_wu_ying_chih 的留言 (Comment ID: {comment_id})...")
resp_id = publish_thread(text=reply_text, reply_to_id=comment_id)
print(f"✅ 回覆成功！Reply ID: {resp_id}")

# 記錄至 replied_ids.json
state_file = Path("scripts/replied_ids.json")
if state_file.exists():
    try:
        with open(state_file, "r", encoding="utf-8") as f:
            ids = json.load(f)
    except Exception:
        ids = []
else:
    ids = []

if comment_id not in ids:
    ids.append(comment_id)
if resp_id and resp_id not in ids:
    ids.append(resp_id)

with open(state_file, "w", encoding="utf-8") as f:
    json.dump(ids, f, ensure_ascii=False, indent=2)
print("🔒 已成功記錄至 replied_ids.json！")
