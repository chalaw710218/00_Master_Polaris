#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
text_hash_gate.py — 極星 Threads 文案物理雜湊與相似度零重複出廠門禁
架構監製：首席品質長戴明 (Dr. Deming) ✕ 首席特務兼生活管家影 (Shadow)

【核心使命】：
徹底消滅社群發文「文案重複發布」、「伺服器重試連發」、「歷史套路撞車」之重大品質事故！
建立「純文字 SHA-256 物理雜湊庫」與「前台動態相似度 >= 75% 硬攔截」雙重防呆！
"""

import hashlib
import json
import re
import sys
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path

# 確保 Windows UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

HUB_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = HUB_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
TEXT_HASH_DB_PATH = DATA_DIR / "published_text_hashes.json"

sys.path.append(str(HUB_DIR / "scripts"))
try:
    from threads_publisher import THREADS_ACCESS_TOKEN, THREADS_USER_ID, API_BASE
except ImportError:
    THREADS_ACCESS_TOKEN = None
    THREADS_USER_ID = None
    API_BASE = "https://graph.threads.net/v1.0"


def normalize_text(text: str) -> str:
    """標準化文本：去除所有空白、換行、標點符號，保留括號內中文核心字元以利精準比對"""
    if not text:
        return ""
    # 移除 URL
    t = re.sub(r"https?://\S+", "", text)
    # 移除標籤如 #台東生活
    t = re.sub(r"#\S+", "", t)
    # 移除所有標點、括號符號與空白，但保留括號內的中文字元！
    t = re.sub(r"[\s\.,!?:;\"'“”‘’，。！？：；、～~…\-_/\\|（）\(\)\[\]【】🐾✨❤️🍵🏠ℹ️⚠️🚀🎉🔒📸💬📝]+", "", t)
    return t.strip().lower()


def compute_text_sha256(text: str) -> str:
    """計算標準化文本的 SHA-256 雜湊"""
    norm = normalize_text(text)
    if not norm:
        # 若過濾後全空，則退回原文本去除空白的雜湊
        norm = re.sub(r"\s+", "", text).lower()
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


def load_text_hashes() -> dict:
    """讀取歷史發布文案雜湊庫"""
    if not TEXT_HASH_DB_PATH.exists():
        return {}
    try:
        with open(TEXT_HASH_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 讀取文案雜湊庫失敗: {e}，建立新庫存", file=sys.stderr)
        return {}


def register_published_text_hash(text: str, post_id: str) -> None:
    """發布成功後，將文案 SHA-256 雜湊與貼文 ID 永久封裝入庫"""
    norm = normalize_text(text)
    h = compute_text_sha256(text)
    db = load_text_hashes()
    db[h] = {
        "post_id": post_id,
        "sample": text[:60].replace("\n", " "),
        "normalized_len": len(norm)
    }
    with open(TEXT_HASH_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    print(f"🔒 [text_hash_gate] 文案物理雜湊已成功烙印至去重庫 ({h[:12]}... ➔ Post {post_id})")


def check_text_poka_yoke(text: str, threshold: float = 0.70, check_remote: bool = True) -> tuple[bool, str]:
    """
    文案出廠防呆硬檢驗：
    1. 本地歷史文案 SHA-256 去重庫比對（100% 相同即阻斷）
    2. 動態比對 Meta 前台最近 30 篇貼文：
       - 全文相似度 >= 70% 阻斷
       - 包含 25 字以上連續完全相同核心語句阻斷
    回傳 (通過與否: bool, 說明訊息: str)
    """
    if not text or len(text.strip()) < 5:
        return False, "文案為空或字數過少（小於5字元），拒絕出廠！"

    norm_target = normalize_text(text)
    target_hash = compute_text_sha256(text)

    # 1. 本地去重庫 100% SHA-256 比對
    db = load_text_hashes()
    if target_hash in db:
        old_info = db[target_hash]
        return False, f"物理阻斷：文案與歷史貼文 {old_info.get('post_id')} 內容 100% 重複（雜湊: {target_hash[:12]}...）！"

    # 2. 前台動態 API 近期貼文相似度與長句撞車比對
    if check_remote and THREADS_ACCESS_TOKEN and THREADS_USER_ID:
        try:
            url = f"{API_BASE}/{THREADS_USER_ID}/threads?fields=id,text&limit=30&access_token={THREADS_ACCESS_TOKEN}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                remote_data = json.loads(resp.read().decode()).get("data", [])

            for item in remote_data:
                remote_txt = item.get("text", "")
                if not remote_txt:
                    continue
                remote_norm = normalize_text(remote_txt)
                if not remote_norm:
                    continue

                # 2-A. 全文字元相似度
                ratio = SequenceMatcher(None, norm_target, remote_norm).ratio()
                if ratio >= 1.0:
                    return False, f"物理阻斷：文案與前台貼文 {item['id']} 內容 100% 一模一樣，嚴禁連發！"
                if ratio >= threshold:
                    return False, f"物理阻斷：文案與前台貼文 {item['id']} 相似度高達 {ratio*100:.1f}% (超過 {threshold*100:.0f}% 門檻)！"

                # 2-B. 長句撞車檢查（連續 25 字以上完全相同）
                match = SequenceMatcher(None, norm_target, remote_norm).find_longest_match(0, len(norm_target), 0, len(remote_norm))
                if match.size >= 25:
                    hit_snippet = norm_target[match.a:match.a+match.size]
                    return False, f"物理阻斷：文案包含與前台貼文 {item['id']} 連續 25 字以上完全相同之片段（「{hit_snippet[:20]}...」）！"
        except Exception as e:
            print(f"⚠️ [text_hash_gate] 連線前台比對超時或略過 ({e})，以本地庫為準", file=sys.stderr)

    return True, f"物理檢驗合格：文案 SHA-256 ({target_hash[:12]}...) 且前台無高相似度重複"


def backfill_existing_posts():
    """首次初始化：自動從前台拉取最近貼文並回填入庫"""
    if not THREADS_ACCESS_TOKEN or not THREADS_USER_ID:
        return
    try:
        url = f"{API_BASE}/{THREADS_USER_ID}/threads?fields=id,text&limit=100&access_token={THREADS_ACCESS_TOKEN}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            items = json.loads(resp.read().decode()).get("data", [])
        db = load_text_hashes()
        added = 0
        for it in items:
            t = it.get("text", "")
            if not t:
                continue
            h = compute_text_sha256(t)
            if h not in db:
                db[h] = {
                    "post_id": it["id"],
                    "sample": t[:60].replace("\n", " "),
                    "normalized_len": len(normalize_text(t))
                }
                added += 1
        with open(TEXT_HASH_DB_PATH, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        print(f"✅ [text_hash_gate] 歷史文案回填完成，新收錄 {added} 筆雜湊（總庫存: {len(db)} 筆）")
    except Exception as e:
        print(f"回填失敗: {e}", file=sys.stderr)


if __name__ == "__main__":
    print("🧪 正在初始化與測試 text_hash_gate...")
    if TEXT_HASH_DB_PATH.exists():
        TEXT_HASH_DB_PATH.unlink()
    backfill_existing_posts()
    
    # 測試自我阻斷案例 1：完全相同的晨間貼文
    test_text_full = """（在老木地板的晨光光斑裡慢慢伸個長長的大懶腰）

