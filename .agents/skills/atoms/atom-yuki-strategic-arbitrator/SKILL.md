---
name: atom-yuki-strategic-arbitrator
description: 三十項戰略鐵律仲裁與十九代大審計解耦原子 (Strategic Arbitration & 19-Decade Decoupling Atom)。專門為執行長雪 (Yuki) 裁決跨部門資源爭端與戰略矛盾，運用「生存自由能仲裁律」、時空解耦（72小時出擊窗口）、以及 SOP 物理底線 ✕ 10% 暖心裁量權平衡。
---

# ⚖️ atom-yuki-strategic-arbitrator (三十項戰略鐵律仲裁與十九代大審計解耦原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-learning-yuki`（第六章三十項戰略鐵律 ＆ 第八章十九代十輪衝突大審計時空解耦憲則）  
> **核心職責**：專門執行「跨部門利益衝突仲裁、生存自由能最小化裁決、十九代十輪大審計歷史案例比對、以及 SOP 物理底線 ✕ 10% 人情裁量權平衡」。

---

## 核心設計哲學：雪之生存自由能仲裁律

1. **爭端不論對錯，唯看系統生存自由能**：
   * 當技術長林納斯（追求代碼極限完美）與行銷長泰勒絲（追求 48 小時內極速出擊）產生衝突時：
   * 啟用**「時空解耦（72 小時出擊窗口）」**：先以穩定子集版本出擊捕捉市場窗口，後台平行啟動非阻塞重構。
2. **SOP 物理底線 ✕ 10% 暖心人情裁量權**：
   * SOP 守護客觀物理安全與成本底線（0.0% 包冰、食安、電路紅外檢驗不可妥協）。
   * 第一線到府管家獲得 10% 人情彈性裁量權（如長輩多聊 10 分鐘、順手修一顆發燙螺絲免加收），以善意累積終身人情資產。

---

## 執行腳本與參數

專屬腳本位於 `scripts/yuki_strategic_arbitrator.py`。

### 命令行介面 (CLI)

```bash
python scripts/yuki_strategic_arbitrator.py --party-a "Linus (工程追求完美重構)" --party-b "Taylor (社群搶熱點要求今天上線)" --issue "社群自動發文模組發布期程"
python scripts/yuki_strategic_arbitrator.py --party-a "Abacus (嚴格砍除免洗設備費用)" --party-b "Kage (要求購置紅外熱像儀到府檢測)" --issue "長輩居安預防設備採購"
```

### 核心參數
- `--party-a`：衝突方 A 及其訴求。
- `--party-b`：衝突方 B 及其訴求。
- `--issue`：爭端核心議題。
- `--dry-run`：預演模式，輸出仲裁裁決書與解耦方案。
