---
name: atom-kage-synaptic-metabolic-learner
description: 首席特務兼生活管家影·突觸代謝與殘酷遺忘自噬原子 (Kage Synaptic Metabolic Learner Protocol v1.0)。落實創辦人親授「這個技能原本的用意是讓影自主學習耶」法旨！精準落實突觸代謝方程：以脆真實後台數據（主頁造訪、淨增粉、真實互動）為物理真值誤差，自主加強高效突觸；並啟動溶酶體代謝自噬機制，對連續 3 次平淡（瀏覽<30且0互動）的陳舊套路進行殘酷遺忘與自噬清空，保持自主學習生命力。
role_key: kage
type: atomic_skill
parent_skill: bionic-learning-kage
version: v1.0
exit_code_verified: true
---

# ⚡ 影之突觸代謝與殘酷遺忘自噬原子 (Kage Synaptic Metabolic Learner)

> 👤 **原子使命**：貫徹創辦人親授心法——**「這個技能原本的用意是讓影自主學習耶！」** 如果只會一味累積死套路而不懂得遺忘與代謝，AI 就會變成充滿陳腔濫調的垃圾場！本原子落實極星神經突觸-代謝方程，以脆（Threads）後台真實物理數據為法官：當貼文獲得高轉化時自主強化突觸權重；當某個題材連續三次表現平淡時，溶酶體機制強制殘酷遺忘，清空大腦，逼迫自己自我突破！

---

## 🏛️ 突觸代謝與自噬運作架構 (Synaptic & Metabolic Architecture)

```mermaid
flowchart TD
    Telemetry["Threads 後台真實數據\n(Views 瀏覽 / Profile Visits 主頁造訪 / Net Followers 淨增粉)"] --> Equation{"突觸更新方程\nΔw = η · Π · δ · e - λ · w"}
    
    Equation -->|轉化優秀 / 品碩認可\n(Π = 1.5~2.0 多巴胺)| Strengthen["🚀 突觸自主強化 (Synapse Strengthened)\n• 提煉核心成功因子 (Credit Assignment)\n• 永久寫入長效神經肌肉記憶"]
    
    Equation -->|連續 3 次平淡 / 無人互動\n(Views < 30 且 0 留言)| Autophagy["✂️ 溶酶體代謝自噬 (Lysozyme Autophagy)\n• 殘酷遺忘無效套路與死模板\n• 清空記憶緩衝區，杜絕偷懶炒冷飯！"]
```

---

## 🧭 自主學習更新方程運算規則 (Rules)

1. **品碩全域激素場 ($\Pi_{global}$)**：
   - 創辦人認可／指引：注入全域多巴胺（1.5~2.0），以加倍速率深化突觸。
   - 創辦人示警／糾偏：注入全域皮質醇（0.2~0.5），迅速煞車並修正方向。
2. **三振自噬門禁（Three-Strike Autophagy Rule）**：
   - 任何發文模板或風格，只要連續 3 輪遙測數據低於門檻（$\text{Views} < 30$ 且 $\text{Replies} == 0$），強制判定為「代謝自噬」，標記為淘汰廢案。

---

## 🛠️ 命令列工具 (CLI Usage)

```powershell
# 計算單篇貼文學習回饋與突觸權重更新
python scripts/synaptic_metabolic_learner.py --update-synapse '{"template_id": "T01_OLD_MEMO", "views": 778, "profile_visits": 42, "net_followers": 5, "replies": 12, "consecutive_low_count": 0, "founder_approval": true}'
```

---

## 真實數據學習入口 (v1.1)

* 腳本：`scripts/kage_real_learning.py`：讀取 `threads-growth-auditor/data/insights_history.jsonl` 真實快照，同一貼文只取最新數據，依「標題前 3 字鉤子」與「發文時段」計算突觸權重；樣本 < 3 標示低信心；每次重算、不重複累加，狀態寫入 `vaults/kage_synaptic_state.json`。
* 指令：`python scripts/kage_real_learning.py --learn`
* 限制：目前無後台轉粉數據，轉化項暫不計入；快照僅 2 份，結論為假說。
