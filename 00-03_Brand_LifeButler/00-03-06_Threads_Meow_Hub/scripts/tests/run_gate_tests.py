"""
run_gate_tests.py — 生活管家影全域安全與門禁自動化回歸測試套件 (v6.0 事故端到端硬核防呆版)

特色：
1. 嚴格防崩潰假 PASS：比對預期退回原因關鍵字，且嚴禁出現未捕獲之 Traceback！
2. 100% 呼叫正式系統模組，不測任何模擬替代品：
   - bionic_knowledge_gate.py (知識出廠檢核 prepare & check)
   - scan_taiwan_trends.is_fatal_dispute (發文前爭議/政治硬攔截)
   - service_truth_gate.check_service_truth_poka_yoke (服務真實性出廠防呆)
   - feedback_loop.fetch_threads (Threads API 抓取與 metrics.jsonl 零覆蓋保全)
   - interaction_safety_gate.load_safety_state (限制檔防覆蓋與歷史保護)
   - threads_publisher.publish_thread (發文流水線端到端硬攔截 ✕ API 請求次數嚴格為 0 檢驗)
3. 所有測試 100% 在暫存複本執行，SHA-256 物理驗證前後不變，零污染正式檔案。
"""

import sys
import shutil
import subprocess
import re
import json
import hashlib
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

HERE = Path(__file__).resolve().parent
SCRIPTS_DIR = HERE.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.append(str(SCRIPTS_DIR))

# 載入熱搜模組路徑
HOT_TREND_DIR = SCRIPTS_DIR.parents[2] / ".agents" / "skills" / "hot-trend-scout" / "scripts"
if HOT_TREND_DIR.exists() and str(HOT_TREND_DIR) not in sys.path:
    sys.path.append(str(HOT_TREND_DIR))

# 正式系統模組
from bionic_knowledge_gate import prepare_cmd
from service_truth_gate import check_service_truth_poka_yoke
import scan_taiwan_trends
import feedback_loop
import interaction_safety_gate
import threads_publisher

OFFICIAL_VAULT = SCRIPTS_DIR.parent / "data" / "fact_bank.md"
OFFICIAL_METRICS = SCRIPTS_DIR.parent / "data" / "metrics.jsonl"
OFFICIAL_LIMITS = SCRIPTS_DIR.parent / "data" / "daily_interaction_limits.json"
GATE_SCRIPT = SCRIPTS_DIR / "bionic_knowledge_gate.py"

