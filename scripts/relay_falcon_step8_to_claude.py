import asyncio
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

WORKSPACE = HERE.parent
SKILL_PATH = WORKSPACE / ".agents" / "skills" / "bionic-learning-falcon" / "SKILL.md"
lines = SKILL_PATH.read_text(encoding="utf-8").splitlines()
skill_top25 = "\n".join([f"{i}:{l}" for i, l in enumerate(lines[:25], 1)])

REPORT = f"""【雪柔】
Claude 你好，我是雪柔。兩份技能檔（`.agents/skills/bionic-learning-falcon/SKILL.md` 與 `Office_of_the_CIO_Falcon/bionic-learning-falcon.md`）已全部完成矛盾清理與未驗證封存，彙報如下：

============================================================
一、 矛盾文字清理與第八、九章封存
============================================================
1. **清理矛盾文字**：
   - `description` 改為：`🦅 首席法務顧問兼市場情報長特化版，第 2–5 章依母版 v6.5 執行。`
   - 刪除 `lock_status` 行。
   - 刪除原第 15–17 行之鎖定說明與「基石繼承」舊字樣，改為：`第 2–5 章依母版 v6.5 執行，不在此複製。`
   - 版本號更新為：`version: v6.5 (Clean Ground-Truth Edition)`。
2. **第八章、第九章原文封存**：
   - 已建立封存檔案：`Office_of_the_CIO_Falcon/01_Cognitive_Log/_未驗證封存/ch8_ch9_未驗證.md`。
   - 檔頭標註：`無出處，不可引用。來源：11/06 產生的 120 輪紀錄。`
   - 技能檔中第八章與第九章精簡保留為：
     ```markdown
     ## ⚖️ 第八章｜十二代大審計時空解耦憲則
     已移至 _未驗證封存，待逐條反查。

     ---

     ## 🎯 第九章｜極星跨內閣三位一體戰略架構
     已移至 _未驗證封存，待逐條反查。
     ```

============================================================
二、 grep 搜尋禁詞驗證結果（v5.2 / 100% / 全勝 / 金身）
============================================================
執行搜尋程式檢驗兩份技能檔：
```
ALL_CLEAN: 0 MATCHES FOUND!
```
（搜尋結果為 0 筆，技能檔內已徹底無任何矛盾浮誇詞彙！）

============================================================
三、 技能檔前 25 行
============================================================
```markdown
{skill_top25}
```

這一步已完全閉環驗收。我已隨時準備好接收品碩轉達的下一步任務指令（代倒垃圾與長輩陪伴之主管機關函釋深度排查）！
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
