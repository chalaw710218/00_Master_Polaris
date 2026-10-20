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
    依據 04_Shadow_Kage_Operative/02_Tactical_Skills 之『三秒共情 ＋ 接梗幽默 ＋ 拋出新反問』
    """
    text_lower = comment_text.lower()
    
    # 1. 購買導流與價格詢問
    if any(k in text_lower for k in ["哪裡買", "怎麼買", "想吃", "多少錢", "價格", "連結", "+1", "訂購"]):
        return f"被 @{author_username} 發現了喵！偷偷去個人檔案看傳送門~（小聲說：闆仔去送外送了，趁他不在快去逛逛，不要跟他說是本喵跟你說的喵🐱）"
    
    # 2. 煎魚脫皮與烹飪翻車
    elif any(k in text_lower for k in ["煎魚", "脫皮", "破皮", "沾鍋", "黏鍋", "燒焦"]):
        return "（摸摸頭）這不是你的問題，是鍋子跟魚皮在鬧脾氣喵！記住本喵四字訣：『乾、熱、定、晃』——魚皮紙巾壓到全乾、熱鍋熱油、下鍋三分鐘絕不手癢戳它、晃動鍋子像溜冰才翻面！下次試試看保證金黃發光喵！"

    # 3. 減脂飲食與雞胸肉
    elif any(k in text_lower for k in ["減脂", "減肥", "雞胸肉", "柴", "高蛋白"]):
        return "別再水煮嚼柴柴橡皮筋了喵！雞胸肉切厚片泡 5% 鹽水 15 分鐘，表面抹點黑胡椒跟橄欖油，煎兩面各兩分鐘蓋鍋悶五分鐘，咬下去直接爆汁！明天要不要用這招拯救你的減脂便當？"

    # 4. 深夜宵夜誘惑
    elif any(k in text_lower for k in ["宵夜", "好餓", "肚子餓", "泡麵", "想吃東西"]):
        return "抓到了吼！這時間還不睡在想吃的！聽本喵的，煎兩顆荷包蛋淋一點黑醋油膏，或者煮碗清湯下幾顆好餛飩，不要吃太鹹，吃飽暖暖去睡覺喵！你現在最想吃鹹的還甜的？"

    # 5. 小孩挑食
    elif any(k in text_lower for k in ["小孩", "挑食", "不吃菜", "青菜"]):
        return "媽媽辛苦了喵！對付挑食小怪獸，試試看把毛豆仁切碎混進絞肉做成小漢堡排，甜甜香香的，小孩不知不覺吃光一整碗！你家小孩最討厭吃哪一種菜？"

    # 6. 台東在地與旅遊
    elif any(k in text_lower for k in ["台東", "旅遊", "在地", "好吃", "推薦"]):
        return "身為正氣北路在線地頭貓，觀光客排隊的大店本喵就不說了~ 來台東先找家在地米苔目加滿柴魚烏醋，再喝碗新鮮豬血湯，吹著太平洋的風才算真正到台東！你這次打算在台東待幾天喵？"

    # 7. 抱怨外送費太貴
    elif any(k in text_lower for k in ["外送費", "運費", "跑腿", "很貴", "熊貓", "ubereats"]):
        return "所以闆仔才在搞什麼 63/99 免跑腿計劃啊！他自己在大太陽下騎機車幫鄰居順路載，算帳算到本喵都替他的輪胎皮捏把冷汗喵（攤手）。你家平常常叫外送嗎？"

    # 8. 抱怨煮飯累、下班很煩
    elif any(k in text_lower for k in ["好累", "累死", "煮飯", "下班", "外送", "好難", "不知道煮什麼"]):
        return "拍拍！今天辛苦了喵~ 不想煮千萬不要勉強，去切兩片肉丟熱水燙一下淋醬油，剩下的時間留給沙發跟耍廢！明天的事明天再說喵🐾"
        
    # 9. 提到闆仔、貓咪、店貓
    elif any(k in text_lower for k in ["闆仔", "貓", "貓咪", "主子", "罐罐", "店貓", "可愛"]):
        return "闆仔剛剛看報價單眉頭又皺起來了，本喵正準備去踩他的計算機鍵盤喵！快給本喵罐罐封口費~😼"

    # 10. 通用親切接梗回覆
    else:
        return f"抓到了吼！感謝 @{author_username} 來留言取暖~ 本喵這就把你加入生活管家 VIP 偷懶名單喵✨！"

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
