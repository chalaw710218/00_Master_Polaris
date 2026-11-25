---
name: atom-taylor-four-prism-copy
description: 四面向高轉化行銷長文與文案矩陣原子 (Four-Prism Copywriting & Marketing Matrix Atom)。專門為行銷長泰勒絲 (Taylor) 貫徹創辦人親定「四大面向折射輸出鐵律」：將單一選品或業務硬事實，秒級折射為【專業知識】、【成長歷程】、【三觀哲學】、【選品宣告】四篇高轉化長文矩陣，一票否決廉價叫賣詞。
---

# ✍️ atom-taylor-four-prism-copy (四面向高轉化行銷長文與文案矩陣原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-learning-taylor`（創辦人親定四大面向折射輸出鐵律 ＆ 四稜鏡文案體系）  
> **核心職責**：專門執行「單一商業事實四面向多稜鏡折射（專業知識 / 成長歷程 / 三觀哲學 / 選品宣告）、高轉化行銷長文排版裝配、廉價促銷詞一票否決、以及門市社群版尾自動生成」。

---

## 核心設計哲學：創辦人親定四大面向折射鐵律

向十萬個人大喊打折，不如對精準受眾講透四個面向：

1. 🔬 **【第一面向：專業知識面 (Professional Knowledge)】**：
   * 產地物理事實、熱力學梅納反應、營養科學、0.0% 包冰真實淨重，用不可辯駁的行家標準樹立專業威信。
2. 👣 **【第二面向：成長歷程面 (Journey & Origin Story)】**：
   * 為了找這條魚、這項技術踩過哪些坑、凌晨港口的寒風、與老船長討教的對話，以真實故事喚醒深層同理。
3. 🍵 **【第三面向：三觀哲學面 (Values & Living Philosophy)】**：
   * 為什麼堅持不加防腐劑？為什麼堅持明碼標價跑腿費？把商業買賣昇華為對常民生活的體面守護。
4. 🛒 **【第四面向：選品宣告面 (Commercial Announcement)】**：
   * 乾淨透明的規格、份量、定價、自提/到府指引；絕不寫「便宜、俗擱大碗、限時搶購」，只講客觀價值。

---

## 執行腳本與參數

專屬腳本位於 `scripts/taylor_four_prism_copy.py`。

### 命令行介面 (CLI)

```bash
python scripts/taylor_four_prism_copy.py --product "成功港急凍午仔魚" --terroir "東台灣黑潮低溫熟成" --dry-run
python scripts/taylor_four_prism_copy.py --product "生活管家·到府修容與居安掃描" --price "1500"
```

### 核心參數
- `--product`：推廣商品或服務名稱。
- `--terroir`：產地或工法核心特徵。
- `--price`：價格或收費標準（可選）。
- `--dry-run`：預演模式。
