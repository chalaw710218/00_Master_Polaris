import json
import os

log_path = r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager\clients\01_Taitung_Shokunin_Diner\data\autopilot_replies.jsonl"

records = []
if os.path.exists(log_path):
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line.strip()))

print(f"Total replies permanently logged in ledger: {len(records)}")
if records:
    print("\n--- [範例 1: 最近一筆回覆存證] ---")
    print(json.dumps(records[-1], ensure_ascii=False, indent=2))
    print("\n--- [範例 2: 歷史回覆存證] ---")
    print(json.dumps(records[0], ensure_ascii=False, indent=2))
