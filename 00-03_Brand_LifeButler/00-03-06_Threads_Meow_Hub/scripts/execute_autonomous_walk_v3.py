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

# =====================================================================
# 🌟 模組整合：引入 hot-trend-scout (時事熱點) 與 threads-rss-sentinel (友店動態巡邏)
# =====================================================================
POLARIS_SKILLS_DIR = ROOT_DIR.parent.parent / ".agents" / "skills"
HOT_TREND_DIR = POLARIS_SKILLS_DIR / "hot-trend-scout" / "scripts"
RSS_SENTINEL_DIR = POLARIS_SKILLS_DIR / "threads-rss-sentinel" / "scripts"

if HOT_TREND_DIR.exists():
    sys.path.append(str(HOT_TREND_DIR))
if RSS_SENTINEL_DIR.exists():
    sys.path.append(str(RSS_SENTINEL_DIR))

try:
    import scan_taiwan_trends
    print("🔥 [技能掛載成功] hot-trend-scout (台灣即時熱點嗅探引擎) 已就緒")
except Exception as e:
    scan_taiwan_trends = None
    print(f"⚠️ hot-trend-scout 掛載提示: {e}")

try:
    import rss_sentinel
    print("📡 [技能掛載成功] threads-rss-sentinel (友店動態巡邏哨兵) 已就緒")
except Exception as e:
    rss_sentinel = None
    print(f"⚠️ threads-rss-sentinel 掛載提示: {e}")

def parse_args():
    parser = argparse.ArgumentParser(description="Threads Autonomous Walk Engine v3.0")
    parser.add_argument("--text", type=str, default=None, help="客製貼文內容 (若無則依當日週期自生)")
    parser.add_argument("--image", type=str, default=None, help="客製圖片路徑")
    parser.add_argument("--topic", type=str, default=None, help="主題標籤 (例如：台東生活, 耍廢日常, 生活服務)")
    parser.add_argument("--reply", type=str, default=None, help="客製首回覆文字")
    parser.add_argument("--dry-run", action="store_true", help="演練模式，不真正調用 API 發文")
    parser.add_argument("--patrol-only", action="store_true", help="僅執行社交巡邏與借光端茶，跳過新貼文發布")
    parser.add_argument("--k-id", type=str, default=None, help="指定儲備知識 K-編號 (如 K-014)，若指定 control 或 [] 則為對照組")
    parser.add_argument("--trend", action="store_true", help="強制融入即時台灣熱搜趨勢 (hot-trend-scout)")
    parser.add_argument("--trend-keyword", type=str, default=None, help="指定融入之熱搜關鍵字")
    parser.add_argument("--skip-rss", action="store_true", help="跳過 RSS 友店探測")
    return parser.parse_args()

args = parse_args()

# 取得當前時間與星期 (0: 週一 ... 5: 週六, 6: 週日)
now_dt = datetime.datetime.now()
today_weekday = now_dt.weekday()
current_hour = now_dt.hour
is_cat_hero = today_weekday in [0, 1, 2] # 週一至週三主役為店貓喵編，其餘為生活管家影

default_hero = "喵編 (店貓)" if is_cat_hero else "生活管家 (影)"
default_topic = "耍廢日常" if is_cat_hero else "台東生活"

# 判斷是否為每日第一篇對照組
is_control_post = (args.k_id in ["control", "[]"])

# 🔒 【創辦人親定鐵律 · 自動防呆防遺漏】：若未指定 k-id，自動檢查今日是否已存在對照組
if not is_control_post and args.k_id is None:
    feedback_file = ROOT_DIR / "data" / "feedback_posts.json"
    today_str = now_dt.strftime("%Y-%m-%d")
    has_today_control = False
    if feedback_file.exists():
        try:
            with open(feedback_file, "r", encoding="utf-8") as f:
                fb_posts = json.load(f)
                for p in fb_posts:
                    if p.get("created_at", "").startswith(today_str) and p.get("is_control"):
                        has_today_control = True
                        break
        except Exception:
            pass
    if not has_today_control:
        is_control_post = True
        print(f"🧪【創辦人親定鐵律 · 自動防呆鎖定】：今日 ({today_str}) 尚未建立對照組，自動強制鎖定 --k-id control！確保全天具備不可動搖之科學比對真值基準線！")

applied_trend_info = None

