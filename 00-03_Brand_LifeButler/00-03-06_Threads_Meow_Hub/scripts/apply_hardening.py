import difflib
from pathlib import Path

p = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\scripts\bionic_knowledge_gate.py")
content = p.read_text(encoding="utf-8")

# 1. 修復出處不合格導致的 IndexError 崩潰
target_source = """        m_source = re.match(r'^\s*[-*]\s+\*\*出處\*\*：\s*(.+)$', raw_line)
        if m_source:
            if state == "EXPECT_SOURCE":
                source_val = m_source.group(1).strip()
                current_entry["source"] = source_val
                if not is_valid_source(source_val):
                    illegal_lines.append((line_idx, f"出處不合格（需帶網址或頁碼/章節數字）：{raw_line}"))
                else:
                    valid_entries.append(current_entry)
                state = "EXPECT_OPTIONAL_EVIDENCE"
                continue
            else:
                illegal_lines.append((line_idx, f"非預期位置出現出處行：{raw_line}"))
                state = "IDLE"
                continue"""

repl_source = """        m_source = re.match(r'^\s*[-*]\s+\*\*出處\*\*：\s*(.+)$', raw_line)
        if m_source:
            if state == "EXPECT_SOURCE":
                source_val = m_source.group(1).strip()
                current_entry["source"] = source_val
                if not is_valid_source(source_val):
                    illegal_lines.append((line_idx, f"出處不合格（需帶網址或頁碼/章節數字）：{raw_line}"))
                    state = "DISCARD_REMAINDER"
                else:
                    valid_entries.append(current_entry)
                    state = "EXPECT_OPTIONAL_EVIDENCE"
                continue
            else:
                illegal_lines.append((line_idx, f"非預期位置出現出處行：{raw_line}"))
                state = "IDLE"
                continue

        if state == "DISCARD_REMAINDER":
            m_url = re.match(r'^\s*[-*]\s+\*\*證據網址\*\*：\s*(.+)$', raw_line)
            m_quote = re.match(r'^\s*[-*]\s+\*\*原文摘句\*\*：\s*(.+)$', raw_line)
            if m_url or m_quote:
                continue
            state = "IDLE" """

# 2. 修復免簽模式下 check 的連網逐字檢驗
target_check = """    if not REQUIRE_SIGNATURE:
        print("ℹ️ 免簽模式 (REQUIRE_SIGNATURE = False) 生效：跳過創辦人簽章驗證。")
        print(f"✅ 全數條目符合白名單與事實格式。Exit Code 0。\\n")
        return True"""

repl_check = """    if not REQUIRE_SIGNATURE:
        print("ℹ️ 免簽模式 (REQUIRE_SIGNATURE = False) 生效：跳過簽章比對，啟動全域連網逐字驗收 (quote_in_page)...")
        failed_checks = []
        for idx, entry in enumerate(valid_entries, 1):
            title = entry.get("title", f"條目 {idx}")
            url = entry.get("url")
            quote = entry.get("quote")
            print(f"  [{idx:02d}/{len(valid_entries):02d}] 正在連網校驗：{title} ...", end=" ")
            if not url or not quote:
                print("❌ 缺少證據網址或原文摘句")
                failed_checks.append((title, "缺少 --url 或 --quote，無法證明逐字真實性"))
                continue
            try:
                page_text = fetch_page_text(url)
                ok, why = quote_in_page(quote, page_text)
                if not ok:
                    print(f"❌ 逐字比對失敗")
                    failed_checks.append((title, f"逐字驗證未通過：{why}"))
                    continue
                print("✅ 逐字驗證 PASS")
            except Exception as ex:
                print(f"❌ 連網抓取失敗")
                failed_checks.append((title, f"無法連線或抓取網頁（{ex}）"))

        if failed_checks:
            print("\\n❌ [安燈阻斷] 免簽模式發現未經連網驗證（或摘句不符）的條目！")
            for t, why in failed_checks:
                print(f"  👉 「{t}」: {why}")
            print("\\nExit Code 1。\\n")
            sys.exit(1)

        print(f"\\n✅ 全數 {len(valid_entries)} 條合格條目皆通過線上逐字物理驗證！Exit Code 0。\\n")
        return True"""

new_content = content
for t, r in [(target_source, repl_source), (target_check, repl_check)]:
    if t not in new_content:
        raise ValueError("Target not found")
    new_content = new_content.replace(t, r, 1)

p.write_text(new_content, encoding="utf-8")

diff = difflib.unified_diff(
    content.splitlines(keepends=True),
    new_content.splitlines(keepends=True),
    fromfile="kage/bionic_knowledge_gate_prev.py",
    tofile="kage/bionic_knowledge_gate_hardened.py"
)
diff_txt = "".join(diff)
print("Updated successfully. Diff:")
print(diff_txt)
Path("scripts/gate_hardened_diff.txt").write_text(diff_txt, encoding="utf-8")
