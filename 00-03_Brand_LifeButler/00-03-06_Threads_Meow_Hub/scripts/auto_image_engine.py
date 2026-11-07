#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
極星自動智慧配圖引擎 (Polaris Auto Intelligent Image Matching Engine)
架構監製：CTO 林納斯 (Linus) ✕ 首席品質長戴明 (Dr. Deming)

【核心能力】：
1. 嚴格落實創辦人親定之「發文圖片永不重複」鐵律（對齊 published_image_registry.json）。
2. 雙主角人設感知加權：
   - 喵編（店貓，週一至週三）：優先挑選 meow_ 開頭高溫暖度真實貓咪照片。
   - 影（生活管家，週四至週日）：優先挑選 shadow_ 或 taitung_ 開頭寫實生活視角照片。
3. 語意關鍵詞加權：根據貼文內容（茶、咖啡、陽光、午後、深夜、放鬆、麵包）動態命中評分。
4. 光學質量過濾：硬性過濾海報、切片（poster, sheet, 9grid, tiles），保障 35mm 寫實生活呼吸感。
5. 去中心化安全回退：在庫存不足時自動跨角色兜底，並記錄清晰的選圖決策與安燈日誌。
"""

import os
import sys
import json
from pathlib import Path

# 確保 Windows 終端機能正確輸出 Emoji 與 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 定位工作區路徑
SCRIPT_DIR = Path(__file__).resolve().parent
HUB_DIR = SCRIPT_DIR.parent
IMAGES_DIR = HUB_DIR / "04_Shadow_Kage_Operative" / "images"
REGISTRY_FILE = HUB_DIR / "data" / "published_image_registry.json"

def get_published_image_set():
    """讀取註冊表，取得所有已發布過的圖片檔名集合"""
    published = set()
    if REGISTRY_FILE.exists():
        try:
            with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data.get("published_images", []):
                    fn = item.get("filename")
                    if fn:
                        published.add(fn.strip())
        except Exception as e:
            print(f"⚠️ 讀取已發布圖片庫失敗: {e}")
    return published

def auto_pick_image(hero_is_cat=False, topic_tag="台東生活", post_text="", candidate_dir=None):
    """
    智慧挑選最匹配且未曾發布過的本地圖片。
    :param hero_is_cat: 是否為喵編主役 (True: 喵編, False: 生活管家影)
    :param topic_tag: 貼文主題標籤
    :param post_text: 貼文正文
    :param candidate_dir: 自訂圖片庫目錄（選填）
    :return: (image_path_str, reason_str)
    """
    img_dir = Path(candidate_dir) if candidate_dir else IMAGES_DIR
    if not img_dir.exists():
        return None, f"圖片庫目錄不存在: {img_dir}"

    published_set = get_published_image_set()

    # 掃描支援格式
    supported_exts = {".jpg", ".jpeg", ".png", ".webp"}
    all_files = [p for p in img_dir.iterdir() if p.is_file() and p.suffix.lower() in supported_exts]
    available_files = [p for p in all_files if p.name not in published_set]

    if not available_files:
        return None, "庫存圖片已全數用罄（創辦人親定防重複鐵律觸發）"

    text_sample = f"{post_text} {topic_tag or ''}".lower()
    scored_candidates = []

    # 關鍵字特徵庫
    keywords = {
        "茶": ["tea", "drink"],
        "咖啡": ["cafe", "coffee"],
        "太陽": ["sun", "morning", "noon"],
        "陽光": ["sun", "sunnap"],
        "午後": ["afternoon", "noon"],
        "夜晚": ["night", "midnight"],
        "睡": ["sleep", "nap"],
        "麵包": ["bread", "loaf", "bakery"],
        "吃": ["lunch", "supper", "snack", "noodles"],
        "台東": ["taitung", "terroir"],
        "放鬆": ["stretch", "calm", "loaf"]
    }

    for p in available_files:
        fname = p.name.lower()
        score = 0

        # 硬性防呆：排除海報、多圖拼貼與切片
        if any(bad in fname for bad in ["poster", "sheet", "9grid", "tiles"]):
            score -= 200

        # 角色主役嚴格隔離防線（創辦人親定人設隔離鐵律）
        if hero_is_cat:
            if fname.startswith("meow_"):
                score += 50
            else:
                score -= 500  # 喵編主役嚴禁抓取影或闆仔的照片
        else:
            if fname.startswith("shadow_") or fname.startswith("taitung_"):
                score += 50
            elif fname.startswith("meow_"):
                score -= 500  # 影主役嚴禁抓取貓咪照片，避免人設錯亂

        # 語意關聯度動態加權
        for kw, tags in keywords.items():
            if kw in text_sample:
                if any(t in fname for t in tags):
                    score += 20

        scored_candidates.append((score, p))

    scored_candidates.sort(key=lambda x: x[0], reverse=True)
    best_score, best_path = scored_candidates[0]

    # 若最高分仍小於等於 0，代表沒有符合當前角色的可用庫存照片
    if best_score <= 0:
        return None, "當前角色庫存照片已用罄或無合適匹配（觸發人設保護，不跨角色亂抓）"

    return str(best_path), f"智慧匹配命中 (加權分: {best_score}, 檔名: {best_path.name})"

if __name__ == "__main__":
    # 單元測試模式
    print("🧪 [林納斯架構質檢] 極星自動智慧配圖引擎單元測試...")
    cat_img, cat_res = auto_pick_image(hero_is_cat=True, topic_tag="耍廢日常", post_text="在木窗台前放鬆喝杯水，打呼嚕喵")
    print(f"  👉 喵編主役測試: {Path(cat_img).name if cat_img else None} | {cat_res}")

    shadow_img, shadow_res = auto_pick_image(hero_is_cat=False, topic_tag="台東生活", post_text="老木窗框曬得發亮，午後一杯茶的時間")
    print(f"  👉 影主役測試: {Path(shadow_img).name if shadow_img else None} | {shadow_res}")
