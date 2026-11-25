import json
from pathlib import Path

HERE = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris")
LOG_DIR = HERE / "00-00_Gamification_Engine" / "Office_of_the_CIO_Falcon" / "01_Cognitive_Log"
LEDGER_PATH = LOG_DIR / "learning_ledger.jsonl"
PENDING_PATH = LOG_DIR / "00_待簽章區.md"

def fix_ledger():
    lines = []
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            r = entry.get("round")
            if r == 14:
                entry["started"] = "2026-11-25T23:12:22+08:00"
                entry["ended"] = "2026-11-25T23:20:02+08:00"
                entry["note"] = "started 依快照建立時間補正"
            elif r == 15:
                entry["started"] = "2026-11-25T23:13:33+08:00"
                entry["ended"] = "2026-11-25T23:20:02+08:00"
                entry["note"] = "started 依快照建立時間補正"
            elif r == 16:
                entry["started"] = "2026-11-25T23:14:05+08:00"
                entry["ended"] = "2026-11-25T23:20:02+08:00"
                entry["note"] = "started 依快照建立時間補正"
            lines.append(entry)
            
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        for entry in lines:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("Ledger 14-16 fixed successfully")

def fix_pending_bank():
    txt = PENDING_PATH.read_text(encoding="utf-8")
    old_source = "出處：勞動部公告 勞動契約認定指導原則（108/11/19） https://www.mol.gov.tw/1607/1632/1640/12431/"
    new_source = "出處：勞動部新聞稿（2019-11-19）勞動部訂定勞動契約認定指導原則 https://www.mol.gov.tw/1607/1632/1640/12431/"
    if old_source in txt:
        txt = txt.replace(old_source, new_source)
        PENDING_PATH.write_text(txt, encoding="utf-8")
        print("00_待簽章區.md round 14 source fixed successfully")
    else:
        print("Warning: old source not found in pending bank, check content")

if __name__ == "__main__":
    fix_ledger()
    fix_pending_bank()
