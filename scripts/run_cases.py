"""
run_cases.py — 執行法規摘句與入庫門禁全維度測試案例檢驗 (支援 case_001～case_026)
讀取 scripts/tests/ 下的測試案例，使用 snapshots/ 快照與測試密鑰調用門禁進行判定
驗證「應通過」與「應退回」案例之判定結果是否 100% 符合預期標記
包含項款證明、法規全名完全比對、URL sha1 快照化、黑名單部分比對、手動貼假條目阻斷、無簽章阻斷、篡改阻斷、合法簽章通過、sign簽前核驗與非falcon辦公室阻斷全套 26 項測試
"""

import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

# 強制 UTF-8 輸出
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
TESTS_DIR = HERE / "tests"
SNAP_DIR = HERE / "snapshots"
BIONIC_CORE = HERE.parent / ".agents" / "skills" / "bionic-learning-system" / "bionic_core"
sys.path.insert(0, str(BIONIC_CORE))
sys.path.insert(0, str(HERE))

from evidence_gate import quote_in_page
import founder_auth
import bionic_knowledge_gate

TEST_META_PATH = TESTS_DIR / "test_founder_vault.meta.json"
TEST_PIN_PATH = TESTS_DIR / "test_founder_pin.txt"
TEST_PASSPHRASE = "test_password_123"


def init_test_auth():
    """確保測試密鑰存在且 PIN 錨定檔案指向測試環境"""
    if not TEST_META_PATH.exists():
        founder_auth.init_meta_file(TEST_PASSPHRASE, TEST_META_PATH)
    founder_auth.PIN_PATH = TEST_PIN_PATH
    founder_auth.pin_meta(TEST_META_PATH)


def verify_item_subitem(source: str, quote: str) -> (bool, str):
    num_map = {
        "1": "一", "2": "二", "3": "三", "4": "四", "5": "五",
        "6": "六", "7": "七", "8": "八", "9": "九", "10": "十"
    }
    m_sub = re.search(r"第([0-9一二三四五六七八九十]+)款", source)
    if m_sub:
        k = m_sub.group(1)
        k_cn = num_map.get(k, k)
        pat = f"{k_cn}、|第{k_cn}款|第{k}款"
        if not re.search(pat, quote):
            return False, f"出處載明第{k}款，但摘句中無對應款次文字（如『{k_cn}、』）"

    m_item = re.search(r"第([0-9一二三四五六七八九十]+)項", source)
    if m_item:
        k = m_item.group(1)
        k_cn = num_map.get(k, k)
        pat = f"第{k_cn}項|第{k}項"
        if not re.search(pat, quote):
            return False, f"出處載明第{k}項，但摘句中無對應項次文字（如『第{k_cn}項』）"

    return True, ""


def parse_case(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    data = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or "：" not in line:
            continue
        k, v = line.split("：", 1)
        data[k.strip()] = v.strip()
    return data


def find_snapshot(url: str, snap_name: str = "") -> Path:
    if snap_name and (SNAP_DIR / snap_name).exists():
        return SNAP_DIR / snap_name

    if url:
        h = hashlib.sha1(url.strip().encode("utf-8")).hexdigest()[:12]
        sha1_file = SNAP_DIR / f"{h}.txt"
        if sha1_file.exists():
            return sha1_file

    pcode_law = {
        "J0080037": "電子簽章法", "J0030011": "電業法", "K0110001": "發展觀光條例",
        "O0050024": "一般廢棄物回收清除處理辦法", "O0050001": "廢棄物清理法",
        "D0070118": "公寓大廈管理條例", "L0070040": "長期照顧服務法", "L0020001": "醫師法",
        "L0040001": "食品安全衛生管理法", "M0060027": "動物保護法", "J0150002": "公平交易法",
        "D0070148": "建築物室內裝修管理辦法", "D0070109": "建築法", "J0080001": "公司法",
        "B0000001": "民法", "I0020001": "仲裁法"
    }
    m = re.search(r"pcode=([A-Z0-9]+)&flno=([0-9\-]+)", url)
    if m:
        pcode, flno = m.group(1), m.group(2)
        law = pcode_law.get(pcode, "")
        for f in SNAP_DIR.glob(f"{law}*.txt"):
            if f"第{flno}條" in f.name or f"第{flno}項" in f.name:
                return f
        return None
    return None


def run_gate_add_case(title: str, url: str, quote: str, source: str) -> (bool, str):
    """在沙盒臨時待簽章區中測試門禁 add 邏輯"""
    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False, suffix=".md") as tmp_pending:
        tmp_pending.write("# 測試待簽章區\n\n### 現有條目_包含電簽法第4條之標題\n出處：舊出處 https://example.com\n原文：「舊摘句」\n\n---\n")
        tmp_pending_path = Path(tmp_pending.name)

    orig_pending = bionic_knowledge_gate.PENDING_BANK_PATH
    try:
        bionic_knowledge_gate.PENDING_BANK_PATH = tmp_pending_path
        ok, msg = bionic_knowledge_gate.cmd_add(title, url, quote, source)
        return ok, msg
    finally:
        bionic_knowledge_gate.PENDING_BANK_PATH = orig_pending
        if tmp_pending_path.exists():
            tmp_pending_path.unlink()


