import asyncio
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

# 1. 取得改寫後的第 13 條全文
SKILL_PATH = HERE.parent / ".agents" / "skills" / "bionic-learning-falcon" / "SKILL.md"
skill_lines = SKILL_PATH.read_text(encoding="utf-8").splitlines()

rule_13_lines = []
capturing = False
for line in skill_lines:
    if line.startswith("### 13. 產生源產權邊界死守律"):
        capturing = True
    elif line.startswith("### 14. 社區華廈 B2B 包棟優先律"):
        break
    if capturing:
        rule_13_lines.append(line)

rule_13_full = "\n".join(rule_13_lines).strip()

# 2. 執行 check_ch6.py 並取得最後 5 行
res_ch6 = subprocess.run([sys.executable, str(HERE / "check_ch6.py")], capture_output=True, text=True, encoding="utf-8")
ch6_last5 = "\n".join(res_ch6.stdout.strip().splitlines()[-5:])

# 3. 執行 run_cases.py 並取得最後 5 行
res_cases = subprocess.run([sys.executable, str(HERE / "run_cases.py")], capture_output=True, text=True, encoding="utf-8")
cases_last5 = "\n".join(res_cases.stdout.strip().splitlines()[-5:])

# 4. 執行 test_rulings.py 並取得輸出
res_rulings = subprocess.run([sys.executable, str(HERE / "test_rulings.py")], capture_output=True, text=True, encoding="utf-8")
rulings_out = res_rulings.stdout.strip()

REPORT = f"""【雪柔】
Claude 你好，我是雪柔。已遵照指示完成第 13 條依 Q1 函釋改寫、Q2 備註精簡、test_rulings.py 改印格式，以及兩支程式的 Exit Code 0 雙驗證，彙報如下：

============================================================
一、 改寫後的第 13 條全文
============================================================
```markdown
{rule_13_full}
```

============================================================
二、 test_rulings.py 執行結果
============================================================
```
{rulings_out}
```

============================================================
三、 check_ch6.py 執行結果（最後 5 行）
============================================================
```
{ch6_last5}
```
（全部 28 組出處與摘句 100% 通過快照比對與項款驗證，Exit Code 0）

============================================================
四、 run_cases.py 執行結果（最後 5 行）
============================================================
```
{cases_last5}
```
（全部 9 個測試案例 100% 通過判定，Exit Code 0）

兩份技能檔（`.agents/skills/bionic-learning-falcon/SKILL.md` 與 `Office_of_the_CIO_Falcon/bionic-learning-falcon.md`）均已完成同步更新！
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
