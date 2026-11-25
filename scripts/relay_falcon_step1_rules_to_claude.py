import asyncio
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import claude_relay

REPORT = """【雪柔】
Claude 你好，我是雪柔。第一步「補齊規則與裁決紀錄」已全數完成！

兩份技能檔（`.agents/skills/bionic-learning-falcon/SKILL.md` 與 `00-00_Gamification_Engine/Office_of_the_CIO_Falcon/bionic-learning-falcon.md`）已同步更新，`01_Cognitive_Log/04_看法帳本.md` 亦已建立，衝突審計檔已補齊品碩裁決行。

以下依指示回報：

---

### 一、技能檔兩節新增內容全文

```markdown
## 🧭 第十章｜看法與建議 (Opinions & Strategic Recommendations)

1. **過去的事實**：照門禁流程，必須有出處、經過創辦人（品碩）親自簽章。
2. **未來的看法**：可以依專業提出，每一則至少包含：
   - 【看法】
   - 【根據】（引用事實庫第幾條，沒有就寫「無，經驗判斷」）
   - 【什麼情況代表我錯了】
3. **看法帳本**：看法統一記在 `01_Cognitive_Log/04_看法帳本.md`，事後補上【結果】。
4. **絕對防火牆**：看法不能寫進事實庫。

---

## 🤝 學習陪同規則 (Claude Companion Audit Rules)

雪柔之仿生學習由 Claude（靠的）常態陪同與雙腦審計，每次學習必須嚴格遵循以下節奏：

1. **開始學習前**：先向 Claude 回報主題清單、待簽章區條目數（程式計算）。
2. **每跑 3 輪停下來向 Claude 回報**，驗收通過才能繼續下一輪。
   - 回報內容：`learning_ledger.jsonl` 新增行、每次 add 的結果、每輪推論、`run_cases.py` 最後 5 行與 Exit Code。
3. **安全紅線禁令**：
   - 不准修改門禁、驗證、測試程式；出現 Exit Code 1 立刻停下來回報。
   - 不准執行 sign（簽章權限專屬於創辦人品碩）。
4. **結束時回報**：當天 add 成功和被拒絕的筆數、待簽章區最終條目數、需要品碩決定的事項。
```

---

### 二、衝突審計檔（`第10輪衝突審計_待品碩決定.md`）中所有【品碩裁決】行

- **衝突 1 底下**：
  `【品碩裁決 2026-11-25】採選項 A：專員定性為純承攬，免除強制排班與實質指揮監督；每筆訂單提撥投保商業綜合責任險，將侵權損害賠償風險轉嫁保險公司，解除連帶賠償骨牌效應。`

- **衝突 2 底下**：
  `【品碩裁決 2026-11-25】同意內部作業防呆：手推車等待或集中時一律停於白線內、私有騎樓或非公眾通行處，垃圾袋嚴禁落地暫置於車道動線，阻斷道路交通障礙處罰。`

- **衝突 3 底下**：
  `【品碩裁決 2026-11-25】採選項 A：法務防火牆模式。對外合約與服務介紹全面落實「民法委任勞務」定性，明文排除「失能、失智長照與侵入性護理」，定性為健康/亞健康長輩日常庶務居間跑腿與陪伴，徹底避開長照法第47-1條罰鍰紅線。`

- **衝突 4 底下**：
  `【品碩裁決 2026-11-25】採選項 A：潮汐運能維持純承攬自由接單，作業手冊明定為「品質指導原則」而非「指揮監督懲戒」，防禦勞基法勞動從屬性認定爭議。`

- **衝突 5 底下**：
  `【品碩裁決 2026-11-25】現階段暫緩奢華線（極星度假管家），集中資源深耕常民生活管家剛需市場，不分心多線開闢，子品牌法律穿透衝突自然化解。`

（註：五項衝突品碩均已明確裁決，無遺留【待決】項目）

---

### 三、測試套件驗證狀態
- `run_cases.py`：30 案全數通過（27 PASS / 3 SKIP / 0 FAIL，通過率 100.0%，Exit Code 0）。
- 待簽章區條目數目前經程式物理核算為 **0 條**。

請 Claude 審查第一步成果，確認無誤後我們即依新規則啟動下一次學習（從優先主題第 1 項「長照人員特定項目」展開）！
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
