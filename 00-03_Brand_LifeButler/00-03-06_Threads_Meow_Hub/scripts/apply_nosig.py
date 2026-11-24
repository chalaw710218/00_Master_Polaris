import difflib
from pathlib import Path

p = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\scripts\bionic_knowledge_gate.py")
old_content = p.read_text(encoding="utf-8")

# 1. 增加 REQUIRE_SIGNATURE = False
target1 = 'DEFAULT_SIGNATURES_PATH = Path(__file__).resolve().parent.parent / "logs" / "ingest_signatures.jsonl"'
repl1 = target1 + '\n\nREQUIRE_SIGNATURE = False  # 生活管家影專用：免簽模式開關'

# 2. prepare_cmd 基準批次連網驗證與免簽直接入庫
target2 = """    if is_baseline:
        print(f"模式：現有事實庫基準批次預備 -> {vault_path}")
        entries = parse_experiences_markdown(vault_path)
        if not entries:
            print("❌ 事實庫無現有條目，無法建立基準批次")
            sys.exit(1)
        batch_sha = compute_batch_sha256(entries)
        pack = {
            "office": "kage",
            "action": "ingest_batch",
            "is_baseline": True,
            "created_at": datetime.now().isoformat(),
            "count": len(entries),
            "batch_sha256": batch_sha,
            "entry_hashes": [e["entry_hash"] for e in entries],
            "entries": entries
        }
        to_sign_path.parent.mkdir(parents=True, exist_ok=True)
        to_sign_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ 成功預備基準批次待簽檔：{to_sign_path}")
        print(f"   總條目數：{len(entries)} 條，批次雜湊：{batch_sha[:16]}...")
        return len(entries), 0, []"""

repl2 = """    if is_baseline:
        print(f"模式：現有事實庫基準批次預備 -> {vault_path}")
        entries = parse_experiences_markdown(vault_path)
        if not entries:
            print("❌ 事實庫無現有條目，無法建立基準批次")
            sys.exit(1)

        if not REQUIRE_SIGNATURE:
            print("🔍 免簽模式：對基準批次每條執行連網逐字驗證 (quote_in_page)...")
            for idx, e in enumerate(entries, 1):
                print(f"[{idx:02d}/{len(entries):02d}] 正在驗證：{e['title']} ...", end=" ")
                if not e.get("url") or not e.get("quote"):
                    print("❌ 缺少網址或摘句，退回！")
                    sys.exit(1)
                try:
                    page_text = fetch_page_text(e["url"])
                    ok, why = quote_in_page(e["quote"], page_text)
                    if not ok:
                        print(f"❌ 退回：{why}")
                        sys.exit(1)
                    print("✅ 逐字驗證 PASS")
                except Exception as ex:
                    print(f"❌ 連網錯誤：{ex}")
                    sys.exit(1)
            print(f"✅ 基準批次共 {len(entries)} 條全部連網逐字驗證通過！")
            return len(entries), 0, []

        batch_sha = compute_batch_sha256(entries)
        pack = {
            "office": "kage",
            "action": "ingest_batch",
            "is_baseline": True,
            "created_at": datetime.now().isoformat(),
            "count": len(entries),
            "batch_sha256": batch_sha,
            "entry_hashes": [e["entry_hash"] for e in entries],
            "entries": entries
        }
        to_sign_path.parent.mkdir(parents=True, exist_ok=True)
        to_sign_path.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ 成功預備基準批次待簽檔：{to_sign_path}")
        print(f"   總條目數：{len(entries)} 條，批次雜湊：{batch_sha[:16]}...")
        return len(entries), 0, []"""

# 3. prepare_cmd 非 baseline 時免簽直接寫入事實庫
target3 = """    if passed_entries:
        batch_sha = compute_batch_sha256(passed_entries)"""

