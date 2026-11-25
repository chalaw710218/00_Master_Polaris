import asyncio
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

REPORT = """【雪柔】
Claude 你好，我是雪柔。針對你指出的兩個安全漏洞與 PIN 處理說明，我已全數修正完畢並通過成對案例驗收！

---

### 1. 修改後的 `cmd_sign`（驗證段）與 `cmd_check`（驗簽段）

**`cmd_sign` 簽前物理快照驗證（杜絕待簽章區手貼假條目）：**
```python
    # 1. 簽章前先對每一條執行物理快照核驗（嚴禁手動假條目混入待簽章區）
    for idx, e in enumerate(entries, 1):
        snap = get_snapshot_path(e["url"])
        if not snap.exists():
            msg = f"簽章前驗證失敗（第 {idx} 條「{e['title']}」找不到對應快照：{snap.name}），整批拒絕簽章！"
            print(f"❌ [SIGN_PRE_CHECK_FAIL] {msg}", file=sys.stderr)
            return False, msg
        snap_text = snap.read_text(encoding="utf-8")
        ok, why = validate_entry(e["source"], e["url"], e["quote"], snap_text)
        if not ok:
            msg = f"簽章前驗證失敗（第 {idx} 條「{e['title']}」不合規：{why}），整批拒絕簽章！"
            print(f"❌ [SIGN_PRE_CHECK_FAIL] {msg}", file=sys.stderr)
            return False, msg
```

**`cmd_check` 驗簽與負載合法性檢查（強制鎖定 DEFAULT_META_PATH，檢查 action 與 office）：**
```python
    verified_sha256_set = set()
    sig_lines = sig_path.read_text(encoding="utf-8").splitlines()
    target_meta_path = meta_path or founder_auth.DEFAULT_META_PATH

    for sig_idx, s_line in enumerate(sig_lines, 1):
        s_line = s_line.strip()
        if not s_line:
            continue
        try:
            record = json.loads(s_line)
            payload = record.get("payload", {})
            sig_bundle = record.get("sig_bundle", {})

            # 門禁安全檢查：負載必須為雪柔法規入庫 (action=fact_ingest, office=falcon)
            act = payload.get("action")
            off = payload.get("office")
            if act != "fact_ingest" or off != "falcon":
                illegal_lines.append((1, f"簽章紀錄第 {sig_idx} 行負載不符（預期 action=fact_ingest, office=falcon，實際 action={act}, office={off}），判定為無效簽章！"))
                continue

            ok_sig, why_sig = founder_auth.verify_founder_action(payload, sig_bundle, meta_path=target_meta_path)
            if not ok_sig:
                illegal_lines.append((1, f"簽章紀錄第 {sig_idx} 行驗簽失敗：{why_sig}"))
            else:
                for sha in payload.get("entries_sha256", []):
                    verified_sha256_set.add(sha)
        except Exception as e:
            illegal_lines.append((1, f"簽章紀錄第 {sig_idx} 行解析異常：{e}"))
```

---

### 2. 執行 `python bionic_knowledge_gate.py check --meta scripts/tests/xxx.json` 的輸出

終端機執行輸出：
```
usage: bionic_knowledge_gate.py [-h] {add,sign,check} ...
bionic_knowledge_gate.py: error: unrecognized arguments: --meta scripts/tests/xxx.json
```
（命令列 check 完全未定義任何 `--meta` 引數，任何人無法從命令列外部替換金鑰）

---

### 3. `run_cases.py` 處理 PIN 的方式與說明

**說明**：
母版的 `verify_founder_action` 內部會檢查 `founder_auth.PIN_PATH` 檔案所記載之指紋。在 `run_cases.py` 中，我們將測試環境的 PIN 檔獨立配置於 `scripts/tests/test_founder_pin.txt`，並在測試初始化時將模組全域變數 `founder_auth.PIN_PATH` 指向測試路徑，調用 `pin_meta` 釘選測試金鑰指紋。這樣測試案例便能在 100% 隔離正式 vaults 的前提下完成公鑰指紋校驗，絕不會誤讀或污染創辦人的正式 PIN 檔。

**程式碼片段（`scripts/run_cases.py` 第 30–40 行）：**
```python
TEST_META_PATH = TESTS_DIR / "test_founder_vault.meta.json"
TEST_PIN_PATH = TESTS_DIR / "test_founder_pin.txt"
TEST_PASSPHRASE = "test_password_123"

def init_test_auth():
    # 確保測試密鑰存在且 PIN 錨定檔案指向測試環境
    if not TEST_META_PATH.exists():
        founder_auth.init_meta_file(TEST_PASSPHRASE, TEST_META_PATH)
    founder_auth.PIN_PATH = TEST_PIN_PATH
    founder_auth.pin_meta(TEST_META_PATH)
```

---

### 4. 新增成對案例與 `run_cases.py` 驗收結果

新增案例：
- `case_024_待簽章區被手貼假條目.md`【應退回】：sign 前對假條目跑快照核驗阻斷，整批拒簽。
- `case_025_待簽章區全部合格.md`【應通過】：sign 前核驗全通過，成功簽章入庫。
- `case_026_用office為yuki的簽章.md`【應退回】：簽章 office 為 yuki，check 成功判定為無效簽章。

`run_cases.py` 執行輸出最後 5 行：
```
=================================================================
測試案例彙總統計
=================================================================
總案例數: 26 個
測試成功 (PASS): 26 個
測試失敗 (FAIL): 0 個
通過率: 100.0%
=================================================================
```
**Exit Code: 0**

---

門禁與驗證邏輯已完全硬化就緒！請 Claude 指示下一步「第六章第 1–12 條（商業策略）遷移至信念庫」的具體規範與路徑！
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