def run_gate_check_case(fake_title: str, fake_url: str, fake_quote: str, fake_source: str) -> (bool, str):
    """測試手動假條目能否被 check 攔截"""
    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False, suffix=".md") as tmp_fb:
        fake_content = f"# 測試事實庫\n\n### {fake_title}\n出處：{fake_source} {fake_url}\n原文：「{fake_quote}」\n\n---\n"
        tmp_fb.write(fake_content)
        tmp_fb_path = Path(tmp_fb.name)

    tmp_sig_path = tmp_fb_path.with_suffix(".sigs.jsonl")

    try:
        ok, count, illegals = bionic_knowledge_gate.cmd_check(
            fact_bank_path=tmp_fb_path,
            sigs_path=tmp_sig_path,
            meta_path=TEST_META_PATH
        )
        if not ok:
            return False, f"check 成功抓出違規行: {illegals[0][1] if illegals else '物理核驗失敗'}"
        return True, "check 未能攔截手動假條目"
    finally:
        if tmp_fb_path.exists():
            tmp_fb_path.unlink()
        if tmp_sig_path.exists():
            tmp_sig_path.unlink()


def run_signature_test_case(mode: str, title: str, url: str, quote: str, source: str) -> (bool, str):
    """
    測試創辦人簽章驗證情境：
    mode == '無簽章'：條目存在但無簽章檔 -> 預期 check 失敗
    mode == '篡改'：簽章後條目文字被改一個字 -> 預期 check 失敗
    mode == '有效'：正常簽章未篡改 -> 預期 check 通過
    """
    init_test_auth()
    
    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False, suffix=".md") as tmp_fb:
        tmp_fb_path = Path(tmp_fb.name)

    tmp_sig_path = tmp_fb_path.with_suffix(".sigs.jsonl")

    try:
        if mode == "無簽章":
            # 寫入條目但不建簽章檔
            content = f"# 測試事實庫\n\n### {title}\n出處：{source} {url}\n原文：「{quote}」\n\n---\n"
            tmp_fb_path.write_text(content, encoding="utf-8")
            ok, count, illegals = bionic_knowledge_gate.cmd_check(
                fact_bank_path=tmp_fb_path,
                sigs_path=tmp_sig_path,
                meta_path=TEST_META_PATH
            )
            return ok, (illegals[0][1] if illegals else "通過")

        elif mode == "篡改":
            # 先對合法內容簽章
            orig_sha = bionic_knowledge_gate.compute_entry_sha256(title, source, url, quote)
            payload = {"action": "fact_ingest", "office": "falcon", "entries_sha256": [orig_sha]}
            sig_bundle = founder_auth.sign_founder_action(payload, meta_path=TEST_META_PATH, _test_passphrase=TEST_PASSPHRASE)
            tmp_sig_path.write_text(json.dumps({"payload": payload, "sig_bundle": sig_bundle}) + "\n", encoding="utf-8")

            # 故意將條目內容篡改一個字（例如「電子形式」改為「數位形式」）
            tampered_quote = quote.replace("電子形式", "數位形式")
            tampered_content = f"# 測試事實庫\n\n### {title}\n出處：{source} {url}\n原文：「{tampered_quote}」\n\n---\n"
            tmp_fb_path.write_text(tampered_content, encoding="utf-8")

            ok, count, illegals = bionic_knowledge_gate.cmd_check(
                fact_bank_path=tmp_fb_path,
                sigs_path=tmp_sig_path,
                meta_path=TEST_META_PATH
            )
            return ok, (illegals[0][1] if illegals else "通過")

        elif mode == "有效":
            # 正常簽章且內容完全吻合
            real_sha = bionic_knowledge_gate.compute_entry_sha256(title, source, url, quote)
            payload = {"action": "fact_ingest", "office": "falcon", "entries_sha256": [real_sha]}
            sig_bundle = founder_auth.sign_founder_action(payload, meta_path=TEST_META_PATH, _test_passphrase=TEST_PASSPHRASE)
            tmp_sig_path.write_text(json.dumps({"payload": payload, "sig_bundle": sig_bundle}) + "\n", encoding="utf-8")

            real_content = f"# 測試事實庫\n\n### {title}\n出處：{source} {url}\n原文：「{quote}」\n\n---\n"
            tmp_fb_path.write_text(real_content, encoding="utf-8")

            ok, count, illegals = bionic_knowledge_gate.cmd_check(
                fact_bank_path=tmp_fb_path,
                sigs_path=tmp_sig_path,
                meta_path=TEST_META_PATH
            )
            return ok, (illegals[0][1] if illegals else "通過")

        elif mode == "非falcon辦公室":
            # 負載故意設為 yuki 辦公室
            real_sha = bionic_knowledge_gate.compute_entry_sha256(title, source, url, quote)
            payload = {"action": "fact_ingest", "office": "yuki", "entries_sha256": [real_sha]}
            sig_bundle = founder_auth.sign_founder_action(payload, meta_path=TEST_META_PATH, _test_passphrase=TEST_PASSPHRASE)
            tmp_sig_path.write_text(json.dumps({"payload": payload, "sig_bundle": sig_bundle}) + "\n", encoding="utf-8")

            real_content = f"# 測試事實庫\n\n### {title}\n出處：{source} {url}\n原文：「{quote}」\n\n---\n"
            tmp_fb_path.write_text(real_content, encoding="utf-8")

            ok, count, illegals = bionic_knowledge_gate.cmd_check(
                fact_bank_path=tmp_fb_path,
                sigs_path=tmp_sig_path,
                meta_path=TEST_META_PATH
            )
            return ok, (illegals[0][1] if illegals else "通過")

        return False, f"未知的簽章測試模式: {mode}"
    finally:
        if tmp_fb_path.exists():
            tmp_fb_path.unlink()
        if tmp_sig_path.exists():
            tmp_sig_path.unlink()