早晨的風吹進木窗，帶著一點點涼意。
太陽剛爬過屋頂，把木地板曬得暖暖的。

管家剛剛把店門拉開，
廚房裡傳來電鍋跳起的一聲「啵」。

新的一天又開始了。
今天不用太著急，先深呼吸一口氣，
把肩膀放鬆，像本喵一樣先把腰伸開再說。

大家早安！今天出門記得帶件外套喔。🐾

#台東生活 #耍廢日常"""
    ok, msg = check_text_poka_yoke(test_text_full)
    print(f"👉 案例 1（完全相同文案）防呆攔截: {'❌ 失敗' if ok else '✅ 成功攔截: ' + msg}")

    # 測試自我阻斷案例 2：改動前幾字但核心語句超過20字完全相同
    test_text_frag = "今天早晨本喵在老木地板的晨光光斑裡慢慢伸個長長的大懶腰，早晨的風吹進木窗帶著一點點涼意。"
    ok2, msg2 = check_text_poka_yoke(test_text_frag)
    print(f"👉 案例 2（核心長句撞車）防呆攔截: {'❌ 失敗' if ok2 else '✅ 成功攔截: ' + msg2}")

    # 測試合格案例 3：全新午後文案
    test_text_new = "午後三點的台東微風吹過老宅走廊，本喵在木桌下安靜看著管家整理茶葉，準備迎接傍晚的夕陽。"
    ok3, msg3 = check_text_poka_yoke(test_text_new)
    print(f"👉 案例 3（全新不重複文案）放行檢驗: {'✅ 成功放行: ' + msg3 if ok3 else '❌ 誤攔截: ' + msg3}")