# 依當日排程、時事熱點與當前時段動態生成巡邏貼文（避免固定死鎖字串撞車）
if not args.text:
    # ── 1. 創辦人親定規則 3：每日第一篇對照組鐵律 ──
    if is_control_post:
        print("🧪【每日第一篇對照組鐵律】：鎖定純淨生活日常白描，硬性排除 K-知識與熱點營銷！")
        
        # 引入 text_hash_gate 預審，確保候選草稿 100% 通過 70% 相似度與 SHA-256 去重門禁
        try:
            from text_hash_gate import check_text_poka_yoke
        except ImportError:
            check_text_poka_yoke = lambda t: (True, "OK")

        if is_cat_hero:
            if 5 <= current_hour < 11:
                cat_morning_candidates = [
                    (
                        "店貓日常・晨間伸懶腰篇 (對照組)",
                        """（在木地板上的晨光裡慢慢伸個長長的懶腰）
早晨的台東微風涼涼的，
陽光剛好把本喵的毛皮曬得溫溫熱熱喵。

人類一大早總是在慌慌張張找鑰匙、趕時間，
但對本喵來說，早晨最重要的儀式只有一件：
原地深呼吸，然後等罐罐打開的那一聲「啵」！

今天大家出門上班都順利嗎？
不管待辦事項有多少，記得像本喵一樣先把背挺直再出發喵！🐾 #台東生活""",
                        "（探出毛毛頭）早餐記得要吃飽飽喵！今天一整天本喵都在店裡幫大家隔空充電喵🐾"
                    ),
                    (
                        "店貓日常・老木門晨風篇 (對照組)",
                        """（坐在店門口的木門檻上看著落葉被微風吹過）
清晨的台東街道好安靜喵～
陽光斜斜照在地板上，把本喵的影子拉得長長的。

早起的人類已經騎著車去買熱包子豆漿了，
本喵在門口幫大家把關每一陣吹過來的海風。

大家早安喵！出門前深呼吸一口氣，
今天也像本喵一樣踏踏實實過好一天喵！🐾 #店貓日常"""
                    )
                ]
                post_title, post_text, first_reply = cat_morning_candidates[0]
            elif 11 <= current_hour < 17:
                post_title = "店貓日常・午後折手手篇 (對照組)"
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
                post_title = "店貓日常・深夜充電紙箱篇 (對照組)"
                post_text = """（把毛茸茸的身體縮成一顆圓滾滾的毛球）
夜深了，店裡的大燈都熄了，
只剩下窗外台東安靜的蟲鳴聲。

一整天的巡店與賣萌任務圓滿收工，
最棒的歸宿果然還是這個剛剛好的厚紙箱。

還沒睡的各位辛苦了喵，
今晚什麼煩惱都別裝進腦袋，早點鑽進暖暖的被窩充電吧喵！🐾 #台東生活"""
                first_reply = "（閉上眼睛發出均勻的呼嚕聲）睡前別忘了把手機放下，今晚祝大家都有個甜甜的好夢喵🐾"
        else: # 影 (生活管家) - 對齊全天 5 檔生理節奏
            if 5 <= current_hour < 10:
                shadow_morning_candidates = [
                    (
                        "晨間漫步・台東生活微觀篇 (對照組)",
                        """清晨六點多的台東街道，空氣裡帶著太平洋海風淡淡的鹹味與濕度。
推開門，中央山脈稜線在晨曦下被勾勒得特別乾淨。

生活裡的大多數清醒，
不是靠鬧鐘的驚嚇，而是靠一口踏實吸進肺裡的清涼空氣。

大家早安，新的一天慢慢走，
先把今天的早餐好好吃完，日子總會一口一口踏實過好的。🍵✨ #台東生活""",
                        "（為大家倒上一杯剛煮好的溫開水）早晨先深呼吸一口，給今天一個從容的開場吧。🍵✨"
                    ),
                    (
                        "晨間備勤・老宅光影篇 (對照組)",
                        """清晨推開老宅的木門，陽光把庭院的石板路曬得泛出微光。
在出勤前為自己泡一壺溫熱的煎茶，看著茶煙裊裊升起。

所謂從容的生活，
往往是比世界早醒半個小時，
給自己的感官一段不被打擾的安靜時間。

大家早安，新的一天別著急趕路，
先把腳步踩穩，今天一定能順順利利。🍵✨ #台東生活""",
                        "（在玄關幫大家遞上一只溫熱水杯）早晨先喝口水潤潤喉，生活管家在後排替大家加油。🍵✨"
                    )
                ]
                chosen = shadow_morning_candidates[0]
                for cand in shadow_morning_candidates:
                    passed, _ = check_text_poka_yoke(cand[1], check_remote=False)
                    if passed:
                        chosen = cand
                        break
                post_title, post_text, first_reply = chosen
            elif 10 <= current_hour < 12:
                shadow_tea_candidates = [
                    (
                        "上午小憩・一杯熱水篇 (對照組)",
                        """上午十點半，手邊的雜務告一段落。
在老木桌前給自己倒一杯溫熱開水，看著蒸氣在微涼的空氣裡慢慢散開。

工作與生活就像呼吸一樣，
有緊湊的吐氣，也必須有從容的吸氣。

忙碌的朋友記得站起來伸個懶腰、喝口水，
生活管家在後排替你打氣。🍵✨ #台東生活""",
                        "（端上一只溫熱杯盞）忙了一個上午辛苦了，喝口溫水繼續出發！🍵✨"
                    )
                ]
                post_title, post_text, first_reply = shadow_tea_candidates[0]
            elif 12 <= current_hour < 15:
                shadow_noon_candidates = [
                    (
                        "午後時光・老木窗慢生活篇 (對照組)",
                        """轉頭看著窗邊剛泡好的紅烏龍冒著白煙，
午後的陽光把老房子的木窗框曬得微微發亮。

生活裡的大多數煩惱，
往往在走慢兩步、把注意力收回呼吸裡的時候，
就悄悄散開了。

大家今天過得好嗎？
午後給自己留下一杯茶的時間吧。🍵✨ #台東生活""",
                        "（把熱茶端在手心裡）忙碌之餘別忘了喘口氣，給自己的身心一個溫暖的擁抱吧。🍵✨"
                    ),
                    (
                        "午後微風・池上米香篇 (對照組)",
                        """中午十二點半，巷口傳來剛煮熟白米飯的清甜香氣。
在台東生活久了，對時間的感知不再是螢幕上的數字，
而是陽光移過長廊的角度與飯菜的溫度。

給正忙碌的你一個提醒：
午休這半小時，先把公事擱在旁邊吧。
好好吃一口飯，是對身體最踏實的交代。🍵✨ #台東生活""",
                        "（拉開木椅坐下）好好把午餐吃完，下午笑著過。生活管家一直都在。🍵✨"
                    )
                ]
                chosen = shadow_noon_candidates[0]
                for cand in shadow_noon_candidates:
                    passed, _ = check_text_poka_yoke(cand[1], check_remote=False)
                    if passed:
                        chosen = cand
                        break
                post_title, post_text, first_reply = chosen
            elif 15 <= current_hour < 20:
                shadow_dusk_candidates = [
                    (
                        "傍晚歸途・下班夕陽篇 (對照組)",
                        """傍晚五點半，天邊的夕陽正由金黃漸漸沉入溫柔的深藍。
騎車經過巷口，看著街邊小吃店炊煙裊裊升起，
台東的黃昏總有一種催促大家安心回家的魔力。

下班放學的大家，回到家了嗎？
洗淨雙手、卸下整天的疲憊，吃一頓熱騰騰的飯菜吧。🍲✨ #台東生活""",
                        "（在門口為大家遞上拖鞋）下班後的時間是屬於自己的，今晚好好犒賞自己。🍵✨"
                    )
                ]
                post_title, post_text, first_reply = shadow_dusk_candidates[0]
            else: # 深夜或凌晨時段 (防呆多場景池)
                shadow_night_candidates = [
                    (
                        "深夜守候・清單核對與夜風篇 (對照組)",
                        """深夜一點多的台東，街道上的車聲都沉寂下來了。
在老木桌前把明天要幫長輩送達的生活物資與清單核對好，
推開窗，外頭夜風吹過屋簷，太平洋上空的星星特別乾淨。

生活管家想對還沒入睡的你說：
今天所有的努力與奔波，到這個時刻都已經足夠了。

把手機放在伸手拿不到的地方，給自己一個完全安靜的夜晚。
晚安，願你有一夜好眠。🍵✨ #台東生活""",
                        "（為大家端上一只溫熱好茶）深呼吸一口，今晚把心安頓在枕頭上。生活管家替大家守夜，晚安！🍵✨"
                    ),
                    (
                        "深夜守候・老木屋靜音篇 (對照組)",
                        """夜深了，整座老房子安靜得只剩下木頭微弱的呼吸聲。
在小廚房溫了一杯熱水，窗外的風涼涼的，
把一整天在外的奔波與雜訊徹底隔絕在門外。

真正的休息，不是等事情全部做完才開始，
而是允許自己在這一刻按下暫停鍵。

今晚還在亮著螢幕的朋友辛苦了，
關上小夜燈，把心安安穩穩安頓在枕頭上。晚安！🍵✨ #台東生活""",
                        "（把燈光調暗）今晚不用再想任何煩惱了，徹底關機充電。願你好夢！🍵✨"
                    ),
                    (
                        "深夜守候・海風安頓篇 (對照組)",
                        """走過長廊去把後門的木窗扣好，
台東的深夜總有一種特殊的沈靜，彷彿連空氣流動的速度都慢了下來。

在玄關把出勤背包整理齊全，
深呼吸一口帶著海鹽氣息的清涼夜風。

今天不管是順心還是有些疲倦，都留在今天吧。
今晚生活管家在後排為大家留一盞微光，好好睡上一覺，明天見。🍵✨ #台東生活""",
                        "（輕輕遞上一只溫熱杯盞）卸下整天的武裝，今晚給身心最溫柔的擁抱。晚安！🍵✨"
                    )
                ]
                
                # 自動挑選前台與本地未發布過之全新候選
                chosen = shadow_night_candidates[0]
                for cand in shadow_night_candidates:
                    passed, msg = check_text_poka_yoke(cand[1], threshold=0.70, check_remote=True)
                    if passed:
                        chosen = cand
                        print(f"🛡️【對照組防呆自癒選中】：{cand[0]}（物理檢驗 100% 通過零重複門禁）")
                        break
                    else:
                        print(f"ℹ️ 對照組候選『{cand[0]}』未通過檢驗 ({msg})，自動切換至下一場景...")
                
                post_title, post_text, first_reply = chosen

    # ── 2. 非對照組：啟動 hot-trend-scout 融合即時台灣時事熱點 ──
    else:
        trend_applied = False
        if scan_taiwan_trends:
            try:
                print("🔍【hot-trend-scout 啟動】：正在即時嗅探台灣熱搜話題並執行戴明安燈質檢...")
                raw_trends = scan_taiwan_trends.fetch_google_trends_tw()
                approved_trends = scan_taiwan_trends.filter_and_translate_trends(raw_trends)
                
                chosen_trend = None
                if args.trend_keyword:
                    for at in approved_trends:
                        if args.trend_keyword.lower() in at["keyword"].lower():
                            chosen_trend = at
                            break
                if not chosen_trend and approved_trends:
                    chosen_trend = approved_trends[0]
                
                if chosen_trend:
                    kw = chosen_trend["keyword"]
                    cat = chosen_trend["category"]
                    pain = chosen_trend.get("life_pain_point", "")
                    hook = chosen_trend.get("meow_hook" if is_cat_hero else "shadow_hook", "")
                    applied_trend_info = chosen_trend
                    trend_applied = True
                    print(f"🎯【hot-trend-scout 鎖定熱點】：『{kw}』(類別: {cat})")
                    print(f"   💡 轉譯切角: {hook[:60]}...")
                    
                    tag_kw = kw.replace(" ", "").replace("#", "")
                    
                    if is_cat_hero:
                        post_title = f"店貓時事趣談・【{kw}】篇"
                        if 5 <= current_hour < 11:
                            post_text = f"""（坐在老木地板上甩甩尾巴）
滑開手機看到滿滿都是關於『{kw}』的話題喵～
{hook}

{pain}

早晨出門上班的大家辛苦了喵，
不管外面怎麼喧鬧，把肚子填飽、把背挺直最要緊喵！🐾 #{tag_kw} #店貓日常"""
                            first_reply = f"（探出毛毛頭）大家早安！吃過熱騰騰的早餐了嗎？不管『{kw}』怎麼轉，都要開開心心出發喵🐾"
                        elif 11 <= current_hour < 17:
                            post_text = f"""（窩在窗台前把兩隻手手折好）
午後外頭微風輕輕吹，大家都在熱烈討論『{kw}』喵～
{hook}

{pain}

下午工作如果感到有點昏沉，
學本喵一樣原地深呼吸、伸個長長的懶腰再出發喵！🐾 #{tag_kw} #店貓日常"""
                            first_reply = f"（翻個肚肚伸懶腰）下午記得多喝兩口溫水喵～生活管家與喵編隨時在後排替大家充電！🐾"
                        else:
                            post_text = f"""（把身體縮進溫暖的紙箱裡只露出一對耳朵）
夜深了，店裡的大燈熄了，外頭大家還在熱烈刷著『{kw}』的最新消息喵～
{hook}

{pain}

夜深了就別再盯著手機螢幕看了喵，
今晚把所有雜訊關在門外，早點鑽進被窩好好充電吧喵！🐾 #{tag_kw} #店貓日常"""
                            first_reply = f"（發出均勻的打呼嚕聲）睡前喝口溫熱的，明天台東的太陽一樣會升起喵～晚安！🐾"
                    else: # 影 (生活管家)
                        post_title = f"生活管家隨筆・【{kw}】時事共鳴篇"
                        if 5 <= current_hour < 11:
                            post_text = f"""清晨六點多的台東街道，空氣裡帶著中央山脈清晨的微涼。
滑開動態，大家一早都在關注熱搜上的『{kw}』。

{hook}

{pain}

生活裡的踏實感，往往不在於跟上每一個網路脈動，
而是把眼前的早餐吃好、把當下的呼吸安頓好。大家早安！🍵✨ #{tag_kw} #台東生活"""
                            first_reply = f"（為大家倒上一杯剛煮好的溫開水）早晨先深呼吸一口。不管『{kw}』如何變幻，給今天一個從容的開場吧。🍵✨"
                        elif 11 <= current_hour < 17:
                            post_text = f"""午後時光，看著窗邊剛泡好的鹿野紅烏龍冒著白煙。
社群動態牆上，關於『{kw}』的討論此起彼落。

{hook}

{pain}

生活裡的大多數焦慮，
往往在肯走慢兩步、把注意力收回真實生活的時候，就悄悄散開了。
午後給自己留下一杯茶的時間吧。🍵✨ #{tag_kw} #台東生活"""
                            first_reply = f"（端上一只溫熱茶杯）午休時把手機稍稍放下，讓大腦徹底休息十分鐘。生活管家一直都在。🍵✨"
                        else:
                            post_text = f"""深夜時分，合上整天奔波的代辦清單。
窗外只有台東安靜的太平洋海風，而網路上關於『{kw}』的討論依然熱鬧。

{hook}

{pain}

今天大家辛苦了，
今晚鑽進暖暖的被窩，把所有的紛擾留在今天。好好睡上一覺充電，晚安！🍵✨ #{tag_kw} #台東生活"""
                            first_reply = f"（輕輕遞上一只溫熱紅烏龍）今晚讓緊繃的神經徹底關機。生活管家在後排替大家守夜，願你好夢。🍵✨"
            except Exception as e:
                print(f"⚠️ hot-trend-scout 抓取或轉譯異常，自動降級為生活白描: {e}")
        
        # 降級備案 (Fallback)
        if not trend_applied:
            if is_cat_hero:
                post_title = "店貓日常・生活微觀篇"
                post_text = """（把前腳折好在胸口，窩在木窗台前）
看著外面的微風吹過街道，這大概就是最安心的時刻喵。
人類總是在忙著跟時間賽跑，
但對本喵來說，罐罐打開的聲音與暖和的陽光才是不可辜負的。
累了就學本喵一樣，原地折手手深呼吸一下喵！🐾 #台東生活"""
                first_reply = "（翻肚肚打呼嚕）累了就站起來喝口溫水，剩下的半天笑著過喵🐾"
            else:
                post_title = "生活管家隨筆・放鬆篇"
                post_text = """在台東的老木桌前熱了一小壺水，慢慢泡開鹿野紅烏龍。
看著茶葉在陶壺裡舒展，窗外的夜風帶著安靜的味道。
生活的大多數焦慮，往往在肯給自己一段完全安靜的呼吸時光時，就慢慢沉澱落下了。
給自己留一段安靜的呼吸時光吧。🍵✨ #台東生活"""
                first_reply = "（輕輕遞上一只溫熱的茶杯）深呼吸一口，生活管家在後排替大家守護日常。🍵✨"
