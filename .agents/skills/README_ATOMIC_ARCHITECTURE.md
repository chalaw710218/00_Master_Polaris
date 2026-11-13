# 🧱 極星原子微技能 (Atoms) 與技能組管線 (Packs) 雙軌架構規範書

> **生效日期**：2026-11-13 (Phase 0 憲政底座)  
> **最高架構原則**：單一職責 (Single Responsibility) ✕ 形式化確定 (Deterministic Contract) ✕ 雙軌零宕機 (Zero-Downtime)

---

## 🏛️ 目錄架構與職責邊界

```
.agents/skills/
├── [legacy_skills]/       <-- 現有 41+ 項實體技能目錄（100% 唯讀保全，生產環境正常待命）
│
├── atoms/                 <-- 【原子微技能庫】(Atomic Primitives)
│   ├── atom-[領域]-[功能]/
│   │   ├── SKILL.md       (YAML 宣告、精煉 I/O 契約、單一職責描述)
│   │   └── scripts/       (純函數式確定性 Python/Shell 工具，無外部耦合)
│
└── packs/                 <-- 【模組化技能組管線】(Composable Pipelines)
    ├── pack-[口語命名]/   (例如: pack-qu-guang-guang / pack-fa-zhang-zhao)
    │   ├── SKILL.md       (管線調度說明、口語喚醒詞、生活管家業務 SOP)
    │   └── pipeline.py    (將對應之 atoms 如積木般串聯的執行管線)
```

---

## 📐 原子微技能 (Atoms) 三大軍規
1. **單一動詞職責**：只做一件事（如「只做 5D 定價計算」、「只做 Threads API 留言」、「只做約瑟夫網格排版」），代碼行數控制在極簡精煉。
2. **零副作用 I/O**：輸入與輸出採標準 JSON，不擅自覆寫外部狀態。
3. **Exit Code 0 形式化保證**：內建單元測試，嚴禁任何未捕獲異常。

---

## 🚀 技能組管線 (Packs) 組裝規範
1. **創辦人口語錨定**：必須以創辦人自然口令（「去逛逛」、「發張照」、「5D定價」等）命名與觸發。
2. **戴明安燈閘門**：管線中的每個節點輸出，若未通過品質驗證（如安燈評分 <90），強制熔斷並發出警報，絕不出廠。
