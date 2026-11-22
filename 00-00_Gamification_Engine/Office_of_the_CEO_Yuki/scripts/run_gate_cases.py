"""
run_gate_cases.py
執行長雪事實庫門禁與創辦人簽章全域安全審計測試套件

測試矩陣：
1. 原生歷史測試案例 (case_001 ~ case_006):
   - case_001: 省略號跳過數字 -> 應退回
   - case_002: 省略號但每段夠長 -> 應通過
   - case_003: 真摘句 (Attention is All You Need) -> 應通過
   - case_004: 編造數字 (45.3 BLEU) -> 應退回
   - case_005: 頁碼數字分散 -> 應退回
   - case_006: 多餘空白 -> 應通過

2. 漏洞防護新案例 (case_010):
   - case_010: 真簽章 + entry_hashes 多塞一條 -> check 應退回

3. 創辦人簽章系列測試 (sig_001 ~ sig_009):
   - sig_001: 乾淨條目（合法網址出處）白名單語法測試
   - sig_002: 合法頁碼與章節出處測試 (p. 315 / Chapter)
   - sig_003: 假出處黑名單退回測試
   - sig_004: 混入游離非法行（散文字句）退回測試
   - sig_005: 缺少出處行或核心事實行結構中斷測試
   - sig_006: 舊 add 指令廢止測試
   - sig_007: 事實庫多一條未簽章條目 -> check 退回測試
   - sig_008: 簽過之後內容改動一個字 -> check 退回測試
   - sig_009: 正常簽過的一批條目 -> check 驗收通過測試
"""

import sys
import os
import re
import json
import shutil
import tempfile
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

WORKSPACE_DIR = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris")
MASTER_BIONIC_CORE_DIR = WORKSPACE_DIR / ".agents" / "skills" / "bionic-learning-system" / "bionic_core"
if str(MASTER_BIONIC_CORE_DIR) not in sys.path:
    sys.path.append(str(MASTER_BIONIC_CORE_DIR))

import founder_auth
import bionic_knowledge_gate as gate

TESTS_DIR = WORKSPACE_DIR / "scripts" / "tests"


def run_original_case(filepath: Path):
    content = filepath.read_text(encoding="utf-8")
    m_decision = re.search(r'判定：【(應通過|應退回)】', content)
    m_title = re.search(r'標題：\s*(.+)', content)
    m_url = re.search(r'網址：\s*(.+)', content)
    m_source = re.search(r'出處：\s*(.+)', content)
    m_quote = re.search(r'摘句：\s*(.+)', content)
    m_fact = re.search(r'核心事實：\s*(.+)', content)
    m_dup_check = re.search(r'檢查網址重複：\s*【(是|否)】', content)
    
    assert m_decision, f"無法解析判定：{filepath.name}"
    expected_pass = (m_decision.group(1) == "應通過")
    title = m_title.group(1).strip() if m_title else f"測試_{filepath.stem}"
    url = m_url.group(1).strip() if m_url else None
    source = m_source.group(1).strip() if m_source else None
    quote = m_quote.group(1).strip() if m_quote else None
    fact = m_fact.group(1).strip() if m_fact else "測試核心事實"

    should_check_dup = False
    if m_dup_check:
        should_check_dup = (m_dup_check.group(1) == "是")
    elif "網址重複" in filepath.name or "網址未重複" in filepath.name:
        should_check_dup = True

    existing_urls = gate.get_vault_urls() if should_check_dup else None

    try:
        gate.validate_entry(
            title=title,
            fact=fact,
            source=source,
            url=url,
            quote=quote,
            existing_urls=existing_urls,
            check_duplicates=should_check_dup
        )
        passed = True
    except Exception as ex:
        passed = False

    if expected_pass:
        assert passed, f"案例 {filepath.name} 預期應通過，但遭到退回！"
        print(f"   ✅ {filepath.name} 正確放行 (應通過)")
    else:
        assert not passed, f"案例 {filepath.name} 預期應退回，但竟然被放行！"
        print(f"   ✅ {filepath.name} 成功攔截 (應退回)")


