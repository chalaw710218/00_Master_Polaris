---
name: atom-taylor-campaign-launchpad
description: 行銷活動策劃、選品攻堅與全域發射原子 (Marketing Campaign Launchpad & Campaign Planner Atom)。專門為行銷長泰勒絲 (Taylor) 執行商業行銷全案策劃：生鮮選品上架、管家新服務推出、實體工作坊招生之全渠道行銷檔期排程、痛點洞察、差異化價值主張 (UVP) 與行銷活動藍圖。
---

# 🎤 atom-taylor-campaign-launchpad (行銷活動策劃、選品攻堅與全域發射原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-learning-taylor`（行銷長全域行銷戰役藍圖 ＆ 商業選品攻堅體系）  
> **核心職責**：專門執行「商業行銷活動全案策劃、選品上市攻堅、受眾痛點精確打擊、差異化價值主張 (UVP) 提煉、四階段行銷檔期推進（預熱 ➔ 發射 ➔ 證言 ➔ 收口）、以及全渠道發射排程」。

---

## 核心設計哲學：泰勒絲行銷戰役四大推進階段

1. **Phase 1: 痛點預熱 (Teaser & Problem Resonance)**：
   * 不直接叫賣商品，而是精準描摹目標受眾在日常中的具體痛點（如長輩卡刺焦慮、打工人下班備餐疲憊）。
2. **Phase 2: 價值發射 (Value Launch & Product Reveal)**：
   * 揭示硬核解決方案（0.0%包冰、手指逆紋摸刺三次、一鍋到底 15 分鐘），確立行銷第一信任壁壘。
3. **Phase 3: 常民證言與社交共鳴 (Social Proof & Kitchen Stories)**：
   * 釋放真實買家、鄰居長輩回饋，透過真切的生活故事形成口碑漣漪。
4. **Phase 4: 誠懇收口與稀缺特權 (Honest Close & Privileged Access)**：
   * 拒絕農場倒數恐嚇行銷，以「產地限量現流孤品、每堂實體課嚴格限額 6 席」之客觀物理稀缺性誠懇收尾。

---

## 執行腳本與參數

專屬腳本位於 `scripts/taylor_campaign_launchpad.py`。

### 命令行介面 (CLI)

```bash
python scripts/taylor_campaign_launchpad.py --campaign-name "成功港冬季高脂午仔魚現流上市" --product "成功港急凍午仔魚" --target-audience "雙薪家庭掌廚媽媽"
python scripts/taylor_campaign_launchpad.py --campaign-name "AI社群自動化實體工作坊第二期" --product "實體手把手教學" --target-audience "在地中小店家與接案者"
```

### 核心參數
- `--campaign-name`：行銷活動名稱。
- `--product`：核心推廣商品或服務名稱。
- `--target-audience`：目標受眾客群描摹。
- `--dry-run`：預演模式。
