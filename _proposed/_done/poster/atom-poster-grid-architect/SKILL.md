---
name: atom-poster-grid-architect
description: 精算 12 欄網格、視距字級方程、光學平衡與風土色盤。在海報開版、幾何排版與視覺階層規劃時使用；印刷送印前安燈質檢時不用。只由 polaris-poster-artisan 呼叫，不單獨使用。
metadata:
  group: 做海報
  parent: polaris-poster-artisan
  owner: 約瑟夫
  status: draft
  version: "1.0"
---

# 📐 約瑟夫視覺建築 12 欄複合網格與光學排版原子技能 (Josef Poster Grid Architect Atom)

專精於海報與圖卡之「物理排版網格精算、字級層級梯隊、阿美族八角花幾何約束、光學灰度平衡」。

---

## 核心功能與深度特性

1. **12 欄複合網格 (12-Column Composite Grid)**：
   - 支援 A3 (3508x4960 px)、A4 (2480x3508 px)、IG 直式 (1080x1350 px)、Reels (1080x1920 px)。
   - 自動精算 3mm 出血線 (85px)、主內距 (Margins)、欄寬 (Column Width) 與欄間距 (Gutters)。
2. **高齡 CSF 視力平權字級 (Contrast Sensitivity Function Typography)**：
   - 拒絕設計師自嗨之微縮字體。
   - 主標題 >= 1/12 畫布高、副標題 >= 1/24 畫布高、正文 >= 1/40 畫布高、電話與二維碼說明 >= 1/60 畫布高。
3. **光學灰度與橫細豎粗平衡 (Optical Balance 1:1.18)**：
   - 繁體中文字體橫向筆畫光學修正，確保遠距離視讀不眩光。
4. **風土色彩與大豆油墨調色盤 (Earth Palette & Soy Ink Pre-compensation)**：
   - 依據主題自動配置符合台東風土之大地色系（如關山熟穗金、鹿野紅烏龍茶紅、寶桑太平洋靛藍、富岡礁岩深灰），並提供 HEX 與 CMYK 推薦值。

---

## 排版幾何與視學工程規範

### 一、 受眾視力與媒介情境分流 (Audience CSF & Context Triage)
1. **高齡受眾辨別**：若目標受眾包含偏鄉長輩、社區長照或銀髮族，強制鎖定：
   * 印刷內文字級 $\ge 12\text{pt}$（實體字高 $\ge 5.0\text{mm}$）。
   * 嚴禁標楷體、細明體與「淺灰配白底」，全面採用方正中黑體且**齊左對齊**。
2. **懸掛視距解算**：依據視距建築方程 $H = D \times \tan(1^\circ) \times 1.2$ 計算實體標題字高。
   * 門市 3 公尺視距：標題字高 $\ge 6.3\text{cm}$。
   * 戶外 5 公尺視距：標題字高 $\ge 10.5\text{cm}$。
3. **動態透視補償**：
   * 騎樓街角外向看板：主標題字寬動態預先水平拉伸 118%（對抗 45 度斜向視角壓縮）。
   * A5 / DM 傳單：下方 15%（31.5mm）劃定為「拇指持握盲區」，嚴禁放置行動點。

### 二、 資訊解剖與認知動線 (Information Hierarchy)
1. **第一凝視點錨定**：版面頂部 28%~35% 幾何中心區間，死死鎖定 H1 痛點大主標（1.5 秒穿透）。
2. **三層動線解剖**：
   * Level 1 (Hook)：直擊痛點（「垃圾車又跑了？」、「AI 學不會？」）。
   * Level 2 (Value)：3 大核心解方（卡片化模組，Modular Scale 1.25 大三度字階）。
   * Level 3 (Action)：50 公分秒級掃碼 CTA（價格錨定對比 + QR Code）。

### 三、 幾何網格與色彩調度 (Grid & Geospatial Palette)
1. **網格佈局**：建立 12 欄複合網格（槽寬 4mm、外安全邊距 24mm）。卡片轉角設定 $\ge 4\text{px}$ 圓角，網格分隔線透明度壓制在 15% 以下，**消除赫曼方格暗斑**。
2. **神聖幾何角標**：四角或主視覺結構點融入**台東阿美族八角花（Falo）45 度中心對稱幾何**，色彩以紅、黑、白三色為基底。
3. **色彩方案調度**：
   * **標準品牌色**：極星炭黑 (`#1A1D20`) 60% + 純白 (`#F8F9FA`) 30% + 朱紅/金 10%。
   * **在地創生色**：黑潮深藍 (`#1F3A52`)、池上金 (`#D4A347`)、太麻里日出赤紅 (`#C84B31`)。
   * **極限降本專色**：勞務服務類強制啟用「雙色調 (Duotone) 專色（深炭黑 + 朱紅）」，製版成本砍半 50%。

---

## 執行腳本

```bash
python scripts/grid_architect.py --format A4 --theme local_produce --title "台東夏雪芒果直送" --dry-run
```
