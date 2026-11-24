import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
REVISED_FILE = HERE / "chapter6_13_24_revised.md"
FACT_BANK_PATH = WORKSPACE / "00-00_Gamification_Engine" / "Office_of_the_CIO_Falcon" / "01_Cognitive_Log" / "01_事實庫.md"
GATE_SCRIPT = HERE / "bionic_knowledge_gate.py"

sys.path.insert(0, str(HERE))
from check_ch6 import parse_revised_file

def main():
    # 如果事實庫已存在，先清理重建，確保純粹由 add 寫入
    if FACT_BANK_PATH.exists():
        FACT_BANK_PATH.unlink()
        print(f"已清理現有事實庫: {FACT_BANK_PATH}")

    pairs = parse_revised_file(REVISED_FILE)
    print(f"自 {REVISED_FILE.name} 解析出 {len(pairs)} 筆待入庫條目\n" + "=" * 60)

    success_count = 0
    reject_count = 0
    rejections = []

    for idx, item in enumerate(pairs, 1):
        rule = item["rule"]
        source = item["source"]
        url = item["url"]
        quote = item["quote"]

        # 構造唯一且具語義之標題
        title = f"{rule} - {source}"

        cmd = [
            sys.executable, str(GATE_SCRIPT), "add",
            "--title", title,
            "--url", url,
            "--quote", quote,
            "--source", source
        ]

        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if res.returncode == 0:
            success_count += 1
            print(f"[{idx:02d}/29] ✅ 成功入庫: {title}")
        else:
            reject_count += 1
            err_msg = res.stderr.strip() or res.stdout.strip()
            rejections.append((title, err_msg))
            print(f"[{idx:02d}/29] ❌ 入庫被拒: {title}")
            print(f"        原因: {err_msg}")

    print("=" * 60)
    print("入庫統計結果（由程式計算）：")
    print(f"總處理筆數: {len(pairs)} 筆")
    print(f"成功寫入: {success_count} 筆")
    print(f"拒絕筆數: {reject_count} 筆")
    if rejections:
        print("\n拒絕原因清單：")
        for t, r in rejections:
            print(f"  - {t}: {r}")
    print("=" * 60)

if __name__ == "__main__":
    main()
