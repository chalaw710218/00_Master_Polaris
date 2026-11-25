---
name: atom-taylor-funnel-telemetry
description: 行銷轉化漏斗設計與共鳴遙測原子 (Marketing Funnel & Resonance Telemetry Atom)。專門為行銷長泰勒絲 (Taylor) 設計與監測四階行銷獲客轉化漏斗（公域觸達 ➔ 個人主頁引流 ➔ 私域客廳沉澱 ➔ 實體履約高 LTV），計算轉化率與受眾共鳴度，嚴格落實防騷擾推播門禁。
---

# 📊 atom-taylor-funnel-telemetry (行銷轉化漏斗設計與共鳴遙測原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-learning-taylor`（行銷四階轉化漏斗 ＆ 關係人口 LTV 沉澱體系）  
> **核心職責**：專門執行「四階行銷獲客漏斗設計、流量穿透與轉化率試算、公域至私域對流機制控管、推播頻率防打擾閘門（每週最多 1~2 則）、以及受眾長期 LTV 信任共鳴遙測」。

---

## 核心設計哲學：極星四階行銷轉化漏斗

拒絕一次性割韭菜的流量思維，構建長效生活風格關係人口：

1. **Stage 1 (公域觸達 · Public Reach)**：
   * Threads / FB 微動態生活切片、喵編純真店貓生活、零外鏈無壓陪伴。
2. **Stage 2 (主頁引流 · Bio Conversion)**：
   * 透過秒回接梗吸引讀者點擊 Bio 個人檔案，建立第一道興趣與信任濾鏡。
3. **Stage 3 (私域客廳 · Private Sovereign Retention)**：
   * 進入 LINE OA 私域主權客廳，享有「產地限量現流孤品認領」、「家庭無刺食育小抄」等非貨幣風土特權。
   * 每週推播嚴格鎖定 1~2 則，封鎖率趨近 0.0%。
4. **Stage 4 (實體履約 · Offline Fulfillment & High LTV)**：
   * 在地友店（海特咖啡等）-18°C 智能櫃自提、或生活管家到府服務；將單純買家昇華為終生台東生活關係人口。

---

## 執行腳本與參數

專屬腳本位於 `scripts/taylor_funnel_telemetry.py`。

### 命令行介面 (CLI)

```bash
python scripts/taylor_funnel_telemetry.py --public-reach 10000 --bio-clicks 800 --private-leads 250 --orders 60
python scripts/taylor_funnel_telemetry.py --simulate-campaign --budget 5000
```

### 核心參數
- `--public-reach`：公域曝光觸達數。
- `--bio-clicks`：個人主頁點擊數。
- `--private-leads`：私域客廳新進名單數。
- `--orders`：實體履約成交訂單數。
- `--simulate-campaign`：模擬行銷活動漏斗指標。
- `--dry-run`：預演模式。
