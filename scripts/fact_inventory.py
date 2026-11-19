import csv
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def find_target_file():
    candidates = [
        Path("00-00_Gamification_Engine/Office_of_the_CEO_Yuki/01_Cognitive_Log/01_Experiences_and_Evidence.md"),
        Path("Office_of_the_CEO_Yuki/01_Cognitive_Log/01_Experiences_and_Evidence.md"),
        Path(__file__).resolve().parent.parent / "00-00_Gamification_Engine/Office_of_the_CEO_Yuki/01_Cognitive_Log/01_Experiences_and_Evidence.md",
    ]
    for c in candidates:
        if c.is_file():
            return c.resolve()
    # Fallback search
    matches = list(Path(".").glob("**/01_Experiences_and_Evidence.md"))
    if matches:
        return matches[0].resolve()
    raise FileNotFoundError("找不到 01_Experiences_and_Evidence.md")


def main():
    target_path = find_target_file()
    output_csv = target_path.parent / "_fact_inventory.csv"

    with open(target_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 以標題切分條目（行首為「## 」「### 」，或「數字. **第」）
    pattern = re.compile(r"^(?:## |### |\d+\.\s*\*\*第)", re.MULTILINE)
    matches = list(pattern.finditer(text))

    items = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        entry_text = text[start:end]
        lines = entry_text.splitlines()
        heading = lines[0].strip() if lines else ""
        body = "\n".join(lines[1:]) if len(lines) > 1 else ""
        items.append((heading, body, entry_text))

    total_count = len(items)
    url_count = 0
    paper_count = 0
    audit_count = 0
    biz_count = 0

    rows = []
    for idx, (heading, body, entry_text) in enumerate(items, 1):
        # 標題前40字
        title_40 = heading[:40]

        # 含網址(是/否)
        has_url_bool = bool(re.search(r"https?://", entry_text))
        has_url = "是" if has_url_bool else "否"
        if has_url_bool:
            url_count += 1

        # 含數字(是/否)
        has_num = "是" if bool(re.search(r"\d", entry_text)) else "否"

        # 類型判定（依序，先符合先算）：
        # 內文含 arXiv 或「文獻」→ 論文
        # 標題含「審計」→ 審計
        # 其他 → 業務
        if bool(re.search(r"arxiv|文獻", body, re.IGNORECASE)):
            item_type = "論文"
            paper_count += 1
        elif "審計" in heading:
            item_type = "審計"
            audit_count += 1
        else:
            item_type = "業務"
            biz_count += 1

        rows.append([idx, title_40, has_url, has_num, item_type])

    # 寫入 CSV
    with open(output_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["序號", "標題前40字", "含網址(是/否)", "含數字(是/否)", "類型"])
        writer.writerows(rows)

    # 輸出統計結果
    print(f"盤點來源: {target_path}")
    print(f"產出檔案: {output_csv}")
    print(f"總條目數: {total_count}")
    print(f"含網址條目數: {url_count}")
    print(f"論文: {paper_count} 條")
    print(f"審計: {audit_count} 條")
    print(f"業務: {biz_count} 條")


if __name__ == "__main__":
    main()
