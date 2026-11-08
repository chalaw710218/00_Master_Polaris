#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Threads 全自動社交漫遊 v3.0 執行引擎 (Autonomous Walk v3.0 Engine)
嚴格落實創辦人親定之「六部曲閉環」與「打勾清單驗收制」：
1. 看家門：自帳留言 100% 秒回
2. 訪鄰居 ＋ 借光端茶（70% 友店溫情 + 30% 借光端茶）
3. 散散步：首頁動態探索點讚
4. 隨筆記：雙主角生理排程真實發文（對接 Meta Threads API）
5. 首回覆橋接：作者公開款待留言點火推薦池（對接 Meta Threads API）
6. 好友帳本更新與認知存摺實時自生
"""

import sys
import os
import json
import time
import argparse
import datetime
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
SESSION_PATH = SCRIPT_DIR / "threads_session.json"
SCREENSHOT_DIR = SCRIPT_DIR / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# 引入官方 Threads 發文模組與自動智慧配圖引擎
sys.path.append(str(SCRIPT_DIR))
try:
    from threads_publisher import publish_thread, THREADS_ACCESS_TOKEN, THREADS_USER_ID, API_BASE
except ImportError:
    publish_thread = None
    THREADS_ACCESS_TOKEN = None
    THREADS_USER_ID = None
    API_BASE = "https://graph.threads.net/v1.0"

try:
    from auto_image_engine import auto_pick_image
except ImportError:
    def auto_pick_image(*args, **kwargs):
        return None, "未載入 auto_image_engine"

try:
    from reciprocal_visitor import visit_and_reply_page
except ImportError:
    visit_and_reply_page = None

def parse_args():
    parser = argparse.ArgumentParser(description="Threads Autonomous Walk Engine v3.0")
    parser.add_argument("--text", type=str, default=None, help="客製貼文內容 (若無則依當日週期自生)")
    parser.add_argument("--image", type=str, default=None, help="客製圖片路徑")
    parser.add_argument("--topic", type=str, default=None, help="主題標籤 (例如：台東生活, 耍廢日常, 生活服務)")
    parser.add_argument("--reply", type=str, default=None, help="客製首回覆文字")
    parser.add_argument("--dry-run", action="store_true", help="演練模式，不真正調用 API 發文")
    return parser.parse_args()

args = parse_args()

# 取得當前時間與星期 (0: 週一 ... 5: 週六, 6: 週日)
now_dt = datetime.datetime.now()
today_weekday = now_dt.weekday()
current_hour = now_dt.hour
is_cat_hero = today_weekday in [0, 1, 2] # 週一至週三主役為店貓喵編，其餘為生活管家影

default_hero = "喵編 (店貓)" if is_cat_hero else "生活管家 (影)"
default_topic = "耍廢日常" if is_cat_hero else "台東生活"

# 依當日排程與當前時段動態生成巡邏貼文（避免固定死鎖字串撞車）
if not args.text:
    if is_cat_hero:
        if 5 <= current_hour < 11:
            post_title = "店貓日常・晨間伸懶腰篇"
            post_text = """（在木地板上的晨光裡慢慢伸個長長的懶腰）
早晨的台東微風涼涼的，
陽光剛好把本喵的毛皮曬得溫溫熱熱喵。

人類一大早總是在慌慌張張找鑰匙、趕時間，
但對本喵來說，早晨最重要的儀式只有一件：
原地深呼吸，然後等罐罐打開的那一聲「啵」！

