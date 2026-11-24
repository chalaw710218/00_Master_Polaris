"""
run_cases.py — 執行法規摘句測試案例檢驗 (支援 case_001～case_015)
讀取 scripts/tests/ 下的測試案例，使用 snapshots/ 快照調用 quote_in_page 或門禁邏輯進行判定
驗證「應通過」與「應退回」案例之判定結果是否 100% 符合預期標記
包含項款證明、法規名稱、快照物理核驗、黑名單阻斷與手動假條目攔截全維度測試
"""

import hashlib
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
import bionic_knowledge_gate


def verify_item_subitem(source: str, quote: str) -> (bool, str):
    """檢驗出處中宣告的項次/款次是否能被摘句本身所證明"""
    num_map = {
        "1": "一", "2": "二", "3": "三", "4": "四", "5": "五",
        "6": "六", "7": "七", "8": "八", "9": "九", "10": "十"
    }
    
    # 檢查「第N款」
    m_sub = re.search(r"第([0-9一二三四五六七八九十]+)款", source)
    if m_sub:
        k = m_sub.group(1)
        k_cn = num_map.get(k, k)
        pat = f"{k_cn}、|第{k_cn}款|第{k}款"
        if not re.search(pat, quote):
            return False, f"出處載明第{k}款，但摘句中無對應款次文字（如『{k_cn}、』）"

    # 檢查「第N項」
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

    # 優先依 URL sha1 比對
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
    """在沙盒臨時事實庫中執行門禁 add 邏輯測試"""
    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False, suffix=".md") as tmp:
        tmp.write("# 測試事實庫\n\n### 現有條目_包含電簽法第4條之標題\n出處：舊出處 https://example.com\n原文：「舊摘句」\n\n---\n")
        tmp_path = Path(tmp.name)

    orig_path = bionic_knowledge_gate.FACT_BANK_PATH
    try:
        bionic_knowledge_gate.FACT_BANK_PATH = tmp_path
        ok, msg = bionic_knowledge_gate.cmd_add(title, url, quote, source)
        return ok, msg
    finally:
        bionic_knowledge_gate.FACT_BANK_PATH = orig_path
        if tmp_path.exists():
            tmp_path.unlink()


def run_gate_check_case(fake_title: str, fake_url: str, fake_quote: str, fake_source: str) -> (bool, str):
    """在沙盒臨時事實庫中測試未經合法 add 寫入的假條目能否被 check 攔截"""
    with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False, suffix=".md") as tmp:
        # 手動寫入格式正確但無快照之假條目
        fake_content = f"# 測試事實庫\n\n### {fake_title}\n出處：{fake_source} {fake_url}\n原文：「{fake_quote}」\n\n---\n"
        tmp.write(fake_content)
        tmp_path = Path(tmp.name)

    orig_path = bionic_knowledge_gate.FACT_BANK_PATH
    try:
        bionic_knowledge_gate.FACT_BANK_PATH = tmp_path
        ok, count, illegals = bionic_knowledge_gate.cmd_check()
        if not ok:
            return False, f"check 成功抓出違規行: {illegals[0][1] if illegals else '物理核驗失敗'}"
        return True, "check 未能攔截手動假條目"
    finally:
        bionic_knowledge_gate.FACT_BANK_PATH = orig_path
        if tmp_path.exists():
            tmp_path.unlink()


def main():
    case_files = sorted(TESTS_DIR.glob("case_*.md"))
    if not case_files:
        print("錯誤：找不到 tests/case_*.md 測試案例檔案", file=sys.stderr)
        sys.exit(1)

    print("=" * 65)
    print("run_cases.py 法規摘句與入庫門禁測試案例執行報告")
    print("=" * 65)

    passed_tests = 0
    failed_tests = 0

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

        # 缺少標記直接判定失敗
        if not label:
            print(f"[FAIL] {name} | 缺少標記，判定失敗！")
            failed_tests += 1
            continue

        # 門禁 check 測試模式 (B7: case_015)
        if verify_method == "門禁check":
            passed_gate, gate_msg = run_gate_check_case(title, url, quote, source)
            # passed_gate == True 代表 check 沒攔住（通過了），passed_gate == False 代表 check 攔住了（退回）
            if label == "【應退回】":
                if not passed_gate:
                    status = "PASS"
                    passed_tests += 1
                    detail = f"符合預期：check 重新物理核驗成功攔截手動假條目（{gate_msg}）"
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

        # 門禁 add 測試模式 (B1~B6: case_010~case_014)
        if verify_method == "門禁add":
            ok_add, add_msg = run_gate_add_case(title, url, quote, source)
            if label == "【應通過】":
                if ok_add:
                    status = "PASS"
                    passed_tests += 1
                    detail = f"符合預期：門禁檢驗全部合規，成功寫入（{add_msg}）"
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
    print("=" * 65)
    print("測試案例彙總統計")
    print("=" * 65)
    print(f"總案例數: {total} 個")
    print(f"測試成功 (PASS): {passed_tests} 個")
    print(f"測試失敗 (FAIL): {failed_tests} 個")
    print(f"通過率: {(passed_tests / total) * 100:.1f}%")
    print("=" * 65)

    if failed_tests > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
