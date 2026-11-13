---
name: atom-deming-poka-yoke-engineer
description: 首席品質長戴明·神級物理與數位不可做錯防呆工坊原子 (Deming Poka-Yoke Engineering Protocol v1.0)。專門落實戴明第10律「流程防呆自癒律」與第15律「局部留置隔離律」。以接觸式、固定數值與動作步驟防呆機制，主動自癒微小髒數據；當遭遇不可修復之嚴重缺陷時，將瑕疵品精準摘除至留置緩衝區 (Quarantine Buffer)，保護 99% 合格品正常流動，兼顧零缺陷與業務高併發連續性。
role_key: deming
type: atomic_skill
parent_skill: bionic-learning-deming
version: v1.0
exit_code_verified: true
---

# 🛠️ 戴明神級防呆工坊與局部隔離原子 (Deming Poka-Yoke Engineer)

> 📐 **原子使命**：貫徹戴明「做進源頭律」與新鄉重夫「防呆 (Poka-Yoke)」工程學。好品質不是靠人緊盯，而是打造「想做錯都不可能」的物理或數位防線。本原子提供自動數據清洗自癒機制，並在批次作業中精確建立「局部留置隔離區」，杜絕一顆老鼠屎壞了一鍋粥，確保大盤業務流暢不卡死！

---

## 🏛️ 防呆三大工法與局部隔離架構 (Poka-Yoke & Quarantine)

```mermaid
flowchart TD
    Raw["原始資料 / 訂單 / 代碼流 (Raw Inflow)"] --> P1["工法 1: 接觸式防呆 (Contact Method)\n• 形態/型別硬校驗 (字串長度、數值區間、Schema 格式)"]
    
    P1 -->|發現輕微格式瑕疵| SelfHeal["✨ 自癒修正 (Self-Healing)\n• 自動去除首尾空白\n• 電話規格正規化 (09xx -> +8869xx)\n• 編碼統一轉 UTF-8"]
    
    SelfHeal --> CleanStream["✅ 合格流水線 (Clean Stream)\n• 99% 合格品持續放行"]
    P1 -->|格式完全合格| CleanStream
    
    P1 -->|發現嚴重不可逆缺陷| P2["工法 2: 局部留置隔離 (Quarantine Buffer)\n• 精準摘除單點瑕疵品\n• 絕不終止整個批次流水線\n• 隔離單自動開立"]
    
    P2 --> Quarantine["🚨 留置區 (Quarantine Box)\n• 保留瑕疵原始快照\n• 呈報 Study 根因改善"]
```

---

## 🛡️ 防呆自癒與隔離規則 (Rules)

1. **自癒優先（Self-Healing First）**：
   - 能透過確定性邏輯修復的邊界瑕疵（如：全半形轉換、多餘空白、常見標點符號溢出），一律自動修補並留痕。
2. **精準隔離（Quarantine Isolation）**：
   - 遭遇致命缺失（如：缺少收件人電話、金額為負數、缺少商品識別碼），嚴禁讓整個伺服器或排程 Crash，而是將該項目抽取存入 `quarantined_items`。
3. **隔離日誌與根因回饋（PDSA Feedback）**：
   - 隔離區累計之物件自動產出「防呆改進工單」，反哺上游輸入端強化表單防呆。

---

## 🛠️ 命令列工具 (CLI Usage)

```powershell
# 執行批次訂單防呆清洗與留置隔離
python scripts/pokayoke_engineer.py --input-json '[{"id": "ORD01", "name": " 王大明 ", "phone": "0912-345-678", "amount": 1200}, {"id": "ORD02", "name": "李小美", "phone": "invalid", "amount": -500}]'
```
