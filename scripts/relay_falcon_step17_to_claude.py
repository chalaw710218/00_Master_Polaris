import asyncio
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

REPORT = """【雪柔】
Claude 你好，我是雪柔。創辦人（品碩）指示我向你回報「入庫門禁接上創辦人簽章」的改動與驗收結果！

### 1. `sign` 與 `check` 核心改動代碼

**`cmd_sign`（創辦人親自審批並簽章）：**
```python
def cmd_sign(meta_path: Path | None = None, _test_passphrase: str | None = None) -> (bool, str):
    init_buffers()
    if not PENDING_BANK_PATH.exists():
        return False, "待簽章區不存在"
    pending_content = PENDING_BANK_PATH.read_text(encoding="utf-8")
    entries = parse_entries_from_markdown(pending_content)
    if not entries:
        return False, "待簽章區目前無待簽章條目"

    # 1. 反盲簽展示
    print("=" * 60)
    print(f"反盲簽展示：待簽章條目清單（共 {len(entries)} 筆）")
    for idx, e in enumerate(entries, 1):
        print(f"[{idx}] {e['title']} | 出處: {e['source']} {e['url']}")
        print(f"    原文: {e['quote']}")
        print(f"    SHA256: {e['sha256']}")
    print("=" * 60)

    # 2. 構造 payload 並調用 founder_auth.sign_founder_action
    payload = {
        "action": "fact_ingest",
        "office": "falcon",
        "entries_sha256": [e["sha256"] for e in entries]
    }
    sig_bundle = founder_auth.sign_founder_action(
        payload, meta_path=meta_path, _test_passphrase=_test_passphrase,
        prompt_label="創辦人（品碩）授權口令："
    )

    # 3. 追加進事實庫、存入 .sigs.jsonl、清空待簽章區
    fact_append_lines = [f"\\n### {e['title']}\\n出處：{e['source']} {e['url']}\\n原文：「{e['quote']}」\\n\\n---\\n" for e in entries]
    with open(FACT_BANK_PATH, "a", encoding="utf-8") as f:
        f.write("".join(fact_append_lines))
    with open(SIGS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps({"payload": payload, "sig_bundle": sig_bundle}, ensure_ascii=False) + "\\n")
    PENDING_BANK_PATH.write_text(header_pending, encoding="utf-8")
    return True, f"成功完成 {len(entries)} 筆條目之創辦人簽章入庫！"
```

**`cmd_check` 簽章驗證核心：**
```python
    # 2. 創辦人密碼學簽章驗證
    if total_entries == 0:
        return (len(illegal_lines) == 0), total_entries, illegal_lines

    if not sig_path.exists():
        illegal_lines.append((1, f"事實庫包含 {total_entries} 筆條目，但找不到創辦人簽章檔案 ({sig_path.name})，全庫未授權！"))
        return False, total_entries, illegal_lines

    verified_sha256_set = set()
    sig_lines = sig_path.read_text(encoding="utf-8").splitlines()
    for sig_idx, s_line in enumerate(sig_lines, 1):
        record = json.loads(s_line)
        payload, sig_bundle = record.get("payload", {}), record.get("sig_bundle", {})
        ok_sig, why_sig = founder_auth.verify_founder_action(payload, sig_bundle, meta_path=meta_path)
        if not ok_sig:
            illegal_lines.append((1, f"簽章紀錄第 {sig_idx} 行驗簽失敗：{why_sig}"))
        else:
            for sha in payload.get("entries_sha256", []):
                verified_sha256_set.add(sha)

    for item in parsed_entries:
        if item["sha256"] not in verified_sha256_set:
            illegal_lines.append((item["line_no"], f"條目未經創辦人有效簽章授權入庫（標題: {item['title']}，SHA256: {item['sha256'][:16]}...）"))

    return (len(illegal_lines) == 0), total_entries, illegal_lines
```

---

### 2. 待簽章區條目數（由程式計算）
執行 `parse_entries_from_markdown(PENDING_BANK_PATH.read_text())` 精確計算：
**待簽章區條目數: 29 條**
（原事實庫 29 條條目已全數安全移回 `00_待簽章區.md`，目前 `01_事實庫.md` 清空重置為只有檔頭）

---

### 3. `bionic_knowledge_gate.py check` 執行結果與最後 5 行
```
============================================================
bionic_knowledge_gate check 白名單、物理核驗與創辦人簽章報告
============================================================
事實庫路徑: C:\\Users\\lenovo\\我的雲端硬碟\\00_Master_Polaris\\00-00_Gamification_Engine\\Office_of_the_CIO_Falcon\\01_Cognitive_Log\\01_事實庫.md
合格條目總數: 0 條（由程式計算）
違規行總數: 0 行
============================================================
✅ 白名單、物理核驗與創辦人簽章全部驗證通過！
Exit Code: 0
```
**Exit Code: 0**

---

### 4. `run_cases.py` 執行結果與最後 5 行
新增了成對測試案例：
- `case_021_事實庫條目無簽章.md`（應退回）
- `case_022_簽章後條目被改一個字.md`（應退回）
- `case_023_簽章有效的條目.md`（應通過）
且測試密鑰完全隔離在 `scripts/tests/`，禁止使用正式 vaults。

執行輸出最後 5 行：
```
=================================================================
測試案例彙總統計
=================================================================
總案例數: 23 個
測試成功 (PASS): 23 個
測試失敗 (FAIL): 0 個
通過率: 100.0%
=================================================================
```
**Exit Code: 0**

---

我們已嚴格落實創辦人最新決策（退出 TWQR，專注生活管家法規；事實庫入庫必由創辦人親自簽章）。
請 Claude 指示下一步工作！
"""

def main():
    pair_key = "c06c2e4f-8afc-4b48-8bd9-11ddbcdeb1e5"
    i, p = claude_relay.find_pair(pair_key)
    tab = claude_relay.find_tab(p["claude_href"])
    print(f"正在傳話至 Claude 分頁 [{tab['title']}]...")
    with claude_relay.TabLock(tab["id"]):
        reply = asyncio.run(claude_relay.relay(tab["webSocketDebuggerUrl"], REPORT, 600))
    print("=" * 60)
    print("Claude 已回覆：")
    print("=" * 60)
    print(reply)

if __name__ == "__main__":
    main()
