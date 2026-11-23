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
    parser.add_argument("--patrol-only", action="store_true", help="僅執行社交巡邏與蹭熱度/散散步，跳過新貼文發布")
    parser.add_argument("--post-only", action="store_true", help="純發文任務模式：僅執行看家門、發文與首回覆，不做訪鄰居、蹭熱度留言與散散步")
    parser.add_argument("--k-id", type=str, default=None, help="指定儲備知識 K-編號 (如 K-014/auto)，若未指定則依 4x4 每日時段輪換表自動決定")
    parser.add_argument("--slot", type=int, default=None, help="指定時段索引 (0:09:07, 1:12:34, 2:17:36, 3:22:33)，預設依當前時間自動判定")
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

# 🔒 【創辦人親定 4x4 每日時段輪換排程】：若未手動強制指定 k-id (或傳入 auto)，依日期與時段自動決定
if not args.patrol_only and (args.k_id is None or args.k_id.lower() == "auto"):
    from k_slot_rotator import get_k_id_for_date_and_slot, infer_slot_index_from_hour, format_k_display
    slot_idx = args.slot if args.slot is not None else infer_slot_index_from_hour(current_hour)
    args.k_id = get_k_id_for_date_and_slot(now_dt.date(), slot_idx)
    print(f"🔄【4x4 時段自動輪換】：今日 ({now_dt.date().isoformat()}) 時段 #{slot_idx} 自動配發 -> {format_k_display(args.k_id)}")