def run_sign_cmd_test_case(mode: str, title: str, url: str, quote: str, source: str) -> (bool, str):
    """
    測試創辦人 cmd_sign 簽前物理快照核驗：
    mode == '手貼假條目'：待簽章區含有快照中不存在之假條目 -> 預期 sign 拒簽退出
    mode == '全部合格'：待簽章區條目全部合法且命中快照 -> 預期 sign 簽章成功入庫
    """
    init_test_auth()

    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False, suffix=".md") as tmp_pb:
        tmp_pb_path = Path(tmp_pb.name)
    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False, suffix=".md") as tmp_fb:
        tmp_fb_path = Path(tmp_fb.name)
    tmp_sig_path = tmp_fb_path.with_suffix(".sigs.jsonl")

    try:
        # 寫入待簽章區
        pending_content = f"# 測試待簽章區\n\n### {title}\n出處：{source} {url}\n原文：「{quote}」\n\n---\n"
        tmp_pb_path.write_text(pending_content, encoding="utf-8")
        tmp_fb_path.write_text("# 測試事實庫\n\n---\n", encoding="utf-8")

        ok, msg = bionic_knowledge_gate.cmd_sign(
            meta_path=TEST_META_PATH,
            _test_passphrase=TEST_PASSPHRASE,
            pending_path=tmp_pb_path,
            fact_path=tmp_fb_path,
            sigs_path=tmp_sig_path
        )
        return ok, msg
    finally:
        if tmp_pb_path.exists():
            tmp_pb_path.unlink()
        if tmp_fb_path.exists():
            tmp_fb_path.unlink()
        if tmp_sig_path.exists():
            tmp_sig_path.unlink()


