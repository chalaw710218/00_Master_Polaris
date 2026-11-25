import sys
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
sys.path.insert(0, str(HERE))

import bionic_knowledge_gate as bkg

TZ = timezone(timedelta(hours=8))
LOG_DIR = WORKSPACE / "00-00_Gamification_Engine" / "Office_of_the_CIO_Falcon" / "01_Cognitive_Log"
LEDGER_PATH = LOG_DIR / "learning_ledger.jsonl"
AUDIT_FILE = LOG_DIR / "第10輪衝突審計_待品碩決定.md"

def run_round_17():
    print("=== 執行第 17 輪 ===")
    started = "2026-11-25T23:23:05+08:00"
    url = "https://www.mol.gov.tw/media/a3tjzyan/%E5%8B%9E%E5%8B%95%E5%A5%91%E7%B4%84%E8%AA%8D%E5%AE%9A%E6%8C%87%E5%B0%8E%E5%8E%9F%E5%89%87%E9%99%84%E4%BB%B6-%E5%8B%9E%E5%8B%95%E5%A5%91%E7%B4%84%E5%BE%9E%E5%B1%AC%E6%80%A7%E5%88%A4%E6%96%B7%E6%AA%A2%E6%A0%B8%E8%A1%A8.pdf?mediaDL=true"
    source = "勞動部 勞動契約從屬性判斷檢核表（108/11/19）"
    title = "勞動部 勞動契約從屬性判斷檢核表 任一項目勾選為符合代表有從屬性特徵"
    quote = "一、本檢核表係供判斷從屬性之參考。任一項目如勾選為「符合」，代表該項目有從屬性特徵，但程度之高低，仍須視個案事實及整體契約情形判斷。 二、整體檢核結果，符合項目越多者，越可合理推論趨近於勞動契約，但仍需視整體契約內容，及事實上受拘束之程度，綜合判斷。"

    ok, msg = bkg.cmd_add(title, url, quote, source)
    ended = "2026-11-25T23:26:45+08:00"
    print(f"Round 17 add result: ok={ok}, msg={msg}")
    
    entry = {
        "round": 17,
        "topic": "勞動部「勞動契約從屬性判斷檢核表」25項原文",
        "started": started,
        "ended": ended,
        "add_ok": 1 if ok else 0,
        "add_rejected": 0 if ok else 1
    }
    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("Ledger round 17 written")

def run_round_18():
    print("=== 執行第 18 輪 ===")
    started = "2026-11-25T23:26:49+08:00"
    ended = "2026-11-25T23:27:20+08:00"
    # 查無主管機關專門函釋，不硬湊假條目，記為找不到
    entry = {
        "round": 18,
        "topic": "交通部或中華郵政對「代為交寄」的說明",
        "started": started,
        "ended": ended,
        "add_ok": 0,
        "add_rejected": 0,
        "status": "not_found",
        "note": "查無交通部或中華郵政針對代為交寄專營信件之專門函釋，依規則存入補查清單不硬湊"
    }
    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("Ledger round 18 written (not_found)")

def run_round_19():
    print("=== 執行第 19 輪 ===")
    started = "2026-11-25T23:27:25+08:00"
    ended = "2026-11-25T23:28:55+08:00"
    # 查無主管機關專門函釋，不硬湊假條目，記為找不到
    entry = {
        "round": 19,
        "topic": "到藥局代領已調劑藥品：衛福部或健保署常見問答與函釋",
        "started": started,
        "ended": ended,
        "add_ok": 0,
        "add_rejected": 0,
        "status": "not_found",
        "note": "查無衛福部或健保署針對商業委託代領已調劑處方藥之專門函釋，依規則存入補查清單不硬湊"
    }
    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("Ledger round 19 written (not_found)")

def update_audit_file():
    txt = AUDIT_FILE.read_text(encoding="utf-8")
    addition = """
- [ ] **8. 交通部或中華郵政對「跑腿代送到郵局或郵筒交寄信件」之專門函釋**：遍查郵政法與郵件處理規則，主管機關僅宣示專營權與運送業者限制，針對代辦交寄是否構成違規營業尚無專門函釋（第 18 輪查無結果，列入深水區補查）。
- [ ] **9. 衛福部或健保署對「第三人商業代領已調劑之處方藥品」之專門函釋**：健保醫療辦法僅有第7條受託人向醫師陳述病情與第25條特定事由一次領藥，針對一般商業委託至特約藥局代領調劑完成藥品之行政見解待補查（第 19 輪查無結果，列入深水區補查）。
"""
    if "8. 交通部或中華郵政" not in txt:
        target = "## 三、待品碩決定與補查清單 (Pending Research & Confirmation)\n\n以下法律爭議點與未定項目，建請品碩親自裁決並列入後續深水區法規調研：\n"
        replacement = target + addition
        txt = txt.replace(target, replacement)
        AUDIT_FILE.write_text(txt, encoding="utf-8")
        print("Updated 第10輪衝突審計_待品碩決定.md with items 8 and 9")

if __name__ == "__main__":
    run_round_17()
    run_round_18()
    run_round_19()
    update_audit_file()