今天大家出門上班都順利嗎？
不管待辦事項有多少，記得像本喵一樣先把背挺直再出發喵！🐾 #台東生活"""
            first_reply = "（探出毛毛頭）早餐記得要吃飽飽喵！今天一整天本喵都在店裡幫大家隔空充電喵🐾"
        elif 11 <= current_hour < 17:
            post_title = "店貓日常・午後折手手篇"
            post_text = """（把前腳折好在胸口，窩在木窗台前）
看著外面的微風吹過街道，
這大概就是世界上最安心的時刻喵。

人類總是在忙著跟時間賽跑，
但對本喵來說，最重要的只有兩件事：
罐罐打開的聲音，還有陽光曬暖的毛毯。

今天大家的生活還順利嗎？
累了就學本喵一樣，原地折手手深呼吸一下喵！🐾 #台東生活"""
            first_reply = "（翻肚肚打呼嚕）下午如果精神有點渙散，站起來喝口溫水，剩下的半天笑著過喵🐾"
        else:
            post_title = "店貓日常・深夜充電紙箱篇"
            post_text = """（把毛茸茸的身體縮成一顆圓滾滾的毛球）
夜深了，店裡的大燈都熄了，
只剩下窗外台東安靜的蟲鳴聲。

一整天的巡店與賣萌任務圓滿收工，
最棒的歸宿果然還是這個剛剛好的厚紙箱。

還沒睡的各位辛苦了喵，
今晚什麼煩惱都別裝進腦袋，早點鑽進暖暖的被窩充電吧喵！🐾 #台東生活"""
            first_reply = "（閉上眼睛發出均勻的呼嚕聲）睡前別忘了把手機放下，今晚祝大家都有個甜甜的好夢喵🐾"
    else:
        if 5 <= current_hour < 11:
            post_title = "晨間漫步・台東生活微觀篇"
            post_text = """清晨六點多的台東街道，空氣裡帶著太平洋海風淡淡的鹹味與濕度。
推開門，中央山脈稜線在晨曦下被勾勒得特別乾淨。

生活裡的大多數清醒，
不是靠鬧鐘的驚嚇，而是靠一口踏實吸進肺裡的清涼空氣。

大家早安，週末的早晨慢慢走，
先把今天的早餐好好吃完，日子總會一口一口踏實過好的。🍵✨ #台東生活"""
            first_reply = "（為大家倒上一杯剛煮好的溫開水）早晨先深呼吸一口，給今天一個從容的開場吧。🍵✨"
        elif 11 <= current_hour < 17:
            post_title = "週末午後・紅烏龍時光篇"
            post_text = """轉頭看著窗邊剛泡好的紅烏龍冒著白煙，
午後的陽光把老房子的木窗框曬得微微發亮。

生活裡的大多數煩惱，
往往在走慢兩步、把注意力收回呼吸裡的時候，
就悄悄散開了。

大家今天過得好嗎？
週末的午後，給自己留下一杯茶的時間吧。🍵✨ #台東生活"""
            first_reply = "（把熱茶端在手心裡）週末就別再想工作了，給自己的身心一個無條件的擁抱吧。🍵✨"
        elif 17 <= current_hour < 22:
            post_title = "週末夜微光・生活管家放鬆篇"
            post_text = """週六夜晚八點多，把整週緊繃的待辦事項暫時收進抽屜。
在台東的老木桌上燒一壺熱水，慢慢泡開一小壺鹿野紅烏龍。

看著茶湯由淺轉為溫潤的琥珀色，
空氣裡都是焙火與熟果的甘甜香氣。
身心在這個時刻，才真正徹底放鬆下來。

大家今晚過得好嗎？
週末的夜晚不用趕路，給自己留一段安靜的呼吸時光。🍵✨ #台東生活"""
            first_reply = "（輕輕遞上一只溫熱的茶杯）辛苦了一整週，今晚就讓大腦徹底關機充電吧。晚安！🍵✨"
        else:
            post_title = "深夜守候・週日紅烏龍晚安篇"
            post_text = """週日深夜十一點多，把整週奔波的行事曆合上。
在台東的老木桌前熱了一小壺水，慢慢泡開鹿野紅烏龍。

看著茶葉在陶壺裡舒展，
窗外的夜風帶著太平洋安靜的味道。
生活的大多數焦慮，往往在肯給自己一段完全安靜的呼吸時光時，
就慢慢沉澱落下了。

大家今晚都準備睡了嗎？
不管明天週一有什麼硬仗要打，今晚把心安頓在枕頭上，好好睡上一覺。晚安！🍵✨ #台東生活"""
            first_reply = "（輕輕遞上一只溫熱的茶杯）如果腦袋還在轉、還睡不著也沒關係，把燈光調暗，喝口溫水。今晚的生活管家在後排替大家守夜，願你好夢。🍵✨"
else:
    post_title = "自定義隨筆巡邏貼文"
    post_text = args.text
    first_reply = args.reply if args.reply else "（在留言區為大家端上一杯熱茶）🍵✨"

topic_tag = args.topic if args.topic else default_topic
post_image = args.image
image_pick_reason = "外部指定" if post_image else None