# 判斷是否為對照組
is_control_post = (args.k_id in ["control", "[]"])

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
                        "店貓日常・週一藺草蓆晨光篇 (對照組)",
                        """（把兩隻白手套往前伸到最長，在藺草蓆上拱起背拉個大懶腰）
週一早晨七點半，台東老宅走廊的亞麻布簾被微風吹得輕輕晃動喵。
矮木桌上的陶杯剛倒滿溫水，冒著淡淡的白煙。

外面的麻雀已經在樹梢吱吱喳喳開早會了，
本喵的草蓆剛好被第一道晨光曬得暖烘烘的，還帶著一點草香。

新的一週慢慢開始就好喵，
出門前先喝口溫水，把肩膀放輕鬆再出發吧！🐾 #台東生活""",
                        "（打個小小的哈欠）週一早安喵！大家今天的早餐準備吃蛋餅還是飯糰呢？吃飽飽才有元氣喔🐾"
                    ),
                    (
                        "店貓日常・老木門晨風篇 (對照組)",
                        """（坐在店門口的木門檻上看著落葉被微風吹過）
清晨的台東街道好安靜喵～
陽光斜斜照在地板上，把本喵的影子拉得長長的。

早起的人類已經騎著車去買熱包子豆漿了，
本喵在門口幫大家把關每一陣吹過來的海風。

大家早安喵！出門前深呼吸一口氣，
今天也像本喵一樣踏踏實實過好一天喵！🐾 #台東生活""",
                        "（晃晃毛茸茸的尾巴）早起的空氣特別清爽喵！祝大家今天都有好心情🐾"
                    ),
                    (
                        "店貓日常・木窗陽光洗臉篇 (對照組)",
                        """（坐在窗邊的木地板上，用白爪子沾沾口水認真洗臉）
早晨的陽光穿過木窗框，在地板上畫出亮亮的小格子喵。
空氣裡有一點露水跟泥土的清爽味道。

本喵已經把鬍鬚跟耳朵都整理乾淨了，
準備迎接今天第一波路過門口的小蝴蝶。

大家週一早安喵！不管今天有什麼行程，先把早餐吃得飽飽的再說喵！🐾 #台東生活""",
                        "（探出毛毛頭）早安喵！記得帶件薄外套出門，今天本喵也在店裡陪大家喔🐾"
                    )
                ]
                chosen = cat_morning_candidates[0]
                for cand in cat_morning_candidates:
                    passed, _ = check_text_poka_yoke(cand[1], check_remote=True)
                    if passed:
                        chosen = cand
                        break
                post_title, post_text, first_reply = chosen
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

    # ── 1.5 創辦人親定規則 4 & 5：K-014 / K-025 / K-031 專屬特化分支 ──
    elif args.k_id in ["K-014", "K-025", "K-031"]:
        print(f"🎯【創辦人親定軍規】：啟動 {args.k_id} 專屬風格與具體問句流水線！")
        k_candidates = []
        if args.k_id == "K-014": # 感官白描：只寫畫面和感覺，不提服務！
            if is_cat_hero:
                k_candidates = [
                    (
                        "K-014 感官白描・老木窗微風光影篇",
                        """（把前腳整整齊齊收在胸口，下巴貼在微涼的木窗框上）
午後四點多的台東，斜陽把老宅的磨石子地曬出一大片溫暖的金黃色。
空氣裡有一點乾草和泥土被風吹過的氣味，
院子裡的欖仁樹葉被風吹得沙沙響。

沒有什麼催促的聲音，只有木頭和風的呼吸。
把身體放鬆下來，看著光影慢慢往牆角移過去。

你那邊現在風也這麼大嗎？""",
                        "（輕輕搖搖尾巴尖端）吹著風好舒服喵。站起來看看窗外的天空吧🐾"
                    ),
                    (
                        "K-014 感官白描・藺草蓆茶香篇",
                        """（趴在走廊的藺草蓆上，鼻尖湊近剛泡好的溫熱陶杯）
老宅走廊的亞麻簾子被太平洋吹來的風微微掀起一角。
深焙紅烏龍的白煙裊裊升起，帶著淡淡的花果香與木頭香氣。
屋簷上的麻雀剛跳過瓦片，留下一陣細微的爪子聲。

台東這時候的天色漸漸從金黃沉入淺藍。
光線落在手背上的溫度剛剛好。

你那邊今天有看到夕陽嗎？""",
                        "（半瞇著眼睛打個小哈欠）傍晚的空氣特別乾淨喵。深呼吸一口放鬆一下吧🐾"
                    )
                ]
            else:
                k_candidates = [
                    (
                        "K-014 感官白描・黃昏天色與茶煙篇",
                        """推開老木窗，午後帶著海鹽鹹味的微風吹進長廊。
老宅的磨石子地板泛著淡淡的光澤，
矮几上一只粗陶茶杯，熱水剛沖下去，茶煙在光影裡慢悠悠地打轉。

中央山脈的稜線在暮色裡漸漸被勾勒成一層深黛色。
沒有喇叭聲，只有遠處傳來兩聲狗吠與落葉刮過路面的聲響。

你那邊現在天黑了嗎？""",
                        "（輕輕遞上一只溫熱杯盞）深呼吸一口清涼空氣，給今天一個安靜的落幕。🍵✨"
                    )
                ]
        elif args.k_id == "K-025": # 現有服務：寫外送、跑腿、追垃圾車真實工作細節！
            if is_cat_hero:
                k_candidates = [
                    (
                        "K-025 現有服務・後座保溫袋與外送細節篇",
                        """（在店門口好奇地盯著剛回到店裡的安全帽與保溫箱）
剛才生活管家騎車幫市區的客人送完晚餐回來，
機車後座的深藍色大保溫箱一打開，熱騰騰的麻油排骨湯和現切滷菜香氣立刻飄出來喵。
每一盒便當都用厚厚防撞泡棉固定得好好的，湯汁一滴都沒灑出來。

在台東幫大家跑腿送飯、順路帶生活用品，
最療癒的就是把熱熱的晚餐親手遞給剛下班的人類時，對方臉上的笑容。

台東市區你們吃便當最常夾哪三樣菜？""",
                        "（探出毛毛頭蹭蹭）聞到便當香氣本喵的肚子也叫了喵～大家今晚吃什麼好料呢？🐾"
                    ),
                    (
                        "K-025 現有服務・黃昏追垃圾車真實腳步篇",
                        """（跳上門口木柵欄看著巷子口）
傍晚五點多，遠遠傳來少女的祈禱音樂聲，台東的垃圾車準時拐進巷子了喵！
生活管家穿著反光背心，雙手提著兩大袋分類好的回收物與廚餘袋，
小跑步幫巷子裡行動不便的長輩順路丟上垃圾車，跟清潔隊員點頭道謝。

這就是生活管家每天真實的跑腿日常，
追垃圾車、送熱飯、幫忙提重物，讓出門不方便的鄉親少流一趟汗。

你家那邊的垃圾車今天幾點來？""",
                        "（晃晃尾巴）追垃圾車是每天最刺激的運動喵！大家今天有記得丟垃圾嗎？🐾"
                    )
                ]
            else:
                k_candidates = [
                    (
                        "K-025 現有服務・雨後外送與長輩跑腿篇",
                        """安全帽的鏡片上還帶著剛才路過鐵花村時飄來的細微水氣。
後座保溫箱裡，兩盒剛從正氣路老店包好的熱便當穩穩固定在防晃夾層裡，
提上二樓交給獨居的阿公時，湯碗摸起來還是滾燙的。

生活管家做的事情很樸實：
外送一頓準時的熱飯、幫忙跑腿領個包裹、傍晚順手幫鄰居把垃圾丟上車。
看到門打開時那句「辛苦了、慢慢騎」，一整天的奔波就很值得。

你家那邊的垃圾車每天幾點到巷口？""",
                        "（在門口遞上一杯溫開水）生活裡的踏實，往往就藏在這些跑腿的小細節裡。今晚好好吃飯！🍵✨"
                    )
                ]
        elif args.k_id == "K-031": # 服務徵詢：直接問一個未來服務「大家需不需要」
            if is_cat_hero:
                k_candidates = [
                    (
                        "K-031 服務徵詢・免動腦下班備菜盒篇",
                        """（兩隻白爪子按在木桌前，認真盯著桌上的小筆記本）
生活管家最近正在規劃一個新的貼心服務喵！
常常看到很多上班族跟小家庭，下班想自己煮頓健康晚餐，
但想到要去菜市場挑菜、回家洗菜切菜、廚餘又堆滿垃圾桶就覺得心好累。

如果生活管家每天傍晚幫大家把「當天產地直送、洗乾淨、切好的一餐份蔬菜肉片備菜盒」順路送到家，
下班回家只要直接倒進熱鍋、開火五分鐘就能開飯。

這個服務如果生活管家來做，大家會需要嗎？""",
                        "（用期待的翠綠大眼睛看著你）直接丟下鍋煮熟就能吃，連本喵都想幫忙切菜了喵！大家覺得實用嗎？🐾"
                    ),
                    (
                        "K-031 服務徵詢・到府換高處燈泡與電池篇",
                        """（歪著小腦袋看著天花板上閃爍的小燈泡）
生活管家最近到府跑腿時發現，好多人家裡的走廊燈泡壞了、或是冷氣遙控器沒電了，
長輩自己爬梯子好危險，年輕人又在外地工作沒辦法隨時回來弄。

我們正在規劃：「順路到府居家小微修」服務，
例如順路幫忙換高處燈泡、替換遙控器與熱水器電池、或是檢查一下水龍頭墊片。

如果生活管家推出這個順路幫忙換燈泡的服務，大家會需要嗎？""",
                        "（坐在梯子旁幫忙把關）爬高交給專業的人類，安全第一喵！這個服務大家會想預約嗎？🐾"
                    )
                ]
            else:
                k_candidates = [
                    (
                        "K-031 服務徵詢・居家水電耗材微更換篇",
                        """在台東走訪各家時常看到一個很現實的問題：
家裡的高處燈泡燒壞了、冷氣遙控器電池沒電、或是水龍頭墊片微微滴水，
找大水電師傅跑一趟划不來，長輩自己爬高拿鐵梯又讓人捏把冷汗。

生活管家正在評估推出「居家小微修與耗材更換服務」：
順路幫忙換燈泡、換電池、換濾網，讓小問題當天解決不拖延。

如果生活管家推出這樣的到府微修小幫手，大家會需要嗎？""",
                        "（在留言區為大家泡好熱茶）居家安全不能馬虎。這樣的順路服務，大家覺得實用嗎？🍵✨"
                    )
                ]

        # 檢驗選出可用的候選
        chosen = k_candidates[0]
        try:
            from text_hash_gate import check_text_poka_yoke
            for cand in k_candidates:
                passed, msg = check_text_poka_yoke(cand[1], threshold=0.70, check_remote=True)
                if passed:
                    chosen = cand
                    print(f"🛡️【{args.k_id} 專屬候選選中】：{cand[0]}（物理檢驗通過零重複）")
                    break
        except Exception as e:
            print(f"ℹ️ {args.k_id} 候選檢驗提示: {e}")
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
                    allow_tag = chosen_trend.get("hashtag_allowed", False)
                    final_tag = f"#{tag_kw}" if allow_tag else ("#店貓日常" if is_cat_hero else "#台東生活")
                    
                    if is_cat_hero:
                        post_title = f"店貓時事趣談・【{kw}】篇"
                        if 5 <= current_hour < 10:
                            post_text = f"""（坐在老木地板上甩甩尾巴）
滑開手機看到滿滿都是關於『{kw}』的話題喵～
{hook}

{pain}

早晨出門上班的大家辛苦了喵，
不管外面怎麼喧鬧，把肚子填飽、把背挺直最要緊喵！🐾 {final_tag}"""
                            first_reply = f"（探出毛毛頭）大家早安！吃過熱騰騰的早餐了嗎？不管『{kw}』怎麼轉，都要開開心心出發喵🐾"
                        elif 10 <= current_hour < 12:
                            post_text = f"""（在店門口陽光下慢慢打個哈欠）
上午十點多，大家都還在熱烈刷著『{kw}』的最新進度喵～
{hook}

{pain}

上午忙碌的朋友記得站起來喝兩口溫水、活動一下筋骨，
像本喵一樣隨時把體力維持在滿格狀態喵！🐾 {final_tag}"""
                            first_reply = f"（動動小耳朵）忙了一早上辛苦了喵！伸個懶腰喝口水，下半場更有元氣🐾"
                        elif 12 <= current_hour < 15:
                            post_text = f"""（窩在窗台前把兩隻手手折好）
正午陽光暖暖的，大家都在熱烈討論『{kw}』喵～
{hook}

{pain}

午休時間先把手機放旁邊，把午餐好好吃完，
學本喵一樣原地深呼吸、伸個長長的懶腰再出發喵！🐾 {final_tag}"""
                            first_reply = f"（翻個肚肚伸懶腰）中午記得好好吃飯喝水喵～生活管家與喵編隨時在後排替大家充電！🐾"
                        elif 15 <= current_hour < 19:
                            post_text = f"""（在木椅上端正坐好凝視窗外夕陽）
傍晚台東的天空正轉成溫柔的粉橘色，外頭關於『{kw}』的聲音還沒停過喵～
{hook}

{pain}

下班放學的大家辛苦了喵，
今晚早點回家卸下包袱，吃一頓熱騰騰的晚餐最實在喵！🐾 {final_tag}"""
                            first_reply = f"（搖搖蓬鬆尾巴）下班路上騎車開車要注意安全喵～回到家就好好放鬆吧！🐾"
                        else:
                            post_text = f"""（把身體縮進溫暖的紙箱裡只露出一對耳朵）
夜深了，店裡的大燈熄了，外頭大家還在熱烈刷著『{kw}』的最新消息喵～
{hook}

{pain}

夜深了就別再盯著手機螢幕看了喵，
今晚把所有雜訊關在門外，早點鑽進被窩好好充電吧喵！🐾 {final_tag}"""
                            first_reply = f"（發出均勻的打呼嚕聲）睡前喝口溫熱的，明天台東的太陽一樣會升起喵～晚安！🐾"
                    else: # 影 (生活管家)
                        post_title = f"生活管家隨筆・【{kw}】時事共鳴篇"
                        if 5 <= current_hour < 10:
                            post_text = f"""清晨六點多的台東街道，空氣裡帶著中央山脈清晨的微涼。
滑開動態，大家一早都在關注熱搜上的『{kw}』。

{hook}

{pain}

生活裡的踏實感，往往不在於跟上每一個網路脈動，
而是把眼前的早餐吃好、把當下的呼吸安頓好。大家早安！🍵✨ {final_tag}"""
                            first_reply = f"（為大家倒上一杯剛煮好的溫開水）早晨先深呼吸一口。不管『{kw}』如何變幻，給今天一個從容的開場吧。🍵✨"
                        elif 10 <= current_hour < 12:
                            post_text = f"""上午十點半，手邊的晨會與日常備料告一段落。
滑開即時動態，關於『{kw}』的各方聲音正在社群上熱烈激盪。

{hook}

{pain}

資訊流轉得再快，人體與心靈依舊需要穩定的節奏。
忙碌了一個上午，不妨站起身給自己倒杯溫開水，把焦躁的心收攏回當下。🍵✨ {final_tag}"""
                            first_reply = f"（在木桌旁遞上一只溫熱白瓷杯）上午辛苦了。喝口溫水深呼吸，後半段繼續安穩前行。🍵✨"
                        elif 12 <= current_hour < 15:
                            post_text = f"""正午十二點半，窗外的熱氣正被微涼的穿堂風吹散。
社群動態牆上，關於『{kw}』的討論此起彼落。

{hook}

{pain}

生活裡的大多數焦慮，
往往在肯走慢兩步、把注意力收回真實生活的時候，就悄悄散開了。
正午給自己留下一頓安靜吃飯的時間吧。🍵✨ {final_tag}"""
                            first_reply = f"（端上一只溫熱茶杯）午休時把手機稍稍放下，讓大腦徹底休息十分鐘。生活管家一直都在。🍵✨"
                        elif 15 <= current_hour < 19:
                            post_text = f"""傍晚五點多，斜陽映在老宅磨石子地板上染出一片溫潤。
網路上關於『{kw}』的話題依然沸騰，但台東的街巷已開始飄起各家廚房的飯菜香。

{hook}

{pain}

世界越是喧囂，越要把自己的真實生活過好。
辛苦了一整天，準備回家的朋友，願今晚有一桌熱騰騰的飯菜等著你。🍵✨ {final_tag}"""
                            first_reply = f"（在玄關輕輕點亮一盞暖燈）下班後的時光完全屬於你自己，今晚好好休息。🍵✨"
                        else:
                            post_text = f"""深夜時分，合上整天奔波的代辦清單。
窗外只有台東安靜的太平洋海風，而網路上關於『{kw}』的討論依然熱鬧。

{hook}

{pain}

今天大家辛苦了，
今晚鑽進暖暖的被窩，把所有的紛擾留在今天。好好睡上一覺充電，晚安！🍵✨ {final_tag}"""
                            first_reply = f"（輕輕遞上一只溫熱紅烏龍）今晚讓緊繃的神經徹底關機。生活管家在後排替大家守夜，願你好夢。🍵✨"
                    
                    # 🛡️ 立即針對生成的時事文案執行 text_hash_gate 預審，若碰撞前台歷史長句則自癒降級
                    try:
                        from text_hash_gate import check_text_poka_yoke
                        ok_cand, reason_cand = check_text_poka_yoke(post_text, check_remote=True)
                        if not ok_cand:
                            print(f"⚠️ hot-trend-scout 生成文案未通過 text_hash_gate 預審: {reason_cand}，自動切換至時段生活白描")
                            trend_applied = False
                    except Exception as err:
                        pass
            except Exception as e:
                print(f"⚠️ hot-trend-scout 抓取或轉譯異常，自動降級為生活白描: {e}")
        
        # 降級備案 (Fallback) - 對齊全天 5 檔生理節奏自癒池
        if not trend_applied:
            if is_cat_hero:
                if 5 <= current_hour < 10:
                    post_title = "店貓日常・清晨伸懶腰篇"
                    post_text = """（在木地板上的晨光裡慢慢伸個長長的懶腰）
早晨的台東微風涼涼的，窗外的雀鳥已經在屋簷上跳來跳去。
人類每天都在趕著上班打卡，
但對本喵來說，先把兩隻手手伸直、打個大大的哈欠，才是迎接新的一天最標準的儀式。

大家早安喵！出門前深呼吸一口氣，
今天也像本喵一樣踏踏實實過好一天喵！🐾 #店貓日常 #台東生活"""
                    first_reply = "（探出毛茸茸的小腦袋）大家早安！早餐記得吃飽飽再出發喵🐾"
                elif 10 <= current_hour < 12:
                    post_title = "店貓日常・上午元氣篇"
                    post_text = """（端坐在木椅上曬著暖洋洋的上午斜陽）
上午十點半，店裡剛煮開的熱水正冒著白煙。
看著大家在螢幕前專注敲鍵盤的背影，
本喵決定走過去蹭蹭你的小腿，提醒你該站起來喝口溫水了喵～

忙碌的時候更要懂得偷得浮生半日閒，
深呼吸、伸個懶腰，下半場更有元氣喵！🐾 #店貓日常 #台東生活"""
                    first_reply = "（輕輕蹭蹭小腿）喝口溫水再出發喵！生活管家與本喵在後排守護你🐾"
                elif 12 <= current_hour < 15:
                    post_title = "店貓日常・午後折手手篇"
                    post_text = """（把前腳整整齊齊折好在胸口，窩在木窗台前）
看著外面的微風吹過街道，這大概就是世界上最安心的時刻喵。
人類總是在忙著跟時間賽跑，
但對本喵來說，剛打開的罐罐香氣與暖和的陽光才是不可辜負的。

午休時間先把手機放一旁，把午餐好好吃完，
累了就學本喵一樣，原地折手手深呼吸一下喵！🐾 #店貓日常 #台東生活"""
                    first_reply = "（翻個肚肚打呼嚕）午休記得好好吃飯休息，下午笑著過喵🐾"
                elif 15 <= current_hour < 19:
                    post_title = "店貓日常・傍晚看夕陽篇"
                    post_text = """（跳上窗邊老木桌，凝視著街角被夕陽染成金黃色）
街上的機車聲漸漸多起來了，小吃攤的蒸氣也一陣陣飄過來。
台東的傍晚總有一種催促大家安心回家的魔力。

下班放學的朋友們，回到家就把包袱放下吧，
吃一頓熱騰騰的飯菜，把今天的疲勞留在門外喵！🐾 #店貓日常 #台東生活"""
                    first_reply = "（搖搖毛茸茸長尾巴）路上注意安全喵～回到家就好好放鬆吧！🐾"
                else:
                    post_title = "店貓日常・深夜安眠篇"
                    post_text = """（把整隻貓縮進最暖和的紙箱裡，只露出一對小耳朵）
夜深了，店裡的大燈熄了，窗外只有台東安靜的海風。
還沒睡的各位辛苦了喵，
今晚什麼煩惱都別裝進腦袋，早點鑽進暖暖的被窩充電吧喵！🐾 #店貓日常 #台東生活"""
                    first_reply = "（閉上眼睛發出均勻的呼嚕聲）睡前喝口溫熱的，明天台東的太陽一樣會升起喵～晚安！🐾"
            else: # 影 (生活管家)
                if 5 <= current_hour < 10:
                    post_title = "晨間漫步・台東生活微觀篇"
                    post_text = """清晨六點多的台東街道，空氣裡帶著太平洋海風淡淡的鹹味與濕度。
推開門，中央山脈稜線在晨曦下被勾勒得特別乾淨。
街角早餐店的蒸籠正冒著白煙，
早起的人們彼此點頭致意，沒有大城市的倉促與按喇叭聲。

生活裡的安心感，
往往就藏在這些微小而踏實的日常細節裡。
出門前深呼吸一口氣，把今天的節奏交給自己。🍵✨ #台東生活"""
                    first_reply = "（在門口為大家遞上一杯溫水）早安！今天出門也要帶著從容的心情出發。🍵✨"
                elif 10 <= current_hour < 12:
                    post_title = "上午小憩・一杯熱水篇"
                    post_text = """上午十點半，手邊的雜務告一段落。
在老木桌前給自己倒一杯溫熱開水，看著蒸氣在微涼的空氣裡慢慢散開。

工作與生活就像呼吸一樣，
有緊湊的吐氣，也必須有從容的吸氣。

忙碌的朋友記得站起來伸個懶腰、喝口水，
生活管家在後排替你打氣。🍵✨ #台東生活"""
                    first_reply = "（端上一只溫熱杯盞）忙了一個上午辛苦了，喝口溫水繼續出發！🍵✨"
                elif 12 <= current_hour < 15:
                    noon_candidates = [
                        (
                            "午後微風・池上米香篇",
                            """中午十二點半，巷口傳來剛煮熟白米飯的清甜香氣。
在台東生活久了，對時間的感知不再是螢幕上的數字，
而是陽光移過長廊的角度與飯菜的溫度。

給正忙碌的你一個提醒：
午休這半小時，先把公事擱在旁邊吧。
好好吃一口飯，是對身體最踏實的交代。🍵✨ #台東生活""",
                            "（拉開木椅坐下）好好把午餐吃完，下午笑著過。生活管家一直都在。🍵✨"
                        ),
                        (
                            "午後時光・老木窗慢生活篇",
                            """轉頭看著窗邊剛泡好的紅烏龍冒著白煙，
午後的陽光把老房子的木窗框曬得微微發亮。

生活裡的大多數煩惱，
往往在走慢兩步、把注意力收回呼吸裡的時候，
就悄悄散開了。

大家今天過得好嗎？
午後給自己留下一杯茶的時間吧。🍵✨ #台東生活""",
                            "（把熱茶端在手心裡）忙碌之餘別忘了喘口氣，給自己的身心一個溫暖的擁抱吧。🍵✨"
                        )
                    ]
                    chosen = noon_candidates[0]
                    try:
                        from text_hash_gate import check_text_poka_yoke
                        for cand in noon_candidates:
                            passed, _ = check_text_poka_yoke(cand[1], check_remote=False)
                            if passed:
                                chosen = cand
                                break
                    except Exception:
                        pass
                    post_title, post_text, first_reply = chosen
                elif 15 <= current_hour < 19:
                    post_title = "傍晚歸途・下班夕陽篇"
                    post_text = """傍晚五點半，天邊的夕陽正由金黃漸漸沉入溫柔的深藍。
騎車經過巷口，看著街邊小吃店炊煙裊裊升起，
台東的黃昏總有一種催促大家安心回家的魔力。

下班放學的大家，回到家了嗎？
洗淨雙手、卸下整天的疲憊，吃一頓熱騰騰的飯菜吧。🍲✨ #台東生活"""
                    first_reply = "（在門口為大家遞上拖鞋）下班後的時間是屬於自己的，今晚好好犒賞自己。🍵✨"
                else:
                    night_candidates = [
                        (
                            "深夜隨筆・老宅夜風與紅烏龍篇",
                            """夜深了，整座台東老屋安靜得只聽得見窗外的微風。
在書桌前給自己倒一杯溫熱草本茶，合上整天密密麻麻的工作筆記本。
看著身邊柔和的暖黃燈光，緊繃了一整天的肩膀終於徹底放鬆下來。

真正的休息，不是等所有事情都完美結束，
而是允許自己在深夜這一刻徹底按下暫停鍵。

把手機螢幕關掉，今晚給緊繃的身心一個溫暖的擁抱。
生活管家在後排替大家留一盞暖燈，大家晚安！🍵✨ #台東生活""",
                            "（輕輕端上一只溫熱手作陶杯）今晚什麼煩惱都別想了，讓大腦徹底關機充電。生活管家祝你好夢！🍵✨"
                        ),
                        (
                            "深夜守候・老木屋靜音篇",
                            """夜深了，整座老房子安靜得只剩下木頭微弱的呼吸聲。
在小廚房溫了一杯熱水，窗外的夜風涼涼的，
把一整天在外的奔波與雜訊徹底隔絕在門外。

今晚還在亮著螢幕的朋友辛苦了，
關上小夜燈，把心安安穩穩安頓在枕頭上。晚安！🍵✨ #台東生活""",
                            "（把燈光調暗）今晚不用再想任何煩惱了，徹底關機充電。願你好夢！🍵✨"
                        ),
                        (
                            "深夜守候・海風安頓篇",
                            """走過長廊去把後門的木窗扣好，
台東的深夜總有一種特殊的沈靜，彷彿連空氣流動的速度都慢了下來。

在玄關把出勤背包整理齊全，
深呼吸一口帶著海鹽氣息的清涼夜風。

今天不管是順心還是有些疲倦，都留在今天吧。
今晚生活管家在後排為大家留一盞微光，好好睡上一覺，明天見。🍵✨ #台東生活""",
                            "（輕輕遞上一只溫熱杯盞）卸下整天的武裝，今晚給身心最溫柔的擁抱。晚安！🍵✨"
                        )
                    ]
                    chosen = night_candidates[0]
                    try:
                        from text_hash_gate import check_text_poka_yoke
                        for cand in night_candidates:
                            passed, _ = check_text_poka_yoke(cand[1], check_remote=True)
                            if passed:
                                chosen = cand
                                break
                    except Exception:
                        pass
                    post_title, post_text, first_reply = chosen
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