def run_all_cases():
    print("=" * 70)
    print("🚀 開始執行雪事實庫門禁全域安全審計測試 (case_001~006, 010~016, sig_001~009)")
    print("=" * 70)

    temp_sandbox = Path(tempfile.mkdtemp(prefix="yuki_gate_test_"))
    test_meta_path = temp_sandbox / "test_founder_meta.json"
    test_pin_path = temp_sandbox / "test_pin.txt"
    test_passphrase = "test_vault_passphrase_yuki_gate_safe"

    original_pin_path = founder_auth.PIN_PATH
    founder_auth.PIN_PATH = test_pin_path

    try:
        # 初始化測試用金鑰
        meta_dict = founder_auth.build_meta_dict(test_passphrase, iters=1000)
        test_meta_path.write_text(json.dumps(meta_dict, indent=2), encoding="utf-8")
        test_pin_path.write_text(meta_dict["fingerprint"] + "\n", encoding="utf-8")
        print(f"🔑 測試金鑰已建立：{test_meta_path} (指紋: {meta_dict['fingerprint']})\n")

        # -------------------------------------------------------------
        # 一、 執行 scripts/tests/ 原始與擴充測試案例 (case_001 ~ case_006, case_011 ~ case_016)
        # -------------------------------------------------------------
        print("▶️ [一、 執行 scripts/tests/ 真實案例 case_001 ~ 006, case_011 ~ 016]")
        orig_cases = [
            "case_001_省略號跳過數字.md",
            "case_002_省略號但每段夠長.md",
            "case_003_真摘句_應通過.md",
            "case_004_編造數字_應退回.md",
            "case_005_頁碼數字分散_應退回.md",
            "case_006_多餘空白_應通過.md",
            "case_011_核心事實多出數字_應退回.md",
            "case_012_核心事實數字都在摘句_應通過.md",
            "case_013_網址重複_應退回.md",
            "case_014_網址未重複_應通過.md",
            "case_015_標題論文名不符_應退回.md",
            "case_016_標題論文名相符_應通過.md",
        ]
        for cf in orig_cases:
            c_path = TESTS_DIR / cf
            assert c_path.exists(), f"找不到案例檔案：{c_path}"
            run_original_case(c_path)
        print("   🎉 case_001 ~ 006, case_011 ~ 016 全數通過！\n")

        # -------------------------------------------------------------
        # 二、 創辦人簽章安全測試 (sig_001 ~ sig_006)
        # -------------------------------------------------------------
        print("▶️ [sig_001] 乾淨條目（合法網址出處）白名單語法測試")
        assert gate.is_valid_source("https://example.com/test")
        print("   ✅ sig_001 通過\n")

        print("▶️ [sig_002] 合法頁碼與章節出處測試 (p. 315 / Chapter)")
        valid_citations = [
            "W. Edwards Deming, Out of the Crisis (1986), Chapter 11, p. 315",
            "Western Electric Handbook (1956), pp. 25-28",
            "品質管制手冊，第 45 頁",
            "統計學導論，第十章「變異分析」",
            "Montgomery, SQC, Chapter 8",
        ]
        for vc in valid_citations:
            assert gate.is_valid_source(vc), f"合規出處誤判：{vc}"
        print("   ✅ sig_002 通過\n")

        print("▶️ [sig_003] 假出處黑名單退回測試")
        fake_citations = ["無", "N/A", "待補", "網路", "-", "網路 p.", "p.", "pp.", "Chapter", "第章", "網路 Chapter"]
        for fc in fake_citations:
            assert not gate.is_valid_source(fc), f"假出處未被攔截：{fc}"
        print("   ✅ sig_003 通過\n")

        print("▶️ [sig_004] 混入游離非法行（散文字句）退回測試")
        c4_file = temp_sandbox / "sig_004.md"
        c4_file.write_text(
            "# 事實庫\n\n---\n\n這是一行不在白名單內的隨意筆記。\n\n1. **測試條目**：\n   - **核心事實**：內容\n   - **出處**：https://example.com\n",
            encoding="utf-8"
        )
        try:
            gate.check_file_whitelist(c4_file, signatures_path=temp_sandbox / "empty.jsonl", meta_path=test_meta_path)
            assert False, "漏洞：混入游離非法行竟然通過了白名單檢驗！"
        except SystemExit as se:
            assert se.code == 1
            print("   ✅ sig_004 成功攔截游離非法行 (Exit Code 1)\n")

        print("▶️ [sig_005] 缺少出處行或核心事實行結構中斷測試")
        c5_file = temp_sandbox / "sig_005.md"
        c5_file.write_text(
            "# 事實庫\n\n---\n\n1. **測試條目**：\n   - **核心事實**：內容直接結束沒有出處\n",
            encoding="utf-8"
        )
        try:
            gate.check_file_whitelist(c5_file, signatures_path=temp_sandbox / "empty.jsonl", meta_path=test_meta_path)
            assert False, "漏洞：缺少出處行竟然通過了白名單檢驗！"
        except SystemExit as se:
            assert se.code == 1
            print("   ✅ sig_005 成功攔截殘缺條目 (Exit Code 1)\n")

        print("▶️ [sig_006] 舊 add 指令廢止測試")
        try:
            sys.argv = ["bionic_knowledge_gate.py", "add", "--title", "T", "--fact", "F", "--source", "https://x.com"]
            try:
                gate.main()
                assert False, "漏洞：add 指令竟然沒有被阻斷！"
            except SystemExit as se:
                assert se.code == 1
                print("   ✅ sig_006 成功阻斷舊 add 指令 (Exit Code 1)\n")
        finally:
            sys.argv = ["bionic_knowledge_gate.py"]

        # -------------------------------------------------------------
        # 準備簽章基礎環境
        # -------------------------------------------------------------
        test_entries = [
            {
                "title": "測試條目 A：分散式神經網絡收斂",
                "fact": "神經網絡在非同步環境下達到 95% 收斂率。",
                "source": "https://arxiv.org/abs/test.001",
                "url": "https://arxiv.org/abs/test.001",
                "quote": "Our network achieves a 95% convergence rate in asynchronous environments."
            },
            {
                "title": "測試條目 B：反脆弱機制設計",
                "fact": "系統在注入混沌擾動後延遲降低 15%。",
                "source": "https://arxiv.org/abs/test.002",
                "url": "https://arxiv.org/abs/test.002",
                "quote": "The system reduces latency by 15% after introducing chaotic perturbation."
            }
        ]
        for e in test_entries:
            e["entry_hash"] = gate.compute_entry_hash(e["title"], e["fact"], e["source"], e["url"], e["quote"])
        
        test_batch_sha = gate.compute_batch_sha256(test_entries)
        to_sign_pack = {
            "office": "yuki",
            "action": "ingest_batch",
            "count": len(test_entries),
            "batch_sha256": test_batch_sha,
            "entry_hashes": [e["entry_hash"] for e in test_entries],
            "entries": test_entries,
            "is_baseline": True  # 設為 True 避免測試時對假網址發動連網
        }
        
        test_to_sign_path = temp_sandbox / "_test_to_sign.json"
        test_to_sign_path.write_text(json.dumps(to_sign_pack, indent=2), encoding="utf-8")

        test_sig_log = temp_sandbox / "test_signatures.jsonl"
        test_vault = temp_sandbox / "test_experiences.md"

        # 建立事實庫初始結構並寫入這兩條
        init_content = (
            "# 測試事實庫\n\n---\n\n"
            f"1. **{test_entries[0]['title']}**：\n   - **核心事實**：{test_entries[0]['fact']}\n   - **出處**：{test_entries[0]['source']}\n   - **證據網址**：{test_entries[0]['url']}\n   - **原文摘句**：{test_entries[0]['quote']}\n\n"
            f"2. **{test_entries[1]['title']}**：\n   - **核心事實**：{test_entries[1]['fact']}\n   - **出處**：{test_entries[1]['source']}\n   - **證據網址**：{test_entries[1]['url']}\n   - **原文摘句**：{test_entries[1]['quote']}\n"
        )
        test_vault.write_text(init_content, encoding="utf-8")

        # 執行簽章
        gate.sign_cmd(
            to_sign_path=test_to_sign_path,
            signatures_path=test_sig_log,
            vault_path=test_vault,
            meta_path=test_meta_path,
            _test_passphrase=test_passphrase
        )
        assert test_vault.exists()
        assert test_sig_log.exists()

        # -------------------------------------------------------------
        # 三、 漏洞防護新測試：case_010（真簽章 + entry_hashes 多塞一條）
        # -------------------------------------------------------------
        print("▶️ [case_010] 漏洞防護測試：真簽章 + entry_hashes 多塞一條 -> check 應退回")
        c10_sig_log = temp_sandbox / "case_010_signatures.jsonl"
        c10_vault = temp_sandbox / "case_010_vault.md"
        c10_vault.write_text(test_vault.read_text(encoding="utf-8"), encoding="utf-8")
        
        # 讀出剛剛正常的簽章記錄，在 entry_hashes 裡偷偷塞一筆偽造的 hash
        sig_lines = test_sig_log.read_text(encoding="utf-8").strip().splitlines()
        rec_tampered = json.loads(sig_lines[-1])
        fake_injected_hash = "000000000000000000000000000000000000000000000000000000000000dead"
        rec_tampered["entry_hashes"].append(fake_injected_hash)
        c10_sig_log.write_text(json.dumps(rec_tampered) + "\n", encoding="utf-8")

        # 在事實庫中也塞入對應這條偽造 hash 的條目
        fake_entry_block = (
            "\n\n3. **偽造注入條目**：\n"
            "   - **核心事實**：利用多塞 hash 漏洞試圖瞞天過海的偽造條目。\n"
            "   - **出處**：https://example.com/exploit\n"
            "   - **證據網址**：https://example.com/exploit\n"
            "   - **原文摘句**：This is an exploit entry that should be rejected by signature integrity check.\n"
        )
        with open(c10_vault, "a", encoding="utf-8") as f:
            f.write(fake_entry_block)

        try:
            gate.check_file_whitelist(c10_vault, signatures_path=c10_sig_log, meta_path=test_meta_path)
            assert False, "重大安全漏洞：真簽章但 entry_hashes 多塞一條，check 竟然放行！"
        except SystemExit as se:
            assert se.code == 1
            print("   ✅ case_010 成功阻斷多塞 hash 漏洞！整筆作廢攔截 (Exit Code 1)\n")

        # -------------------------------------------------------------
        # 四、 簽章進階測試 (sig_007 ~ sig_009)
        # -------------------------------------------------------------
        print("▶️ [sig_007] 事實庫多一條未簽章條目 -> check 退回測試")
        c7_vault = temp_sandbox / "sig_007_vault.md"
        c7_vault.write_text(test_vault.read_text(encoding="utf-8"), encoding="utf-8")
        unsigned_block = (
            "\n\n3. **未經簽章之私自注入條目**：\n"
            "   - **核心事實**：未經創辦人認證的私人筆記。\n"
            "   - **出處**：https://example.com/unauthorized\n"
            "   - **證據網址**：https://example.com/unauthorized\n"
            "   - **原文摘句**：This is an unauthorized entry inserted without founder signature.\n"
        )
        with open(c7_vault, "a", encoding="utf-8") as f:
            f.write(unsigned_block)

        try:
            gate.check_file_whitelist(c7_vault, signatures_path=test_sig_log, meta_path=test_meta_path)
            assert False, "漏洞：事實庫多了一條未簽章條目，check 竟然放行！"
        except SystemExit as se:
            assert se.code == 1
            print("   ✅ sig_007 成功阻斷未簽條目入庫 (Exit Code 1)\n")

        print("▶️ [sig_008] 簽過之後內容改動一個字 -> check 退回測試")
        c8_vault = temp_sandbox / "sig_008_vault.md"
        c8_text = test_vault.read_text(encoding="utf-8")
        c8_text_tampered = c8_text.replace("95%", "99%")
        c8_vault.write_text(c8_text_tampered, encoding="utf-8")

        try:
            gate.check_file_whitelist(c8_vault, signatures_path=test_sig_log, meta_path=test_meta_path)
            assert False, "漏洞：簽過之後改動內容，check 竟然放行！"
        except SystemExit as se:
            assert se.code == 1
            print("   ✅ sig_008 成功阻斷篡改內容 (Exit Code 1)\n")

        print("▶️ [sig_009] 正常簽過的一批 -> check 驗收通過測試")
        res = gate.check_file_whitelist(test_vault, signatures_path=test_sig_log, meta_path=test_meta_path)
        assert res is True
        print("   ✅ sig_009 成功驗簽通過 (Exit Code 0)\n")

        print("=" * 70)
        print("🎉 恭喜！case_001～006、case_010、case_011、case_012、sig_001～009 全數測試通過！Exit Code 0。")
        print("=" * 70)
        sys.exit(0)

    finally:
        founder_auth.PIN_PATH = original_pin_path
        shutil.rmtree(temp_sandbox, ignore_errors=True)

if __name__ == "__main__":
    run_all_cases()
