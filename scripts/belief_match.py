import csv
import re
import sys
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
COG_LOG_DIR = PROJECT_ROOT / "00-00_Gamification_Engine" / "Office_of_the_CEO_Yuki" / "01_Cognitive_Log"

FACT_FILE = COG_LOG_DIR / "01_Experiences_and_Evidence.md"
BELIEF_INV_CSV = COG_LOG_DIR / "_belief_inventory.csv"
OUTPUT_CSV = COG_LOG_DIR / "_belief_match_proposal.csv"


def main():
    if not FACT_FILE.is_file():
        print(f"錯誤：找不到事實庫 {FACT_FILE}", file=sys.stderr)
        sys.exit(1)
    if not BELIEF_INV_CSV.is_file():
        print(f"錯誤：找不到信念盤點檔 {BELIEF_INV_CSV}", file=sys.stderr)
        sys.exit(1)

    # 1. 讀取新事實庫，建立 方括號標記 -> (事實序號, 事實狀態)
    fact_text = FACT_FILE.read_text(encoding="utf-8")
    # 抓取每個「### [序號 N] 標題」以及其「- 狀態：狀態值」
    fact_entries = re.findall(
        r"^### \[序號 (\d+)\] (.*?)\n- 狀態：(.*?)(?:\n|$)",
        fact_text,
        re.MULTILINE
    )

    fact_tag_map = {}
    for seq, title, status in fact_entries:
        status_clean = status.strip()
        tags = re.findall(r"\[(.*?)\]", title)
        for t in tags:
            bracket_tag = f"[{t.strip()}]"
            fact_tag_map[bracket_tag] = (seq.strip(), status_clean)

    # 2. 讀取 _belief_inventory.csv，逐條進行比對
    matched_count = 0
    matched_verified = 0
    matched_mismatch = 0
    matched_internal = 0
    unmatched_count = 0

    output_rows = []

    with open(BELIEF_INV_CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row:
                continue
            b_seq = row[0].strip()
            b_title = row[1].strip() if len(row) > 1 else ""

            # 從標題抓出方括號裡的標記
            b_tags = re.findall(r"\[(.*?)\]", b_title)

            matched_tag = ""
            matched_fact_seq = ""
            matched_fact_status = ""

            # 優先比對是否有完全相同的輪次標記出現在事實庫中
            for t in b_tags:
                bracket_tag = f"[{t.strip()}]"
                if bracket_tag in fact_tag_map:
                    matched_tag = bracket_tag
                    matched_fact_seq, matched_fact_status = fact_tag_map[bracket_tag]
                    break

            if matched_fact_seq:
                matched_count += 1
                if "內部證據" in matched_fact_status:
                    matched_internal += 1
                elif matched_fact_status == "已驗證":
                    matched_verified += 1
                elif matched_fact_status == "對不上":
                    matched_mismatch += 1
            else:
                unmatched_count += 1
                # 沒有對應時，若原本有輪次標記（如 Cycle/Web-Iter/EXP 等），可記錄該標記
                if b_tags:
                    first_tag = f"[{b_tags[0].strip()}]"
                    if any(k in first_tag for k in ("Cycle", "Web-Iter", "EXP", "Iter")):
                        matched_tag = first_tag

            output_rows.append([
                b_seq,
                b_title,
                matched_tag,
                matched_fact_seq,
                matched_fact_status
            ])

    # 3. 輸出 _belief_match_proposal.csv
    with open(OUTPUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["信念序號", "信念標題前40字", "輪次標記", "對應事實序號", "事實狀態"])
        for r in output_rows:
            writer.writerow(r)

    total_beliefs = len(output_rows)

    print("=" * 40)
    print(f"總信念數: {total_beliefs}")
    print(f"找得到對應: {matched_count} 條")
    print(f"  - 對應到已驗證: {matched_verified} 條")
    print(f"  - 對應到對不上: {matched_mismatch} 條")
    print(f"  - 對應到內部證據: {matched_internal} 條")
    print(f"找不到對應: {unmatched_count} 條")
    print("=" * 40)
    print(f"csv 路徑: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
