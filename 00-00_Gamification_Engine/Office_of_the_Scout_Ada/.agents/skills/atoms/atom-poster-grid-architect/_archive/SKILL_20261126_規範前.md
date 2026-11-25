---
name: atom-poster-grid-architect
description: "約瑟夫視覺建築 12 欄複合網格與光學排版原子技能。嚴格依循約瑟夫六十項終極法典，計算黃金比例 12 欄排版網格、高齡 CSF 視力平權字級、阿美族八角花幾何比例、光學灰度平衡 (橫細豎粗 1:1.18) 與大地色系調色盤。"
---

# 📐 約瑟夫視覺建築 12 欄複合網格與光學排版原子技能 (Josef Poster Grid Architect Atom)

> **所屬技能組**：做海報 / 視覺工匠  
> **核心職責**：專精於海報與圖卡之「物理排版網格精算、字級層級梯隊、阿美族八角花幾何約束、光學灰度平衡」。  
> **原技能母體**：`polaris-poster-artisan`

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

## 執行腳本
```bash
python scripts/grid_architect.py --format A4 --theme local_produce --title "台東夏雪芒果直送" --dry-run
```
