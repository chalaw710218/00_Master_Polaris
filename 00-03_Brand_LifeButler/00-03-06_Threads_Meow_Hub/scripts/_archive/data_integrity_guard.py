#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data_integrity_guard.py — 數據採集與歷史指標完整性防護門禁 (v2.0 雙重防呆版)

核心防呆：
1. 【API 異常防歸零】：當外部 API 發生異常（如 token 過期 code 190、網路逾時、500 錯誤）回傳空值或錯誤時，
   強制中斷寫入流程，嚴禁將歷史有效數據覆蓋成 0 或清空！
2. 【限制檔防損毀覆蓋】：當 daily_interaction_limits.json 讀取失敗（如 JSON 格式損毀或空檔）時，
   強制中斷流程，嚴禁初始化空白預設值覆蓋原檔，保護真實累積次數與歷史紀錄！
"""

import json
from pathlib import Path

def update_metrics_safely(new_data: dict, history_file: Path) -> tuple[bool, str]:
    """
    安全更新歷史指標資料庫。
    若 new_data 為空、包含 error_code（如 190）或 status 為 error，堅決拒絕寫入並保留歷史檔案。
    """
    if not new_data:
        return False, "【更新拒絕】API回傳空值，API回傳錯誤中斷，保留歷史數據不覆蓋！"

    status = new_data.get("status")
    error_code = new_data.get("error_code")
    is_valid = new_data.get("valid", True)

    if status == "error" or error_code == 190 or not is_valid:
        msg = new_data.get("message", "未知 API 錯誤")
        return False, f"【更新拒絕】API回傳錯誤中斷，保留歷史數據不覆蓋！（code: {error_code}, 原因: {msg}）"

    # 若合格才執行寫入
    if history_file.exists():
        existing = history_file.read_text(encoding="utf-8")
    else:
        existing = ""

    # 模擬寫入新數據
    history_file.write_text(json.dumps(new_data, ensure_ascii=False, indent=2), encoding="utf-8")
    return True, "✅ 數據驗收合格，安全寫入歷史指標"


def load_and_increment_limits_safely(limits_file: Path, action_type: str = "like") -> tuple[bool, str, dict | None]:
    """
    安全讀取 daily_interaction_limits.json 並進行計數。
    核心防呆：若檔案不存在、為空、或 JSON 格式損毀，立即攔截中斷，
    嚴禁使用預設空資料覆蓋原檔！
    """
    if not limits_file.exists():
        return False, "【防護攔截】讀取限制檔失敗中斷，嚴禁覆蓋或重置原檔！（檔案不存在）", None

    raw_content = limits_file.read_text(encoding="utf-8").strip()
    if not raw_content:
        return False, "【防護攔截】讀取限制檔失敗中斷，嚴禁覆蓋或重置原檔！（檔案內容為空）", None

    try:
        data = json.loads(raw_content)
    except Exception as e:
        return False, f"【防護攔截】讀取限制檔失敗中斷，嚴禁覆蓋或重置原檔！（JSON 解析失敗: {e}）", None

    if not isinstance(data, dict) or "comments_count" not in data or "likes_count" not in data:
        return False, "【防護攔截】讀取限制檔失敗中斷，嚴禁覆蓋或重置原檔！（關鍵欄位缺失）", None

    # 正常計數累加
    if action_type == "comment":
        data["comments_count"] = data.get("comments_count", 0) + 1
    elif action_type == "like":
        data["likes_count"] = data.get("likes_count", 0) + 1

    return True, "✅ 限制檔讀取成功，計數安全累加", data