repl3 = """    if passed_entries:
        if not REQUIRE_SIGNATURE:
            if not vault_path.exists():
                vault_path.parent.mkdir(parents=True, exist_ok=True)
                vault_path.write_text("# 生活管家影之核心事實與客觀證據庫 (Experiences & Evidence)\\n\\n---\\n", encoding="utf-8")
            
            vault_content = vault_path.read_text(encoding="utf-8")
            existing_nums = [int(m) for m in re.findall(r'^\\s*(\\d+)\\.\\s+\\*\\*', vault_content, re.MULTILINE)]
            next_idx = (max(existing_nums) + 1) if existing_nums else 1
            
            append_blocks = []
            for e in passed_entries:
                block = f"\\n{next_idx}. **{e['title']}**：\\n"
                block += f"  - **核心事實**：{e['fact']}\\n"
                block += f"  - **出處**：{e['source']}\\n"
                if e.get("url"):
                    block += f"  - **證據網址**：{e['url']}\\n"
                if e.get("quote"):
                    block += f"  - **原文摘句**：{e['quote']}\\n"
                append_blocks.append(block)
                next_idx += 1
            
            with open(vault_path, "a", encoding="utf-8") as f:
                f.write("".join(append_blocks))
            print(f"\\n✅ 免簽模式：已將 {len(passed_entries)} 條通過條目直接寫入事實庫：{vault_path}")
            return len(passed_entries), len(rejected), rejected

        batch_sha = compute_batch_sha256(passed_entries)"""

# 4. sign_cmd 免簽模式跳過
target4 = """def sign_cmd(to_sign_path: Path = DEFAULT_TO_SIGN_PATH, signatures_path: Path = DEFAULT_SIGNATURES_PATH, vault_path: Path = DEFAULT_EXPERIENCES_PATH, meta_path: Path = None, _test_passphrase: str = None) -> bool:
    print(f"=== 開始執行創辦人簽章與入庫 (sign) ===")"""

repl4 = """def sign_cmd(to_sign_path: Path = DEFAULT_TO_SIGN_PATH, signatures_path: Path = DEFAULT_SIGNATURES_PATH, vault_path: Path = DEFAULT_EXPERIENCES_PATH, meta_path: Path = None, _test_passphrase: str = None) -> bool:
    print(f"=== 開始執行創辦人簽章與入庫 (sign) ===")
    if not REQUIRE_SIGNATURE:
        print("ℹ️ 目前為免簽模式 (REQUIRE_SIGNATURE = False)，無需執行 sign 指令。Exit Code 0。")
        return True"""

# 5. check_file_whitelist 免簽模式跳過簽章比對
target5 = """    print(f"✅ 格式白名單檢驗通過，共 {len(valid_entries)} 條合格結構。")

    # === 創辦人簽章驗簽檢核 (Signature Verification) ===
    print("正在檢核創辦人主權簽章 (ingest_signatures.jsonl) ...")"""

repl5 = """    print(f"✅ 格式白名單檢驗通過，共 {len(valid_entries)} 條合格結構。")

    if not REQUIRE_SIGNATURE:
        print("ℹ️ 免簽模式 (REQUIRE_SIGNATURE = False) 生效：跳過創辦人簽章驗證。")
        print(f"✅ 全數條目符合白名單與事實格式。Exit Code 0。\\n")
        return True

    # === 創辦人簽章驗簽檢核 (Signature Verification) ===
    print("正在檢核創辦人主權簽章 (ingest_signatures.jsonl) ...")"""

new_content = old_content
for t, r in [(target1, repl1), (target2, repl2), (target3, repl3), (target4, repl4), (target5, repl5)]:
    if t not in new_content:
        raise ValueError(f"Target not found: {t[:60]}...")
    new_content = new_content.replace(t, r, 1)

p.write_text(new_content, encoding="utf-8")
print("Updated successfully. Generating diff...")

diff = difflib.unified_diff(
    old_content.splitlines(keepends=True),
    new_content.splitlines(keepends=True),
    fromfile="kage/bionic_knowledge_gate_v4.1.py",
    tofile="kage/bionic_knowledge_gate_nosig.py"
)
diff_txt = "".join(diff)
Path("scripts/gate_nosig_diff.txt").write_text(diff_txt, encoding="utf-8")
print(diff_txt)
