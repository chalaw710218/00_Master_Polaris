"""
run_gate_tests.py — 生活管家影全域安全與門禁自動化回歸測試套件 (v3.0)
特色：
1. 嚴格防崩潰假 PASS：同時比對 Exit Code、預期退回原因關鍵字，且嚴禁出現 Traceback！
2. 全域多維閘門支援：
   - bionic_knowledge_gate (prepare & check)
   - topic_safety_gate (政治敏感與爭議過濾)
   - service_truth_gate (服務真實性出廠防呆)
   - data_integrity_guard (API 異常防覆蓋歸零)
3. 知識庫一律在複本 tmp_fact_bank.md 上執行，零污染正式庫。
"""

import sys
import shutil
import subprocess
import re
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS_DIR = HERE.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.append(str(SCRIPTS_DIR))

from bionic_knowledge_gate import prepare_cmd
from service_truth_gate import check_service_truth_poka_yoke
from topic_safety_gate import check_topic_safety
from data_integrity_guard import update_metrics_safely

OFFICIAL_VAULT = SCRIPTS_DIR.parent / "data" / "fact_bank.md"
TMP_VAULT = HERE / "tmp_fact_bank.md"
GATE_SCRIPT = SCRIPTS_DIR / "bionic_knowledge_gate.py"

def main():
    print("=== 生活管家影全域品質與安全回歸測試套件 (v3.0) 開始 ===")
    case_files = sorted(list(HERE.glob("case_*.md")))
    if not case_files:
        print("❌ 未在 scripts/tests/ 找到任何 case_*.md 測試案例！")
        sys.exit(1)

    print(f"找到 {len(case_files)} 個測試案例。\n")
    results = []
    all_passed = True

    for case_path in case_files:
        case_name = case_path.name
        content = case_path.read_text(encoding="utf-8")
        
        # 1. 預期結果標註判定
        expected = None
        if "【應通過】" in case_name or "【應通過】" in content:
            expected = "PASS"
        elif "【應退回】" in case_name or "【應退回】" in content:
            expected = "REJECT"
        else:
            print(f"❌ [FAIL] 案例「{case_name}」缺少【應通過】或【應退回】標註！直接判定失敗。")
            results.append((case_name, "無標註", "FAIL", "缺少必要預期標註"))
            all_passed = False
            continue

        # 2. 提取預期原因（若有）
        expected_reason = None
        m_reason = re.search(r'預期原因：\s*(.+)$', content, re.MULTILINE)
        if m_reason:
            expected_reason = m_reason.group(1).strip()

        # 3. 判斷測試模式
        mode = "prepare"
        if "test_mode: check" in content:
            mode = "check"
        elif "test_mode: topic_safety" in content:
            mode = "topic_safety"
        elif "test_mode: service_truth" in content:
            mode = "service_truth"
        elif "test_mode: data_integrity" in content:
            mode = "data_integrity"

        print(f"▶ 執行案例：{case_name}（模式：{mode} | 預期：{expected}）")

        actual = None
        output_text = ""
        has_traceback = False

        if mode == "check":
            cmd = [sys.executable, str(GATE_SCRIPT), "check", "--file", str(case_path)]
            proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
            output_text = proc.stdout + "\n" + proc.stderr
            has_traceback = "Traceback" in output_text
            actual = "PASS" if proc.returncode == 0 else "REJECT"

        elif mode == "prepare":
            shutil.copyfile(OFFICIAL_VAULT, TMP_VAULT)
            try:
                passed_cnt, rejected_cnt, rejected_list = prepare_cmd(
                    pending_path=case_path,
                    vault_path=TMP_VAULT,
                    is_baseline=False
                )
                actual = "PASS" if passed_cnt > 0 and rejected_cnt == 0 else "REJECT"
                if rejected_list:
                    output_text = "\n".join([r[1] for r in rejected_list])
            except Exception as e:
                output_text = f"Traceback: {e}"
                has_traceback = True
                actual = "EXCEPTION"

        elif mode == "topic_safety":
            # 提取草稿內容
            m_draft = re.search(r'草稿內容：\s*\n(.+)', content, re.DOTALL)
            draft = m_draft.group(1).strip() if m_draft else content
            ok, reason = check_topic_safety(draft)
            actual = "PASS" if ok else "REJECT"
            output_text = reason

        elif mode == "service_truth":
            m_draft = re.search(r'草稿內容：\s*\n(.+)', content, re.DOTALL)
            draft = m_draft.group(1).strip() if m_draft else content
            ok, reason = check_service_truth_poka_yoke(draft)
            actual = "PASS" if ok else "REJECT"
            output_text = reason

        elif mode == "data_integrity":
            # 模擬傳入錯誤 API 響應
            err_payload = {"status": "error", "message": "API token invalid"}
            ok, reason = update_metrics_safely(err_payload, HERE / "tmp_history.json")
            actual = "PASS" if ok else "REJECT"
            output_text = reason

        # 4. 嚴格判定邏輯（Exit Code / 結果 + 原因關鍵字 + 無 Traceback）
        case_passed = True
        fail_reasons = []

        if actual != expected:
            case_passed = False
            fail_reasons.append(f"結果不符（預期: {expected}, 實測: {actual}）")

        if has_traceback:
            case_passed = False
            fail_reasons.append("檢測到未捕獲之異常 Traceback 崩潰")

        if expected == "REJECT" and expected_reason:
            if expected_reason not in output_text:
                case_passed = False
                fail_reasons.append(f"未匹配到預期原因關鍵字「{expected_reason}」")

        if case_passed:
            status_str = "✅ PASS"
            detail = f"實測 {actual}，原因匹配成功，無崩潰"
            print(f"  結果：{status_str} | {detail}\n")
            results.append((case_name, expected, actual, status_str))
        else:
            status_str = "❌ FAIL"
            detail = "；".join(fail_reasons)
            print(f"  結果：{status_str} | {detail}\n")
            results.append((case_name, expected, actual, status_str))
            all_passed = False

    # 清理臨時檔案
    if TMP_VAULT.exists():
        TMP_VAULT.unlink()

    print("=== 測試矩陣總結 (Test Matrix Summary) ===")
    for c_name, exp, act, st in results:
        print(f"  [{st}] {c_name} (預期: {exp} | 實際: {act})")

    if all_passed:
        print(f"\n🎉 全部 {len(case_files)} 個回歸案例 100% 驗證通過！Exit Code 0。")
        sys.exit(0)
    else:
        print("\n❌ 存在失敗案例，安燈阻斷！Exit Code 1。")
        sys.exit(1)

if __name__ == "__main__":
    main()
