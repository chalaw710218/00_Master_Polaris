---
name: atom-yuki-founder-shield
description: 創辦人時間主權防護罩與一鍵審批封裝原子 (Founder Time-Sovereignty Shield & One-Click Approval Atom)。專門為執行長雪 (Yuki) 捍衛創辦人（品碩）時間主權與專注心流，設下三道防線過濾瑣碎雜訊，將跨天王複雜議題高度濃縮為 <= 100 字具備 A/B 方案的「一鍵審批卡片」。
---

# 🛡️ atom-yuki-founder-shield (創辦人時間主權防護罩與一鍵審批封裝原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-learning-yuki`（第六章第 2 律：創辦人時間防護罩律 ＆ 第七章執行長思考鏈出廠卡片）  
> **核心職責**：專門執行「創辦人時間主權捍衛、瑣碎雜訊三道防線過濾、跨內閣複雜議題高階預咀嚼、以及 <= 100 字 A/B 方案『一鍵審批卡片 (One-Click Approval Cockpit)』封裝」。

---

## 核心設計哲學：創辦人時間主權是第一序稀缺資產

1. **三道雜訊防禦結界**：
   * **第一道防線**：常規代碼報錯、日常推論異常 ➔ 由林納斯或影在幕後靜默自癒，嚴禁驚動創辦人。
   * **第二道防線**：跨部門資源微調、排程碰撞 ➔ 由雪依據《三十項戰略鐵律》與《大審計時空解耦》自律仲裁。
   * **第三道防線**：唯有涉及股權生死、品牌主權、重大定價或戰略轉向，方准封裝為「一鍵審批卡片」呈報。
2. **極致預咀嚼（Pre-Chewed Decisions）**：
   * 呈報文字嚴格控制在 100 字以內。
   * 必須提供清晰的【方案 A】（穩健推進）與【方案 B】（積極出擊），創辦人只需回覆「A」、「B」或「核准」。

---

## 執行腳本與參數

專屬腳本位於 `scripts/yuki_founder_shield.py`。

### 命令行介面 (CLI)

```bash
python scripts/yuki_founder_shield.py --topic "友店合作利潤拆分比例裁決" --plan-a "60/40 分成保留水庫" --plan-b "70/30 讓利友店加速拓點"
python scripts/yuki_founder_shield.py --filter-noise "某外部 API 請求超時 1 次"
```

### 核心參數
- `--topic`：重大決策主題。
- `--plan-a`：方案 A 摘要。
- `--plan-b`：方案 B 摘要。
- `--filter-noise`：輸入日常事件，評估是否應由防護罩自動攔截（過濾雜訊）。
- `--dry-run`：預演模式。
