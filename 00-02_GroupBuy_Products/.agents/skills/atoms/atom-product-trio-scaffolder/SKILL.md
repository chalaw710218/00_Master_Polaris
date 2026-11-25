---
name: atom-product-trio-scaffolder
description: 自動裝配三合一交付套版物理檔案與結構化規格骨架。在新業務初始化裝配 SOP 與手冊時使用；出廠前黑臉審查時不用。只由 polaris-productization-master 呼叫，不單獨使用。
metadata:
  group: 商品化
  parent: polaris-productization-master
  owner: 雪
  status: draft
  version: "1.0"
---

# 📦 三合一商品化交付套版自動裝配原子技能 (Product Trio Scaffolder Atom)

> **核心職責**：專精於「三合一交付套版物理檔案自動初始化、結構化欄位無遺漏裝配、5D 商業邊界設定、跨平台行銷骨架封裝」。  

---

## 核心功能與深度特性
1. **三位一體交付同構性 (Universal 3-in-1 Guarantee)**：
   - 強制在目標模組資料夾生成 3 份標準化 Markdown 文件，杜絕任何欄位與防呆漏洞。
2. **01_SOP 標準流程骨架 (Delivery Closed-Loop)**：
   - 內建：前置準備清單、標準履約五步法、現場排錯與意外應變、客訴防呆賠償上限、二次出勤條款。
3. **02_產品規格與定價手冊骨架 (Contract & Economics)**：
   - 內建：服務邊界（哪些做、哪些堅決不做）、5D 矩陣明碼定價（服務費與代墊費完全解耦）、老學員/熟客免單政策、家宅地理座標與自取流程。
4. **03_行銷文案與地推話術骨架 (Multi-Channel Copy)**：
   - 內建：泰勒絲 FB 長文故事版（含第一則留言置頂導流）、影 Threads 扎心隨筆版（含首留言點火橋接）、生活管家地推面對面高情商口語話術。
5. **乾跑防呆 (Dry-Run Support)**：
   - 支援 `--dry-run` 模式，在不觸發磁碟寫入的前提下驗證完整三合一結構與預填充內容。

---

## 執行腳本
```bash
python scripts/product_trio_scaffolder.py --target-dir "00-02-08_Product_NewService" --service-name "台東在地慢活居安管家" --dry-run
```
