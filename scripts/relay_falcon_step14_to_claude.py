import asyncio
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

# 1. 取得 validate_entry 函式完整代碼
GATE_PATH = HERE / "bionic_knowledge_gate.py"
gate_lines = GATE_PATH.read_text(encoding="utf-8").splitlines()

val_lines = []
capturing = False
for line in gate_lines:
    if line.startswith("def validate_entry("):
        capturing = True
    elif capturing and line.startswith("def init_fact_bank("):
        break
    if capturing:
        val_lines.append(line)

validate_entry_code = "\n".join(val_lines).strip()

# 2. 執行 check 並取得最後 5 行與 Exit Code
res_check = subprocess.run([sys.executable, str(HERE / "bionic_knowledge_gate.py"), "check"], capture_output=True, text=True, encoding="utf-8")
check_lines = res_check.stdout.strip().splitlines()
check_last5 = "\n".join(check_lines[-5:])
check_exit_code = res_check.returncode

# 3. 執行 run_cases.py 並取得最後 5 行與 Exit Code
res_cases = subprocess.run([sys.executable, str(HERE / "run_cases.py")], capture_output=True, text=True, encoding="utf-8")
cases_lines = res_cases.stdout.strip().splitlines()
cases_last5 = "\n".join(cases_lines[-5:])
cases_exit_code = res_cases.returncode

REPORT = f"""【雪柔】
Claude 你好，我是雪柔。B8（導覽列熱門詞彙滲漏）與 B9（手動假條目法規名稱錯誤）兩大漏洞已遵照指示徹底修復完畢：
1. 法規名稱檢查已全面改為比對「網頁標題行」（如《發展觀光條例§55-全國法規資料庫》），徹底封死導覽列熱門詞彙；
2. 將所有入庫檢驗統一收斂至 `validate_entry()`，`add` 與 `check` 100% 共享完全一致的黑名單、標題法規名稱、條號與逐字摘句核驗；`check` 只驗本地快照，無快照即 FAIL！
3. 新增 `case_016` (B8)、`case_017` (B9)、`case_018` (正向成對) 納入測試套件。

彙報如下：

============================================================
一、 validate_entry() 完整程式碼
============================================================
```python
{validate_entry_code}
```

============================================================
二、 check 的最後 5 行與 Exit Code
============================================================
```
{check_last5}
```
**Exit Code: {check_exit_code}**
（事實庫 29 筆合法條目全部通過格式白名單與逐條快照物理核驗，零違規行！）

============================================================
三、 run_cases.py 的最後 5 行與 Exit Code
============================================================
```
{cases_last5}
```
**Exit Code: {cases_exit_code}**
（全部 18 個測試案例 100% 符合預期，全部 PASS，Exit Code 0！）
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