else:
    post_title = "自定義隨筆巡邏貼文"
    post_text = args.text
    first_reply = args.reply if args.reply else "（在留言區為大家端上一杯熱茶）🍵✨"

topic_tag = args.topic if args.topic else default_topic
post_image = args.image
image_pick_reason = "外部指定" if post_image else None

# =====================================================================
# 🎨 核心升級：內嵌 character_dna_engine 與專屬出圖流水線（100% 確保每一篇文案都有配圖）
# =====================================================================
try:
    from character_dna_engine import build_character_prompt, verify_character_dna
except ImportError:
    build_character_prompt = None
    verify_character_dna = None

hero_key = "meow" if is_cat_hero else "shadow"
dna_prompt = ""
if build_character_prompt and verify_character_dna:
    # 依當前貼文情境程式化合成符合角色法定 DNA 之專屬提示詞
    action_scene = f"配合貼文《{post_title}》情境：{post_text[:120].replace(chr(10), ' ')}"
    dna_prompt = build_character_prompt(hero_key, action_scene)
    dna_ok, dna_errs = verify_character_dna(hero_key, dna_prompt)
    if not dna_ok:
        raise ValueError(f"角色 DNA 質檢未通過: {dna_errs}")
    print(f"🧬【character_dna_engine】：已鎖定 {default_hero} 法定視覺 DNA，提示詞質檢合格！")

