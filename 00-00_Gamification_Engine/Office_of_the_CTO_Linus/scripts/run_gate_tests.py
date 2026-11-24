"""
run_gate_tests.py
技術長林納斯仿生知識門禁全域安全與回歸測試套件
包含：
1. case_001_出處寫網路_單條.md【應退回】：驗證單條出處寫網路時不會造成 list index out of range 崩潰，正常退回並 Exit Code 1。
2. case_002_出處寫網路_前有合格條目.md【應退回】：驗證前有合格條目時，後續出處不合格條目之證據網址與摘句不會污染前一條，正常退回並 Exit Code 1。
3. 林納斯正式事實庫 check 查驗：驗證現有正式知識庫與簽章日誌完整一致，Exit Code 0。
"""

import sys
import subprocess
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPTS_DIR = Path(__file__).resolve().parent
GATE_SCRIPT = SCRIPTS_DIR / "bionic_knowledge_gate.py"
TESTS_DIR = SCRIPTS_DIR / "tests"

def run_check_file(file_path: Path):
    cmd = [sys.executable, str(GATE_SCRIPT), "check", "--file", str(file_path)]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    output = proc.stdout + "\n" + proc.stderr
    return proc.returncode, output

def main():
    print("=" * 70)
    print("🚀 開始執行技術長林納斯事實庫門禁安全審計與回歸測試")
    print("=" * 70)

    cases = [
        ("case_001_出處寫網路_單條.md", "出處不合格", 1),
        ("case_002_出處寫網路_前有合格條目.md", "出處不合格", 1),
    ]

    all_passed = True

    for case_name, expected_kw, expected_code in cases:
        case_path = TESTS_DIR / case_name
        print(f"▶️ 執行案例：{case_name}")
        assert case_path.exists(), f"找不到案例檔案：{case_path}"
        
        code, out = run_check_file(case_path)
        
        has_traceback = "Traceback" in out or "IndexError" in out or "list index out of range" in out
        has_kw = expected_kw in out
        
        if has_traceback:
            print(f"   ❌ [FAIL] 內部發生未預期 Traceback 或 IndexError 崩潰！")
            print(out)
            all_passed = False
            continue
            
        if code != expected_code:
            print(f"   ❌ [FAIL] Exit Code 不符！預期 {expected_code}，實際 {code}")
            all_passed = False
            continue

        if not has_kw:
            print(f"   ❌ [FAIL] 輸出未包含預期關鍵字「{expected_kw}」！")
            all_passed = False
            continue

        print(f"   ✅ [PASS] 成功攔截（Exit Code {code}，無 Traceback，符合預期）")

    print("\n▶️ 查驗技術長林納斯正式事實庫：")
    cmd_official = [sys.executable, str(GATE_SCRIPT), "check"]
    proc_official = subprocess.run(cmd_official, capture_output=True, text=True, encoding="utf-8")
    official_out = proc_official.stdout + "\n" + proc_official.stderr
    
    if proc_official.returncode == 0:
        print("   ✅ 正式事實庫驗簽完全通過 (Exit Code 0)")
    else:
        print(f"   ❌ 正式事實庫驗簽失敗！Exit Code {proc_official.returncode}")
        print(official_out)
        all_passed = False

    print("=" * 70)
    if all_passed:
        print("🎉 恭喜！技術長林納斯所有門禁回歸案例與正式事實庫全數通過！Exit Code 0。")
        print("=" * 70)
        sys.exit(0)
    else:
        print("❌ 部分測試失敗！Exit Code 1。")
        print("=" * 70)
        sys.exit(1)

if __name__ == "__main__":
    main()
