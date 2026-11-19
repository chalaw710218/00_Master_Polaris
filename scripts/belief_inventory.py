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

BELIEF_FILE = COG_LOG_DIR / "02_Belief_Evolution.md"
FACT_FILE = COG_LOG_DIR / "01_Experiences_and_Evidence.md"
OUTPUT_CSV = COG_LOG_DIR / "_belief_inventory.csv"


def main():
    if not BELIEF_FILE.is_file():
        print(f"錯誤：找不到信念庫 {BELIEF_FILE}", file=sys.stderr)
        sys.exit(1)
    if not FACT_FILE.is_file():
        print(f"錯誤：找不到事實庫 {FACT_FILE}", file=sys.stderr)
        sys.exit(1)

    # 讀取新事實庫的序號集合
    fact_text = FACT_FILE.read_text(encoding="utf-8")
    new_fact_seqs = set(re.findall(r"^### \[序號 (\d+)\]", fact_text, re.MULTILINE))

    # 讀取信念庫
    belief_text = BELIEF_FILE.read_text(encoding="utf-8")

    # 以標題切分條目（行首為「## 」「### 」，或「數字. **」）
    pattern = re.compile(r"^(?:## |### |\d+\.\s*\*\*)", re.MULTILINE)
    matches = list(pattern.finditer(belief_text))

    rows = []
    has_basis_count = 0
    found_in_bank_count = 0
    no_basis_count = 0

    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(belief_text)
        entry_text = belief_text[start:end]
        first_line = entry_text.splitlines()[0].strip() if entry_text.splitlines() else ""
        heading_40 = first_line[:40]

        seq = i + 1

        # 判定：條目內有「依據」二字並帶數字
        # 尋找「依據」後接數字（允許中間有冒號、空格等非數字字元）
        basis_match = re.search(r"依據[^\n\d]{0,20}(\d+)", entry_text)

        if basis_match:
            has_basis = "是"
            ref_seq = basis_match.group(1)
            if ref_seq in new_fact_seqs:
                in_bank = "是"
                found_in_bank_count += 1
            else:
                in_bank = "否"
            has_basis_count += 1
        else:
            has_basis = "否"
            ref_seq = "無"
            in_bank = "無"
            no_basis_count += 1

        rows.append([seq, heading_40, has_basis, ref_seq, in_bank])

    # 輸出 CSV
    with open(OUTPUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["序號", "標題前40字", "有寫依據(是/否)", "依據指向的事實序號", "該序號在新事實庫裡(是/否/無)"])
        for r in rows:
            writer.writerow(r)

    total_count = len(rows)

    print("=" * 40)
    print(f"總條目數: {total_count}")
    print(f"有寫依據: {has_basis_count} 條")
    print(f"依據在新事實庫裡找得到: {found_in_bank_count} 條")
    print(f"沒有依據: {no_basis_count} 條")
    print("=" * 40)
    print(f"csv 路徑: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
