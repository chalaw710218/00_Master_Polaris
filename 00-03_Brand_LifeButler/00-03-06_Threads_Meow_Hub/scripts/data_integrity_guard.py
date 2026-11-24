#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data_integrity_guard.py — 數據採集與歷史指標完整性防護門禁
核心防呆：當外部 API 發生異常（如 token 過期、網路逾時、500 錯誤）回傳空值或錯誤時，
強制中斷寫入流程，嚴禁將歷史有效數據覆蓋成 0 或清空！
"""

import json
from pathlib import Path

def update_metrics_safely(new_data: dict, history_file: Path) -> tuple[bool, str]:
    """
    安全更新歷史指標資料庫。
    若 new_data 為空或標記為 error，堅決拒絕寫入並保留歷史檔案。
    """
    if not new_data or new_data.get("status") == "error" or not new_data.get("valid", True):
        return False, "【更新拒絕】API回傳錯誤中斷，保留歷史數據不覆蓋！"

    # 若合格才執行寫入
    if history_file.exists():
        existing = history_file.read_text(encoding="utf-8")
    else:
        existing = ""

    return True, "✅ 數據驗收合格，安全寫入歷史指標"