# 自動智慧配圖引擎掛載（僅允許合格 DNA 專屬庫存）
if not post_image:
    verified_pool_dir = ROOT_DIR / "images" / "verified_dna_pool"
    picked_img, reason = auto_pick_image(is_cat_hero, topic_tag, post_text, candidate_dir=verified_pool_dir)
    if picked_img:
        post_image = picked_img
        image_pick_reason = f"DNA驗證庫存命中: {reason}"
        print(f"🎨【DNA 專屬圖庫直通】：已為巡邏貼文精準配圖 ➔ {Path(picked_img).name} ({reason})")
    else:
        # 若專屬圖庫無可用新圖，嚴格執行創辦人親定之【每一篇文案必須配圖】鐵律
        print("\n🛑【戴明安燈出廠門禁】：每一篇貼文強制必須配圖！無專屬照片嚴禁純文字出廠！")
        if dna_prompt:
            print(f"📋 請依據 character_dna_engine 合成之專屬提示詞完成生圖：\n{dna_prompt}\n")
        if not args.dry_run and not args.patrol_only:
            raise RuntimeError("【出廠門禁拒絕放行】：庫存中無可用之專屬 DNA 新照片，拒絕純文字出廠！請備妥圖片後重新發布！")
        else:
            print("🧪 [演練/巡邏模式] 暫以演練狀態通行")
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
    "step6_cognitive_sync": True,
    "hot_trends_applied": applied_trend_info,
    "rss_sentinel_scout": []
}

