"""
run_audit_tests.py
戴明審查測試集自動回歸執行器 (Deming Audit Test Suite Runner)

規則：遍歷 scripts/tests/ 下的所有 .md 測試案例，
透過 three_gates_auditor.py 執行審查，
驗證實際判定是否符合案例中標記之「應退回」或「應通過」。
全部正確 Exit Code 0，任一不符 Exit Code 1。
"""

import sys
import re
from pathlib import Path

# 將 scripts 目錄加入 path
CURRENT_DIR = Path(__file__).resolve().parent
sys.path.append(str(CURRENT_DIR))

from three_gates_auditor import ThreeGatesAuditor

TESTS_DIR = CURRENT_DIR / "tests"

def run_all_tests():
    test_files = sorted(list(TESTS_DIR.glob("*.md")) + list(TESTS_DIR.glob("*.docx")))
    if not test_files:
        print(f"❌ 錯誤：在 {TESTS_DIR} 未找到任何測試案例！")
        sys.exit(1)

    print(f"=======================================================")
    print(f"   戴明審查把關程式自動回歸測試 (共有 {len(test_files)} 個案例)")
    print(f"=======================================================\n")

    all_passed = True
    summary = []

    for tf in test_files:
        expected = None
        if tf.suffix.lower() == ".md":
            content = tf.read_text(encoding="utf-8")
            if "【應退回】" in content or "應退回" in tf.stem:
                expected = "REJECTED"
            elif "【應通過】" in content or "應通過" in tf.stem:
                expected = "PASSED"
        else:
            if "應退回" in tf.stem:
                expected = "REJECTED"
            elif "應通過" in tf.stem:
                expected = "PASSED"

        if expected is None:
            print(f"❌ [失敗] 案例 {tf.name} 缺少預期標註（未標明【應退回】或【應通過】）！")
            summary.append((tf.name, "MISSING_TAG", "UNKNOWN", False))
            all_passed = False
            continue

        auditor = ThreeGatesAuditor(str(tf))
        verdict, record_path = auditor.audit_all()
        actual = "REJECTED" if "REJECTED" in verdict else "PASSED"

        match = (expected == actual)
        if match:
            print(f"✅ [通過] {tf.name} -> 預期: {expected}, 實際: {actual}")
            summary.append((tf.name, expected, actual, True))
        else:
            print(f"❌ [失敗] {tf.name} -> 預期: {expected}, 實際: {actual}")
            summary.append((tf.name, expected, actual, False))
            all_passed = False

    print(f"\n=======================================================")
    print(f"   測試彙總結果：{'全部通過 (PASS)' if all_passed else '存在失敗案例 (FAIL)'}")
    print(f"=======================================================")
    for name, exp, act, ok in summary:
        mark = "✅" if ok else "❌"
        print(f"  {mark} {name}: 預期 {exp} | 實際 {act}")

    if all_passed:
        print("\n🎉 回歸測試全部正確！Exit Code 0。\n")
        sys.exit(0)
    else:
        print("\n❌ 存在不符預期之測試案例！Exit Code 1。\n")
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()