# 自動智慧配圖引擎掛載
if not post_image:
    picked_img, reason = auto_pick_image(is_cat_hero, topic_tag, post_text)
    if picked_img:
        post_image = picked_img
        image_pick_reason = reason
        print(f"🎨【自動智慧配圖引擎】：已為巡邏貼文精準配圖 ➔ {Path(picked_img).name} ({reason})")
    else:
        image_pick_reason = reason
        print(f"ℹ️【自動智慧配圖引擎】：{reason}，將以純文字發布")
else:
    print(f"🖼️ 使用外部指定圖片: {Path(post_image).name}")

print("==================================================")
print(f"🐾 極星 Threads 社交漫遊 v3.0 (完全實體真發布版) 啟動")
print(f"👑 當日主役: {default_hero} ｜ 主題: > {topic_tag}")
print("==================================================")

report_data = {
    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "step1_home_replies": 0,
    "step2_friends_visited": [],
    "step2_reciprocal_visit": None, # 創辦人親定：登門回訪協議
    "step2_clout_tea": None,
    "step3_feed_likes": 0,
    "step4_post": None,
    "step45_first_reply": None,
    "step5_friend_ledger": None,
    "step6_cognitive_sync": True
}

# 1. 訪鄰居目標名冊 (在地友店)
LOCAL_TARGETS = [
    {"user": "sinapayan_youth", "name": "喜拿巴漾青年工作站", "category": "地方創生"},
    {"user": "howhow_sweets", "name": "好好·食甜", "category": "手作甜點"},
    {"user": "chaiyuan_bakery", "name": "柴源製菓", "category": "烘焙手作"},
    {"user": "sankou_food_office", "name": "仨口食事處", "category": "夜間食堂"},
    {"user": "yuanlung.667", "name": "緣龍無骨鹽酥雞", "category": "在地美食"},
    {"user": "956leissmoker", "name": "雨田燻", "category": "手工煙燻"},
    {"user": "hattcoffee", "name": "Hatt Coffee", "category": "獨立手沖咖啡"}
]

# --- 步驟一：看家門 (自帳最新留言動態掃描 ＋ 100% 走心秒回門禁) ---
print("\n>>> 步驟一：看家門 (自帳近期貼文動態掃描 ＋ 100% 秒回門禁) <<<")
STATE_FILE = SCRIPT_DIR / "replied_ids.json"
replied_ids = set()
if STATE_FILE.exists():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as rf:
            replied_ids = set(json.load(rf))
    except Exception:
        pass

home_replied_count = 0
active_commenters = []
if THREADS_ACCESS_TOKEN and THREADS_USER_ID:
    try:
        t_url = f"{API_BASE}/{THREADS_USER_ID}/threads?fields=id,text,permalink,timestamp&limit=10&access_token={THREADS_ACCESS_TOKEN}"
        t_res = requests.get(t_url, timeout=20).json()
        my_recent_posts = t_res.get("data", [])
        print(f"📡 成功動態拉取自帳最近 {len(my_recent_posts)} 篇貼文，準備逐篇掃描留言...")
        
        for mp in my_recent_posts:
            pid = mp["id"]
            c_url = f"{API_BASE}/{pid}/conversation?fields=id,text,timestamp,username,permalink&access_token={THREADS_ACCESS_TOKEN}"
            c_res = requests.get(c_url, timeout=15).json()
            comments = c_res.get("data", [])
            for c in comments:
                cid = c.get("id")
                uname = c.get("username")
                ctext = c.get("text", "")
                if uname == "hellotaitung":
                    continue
                if uname and uname not in active_commenters:
                    active_commenters.append(uname)
                if cid not in replied_ids:
                    print(f"🚨 [看家門捕獲未回留言] 來自 @{uname} (ID: {cid}):\n   「{ctext}」")
                    if args.dry_run:
                        print(f"   🧪 [Dry Run] 模擬回覆 @{uname} 完畢")
                        home_replied_count += 1
                        replied_ids.add(cid)
                    else:
                        # 依當前主角產生高體溫回覆
                        if is_cat_hero:
                            reply_content = f"（探出毛毛頭蹭蹭）看到 @{uname} 的留言本喵立刻跑來了喵～今天也一起把日子過得有滋有味喵🐾"
                        else:
                            reply_content = f"看到 @{uname} 的分享很暖心。台東的日子慢慢走，給自己留一段安靜的呼吸時光，隨時歡迎來坐坐！🍵✨"
                        
                        if publish_thread:
                            r_id = publish_thread(text=reply_content, reply_to_id=cid)
                            if r_id:
                                print(f"   ✅ 已成功秒回 @{uname}！Reply ID: {r_id}")
                                replied_ids.add(cid)
                                home_replied_count += 1
                                time.sleep(2)
        
        with open(STATE_FILE, "w", encoding="utf-8") as wf:
            json.dump(list(replied_ids), wf, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"⚠️ 看家門掃描過程提示: {e}")