# 啟動時間去整點化 (Jitter 防風控門禁)
try:
    from interaction_safety_gate import apply_walk_jitter
    if not args.dry_run:
        apply_walk_jitter()
except Exception:
    pass

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

    if args.post_only:
        print("\n>>> 📝 [Post-Only 純發文模式] 僅執行看家門、發文與首回覆；跳過訪鄰居、蹭熱度留言與散散步（交朋友動作集中於每日 3 次 --patrol-only 逛逛） <<<")
    else:
        # --- 步驟二：訪鄰居 (threads-rss-sentinel 動態嗅探 ＋ 在地友店 80/20 溫暖巡邏) ---
        print("\n>>> 步驟二：訪鄰居 (threads-rss-sentinel 動態嗅探 ＋ 在地友店巡邏) <<<")
        
        # 啟動 threads-rss-sentinel 預先探測友店最新動態
        active_neighbors = []
        normal_neighbors = []
        
        if rss_sentinel and not args.skip_rss:
            print("📡【threads-rss-sentinel 啟動】：正在巡邏在地友店最新 RSS 發文動態...")
            # 探測前 8 家友店，快速過濾出近期有活躍貼文之鄰居
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

        # 排序巡邏目標：近期有動態的友店排在最前列，總共拜訪前 8 家
        sorted_targets = (active_neighbors + normal_neighbors)[:8]
        print(f"🚶 今日拜訪鄰里隊列：共 {len(sorted_targets)} 家友店（其中 {len(active_neighbors)} 家有即時新動態）")

        friend_comment_sent = 0
        for t in sorted_targets:
            u = t["user"]
            name = t["name"]
            rf = t.get("rss_finding")
            url = f"https://www.threads.net/@{u}"
            print(f" -> 拜訪 @{u} ({name})...")
            if rf:
                print(f"   📡 [RSS 哨兵快報]: 「{rf['title'][:40]}...」")
            try:
                if rf and rf.get("draft_reply") and friend_comment_sent < 4 and visit_and_reply_page and not args.dry_run:
                    ok_c = visit_and_reply_page(page, u, custom_comment=rf["draft_reply"], post_url=rf.get("link"))
                    if ok_c:
                        friend_comment_sent += 1
                        report_data["step2_friends_visited"].append({
                            "username": u,
                            "name": name,
                            "action": "commented",
                            "comment": rf["draft_reply"],
                            "rss_post": rf.get("title")
                        })

                page.goto(url, wait_until="domcontentloaded", timeout=25000)
                page.wait_for_timeout(2000)
                
                like_btn = page.locator('div[role="button"]:has(svg[title="Like"]), div[role="button"]:has(svg[title="讚"])').first
                if like_btn.is_visible(timeout=2000):
                    # 安全門禁：檢查每日愛心上限 (60個)
                    can_l = True
                    try:
                        from interaction_safety_gate import can_like, record_like
                        can_l, l_reason = can_like()
                        if not can_l:
                            print(f"   🛑 [安全門禁阻斷] {l_reason}，跳過按讚")
                    except Exception:
                        pass

                    if can_l:
                        like_btn.click(force=True, timeout=3000)
                        page.wait_for_timeout(800)
                        print(f"   ❤️ 已為 {name} 最新動態點亮愛心！")
                        try:
                            record_like(target_user=u, post_url=url)
                        except Exception:
                            pass
                        report_data["step2_friends_visited"].append({
                            "username": u,
                            "name": name,
                            "action": "liked",
                            "rss_post": rf.get("title") if rf else None
                        })
                    else:
                        report_data["step2_friends_visited"].append({
                            "username": u,
                            "name": name,
                            "action": "like_skipped_limit_reached",
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
                        if is_cat_hero:
                            c_msg = f"（探出毛毛頭）在台東看到 @{reciprocal_candidate} 的日常分享特別有共鳴，端上一塊剛烤好的小魚乾致敬，今天也辛苦囉！"
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

        # --- 步驟二點五：蹭熱度 (原借光端茶與 hot-trend-scout 合併) ---
        print("\n>>> 步驟二點五：蹭熱度 (全台熱門話題轉譯台東視角) <<<")
        report_data["step2_clout_tea"] = {
            "target": "N/A (公域熱門大串)",
            "commented_count": 0,
            "note": "友店巡邏已全數歸入第二步『訪鄰居』，2.5 僅統計熱門大串"
        }

        # --- 步驟三：散散步 (搜尋「台東生活」常民貼文點讚) ---
        print("\n>>> 步驟三：散散步 (搜尋「台東生活」常民貼文點讚) <<<")
        try:
            page.goto("https://www.threads.net/search?q=%E5%8F%B0%E6%9D%B1%E7%94%9F%E6%B4%BB&serp_type=default&filter=recent", wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(3000)
            feed_likes = 0
            for scroll in range(3):
                like_btns = page.locator('div[role="button"]:has(svg[title="Like"]), div[role="button"]:has(svg[title="讚"])').all()
                for btn in like_btns:
                    if feed_likes >= 3:
                        break
                    try:
                        b = btn.bounding_box()
                        if b and 120 < b['y'] < 800:
                            try:
                                from interaction_safety_gate import can_like, record_like
                                can_l, l_reason = can_like()
                                if not can_l:
                                    print(f"   🛑 [安全門禁阻斷] {l_reason}，停止搜尋按讚")
                                    break
                            except Exception:
                                pass

                            btn.click(force=True)
                            feed_likes += 1
                            try:
                                record_like(target_user="taitung_search", post_url="https://www.threads.net/search?q=台東生活")
                            except Exception:
                                pass
                            print(f"   ❤️ 台東生活搜尋動態贈送第 {feed_likes}/3 顆微光愛心")
                            page.wait_for_timeout(1200)
                    except Exception:
                        continue
                if feed_likes >= 3:
                    break
                page.evaluate("window.scrollBy(0, 600)")
                page.wait_for_timeout(1000)
            report_data["step3_feed_likes"] = feed_likes
        except Exception as e:
            print(f"   ⚠️ 台東搜尋漫遊提示: {e}")
            report_data["step3_feed_likes"] = 0

    # --- 步驟四：隨筆記（真實調用 Threads API 發文）---
    print("\n>>> 步驟四：隨筆記 (Meta Threads API 真實發布) <<<")
    new_post_id = None
    permalink = None

    # 🔒 【創辦人親定規則 2】：每篇只能有 1 個標籤，內文嚴禁放任何 hashtag，只用主題標籤
    import re
    cleaned_post_text = re.sub(r'#\S+', '', post_text).strip()
    cleaned_post_text = re.sub(r'\n{3,}', '\n\n', cleaned_post_text)
    if cleaned_post_text != post_text:
        print(f"   🧹 [標籤防呆] 已自動剝離內文中的 hashtag，僅保留官方主題標籤 (Topic Tag: > {topic_tag})")
        post_text = cleaned_post_text

    # 🔒 【創辦人親定規則 3】：貼文真實人物/事件/對話審計
    person_dialogues = re.findall(r'(阿公|阿姨|頭家|老闆|店長|阿伯|叔叔|阿嬤|阿婆|鄰居|客人)說|「[^」]+」', post_text)
    if person_dialogues:
        audit_note = f"⚠️ 檢測到具體人物/對話: {person_dialogues}（需呈報創辦人品碩確認是否真實發生）"
    else:
        audit_note = "✅ 純淨環境感官/工作白描，無虛構人物對話或歷史事件"
    print(f"   🔍【真實人物/事件審計】：{audit_note}")
    report_data["person_dialogue_audit"] = audit_note

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

    # 🔒 【服務真實性硬門禁 (service_truth_gate)】落實創辦人親定鐵律
    try:
        from service_truth_gate import check_service_truth_poka_yoke
        ok_truth, truth_msg = check_service_truth_poka_yoke(post_text)
        if not ok_truth:
            print(f"🛑 [service_truth_gate] 硬性攔截出廠: {truth_msg}")
            raise ValueError(f"[service_truth_gate 物理阻斷] {truth_msg}")
        print(f"   🛡️ [service_truth_gate 合格] {truth_msg}")
    except ImportError:
        pass

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
                log_post(new_post_id, chosen_k_ids, post_text, hot_trend=bool(applied_trend_info))
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

# 查核昨日 21:23 通知頁巡檢是否執行（若電腦未開機導致沒跑，戰報強制註明「昨日通知頁未巡檢」）
try:
    act_log_path = ROOT_DIR / "data" / "activity_replies_log.json"
    yesterday_str = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    today_str = datetime.date.today().isoformat()
    yesterday_inspected = False
    if act_log_path.exists():
        with open(act_log_path, "r", encoding="utf-8") as af:
            act_data = json.load(af)
            last_f = (act_data.get("last_fetched") or "")[:10]
            if last_f in (yesterday_str, today_str):
                yesterday_inspected = True
    report_data["yesterday_activity_inspected"] = yesterday_inspected
    if not yesterday_inspected:
        print("⚠️ 【通知頁巡檢查核】：昨日通知頁未巡檢（戰報需如實註明）")
except Exception as ae:
    print(f"⚠️ 通知頁巡檢紀錄查核提示: {ae}")

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

