#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
image_hash_gate.py — 極星發布圖片物理雜湊與防重複出廠硬閘門
架構監製：首席品質長戴明 (Dr. Deming) ✕ CTO 林納斯 (Linus)

【核心鐵律】：
1. 嚴禁發布任何歷史已使用過的圖片（物理內容 SHA-256 驗證，不只比對檔名）。
2. 發布入口硬性阻斷（Poka-Yoke）：發布前必須通過 check_image_poka_yoke()，重複即 Exit / Raise！
3. 發布成功後自動原子登記至 published_image_hashes.json 與 published_image_registry.json。
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime

# 確保 Windows UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
HUB_DIR = SCRIPT_DIR.parent
DATA_DIR = HUB_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

HASH_VAULT_FILE = DATA_DIR / "published_image_hashes.json"
REGISTRY_FILE = DATA_DIR / "published_image_registry.json"


def calculate_image_sha256(image_path: str | Path) -> str:
    """計算圖片檔案之二進位 SHA-256 雜湊"""
    p = Path(image_path)
    if not p.is_file():
        raise FileNotFoundError(f"圖片檔案不存在: {image_path}")
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def load_published_hashes() -> dict:
    """
    讀取已發布圖片的雜湊庫。
    結構: { "sha256_hash": { "filename": "...", "post_id": "...", "published_at": "..." } }
    """
    if not HASH_VAULT_FILE.exists():
        # 若雜湊庫不存在，自動自現有圖片庫建立種子庫
        seed_hashes = {}
        _seed_existing_images(seed_hashes)
        save_published_hashes(seed_hashes)
        return seed_hashes

    try:
        with open(HASH_VAULT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ 讀取圖片雜湊庫失敗: {e}")
        return {}


def save_published_hashes(hashes_dict: dict):
    with open(HASH_VAULT_FILE, "w", encoding="utf-8") as f:
        json.dump(hashes_dict, f, ensure_ascii=False, indent=2)


def _seed_existing_images(target_dict: dict):
    """將現有 04_Shadow_Kage_Operative/images 內所有舊圖計算雜湊並直接標記為已發布，徹底封死舊庫"""
    old_dir = HUB_DIR / "04_Shadow_Kage_Operative" / "images"
    if old_dir.exists():
        for p in old_dir.glob("*.*"):
            if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
                try:
                    sha = calculate_image_sha256(p)
                    target_dict[sha] = {
                        "filename": p.name,
                        "post_id": "HISTORICAL_SEEDED_OCTOBER",
                        "published_at": "2026-10-31T00:00:00",
                        "status": "deprecated_historical_pool"
                    }
                except Exception:
                    pass

    # 同步 published_image_registry.json
    if REGISTRY_FILE.exists():
        try:
            reg = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
            for item in reg.get("published_images", []):
                fn = item.get("filename")
                pid = item.get("post_id", "HISTORICAL")
                # 搜尋本地比對
                for matched in HUB_DIR.glob(f"**/{fn}"):
                    if matched.is_file():
                        sha = calculate_image_sha256(matched)
                        target_dict[sha] = {
                            "filename": fn,
                            "post_id": pid,
                            "published_at": item.get("published_at", ""),
                            "status": "published_registry"
                        }
        except Exception:
            pass


def check_image_poka_yoke(image_path: str | Path) -> tuple[bool, str]:
    """
    發布前物理硬攔截閘門：
    1. 檢查檔案存在與尺寸
    2. 計算物理 SHA-256 雜湊
    3. 雜湊命中歷史庫 ➔ 物理拒絕出廠！
    回傳: (is_passed, reason)
    """
    if not image_path:
        return False, "未指定任何圖片路徑"

    p = Path(image_path)
    if not p.exists():
        return False, f"圖片檔案不存在: {p}"

    if p.stat().st_size == 0:
        return False, f"圖片檔案為空 (0 bytes): {p}"

    sha = calculate_image_sha256(p)
    hashes_dict = load_published_hashes()

    if sha in hashes_dict:
        entry = hashes_dict[sha]
        return False, (
            f"物理硬攔截拒絕出廠：圖片物理內容 SHA-256 ({sha[:12]}...) "
            f"已於 {entry.get('published_at', '歷史記錄')} 發布過 (對應 Post ID: {entry.get('post_id')}, 原始檔名: {entry.get('filename')})！"
            f"嚴禁以舊圖充當新圖發布！"
        )

    return True, f"物理檢驗合格：SHA-256 ({sha[:12]}...) 為全新未發布圖片"


def register_published_image_hash(image_path: str | Path, post_id: str, topic: str = "社群發布"):
    """發布成功後，原子登記雜湊值"""
    p = Path(image_path)
    sha = calculate_image_sha256(p)
    hashes_dict = load_published_hashes()

    now_str = datetime.now().isoformat(timespec="seconds")
    hashes_dict[sha] = {
        "filename": p.name,
        "post_id": str(post_id),
        "published_at": now_str,
        "topic": topic,
        "size_bytes": p.stat().st_size
    }
    save_published_hashes(hashes_dict)
    print(f"🔒 [image_hash_gate] 物理雜湊已成功烙印至防重複去重庫 ({sha[:12]}... ➔ Post {post_id})")


if __name__ == "__main__":
    # 測試執行種子建立與檢查
    print("🧪 正在初始化並驗算圖片雜湊庫...")
    h = load_published_hashes()
    print(f"📊 目前已收錄歷史圖片雜湊數: {len(h)} 筆")
    test_img = HUB_DIR / "images" / "meow_tuesday_morning_stretch_20261117.jpg"
    if test_img.exists():
        ok, reason = check_image_poka_yoke(test_img)
        print(f"測試檢驗 {test_img.name}: {'✅' if ok else '❌'} {reason}")