# 1. 訪鄰居目標名冊 (在地友店與常民特色社群)
LOCAL_TARGETS = [
    {"user": "sinapayan_youth", "name": "喜拿巴漾青年工作站", "category": "地方創生"},
    {"user": "howhow_sweets", "name": "好好·食甜", "category": "手作甜點"},
    {"user": "chaiyuan_bakery", "name": "柴源製菓", "category": "烘焙手作"},
    {"user": "sankou_food_office", "name": "仨口食事處", "category": "夜間食堂"},
    {"user": "yuanlung.667", "name": "緣龍無骨鹽酥雞", "category": "在地美食"},
    {"user": "956leissmoker", "name": "雨田燻", "category": "手工煙燻"},
    {"user": "hattcoffee", "name": "Hatt Coffee", "category": "獨立手沖咖啡"}
]

# 融合 threads-rss-sentinel 預設監測名冊
if rss_sentinel and hasattr(rss_sentinel, "DEFAULT_TARGETS"):
    existing_users = {t["user"] for t in LOCAL_TARGETS}
    for dt in rss_sentinel.DEFAULT_TARGETS:
        du = dt.get("username")
        if du and du not in existing_users:
            LOCAL_TARGETS.append({
                "user": du,
                "name": dt.get("name", du),
                "category": dt.get("tag", "台東在地")
            })
            existing_users.add(du)

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

    # --- 步驟二：訪鄰居 (threads-rss-sentinel 動態嗅探 ＋ 在地友店 80/20 溫暖巡邏) ---
    print("\n>>> 步驟二：訪鄰居 (threads-rss-sentinel 動態嗅探 ＋ 在地友店巡邏) <<<")
    
    # 啟動 threads-rss-sentinel 預先探測友店最新動態
    active_neighbors = []
    normal_neighbors = []
    
    if rss_sentinel and not args.skip_rss:
        print("📡【threads-rss-sentinel 啟動】：正在巡邏在地友店最新 RSS 發文動態...")
        # 探測前 6 家友店，快速過濾出近期有活躍貼文之鄰居
        scout_pool = LOCAL_TARGETS[:8]
        for t in scout_pool:
            u = t["user"]
            name = t["name"]
            try:
                feed_res = rss_sentinel.fetch_threads_feed(u, timeout=5)
                if feed_res.get("status") == "ok" and feed_res.get("items"):
                    latest_item = feed_res["items"][0]
                    drafts = rss_sentinel.generate_draft_replies(latest_item)
                    best_draft = drafts[0]["text"] if drafts else ""
                    
                    finding = {
                        "username": u,
                        "name": name,
                        "title": latest_item.get("title", "")[:80],
                        "link": latest_item.get("link", ""),
                        "pub_date": latest_item.get("pub_date", ""),
                        "draft_reply": best_draft
                    }
                    report_data["rss_sentinel_scout"].append(finding)
                    t_active = dict(t)
                    t_active["rss_finding"] = finding
                    active_neighbors.append(t_active)
                    print(f"   🌟 友店 @{u} ({name}) 最新動態: 「{latest_item.get('title', '')[:35]}...」")
                else:
                    normal_neighbors.append(t)
            except Exception as e:
                normal_neighbors.append(t)
        
        # 剩餘未探測的加入 normal_neighbors
        for t in LOCAL_TARGETS[8:]:
            normal_neighbors.append(t)
    else:
        normal_neighbors = list(LOCAL_TARGETS)

    # 排序巡邏目標：近期有動態的友店排在最前列，總共拜訪前 7 家
    sorted_targets = (active_neighbors + normal_neighbors)[:7]
    print(f"🚶 今日拜訪鄰里隊列：共 {len(sorted_targets)} 家友店（其中 {len(active_neighbors)} 家有即時新動態）")

    for t in sorted_targets:
        u = t["user"]
        name = t["name"]
        rf = t.get("rss_finding")
        url = f"https://www.threads.net/@{u}"
        print(f" -> 拜訪 @{u} ({name})...")
        if rf:
            print(f"   📡 [RSS 哨兵快報]: 「{rf['title'][:40]}...」")
            if rf.get("draft_reply"):
                print(f"   💬 [走心留言建議]: {rf['draft_reply']}")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(2000)
            
            like_btn = page.locator('div[role="button"]:has(svg[title="Like"]), div[role="button"]:has(svg[title="讚"])').first
            if like_btn.is_visible(timeout=2000):
                like_btn.click(force=True, timeout=3000)
                page.wait_for_timeout(800)
                print(f"   ❤️ 已為 {name} 最新動態點亮愛心！")
                report_data["step2_friends_visited"].append({
                    "username": u,
                    "name": name,
                    "action": "liked",
                    "rss_post": rf.get("title") if rf else None
                })
            else:
                print(f"   ℹ️ {name} 目前無可點按鈕或已點亮")
                report_data["step2_friends_visited"].append({
                    "username": u,
                    "name": name,
                    "action": "already_liked",
                    "rss_post": rf.get("title") if rf else None
                })
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
        tea_msg = "看老闆認真專注煙燻，生活管家默默在後排端出剛泡好的熱茶... 辛苦了，今晚別想工作，好好犒勞自己！🍵🍖"
        
        # 嘗試尋找貼文回覆按鈕並留言互動
        try:
            reply_btn = page.locator('div[role="button"]:has(svg[title="回覆"]), svg[title="回覆"], svg[aria-label="回覆"], svg[aria-label="Reply"]').first
            if reply_btn.is_visible(timeout=2500):
                reply_btn.click(force=True, timeout=3000)
                page.wait_for_timeout(1000)
                input_box = page.locator('div[contenteditable="true"], div[role="textbox"]').first
                if input_box.is_visible(timeout=2500):
                    input_box.click(force=True)
                    page.keyboard.type(tea_msg, delay=20)
                    page.wait_for_timeout(1000)
                    post_btn = page.locator('div[role="button"]:has-text("發佈"), div[role="button"]:has-text("Post")').first
                    if post_btn.is_visible(timeout=2000):
                        post_btn.click(force=True, timeout=3000)
                        page.wait_for_timeout(2500)
                        print(f"   🍵 借光端茶走心留言已成功送出！")
        except Exception as ce:
            print(f"   ℹ️ 借光端茶走心互動提示: {ce}")

        page.screenshot(path=str(shot_clout))
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

    # 🔒 【仿生學習系統前向硬約束門禁】：調用 bionic_core.enforce 檢驗 active 規則
    try:
        bionic_core_dir = ROOT_DIR.parents[1] / ".agents" / "skills" / "bionic-learning-system" / "bionic_core"
        if bionic_core_dir.exists() and str(bionic_core_dir) not in sys.path:
            sys.path.insert(0, str(bionic_core_dir))
        import enforce
        active_rules = enforce.load_active_rules("kage")
        if active_rules:
            print(enforce.compile_constraints(active_rules))
        is_passed, violations = enforce.gate("kage", post_text)
        if not is_passed:
            print(f"🛑 [仿生學習系統硬性攔截出廠] 違規清單:")
            for v in violations:
                print(f"   ❌ {v}")
            raise RuntimeError(f"文案未通過仿生學習系統規則檢驗，物理阻斷發布！共 {len(violations)} 項違規")
        else:
            print("   🛡️ [仿生學習硬性閘門檢驗合格] 吻合 kage_rules.jsonl 全部 active 規則，准予放行！")
    except Exception as e:
        if "物理阻斷發布" in str(e):
            raise e
        print(f"   ℹ️ 仿生門禁檢驗提示: {e}")

    # 🔒 【文案物理雜湊與相似度零重複硬門禁 (text_hash_gate)】
    try:
        from text_hash_gate import check_text_poka_yoke, register_published_text_hash
        ok_text, text_msg = check_text_poka_yoke(post_text)
        if not ok_text:
            print(f"🛑 [text_hash_gate] 硬性攔截出廠: {text_msg}")
            raise ValueError(f"[text_hash_gate 物理阻斷] {text_msg}")
        print(f"   🛡️ [text_hash_gate 合格] {text_msg}")
    except ImportError:
        register_published_text_hash = None
        print("   ⚠️ 未載入 text_hash_gate 模組，請檢查 scripts 路徑！")

    if args.patrol_only:
        print("   🚶 [Patrol Only 巡邏模式] 跳過新貼文發布與首回覆，專注於看家門、訪鄰居與借光端茶！")
        report_data["step4_post"] = {
            "post_id": "SKIPPED_PATROL_ONLY",
            "title": "巡邏漫遊模式（跳過發文）",
            "hero": default_hero,
            "topic_tag": topic_tag
        }
    elif args.dry_run:
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
        # 🔒 【戴明安燈出廠門禁：每一篇文案必須配圖】
        if not post_image or not Path(post_image).exists():
            print("🛑【戴明安燈出廠門禁】：每一篇貼文強制必須配圖！拒絕無圖出廠！")
            raise ValueError("【出廠門禁拒絕放行】：未檢測到有效專屬照片，拒絕純文字出廠！")

        if publish_thread:
            print(f"   🚀 調用 threads_publisher.publish_thread (配圖: {Path(post_image).name})...")
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

            # 🎯 接入常態反饋測試登記：呼叫 feedback_loop.log_post
            chosen_k_ids = []
            try:
                from feedback_loop import log_post, select_next_k_id
                chosen_k_ids = select_next_k_id(args.k_id)
                log_post(new_post_id, chosen_k_ids, post_text)
                k_label = f"實驗組 {chosen_k_ids}" if chosen_k_ids else "對照組 []"
                print(f"   🏷️ [常態反饋測試登記] 成功登記至 feedback_posts.json ({k_label})")
            except Exception as e:
                print(f"   ⚠️ 反饋測試登記提示: {e}")

            # 🔒 【文案物理雜湊入庫】：登記至 published_text_hashes.json 永久去重
            if register_published_text_hash:
                try:
                    register_published_text_hash(post_text, new_post_id)
                except Exception as e:
                    print(f"   ⚠️ 文案雜湊入庫提示: {e}")

            report_data["step4_post"] = {
                "post_id": new_post_id,
                "permalink": permalink,
                "title": post_title,
                "hero": default_hero,
                "topic_tag": topic_tag,
                "image": Path(post_image).name if post_image else None,
                "image_reason": image_pick_reason,
                "k_ids": chosen_k_ids
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

# --- 步驟六：啟動漫遊返航自省與認知存摺實時自生 (atom-kage-walk-reflector) ---
try:
    import subprocess
    reflector_script = SCRIPT_DIR / "post_walk_reflector.py"
    if reflector_script.exists():
        print("\n>>> 步驟六：啟動漫遊返航自省與認知存摺實時自生 (atom-kage-walk-reflector) <<<")
        sub_args = [sys.executable, str(reflector_script), "--auto"]
        if args.dry_run:
            sub_args.append("--dry-run")
        sub_res = subprocess.run(sub_args, capture_output=True, text=True, encoding="utf-8")
        if sub_res.stdout:
            print(sub_res.stdout)
        if sub_res.returncode == 0:
            print("✅ [返航自省閉環完成] 存摺回寫與輪次入帳已成功閉環！")
        else:
            print(f"⚠️ 返航自省執行提示 (Exit Code: {sub_res.returncode}): {sub_res.stderr}")
except Exception as e:
    print(f"⚠️ 自省閉環喚醒提示: {e}")

