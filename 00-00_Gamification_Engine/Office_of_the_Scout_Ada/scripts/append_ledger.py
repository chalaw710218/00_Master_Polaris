#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
append_ledger.py
================
艾達學習帳本追加記錄器
強制固定使用 UTF-8 (不帶 BOM) 寫入，禁止使用 PowerShell > 或 >> 輸出。
"""
import os
import re
import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
VAULT_PATH = HERE / "01_Cognitive_Log" / "01_事實庫.md"
LEDGER_PATH = HERE / "01_Cognitive_Log" / "學習帳本.txt"


def append_entry(round_num=None, note="日報"):
    if not LEDGER_PATH.exists():
        LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        LEDGER_PATH.write_text("", encoding="utf-8")

    ledger_text = LEDGER_PATH.read_text(encoding="utf-8")
    if round_num is None:
        matches = re.findall(r'第(\d+)輪', ledger_text)
        next_round = int(matches[-1]) + 1 if matches else 1
    else:
        next_round = round_num

    count = 0
    if VAULT_PATH.exists():
        vault_text = VAULT_PATH.read_text(encoding="utf-8")
        count = vault_text.count("**核心事實**")

    timestamp = datetime.datetime.now().isoformat(timespec="seconds")
    line = f"{timestamp} 第{next_round}輪 {note} 條目數 {count}\n"

    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(line)

    print(f"✅ 成功以 UTF-8 寫入帳本：{line.strip()}")
    return line


if __name__ == "__main__":
    append_entry()