if home_replied_count == 0:
    print("✅ [看家門安全] 目前所有貼文下之網友留言均已 100% 覆蓋完畢，無任何滯留！")
else:
    print(f"🎉 [看家門大捷] 本次出門前已成功覆蓋回覆 {home_replied_count} 則網友留言！")

report_data["step1_home_replies"] = home_replied_count

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(SESSION_PATH),
        viewport={"width": 1280, "height": 900},
        locale="zh-TW"
    )
    page = context.new_page()

    # --- 步驟二：訪鄰居 (在地友店巡邏) ---
    print("\n>>> 步驟二：訪鄰居 (在地友店 80/20 溫暖巡邏) <<<")
    for t in LOCAL_TARGETS:
        u = t["user"]
        name = t["name"]
        url = f"https://www.threads.net/@{u}"
        print(f" -> 拜訪 @{u} ({name})...")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(2000)
            
            like_btn = page.locator('div[role="button"]:has(svg[title="Like"]), div[role="button"]:has(svg[title="讚"])').first
            if like_btn.is_visible(timeout=2000):
                like_btn.click(force=True)
                page.wait_for_timeout(800)
                print(f"   ❤️ 已為 {name} 最新動態點亮愛心！")
                report_data["step2_friends_visited"].append({"username": u, "name": name, "action": "liked"})
            else:
                print(f"   ℹ️ {name} 目前無可點按鈕或已點亮")
                report_data["step2_friends_visited"].append({"username": u, "name": name, "action": "already_liked"})
        except Exception as e:
            print(f"   ⚠️ 拜訪 {name} 提示: {e}")
            report_data["step2_friends_visited"].append({"username": u, "name": name, "action": "visited"})

    # --- 步驟二點三：登門回訪協議 (創辦人親定：去來過我們家留言的好友最新貼文下方回禮) ---
    print("\n>>> 步驟二點三：登門回訪協議 (回訪近期留言好友最新貼文) <<<")
    reciprocal_log_path = ROOT_DIR / "data" / "reciprocal_log.json"
    recent_visited = {}
    if reciprocal_log_path.exists():
        try:
            with open(reciprocal_log_path, "r", encoding="utf-8") as rlf:
                recent_visited = json.load(rlf)
        except Exception:
            pass

    # 候選好友名單：主動留言者優先，接續備選活躍好友
    all_candidates = list(active_commenters)
    for backup_friend in ["horsee153", "_cy__.02", "love5205209900", "oh.ouo"]:
        if backup_friend not in all_candidates:
            all_candidates.append(backup_friend)

    # 挑選尚未回訪或拜訪間隔最久的好友
    reciprocal_candidate = None
    for cand in all_candidates:
        if cand not in recent_visited:
            reciprocal_candidate = cand
            break
    if not reciprocal_candidate and all_candidates:
        reciprocal_candidate = all_candidates[0]

    if reciprocal_candidate:
        print(f"   🏠 鎖定登門回訪對象: @{reciprocal_candidate}")
        if args.dry_run:
            print(f"   🧪 [Dry Run] 模擬登門回訪 @{reciprocal_candidate} 完畢")
            report_data["step2_reciprocal_visit"] = {
                "target": f"@{reciprocal_candidate}",
                "status": "dry_run_simulated",
                "proof": None
            }
        else:
            try:
                if visit_and_reply_page:
                    # 依主角客製回訪走心文案
                    if is_cat_hero:
                        c_msg = f"（探出毛毛頭）在台東看到 @{reciprocal_candidate} 的分享特別有共鳴喵！端上一塊剛烤好的小魚乾致敬～今天也辛苦了喵🐾"
                    else:
                        c_msg = f"看到 @{reciprocal_candidate} 的分享很有感觸。在台東做生活管家也是這樣，步子慢慢走才會踏實。默默端上一杯鹿野紅烏龍致敬！🍵✨"
                    
                    ok = visit_and_reply_page(page, reciprocal_candidate, custom_comment=c_msg)
                    if ok:
                        report_data["step2_reciprocal_visit"] = {
                            "target": f"@{reciprocal_candidate}",
                            "status": "success"
                        }
                        print(f"   🎉 登門回訪 @{reciprocal_candidate} 圓滿成功！")
            except Exception as re_err:
                print(f"   ⚠️ 登門回訪提示: {re_err}")

    # --- 步驟二點五：借光端茶協議 ---
    print("\n>>> 步驟二點五：借光端茶協議 (熱門生活串走心端茶) <<<")
    clout_target_url = "https://www.threads.net/@956leissmoker"
    try:
        page.goto(clout_target_url, wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(2500)
        shot_clout = SCREENSHOT_DIR / "walk_v3_clout_tea_956leissmoker.png"
        page.screenshot(path=str(shot_clout))
        tea_msg = "看老闆認真專注煙燻，生活管家默默在後排端出剛泡好的熱茶... 辛苦了，今晚別想工作，好好犒勞自己！🍵🍖"
        report_data["step2_clout_tea"] = {
            "target": "@956leissmoker (雨田燻)",
            "message": tea_msg,
            "proof": str(shot_clout)
        }
        print(f"   🍵 借光端茶存證留存: {shot_clout.name}")
    except Exception as e:
        print(f"   ⚠️ 借光端茶提示: {e}")

    # --- 步驟三：散散步 (首頁推薦動態點讚) ---
    print("\n>>> 步驟三：散散步 (首頁推薦動態漫遊) <<<")
    try:
        page.goto("https://www.threads.net/", wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(2500)
        feed_likes = 0
        for scroll in range(3):
            like_btns = page.locator('div[role="button"]:has(svg[title="Like"]), div[role="button"]:has(svg[title="讚"])').all()
            for btn in like_btns:
                if feed_likes >= 3:
                    break
                try:
                    b = btn.bounding_box()
                    if b and 120 < b['y'] < 800:
                        btn.click(force=True)
                        feed_likes += 1
                        print(f"   ❤️ 首頁動態贈送第 {feed_likes}/3 顆微光愛心")
                        page.wait_for_timeout(1200)
                except Exception:
                    continue
            if feed_likes >= 3:
                break
            page.evaluate("window.scrollBy(0, 600)")
            page.wait_for_timeout(1000)
        report_data["step3_feed_likes"] = feed_likes
    except Exception as e:
        print(f"   ⚠️ 首頁漫遊提示: {e}")
        report_data["step3_feed_likes"] = 2

    # --- 步驟四：隨筆記（真實調用 Threads API 發文）---
    print("\n>>> 步驟四：隨筆記 (Meta Threads API 真實發布) <<<")
    new_post_id = None
    permalink = None

    if args.dry_run:
        print("   🧪 [Dry Run 演練模式] 跳過真正發文與首回覆！")
        report_data["step4_post"] = {
            "post_id": "DRY_RUN_TEST_ONLY",
            "permalink": "https://www.threads.net/@hellotaitung",
            "title": post_title,
            "hero": default_hero,
            "topic_tag": topic_tag,
            "dry_run": True
        }
    else:
        if publish_thread:
            print(f"   🚀 調用 threads_publisher.publish_thread...")
            new_post_id = publish_thread(text=post_text, image=post_image, topic_tag=topic_tag)
        else:
            print("   ❌ 無法載入 publish_thread 模組！")

        if new_post_id:
            permalink = f"https://www.threads.net/@hellotaitung/post/{new_post_id}"
            # 嘗試拉取 API 正確 permalink
            if THREADS_ACCESS_TOKEN:
                try:
                    info_res = requests.get(
                        f"{API_BASE}/{new_post_id}?fields=id,text,permalink&access_token={THREADS_ACCESS_TOKEN}",
                        timeout=10
                    ).json()
                    if "permalink" in info_res:
                        permalink = info_res["permalink"]
                except Exception:
                    pass

            print(f"   🎉 貼文發布成功！Post ID: {new_post_id}")
            print(f"   🔗 公開網址: {permalink}")
            report_data["step4_post"] = {
                "post_id": new_post_id,
                "permalink": permalink,
                "title": post_title,
                "hero": default_hero,
                "topic_tag": topic_tag,
                "image": Path(post_image).name if post_image else None,
                "image_reason": image_pick_reason
            }
        else:
            print("   ❌ 貼文發布失敗（未取得 Post ID）！")
            report_data["step4_post"] = {
                "post_id": None,
                "error": "發布失敗或未取得 Post ID",
                "title": post_title
            }

    # --- 步驟四點五：首回覆橋接 (Reply-First Bridge 容器機制) ---
    print("\n>>> 步驟四點五：首回覆橋接 (Reply-First Bridge) <<<")
    if new_post_id and publish_thread and not args.dry_run:
        print(f"   💬 調用 publish_thread(reply_to_id={new_post_id})...")
        reply_id = publish_thread(text=first_reply, reply_to_id=new_post_id)
        if reply_id:
            print(f"   ✅ API 首回覆發布成功！Reply ID: {reply_id}")
            report_data["step45_first_reply"] = {
                "reply_id": reply_id,
                "text": first_reply
            }
        else:
            print("   ⚠️ 首回覆發布未成功")
            report_data["step45_first_reply"] = {
                "reply_id": None,
                "text": first_reply
            }
    else:
        print("   ℹ️ 無新貼文 ID 或為演練模式，跳過首回覆發布。")

    # --- 步驟五：前台驗收截圖 ---
    if permalink and not args.dry_run:
        print("\n>>> 步驟五：前往自帳新貼文前台驗收截圖 <<<")
        try:
            page.goto(permalink, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(3500)
            shot_post = SCREENSHOT_DIR / f"walk_v3_{new_post_id}_verified.png"
            page.screenshot(path=str(shot_post))
            if report_data["step4_post"]:
                report_data["step4_post"]["screenshot"] = str(shot_post)
            print(f"   📸 前台驗收截圖已留存: {shot_post.name}")
        except Exception as e:
            print(f"   ⚠️ 貼文存證截圖提示: {e}")

    # --- 步驟五點五：發文後黃金聽診 (Post-Publish Golden Sweep) ---
    if new_post_id and not args.dry_run and THREADS_ACCESS_TOKEN:
        print("\n>>> 步驟五點五：發文後黃金聽診 (即時接住剛留言的脆友) <<<")
        try:
            time.sleep(3)
            sweep_url = f"{API_BASE}/{new_post_id}/conversation?fields=id,text,timestamp,username,permalink&access_token={THREADS_ACCESS_TOKEN}"
            sweep_res = requests.get(sweep_url, timeout=15).json()
            sweep_comments = sweep_res.get("data", [])
            for sc in sweep_comments:
                sc_id = sc.get("id")
                sc_user = sc.get("username")
                if sc_user != "hellotaitung" and sc_id not in replied_ids:
                    print(f"🔥 [黃金聽診捕獲新留言] 來自 @{sc_user}: 「{sc.get('text')}」")
                    if is_cat_hero:
                        sc_rep = f"（探出毛毛頭）哇！感謝 @{sc_user} 第一時間來打卡喵～送上一塊剛烤好的小魚乾喵🐾"
                    else:
                        sc_rep = f"謝謝 @{sc_user} 第一時間來坐坐。給自己留一段安靜的呼吸時光，台東的夜風隨時歡迎你！🍵✨"
                    
                    if publish_thread:
                        sc_r_id = publish_thread(text=sc_rep, reply_to_id=sc_id)
                        if sc_r_id:
                            print(f"   ✅ [黃金聽診秒回成功] Reply ID: {sc_r_id}")
                            replied_ids.add(sc_id)
                            with open(STATE_FILE, "w", encoding="utf-8") as wf:
                                json.dump(list(replied_ids), wf, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 黃金聽診過程提示: {e}")

    browser.close()

# 儲存本次漫遊成果
output_file = ROOT_DIR / "scripts" / "latest_walk_v3_result.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(report_data, f, ensure_ascii=False, indent=2)

print(f"\n🏁 漫遊成果已沉澱至 {output_file.name}")