def main():
    case_files = sorted(TESTS_DIR.glob("case_*.md"))
    if not case_files:
        print("錯誤：找不到 tests/case_*.md 測試案例檔案", file=sys.stderr)
        sys.exit(1)

    print("=" * 65)
    print("run_cases.py 法規摘句與入庫門禁全維度測試案例執行報告")
    print("=" * 65)

    passed_tests = 0
    failed_tests = 0
    skipped_manual = 0

    for case_file in case_files:
        data = parse_case(case_file)
        name = case_file.name
        label = data.get("標記") or data.get("判定") or ""
        quote = data.get("摘句", "")
        url = data.get("網址", "")
        desc = data.get("說明", "")
        source = data.get("出處", "")
        snap_name = data.get("快照檔", "")
        title = data.get("標題", f"條目_{name}")
        verify_method = data.get("驗證方式", "標準法規核驗")

        if not label:
            print(f"[FAIL] {name} | 缺少標記，判定失敗！")
            failed_tests += 1
            continue

        # 人工審查案例（標題/推論跨層核對，非程式單元驗證，自動略過）
        if "人工審查" in verify_method:
            skipped_manual += 1
            print(f"[SKIP] {name}")
            print(f"       標記: {label} | 模式: 人工審查案例")
            print(f"       說明: {desc}（程式略過判定，供人工法務審查參考）")
            print("-" * 65)
            continue

        # 門禁簽章 sign 簽前審批測試模式 (case_024, case_025)
        if verify_method.startswith("門禁簽章sign"):
            sub_mode = verify_method.split("_")[-1]  # 手貼假條目, 全部合格
            ok_sign, sign_msg = run_sign_cmd_test_case(sub_mode, title, url, quote, source)
            if label == "【應退回】":
                if not ok_sign:
                    status = "PASS"
                    passed_tests += 1
                    detail = f"符合預期：sign 簽前驗證成功拒簽攔截（{sign_msg}）"
                else:
                    status = "FAIL"
                    failed_tests += 1
                    detail = f"不符預期：待簽章區有假條目，sign 竟然放行簽章了！"
            elif label == "【應通過】":
                if ok_sign:
                    status = "PASS"
                    passed_tests += 1
                    detail = f"符合預期：待簽章區條目全部合格，sign 簽章成功入庫（{sign_msg}）"
                else:
                    status = "FAIL"
                    failed_tests += 1
                    detail = f"不符預期：全部合規但 sign 簽章失敗（{sign_msg}）"
            else:
                status = "FAIL"
                failed_tests += 1
                detail = f"未知的標記格式: {label}"

            print(f"[{status}] {name}")
            print(f"       標記: {label} | 模式: 創辦人簽前審批核驗 ({sub_mode})")
            print(f"       判定: {detail}")
            print(f"       說明: {desc}")
            print("-" * 65)
            continue

        # 門禁簽章 check 測試模式 (case_021～case_023, case_026)
        if verify_method.startswith("門禁簽章check"):
            sub_mode = verify_method.split("_")[-1]  # 無簽章, 篡改, 有效
            ok_check, check_msg = run_signature_test_case(sub_mode, title, url, quote, source)
            if label == "【應退回】":
                if not ok_check:
                    status = "PASS"
                    passed_tests += 1
                    detail = f"符合預期：check 成功攔截退回（{check_msg}）"
                else:
                    status = "FAIL"
                    failed_tests += 1
                    detail = f"不符預期：應退回但 check 竟然通過了！"
            elif label == "【應通過】":
                if ok_check:
                    status = "PASS"
                    passed_tests += 1
                    detail = f"符合預期：創辦人簽章驗證通過，條目合法入庫"
                else:
                    status = "FAIL"
                    failed_tests += 1
                    detail = f"不符預期：應通過但 check 失敗（{check_msg}）"
            else:
                status = "FAIL"
                failed_tests += 1
                detail = f"未知的標記格式: {label}"

            print(f"[{status}] {name}")
            print(f"       標記: {label} | 模式: 創辦人密碼學簽章核驗 ({sub_mode})")
            print(f"       判定: {detail}")
            print(f"       說明: {desc}")
            print("-" * 65)
            continue

        # 門禁 check 測試模式 (B7, B9: case_015, case_017)
        if verify_method == "門禁check":
            passed_gate, gate_msg = run_gate_check_case(title, url, quote, source)
            if label == "【應退回】":
                if not passed_gate:
                    status = "PASS"
                    passed_tests += 1
                    detail = f"符合預期：check 重新物理核驗成功攔截（{gate_msg}）"
                else:
                    status = "FAIL"
                    failed_tests += 1
                    detail = "不符預期：check 竟然放行了手動假條目！"
            else:
                status = "FAIL"
                failed_tests += 1
                detail = "未配置之標記"

            print(f"[{status}] {name}")
            print(f"       標記: {label} | 模式: 門禁 check 物理核驗")
            print(f"       判定: {detail}")
            print(f"       說明: {desc}")
            print("-" * 65)
            continue

        # 門禁 add 測試模式 (case_010～case_014, case_016, case_018～case_020)
        if verify_method == "門禁add":
            ok_add, add_msg = run_gate_add_case(title, url, quote, source)
            if label == "【應通過】":
                if ok_add:
                    status = "PASS"
                    passed_tests += 1
                    detail = f"符合預期：門禁檢驗全部合規，成功寫入待簽章區（{add_msg}）"
                else:
                    status = "FAIL"
                    failed_tests += 1
                    detail = f"不符預期：應通過但門禁阻斷（{add_msg}）"
            elif label == "【應退回】":
                if not ok_add:
                    status = "PASS"
                    passed_tests += 1
                    detail = f"符合預期：門禁檢驗成功攔截退回（{add_msg}）"
                else:
                    status = "FAIL"
                    failed_tests += 1
                    detail = f"不符預期：應退回但門禁竟然放行寫入了！"
            else:
                status = "FAIL"
                failed_tests += 1
                detail = f"未知的標記格式：{label}"

            print(f"[{status}] {name}")
            print(f"       標記: {label} | 模式: 門禁 add 寫入驗證")
            print(f"       判定: {detail}")
            print(f"       說明: {desc}")
            print("-" * 65)
            continue

        # 原有標準摘句測試案例 (case_001～case_009)
        ok_item, item_msg = verify_item_subitem(source, quote)
        if not ok_item:
            if label == "【應退回】":
                status = "PASS"
                passed_tests += 1
                detail = f"符合預期：出處項款無法由摘句證明（{item_msg}），業務判定 FAIL，成功攔截退回"
            else:
                status = "FAIL"
                failed_tests += 1
                detail = f"不符預期：應通過但出處項款無法由摘句證明（{item_msg}）"

            print(f"[{status}] {name}")
            print(f"       標記: {label} | 檢驗: 項款核驗阻斷")
            print(f"       判定: {detail}")
            print(f"       說明: {desc}")
            print("-" * 65)
            continue

        snap_path = find_snapshot(url, snap_name)
        if not snap_path or not snap_path.exists():
            if label == "【應退回】":
                status = "PASS"
                passed_tests += 1
                detail = "符合預期：找不到對應條號快照，業務判定 FAIL，成功攔截退回"
            else:
                status = "FAIL"
                failed_tests += 1
                detail = "不符預期：應通過但找不到對應條號快照，業務判定 FAIL"
            
            print(f"[{status}] {name}")
            print(f"       標記: {label} | 快照: 無 (條號不符或檔案不存在)")
            print(f"       判定: {detail}")
            print(f"       說明: {desc}")
            print("-" * 65)
            continue

        snap_text = snap_path.read_text(encoding="utf-8")
        hit, msg = quote_in_page(quote, snap_text)

        if label == "【應通過】":
            if hit:
                status = "PASS"
                passed_tests += 1
                detail = "符合預期：現行法摘句真實命中快照 (驗證通過)"
            else:
                status = "FAIL"
                failed_tests += 1
                detail = f"不符預期：應通過但未命中快照！({msg})"
        elif label == "【應退回】":
            if not hit:
                status = "PASS"
                passed_tests += 1
                detail = "符合預期：舊版/錯誤摘句未出現在現行快照中，成功攔截退回"
            else:
                status = "FAIL"
                failed_tests += 1
                detail = "不符預期：應退回之摘句竟命中了快照！"
        else:
            status = "FAIL"
            failed_tests += 1
            detail = f"未知的標記格式：{label}"

        print(f"[{status}] {name}")
        print(f"       標記: {label} | 快照: {snap_path.name}")
        print(f"       判定: {detail}")
        print(f"       說明: {desc}")
        print("-" * 65)

    total = len(case_files)
    effective_total = total - skipped_manual
    print("=" * 65)
    print("測試案例彙總統計")
    print("=" * 65)
    print(f"總案例數: {total} 個 (包含 {skipped_manual} 個人工審查案例)")
    print(f"測試成功 (PASS): {passed_tests} 個")
    print(f"測試失敗 (FAIL): {failed_tests} 個")
    print(f"人工審查略過 (SKIP): {skipped_manual} 個")
    if effective_total > 0:
        print(f"通過率: {(passed_tests / effective_total) * 100:.1f}%")
    print("=" * 65)

    if failed_tests > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