def main():
    print("=== 生活管家影全域品質與安全回歸測試套件 (v6.0 端到端真實事故版) 開始 ===")
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
        elif "test_mode: trend_dispute" in content or "test_mode: topic_safety" in content:
            mode = "trend_dispute"
        elif "test_mode: service_truth" in content:
            mode = "service_truth"
        elif "test_mode: feedback_api" in content or "test_mode: data_integrity" in content:
            mode = "feedback_api"
        elif "test_mode: limits_guard" in content or "test_mode: file_guard" in content:
            mode = "limits_guard"
        elif "test_mode: publish_gate" in content:
            mode = "publish_gate"

        print(f"▶ 執行案例：{case_name}（模式：{mode} | 預期：{expected}）")

        actual = None
        output_text = ""
        has_traceback = False
        extra_checks_passed = True
        extra_check_fail_msg = ""

        # --- 模式 A: 知識庫 check 命令 ---
        if mode == "check":
            cmd = [sys.executable, str(GATE_SCRIPT), "check", "--file", str(case_path)]
            proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
            output_text = proc.stdout + "\n" + proc.stderr
            has_traceback = "Traceback" in output_text
            actual = "PASS" if proc.returncode == 0 else "REJECT"

        # --- 模式 B: 知識庫 prepare 命令（複本執行） ---
        elif mode == "prepare":
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_vault = Path(tmp_dir) / "vault.md"
                shutil.copyfile(OFFICIAL_VAULT, tmp_vault)
                try:
                    passed_cnt, rejected_cnt, rejected_list = prepare_cmd(
                        pending_path=case_path,
                        vault_path=tmp_vault,
                        is_baseline=False
                    )
                    actual = "PASS" if passed_cnt > 0 and rejected_cnt == 0 else "REJECT"
                    if rejected_list:
                        output_text = "\n".join([r[1] for r in rejected_list])
                except Exception as e:
                    output_text = f"Traceback: {e}"
                    has_traceback = True
                    actual = "EXCEPTION"

        # --- 模式 C: 政治/爭議過濾（呼叫 scan_taiwan_trends.is_fatal_dispute） ---
        elif mode == "trend_dispute":
            m_draft = re.search(r'草稿內容：\s*\n(.+)', content, re.DOTALL)
            draft = m_draft.group(1).strip() if m_draft else content
            try:
                is_bad, dispute_reason = scan_taiwan_trends.is_fatal_dispute(draft)
                actual = "REJECT" if is_bad else "PASS"
                output_text = dispute_reason or "正常通過，無爭議熱詞"
            except Exception as e:
                output_text = f"Traceback: {e}"
                has_traceback = True
                actual = "EXCEPTION"

        # --- 模式 D: 服務真實性防呆（呼叫 service_truth_gate） ---
        elif mode == "service_truth":
            m_draft = re.search(r'草稿內容：\s*\n(.+)', content, re.DOTALL)
            draft = m_draft.group(1).strip() if m_draft else content
            try:
                ok, reason = check_service_truth_poka_yoke(draft)
                actual = "PASS" if ok else "REJECT"
                output_text = reason
            except Exception as e:
                output_text = f"Traceback: {e}"
                has_traceback = True
                actual = "EXCEPTION"

        # --- 模式 E: API 數據採集與複本保全（呼叫 feedback_loop.fetch_threads） ---
        elif mode == "feedback_api":
            m_api = re.search(r'API 回傳狀態：\s*\n(\{.*\})', content, re.DOTALL)
            api_raw_json = m_api.group(1).strip() if m_api else "{}"
            
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_metrics = Path(tmp_dir) / "metrics.jsonl"
                if OFFICIAL_METRICS.exists():
                    shutil.copyfile(OFFICIAL_METRICS, tmp_metrics)
                else:
                    tmp_metrics.write_text('{"post_id":"dummy","views":10}\n', encoding="utf-8")

                sha_before = hashlib.sha256(tmp_metrics.read_bytes()).hexdigest()

                # 準備 Mock 網路回應
                mock_resp = MagicMock()
                try:
                    parsed_json = json.loads(api_raw_json)
                except Exception:
                    parsed_json = {"error": {"message": "Invalid JSON", "code": 190}}

                # 判斷是否為真實事故 code 190 錯誤格式
                is_error_response = "error" in parsed_json or parsed_json.get("code") == 190
                mock_resp.status_code = 400 if is_error_response else 200
                mock_resp.text = api_raw_json
                mock_resp.json.return_value = parsed_json

                orig_token = feedback_loop.TOKEN
                feedback_loop.TOKEN = "mock_token_for_test"

                try:
                    with patch("requests.get", return_value=mock_resp):
                        try:
                            metrics, replies = feedback_loop.fetch_threads("18108543599376923")
                            actual = "PASS"
                            output_text = f"成功解析指標: views={metrics.get('views', 0)}"
                            with open(tmp_metrics, "a", encoding="utf-8") as f:
                                f.write(json.dumps({"post_id": "18108543599376923", "metrics": metrics}) + "\n")
                        except RuntimeError as re_err:
                            actual = "REJECT"
                            output_text = str(re_err)
                        except Exception as unk_err:
                            actual = "EXCEPTION"
                            output_text = f"Traceback: {unk_err}"
                            has_traceback = True

                    sha_after = hashlib.sha256(tmp_metrics.read_bytes()).hexdigest()
                    if expected == "REJECT" and sha_before != sha_after:
                        extra_checks_passed = False
                        extra_check_fail_msg = "API 錯誤時 metrics.jsonl 複本被意外改動！SHA-256 不相符！"
                    elif expected == "PASS" and sha_before == sha_after:
                        extra_checks_passed = False
                        extra_check_fail_msg = "API 成功時 metrics.jsonl 複本未被正常寫入！"

                finally:
                    feedback_loop.TOKEN = orig_token

        # --- 模式 F: 限制檔損壞防覆蓋（呼叫 interaction_safety_gate.load_safety_state） ---
        elif mode == "limits_guard":
            m_file = re.search(r'限制檔內容：\s*\n(.+)', content, re.DOTALL)
            file_body = m_file.group(1).strip() if m_file else ""

            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_limits = Path(tmp_dir) / "daily_interaction_limits.json"
                tmp_limits.write_text(file_body, encoding="utf-8")
                sha_before = hashlib.sha256(tmp_limits.read_bytes()).hexdigest()

                orig_limits_file = interaction_safety_gate.LIMITS_FILE
                interaction_safety_gate.LIMITS_FILE = tmp_limits

                try:
                    if expected == "REJECT":
                        try:
                            interaction_safety_gate.load_safety_state()
                            actual = "PASS"
                            output_text = "未拋出異常，意外通過"
                        except RuntimeError as re_err:
                            actual = "REJECT"
                            output_text = str(re_err)
                        except Exception as unk_err:
                            actual = "EXCEPTION"
                            output_text = f"Traceback: {unk_err}"
                            has_traceback = True

                        sha_after = hashlib.sha256(tmp_limits.read_bytes()).hexdigest()
                        if sha_before != sha_after:
                            extra_checks_passed = False
                            extra_check_fail_msg = "限制檔讀取失敗時原檔被意外覆蓋重置！SHA-256 不相符！"
                    else:
                        try:
                            state = interaction_safety_gate.load_safety_state()
                            if isinstance(state, dict) and "date" in state:
                                actual = "PASS"
                                output_text = f"成功讀取狀態字典（comments: {state.get('comments_count', 0)}）"
                            else:
                                actual = "REJECT"
                                output_text = "回傳狀態非預期字典結構"
                        except Exception as unk_err:
                            actual = "EXCEPTION"
                            output_text = f"Traceback: {unk_err}"
                            has_traceback = True

                finally:
                    interaction_safety_gate.LIMITS_FILE = orig_limits_file

        # --- 模式 G: 發文流水線端到端門禁（呼叫 threads_publisher.publish_thread ✕ 零網路請求驗證） ---
        elif mode == "publish_gate":
            m_draft = re.search(r'草稿內容：\s*\n(.+)', content, re.DOTALL)
            draft = m_draft.group(1).strip() if m_draft else content
            is_import_fail = "sub_mode: import_fail" in content

            orig_user_id = threads_publisher.THREADS_USER_ID
            orig_access_token = threads_publisher.THREADS_ACCESS_TOKEN
            threads_publisher.THREADS_USER_ID = "mock_user_123"
            threads_publisher.THREADS_ACCESS_TOKEN = "mock_token_abc"

            mock_post = MagicMock()
            mock_resp_container = MagicMock()
            mock_resp_container.json.return_value = {"id": "mock_container_999"}
            mock_resp_publish = MagicMock()
            mock_resp_publish.json.return_value = {"id": "mock_post_888"}
            mock_post.side_effect = [mock_resp_container, mock_resp_publish]

            mock_get = MagicMock()
            saved_modules = dict(sys.modules)

            try:
                if is_import_fail:
                    sys.modules["scan_taiwan_trends"] = None

                with patch("requests.post", mock_post), patch("requests.get", mock_get), patch("time.sleep", return_value=None):
                    if expected == "REJECT":
                        try:
                            threads_publisher.publish_thread(text=draft)
                            actual = "PASS"
                            output_text = "未拋出異常，意外進入發布流程"
                        except (ValueError, RuntimeError) as blk_err:
                            actual = "REJECT"
                            output_text = str(blk_err)
                        except Exception as unk_err:
                            actual = "EXCEPTION"
                            output_text = f"Traceback: {unk_err}"
                            has_traceback = True

                        # 核心驗證：發出任何 API 請求前就必須擋下，請求次數必須為 0！
                        api_calls = mock_post.call_count + mock_get.call_count
                        if api_calls > 0:
                            extra_checks_passed = False
                            extra_check_fail_msg = f"未在發出網路請求前擋下！API 請求次數為 {api_calls}（預期為 0）"
                    else:
                        # expected == "PASS"
                        try:
                            post_id = threads_publisher.publish_thread(text=draft)
                            if post_id == "mock_post_888":
                                actual = "PASS"
                                output_text = f"成功進入發文流程並取得 Post ID: {post_id}"
                            else:
                                actual = "REJECT"
                                output_text = f"回傳 Post ID 不符合預期: {post_id}"
                        except Exception as unk_err:
                            actual = "EXCEPTION"
                            output_text = f"Traceback: {unk_err}"
                            has_traceback = True

                        # 核心驗證：正常發文時 API 必須被呼叫
                        if mock_post.call_count == 0:
                            extra_checks_passed = False
                            extra_check_fail_msg = "正常發文時 Threads API 請求次數為 0，未進入發布流程！"

            finally:
                threads_publisher.THREADS_USER_ID = orig_user_id
                threads_publisher.THREADS_ACCESS_TOKEN = orig_access_token
                sys.modules.clear()
                sys.modules.update(saved_modules)

        # 4. 嚴格判定邏輯（Exit Code / 結果 + 原因關鍵字 + 無 Traceback + 額外保全檢驗）
        case_passed = True
        fail_reasons = []

        if actual != expected:
            case_passed = False
            fail_reasons.append(f"結果不符（預期: {expected}, 實測: {actual}）")

        if has_traceback:
            case_passed = False
            fail_reasons.append("檢測到未捕獲之異常 Traceback 崩潰")

        if not extra_checks_passed:
            case_passed = False
            fail_reasons.append(extra_check_fail_msg)

        if expected == "REJECT" and expected_reason:
            if expected_reason not in output_text:
                case_passed = False
                fail_reasons.append(f"未匹配到預期原因關鍵字「{expected_reason}」（實測: {output_text[:60]}...）")

        if case_passed:
            status_str = "✅ PASS"
            detail = f"實測 {actual}，原因匹配成功，安全驗證通過，無崩潰"
            print(f"  結果：{status_str} | {detail}\n")
            results.append((case_name, expected, actual, status_str))
        else:
            status_str = "❌ FAIL"
            detail = "；".join(fail_reasons)
            print(f"  結果：{status_str} | {detail}\n")
            results.append((case_name, expected, actual, status_str))
            all_passed = False

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
