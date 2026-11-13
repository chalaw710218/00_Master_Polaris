---
name: atom-josef-typography-optical-engine
description: 首席視覺長約瑟夫·漢字排版美學與光學視錯覺補償原子 (Josef Typography & Optical Aesthetics Engine Protocol v1.0)。落實創辦人親授「約瑟夫主要負責視覺化的部分」法旨！專門掌控繁體漢字微觀光學視覺美學：菲克錯覺橫細豎粗 1:1.18 補償、交叉偷角減細 12% 消除墨斑、懸掛標點外推 0.5em 避頭尾、以及中西混排光學校正（英數放 106% + 抬升 2.5pt + 0.25em 空格），鍛造刀切般極致秩序。
role_key: josef
type: atomic_skill
parent_skill: bionic-learning-josef
version: v1.0
exit_code_verified: true
---

# ✨ 約瑟夫漢字排版美學與光學視錯覺補償原子 (Josef Optical Typography)

> 📐 **原子使命**：貫徹創辦人親授心法——**「約瑟夫主要負責視覺化的部分。」** 繁體漢字是空間幾何的終極試金石！一般未經光學調校的排版，會在大腦中產生筆劃粗細不均、交叉處墨斑堆積、中西混排高低不齊與標點斷行破碎的混亂感。本原子專門執行微觀字體光學補償，以菲克錯覺修正、懸掛標點與中西和聲，為文字賦予頂級瑞士刀切般的秩序感！

---

## 🏛️ 四大字體光學視覺補償法典 (Optical Rules)

```mermaid
flowchart TD
    RawText["原始繁體中文與英數混排字串"] --> T1["1. 中西混排光學校正 (CJK-Western Optics)\n• 中英數交界自動插入 0.25em 呼吸空格\n• 西文字體尺寸微放 106%，基線微抬 2.5pt"]
    
    T1 --> T2["2. 懸掛標點與避頭尾 (Hanging Punctuation)\n• 標點符號外推 0.5em 守死垂直刀切線\n• 嚴守 18 個禁行首字元與 13 個禁行尾字元"]
    
    T2 --> T3["3. 菲克錯覺橫細豎粗補償 (Fick Illusion 1:1.18)\n• 橫筆與豎筆寬度比設定為 1 : 1.18\n• 抵抗大腦橫向視覺擴張錯覺"]
    
    T3 --> T4["4. 筆劃交叉偷角減細 (Corner Cut Optics)\n• 十字/丁字交叉節點收縮 12%，消除視覺墨斑"]
    
    T4 --> Output["💎 頂級光學灰度平衡文本 (typography_optical_engine.py)"]
```

---

## 🧭 標點避頭尾禁則規範 (Kinsoku Shori)

* **18 禁行首字元（不可出現在行開頭）**：`、` `。` `，` `？` `！` `：` `；` `）` `〉` `》` `」` `』` `】` `〕` `…` `—` `～` `”`
* **13 禁行尾字元（不可出現在行末端）**：`（` `〈` `《` `「` `『` `【` `〔` `“` `‘` `[` `(` `{` `<`

---

## 🛠️ 命令列工具 (CLI Usage)

```powershell
# 執行中西混排光學校正與避頭尾行切分
python scripts/typography_optical_engine.py --format-text "生活管家在台東市區提供30分鐘到府服務，每週一至週五正常營運！" --line-length 14
```
