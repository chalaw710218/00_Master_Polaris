"""
run_pricing_tests.py
戴明首席品質長 · 防區 A（5D 報價）把關測試集自動回歸執行器

遍歷 scripts/tests/ 下的 case_pricing_*.md 測試案例，
透過 zone_a_pricing_auditor.py 執行審查，
驗證實際判定是否符合案例標記之【應退回】或【應通過】。
全部正確 Exit Code 0，任一不符 Exit Code 1。
"""

import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
TESTS_DIR = CURRENT_DIR / "tests"

sys.path.append(str(CURRENT_DIR))
from zone_a_pricing_auditor import ZoneAPricingAuditor

def run_all_pricing_tests():
    test_files = sorted(list(TESTS_DIR.glob("case_pricing_*.md")))
    if not test_files:
        print(f"❌ 錯誤：在 {TESTS_DIR} 未找到任何防區 A 測試案例！")
        sys.exit(1)

    print("=======================================================")
    print(f"   戴明防區 A (5D 報價) 把關程式自動回歸測試 (共有 {len(test_files)} 個案例)")
    print("=======================================================\n")

    all_passed = True
    summary = []

    for tf in test_files:
        content = tf.read_text(encoding="utf-8")
        expected = None
        if "【應退回】" in content or "應退回" in tf.stem:
            expected = "REJECTED"
        elif "【應通過】" in content or "應通過" in tf.stem:
            expected = "PASSED"
        else:
            print(f"❌ [失敗] 案例 {tf.name} 缺少預期標註！")
            summary.append((tf.name, "MISSING_TAG", "UNKNOWN", False))
            all_passed = False
            continue

        auditor = ZoneAPricingAuditor(str(tf))
        verdict, record_path = auditor.audit()
        actual = "REJECTED" if "REJECTED" in verdict else "PASSED"

        match = (expected == actual)
        if match:
            print(f"✅ [通過] {tf.name} -> 預期: {expected}, 實際: {actual}")
            summary.append((tf.name, expected, actual, True))
        else:
            print(f"❌ [失敗] {tf.name} -> 預期: {expected}, 實際: {actual}")
            summary.append((tf.name, expected, actual, False))
            all_passed = False

    print("\n=======================================================")
    if all_passed:
        print("   測試彙總結果：全部通過 (PASS)")
    else:
        print("   測試彙總結果：存在失敗案例 (FAIL)")
    print("=======================================================")

    for name, exp, act, ok in summary:
        icon = "✅" if ok else "❌"
        print(f"  {icon} {name}: 預期 {exp} | 實際 {act}")

    if all_passed:
        print("\n🎉 防區 A 回歸測試全部正確！Exit Code 0。\n")
        sys.exit(0)
    else:
        print("\n❌ 存在不符預期之測試案例！Exit Code 1。\n")
        sys.exit(1)

if __name__ == "__main__":
    run_all_pricing_tests()
