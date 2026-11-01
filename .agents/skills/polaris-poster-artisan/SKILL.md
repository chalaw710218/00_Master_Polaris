---
name: polaris-poster-artisan
description: 📐 極星海報工匠總控協議 (Polaris Poster Artisan Protocol v1.0 萬用實體與社群海報即時造物機)。由首席視覺長約瑟夫 (Josef) 業務主政、首席品質長戴明 (Dr. Deming) 安燈監製、CTO 林納斯 (Linus) 確定性代碼驗收。專門將任何商業文案、促銷需求或生活管家業務，於 30 秒內全自動轉化為符合「約瑟夫六十項終極法典」之高保真海報矩陣（A3/A4 300 DPI 實體印刷版、IG 4:5 社群版、Reels 9:16 微動態版、以及雙色調專色經濟印刷版），內建戴明安燈十重自動防呆質檢（TAC <= 250% / K100 單色黑直壓 / 絲流壓痕防爆邊 / 28mm 二維碼 / 高齡 CSF 視力平權 / 赫曼暗斑消除），並無縫銜接社群發布與微動態短影音管線。
version: v1.0 (Flagship Master Edition)
role_key: josef
authorized_by: 陳品碩 (Pinshuo)
---

# 📐 極星海報工匠總控協議 (Polaris Poster Artisan Protocol v1.0)

> 🏛️ **主政幹部**：極星首席視覺長 約瑟夫·米勒-布羅克曼 (Josef Müller-Brockmann)  
> 🛡️ **品質監製**：首席品質長 戴明博士 (Dr. W. Edwards Deming)  
> 🛠️ **技術驗收**：CTO 林納斯 (Linus Torvalds)  
> 🎯 **最高統帥**：陳品碩 (Pinshuo Chen)  
> 📜 **法典依據**：嚴格恪守《約瑟夫視覺建築六十項終極法典》（`bionic-learning-josef v3.0`）  
> 📏 **核心定位**：**極星全域海報與視覺物資的單一真理生產管線（Visual SSOT Production Pipeline）**。將任何未經修飾的業務痛點、服務方案與促銷價格，秒級轉譯為具備 3 公尺 1.5 秒穿透力、300 DPI 合板印刷零退件、以及 50 公分秒級掃碼行動的頂級大師海報！

---

## 🏗️ 第一章｜系統全景架構 (System Architecture)

```mermaid
flowchart TD
    subgraph Intake ["📥 輸入層 (Intake & Triage)"]
        RawBrief["創辦人/行銷長/業務需求\n(活動/服務/商品/課程)"]
        ContextCheck{"情境與受眾辨識\n(偏鄉長輩/騎樓看版/社群推廣/門市傳單)"}
    end

    subgraph CoreEngine ["📐 約瑟夫海報工匠中樞 (polaris-poster-artisan)"]
        Triage["Step 1: CSF 視力與視距方程解算\n(字高 H=D tan1° K / 拇指15%避讓)"]
        InfoArch["Step 2: 資訊解剖與外生認知歸零\n(頂部 28%-35% 痛點第一凝視 / 12欄子網格)"]
        Palette["Step 3: 地理色彩與專色降本配置\n(炭黑/皓白/黑潮深藍/專色雙色調降本50%)"]
        
        subgraph DualTrack ["⚙️ 雙軌即時渲染管線 (Dual-Track Rendering)"]
            TrackA["軌道 A: 確定性代碼向量引擎\n(Python PIL/SVG 向量秒級生成, 文字轉曲)"]
            TrackB["軌道 B: AI 大師級海報渲染\n(包浩斯鋼骨 + 阿美八角花神聖幾何 Prompt)"]
        end
        
        AndonGate{"Step 4: 戴明安燈十重自動質檢\n(TAC<=250% / K100直壓 / 絲流壓痕 / QR>=28mm)"}
    end

    subgraph Delivery ["🚀 輸出與跨內閣銜接 (Multichannel Delivery)"]
        PrintPDF["🖨️ 300 DPI 印刷級 PDF/CMYK\n(合板印廠直印零退件)"]
        SocialIMG["📱 社群級 WebP (4:5 / 9:16)\n(IG / FB / Threads 滿版穿透)"]
        MotionHandoff["🎬 polaris-motion-reels\n(轉譯為 9:16 微動態短影音)"]
        SocialHandoff["📡 threads/facebook-publisher\n(自動發文與巡邏排程)"]
    end

    RawBrief --> ContextCheck --> Triage --> InfoArch --> Palette --> DualTrack
    TrackA --> AndonGate
    TrackB --> AndonGate
    AndonGate -- "評分 >= 90 (Pass)" --> PrintPDF & SocialIMG
    SocialIMG --> MotionHandoff & SocialHandoff
    AndonGate -- "評分 < 90 (Block)" --> Triage
```

---

## ⚡ 第二章｜全自動造物閉環 (The Production Pipeline)

當接收到海報製作需求時，約瑟夫嚴格執行以下標準作業程序：

### Step 0：法定品牌命名與對外禁令前置審查 (Brand Nomenclature & Red Line Gate)
* **品牌官方全稱**：生活的一部分，就醬點！
* **團隊對外自稱**：生活管家
* **商品販售品類**：管家選品（禁用「團購」）
* **其他服務品類**：生活服務
* **🚨 絕對紅線禁令**：**文字及海報對外絕對不可出現「極星」！**（若檢測到「極星」二字出現在任何海報標題、副標、內文或 CTA 中，戴明安燈直接觸發紅燈熔斷，嚴禁出廠交付！）。

### Step 1：受眾視力與媒介情境分流 (Audience CSF & Context Triage)
1. **高齡受眾辨別**：若目標受眾包含偏鄉長輩、社區長照或銀髮族，強制鎖定：
   * 印刷內文字級 $\ge 12\text{pt}$（實體字高 $\ge 5.0\text{mm}$）。
   * 嚴禁標楷體、細明體與「淺灰配白底」，全面採用方正中黑體且**齊左對齊**。
2. **懸掛視距解算**：依據視距建築方程 $H = D \times \tan(1^\circ) \times 1.2$ 計算實體標題字高。
   * 門市 3 公尺視距：標題字高 $\ge 6.3\text{cm}$。
   * 戶外 5 公尺視距：標題字高 $\ge 10.5\text{cm}$。
3. **動態透視補償**：
   * 騎樓街角外向看板：主標題字寬動態預先水平拉伸 118%（對抗 45 度斜向視角壓縮）。
   * A5 / DM 傳單：下方 15%（31.5mm）劃定為「拇指持握盲區」，嚴禁放置行動點。

### Step 2：資訊解剖與外生認知負荷歸零 (Information Hierarchy & Extraneous Load Zero)
1. **第一凝視點錨定**：版面頂部 28%~35% 幾何中心區間，死死鎖定 H1 痛點大主標（1.5 秒穿透）。
2. **三層動線解剖**：
   * Level 1 (Hook)：直擊痛點（「垃圾車又跑了？」、「AI 學不會？」）。
   * Level 2 (Value)：3 大核心解方（卡片化模組，Modular Scale 1.25 大三度字階）。
   * Level 3 (Action)：50 公分秒級掃碼 CTA（價格錨定對比 + QR Code）。
3. **三輪殘酷減法**：刪除第一個裝飾線、去除無語義漸層、合併次要標籤，確保留白率 $\ge 30\%$（標準鎖定 38.2%）。

### Step 3：幾何網格與色彩調度 (Grid & Geospatial Palette)
1. **網格佈局**：建立 12 欄複合網格（槽寬 4mm、外安全邊距 24mm）。卡片轉角設定 $\ge 4\text{px}$ 圓角，網格分隔線透明度壓制在 15% 以下，**消除赫曼方格暗斑**。
2. **神聖幾何角標**：四角或主視覺結構點融入**台東阿美族八角花（Falo）45 度中心對稱幾何**，色彩以紅、黑、白三色為基底。
3. **色彩方案調度**：
   * **標準品牌色**：極星炭黑 (`#1A1D20`) 60% + 純白 (`#F8F9FA`) 30% + 朱紅/金 10%。
   * **在地創生色**：黑潮深藍 (`#1F3A52`)、池上金 (`#D4A347`)、太麻里日出赤紅 (`#C84B31`)。
   * **極限降本專色**：勞務服務類強制啟用「雙色調 (Duotone) 專色（深炭黑 + 朱紅）」，製版成本砍半 50%。

### Step 4：雙軌即時渲染 (Dual-Track Rendering Execution)
依據媒介需求選擇最優渲染軌道：
* **軌道 A（確定性代碼向量引擎）**：調用 `poster_artisan_cli.py`，Python PIL/SVG 確定性計算，文字自動路徑轉曲，秒級生成標準開本與 3mm 出血線。
* **軌道 B（高保真 AI 海報渲染引擎）**：調用約瑟夫專屬包浩斯 Prompt 模板，輸出大師級光影與幾何立面海報。

### Step 5：戴明安燈十重自動質檢與全渠道交付 (Decuple Andon Gate & Delivery)
通過十道物理安燈閘門（詳見第三章），輸出符合工業標準之成品並自動歸檔至 `00-14` 實體主權目錄。

---

## 🔬 第三章｜戴明安燈十道物理閘門 (The 10 Andon Gates)

任何海報成品必須通過以下十道自動化質檢（分數 $\ge 90$ 分通過，任一項一票否決即熔斷攔截）：

| 序號 | 安燈閘門名稱 | 物理檢驗標準 | 一票否決 (Red Line) |
| :--- | :--- | :--- | :--- |
| **G-01** | **K100 單色黑直壓** | 文字、細線、條碼強制為 $\text{C}0\text{ M}0\text{ Y}0\text{ K}100$ 並設定直壓 (Overprint)。 | 文字含 CMY 色版產生套印彩邊即否決。 |
| **G-02** | **總墨量 TAC 紅線** | 大面積黑底複色黑（$\text{C}40\text{ M}30\text{ Y}30\text{ K}100$）總墨量 $\le 250\%$。 | 總墨量 $> 250\%$ 導致合板印刷背印即否決。 |
| **G-03** | **紙張絲流壓痕防爆邊** | 紙張 $\ge 150\text{gsm}$ 摺頁標註壓痕 (Creasing)，摺痕平行於絲流 (Grain)。 | 厚紙摺頁未壓痕導致破裂即否決。 |
| **G-04** | **3mm 出血與裁刀公差** | 畫布四周預留 3mm 出血，文字離裁切線距離 $\ge 5\text{mm}$。 | 重要文字落入 3mm 裁切危險區即否決。 |
| **G-05** | **WCAG AAA 對比度** | 主文字與背景對比度 $\ge 7:1$（大字 UI $\ge 3:1$）。 | 文字對比度不足造成閱讀障礙即否決。 |
| **G-06** | **QR Code 物理秒掃** | 實體印刷寬度 $\ge 28\text{mm}$，四周預留 $\ge 4$ 模組 Quiet Zone 白邊。 | QR Code 小於 25mm 或無白邊即否決。 |
| **G-07** | **傳單 15% 拇指盲區** | A5/DM 傳單下方 15%（31.5mm）保留為安全留白區。 | QR Code 或電話落入拇指握持區即否決。 |
| **G-08** | **高齡 CSF 視力平權** | 長輩面向海報內文 $\ge 12\text{pt}$，齊左對齊，禁標楷細明與淺灰。 | 出現淺灰字配白底或標楷體即否決。 |
| **G-09** | **赫曼暗斑光學消除** | 網格線透明度 $\le 15\%$，交叉處圓角 $\ge 4\text{px}$ 或 18% 虛擬縫隙。 | 網格出現強烈側抑制暗斑鬼影即否決。 |
| **G-10** | **繁體避頭尾與錯字防呆** | 嚴守 18 個禁行首字元與 13 個禁行尾字元，標點懸掛外推 0.5em。 | 行首出現結束標點符號即否決。 |
| **G-11** | **品牌對外安全防線** | 海報對外文字絕對零出現「極星」，恪守法定品牌名稱與自稱。 | 出現「極星」二字一票否決，立即熔斷！ |

---

## 🛠️ 第四章｜確定性代碼向量引擎 CLI 規範 (Track A Specification)

極星系統內建之自動化海報渲染腳本位於：
👉 `00-14_Visual_Design_and_Poster_Craft/scripts/poster_artisan_cli.py`

### CLI 調用語法：
```bash
python 00-14_Visual_Design_and_Poster_Craft/scripts/poster_artisan_cli.py \
  --title "生活管家 · 代倒垃圾" \
  --subtitle "台東在地生活剛需服務 · 免追垃圾車" \
  --points "999 元包月服務|官方代收專業安全|每週固定排程收運" \
  --price "NT$ 999" \
  --anchor_price "NT$ 1,500" \
  --cta "即刻預約享早鳥優惠" \
  --qr_text "https://line.me/R/ti/p/@lifebutler" \
  --format "a4_print" \
  --style "duotone_vermilion" \
  --output_dir "00-14_Visual_Design_and_Poster_Craft/02_Posters_Archive/02_Trash_Collection"
```

### 支援格式規格 (--format)：
* `a4_print`: A4 實體印刷版 ($210 \times 297\text{mm}$ + 3mm 出血 = $216 \times 303\text{mm}$ @ 300 DPI, $2551 \times 3579\text{px}$)
* `a3_print`: A3 門市海報版 ($297 \times 420\text{mm}$ + 3mm 出血 @ 300 DPI)
* `ig_social`: Instagram / Facebook 直式圖卡 ($1080 \times 1350\text{px}$, 4:5)
* `reels_social`: Reels / 限時動態全屏圖卡 ($1080 \times 1920\text{px}$, 9:16，留出上下 15% 介面區)

### 支援色彩風格 (--style)：
* `bauhaus_classic`: 極星炭黑底 (`#1A1D20`) + 皓白文字 + 包浩斯朱紅 (`#E63946`)
* `duotone_vermilion`: 雙色調專色（深炭黑 + 專色朱紅，印刷成本降 50%）
* `kuroshio_gold`: 台東黑潮深藍 (`#1F3A52`) + 池上稻穗金 (`#D4A347`)
* `senior_high_contrast`: 高齡高對比純白底 + 炭黑大字 + 深紅標籤 (`#C1121F`)

---

## 🎨 第五章｜AI 大師級海報 Prompt 編譯規範 (Track B Specification)

當需要生成具備強烈情感感染力、電影級光影或 3D 空間感之品牌旗艦海報時，約瑟夫自動將文案編譯為**「約瑟夫包浩斯結構化 Prompt 矩陣」**：

```text
[System Role: Master Poster Artisan Josef Müller-Brockmann]
A masterpiece promotional poster for [Product/Service Name], Taiwanese New Bauhaus style, designed on a rigorous 12-column Swiss grid system.
Visual Structure:
- Top 30% Prime Fixation Zone: Prominent, bold Chinese typography hook "[Main Title]" in clean geometric sans-serif, perfect optical grayness balance and kerning.
- Center 40%: Minimalist, high-contrast visual icon/metaphor of [Key Metaphor, e.g. cleanly tied geometric trash bag with glowing ambient light / futuristic glowing abacus], dramatic chiaroscuro lighting, deep shadows.
- Bottom 30%: Structured 3-column modular value proposition cards, crisp legible pricing and clear CTA button, quiet zone surrounding QR code.
Cultural & Geometric Identity:
- Sacred geometric 8-pointed flower (Amis Falo) subtle corner markers with 45-degree rotational symmetry.
- Color Palette: 60% deep Kuroshio Slate Charcoal (#1A1D20 / #1F3A52), 30% Pure White (#F8F9FA), 10% vivid Bauhaus Vermilion Red (#E63946).
- Negative Space: 38% generous, elegant negative space creating architectural breathing room.
- Aesthetics: Ultra-clean, deterministic order, zero decorative clutter, international design award winner, 8k resolution, vector perfection.
```

---

## 🤝 第六章｜跨內閣橫向協同接口 (Cross-Cabinet Integration)

本協議與極星現有生態系統無縫銜接：
1. **銜接行銷長泰勒絲 (Taylor)**：接收經過字數定額的黃金文案，空間定格開版，杜絕字圖互斥。
2. **銜接財務長算盤 (Abacus)**：自動計算標準開本排廢率（$\le 2.8\%$），勞務服務強制推薦雙色調專色（節約 50% 製版印工）。
3. **銜接生活管家影 (Kage)**：海報產出後秒級同步至社群發布管線：
   * 調用 [`threads-publisher`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/.agents/skills/threads-publisher/SKILL.md) 與 [`facebook-publisher`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/.agents/skills/facebook-publisher/SKILL.md) 一鍵排程。
   * 調用 [`polaris-motion-reels`](file:///c:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/.agents/skills/polaris-motion-reels/SKILL.md) 注入 Ken Burns 緩動與微光呼吸，合成 9:16 短影音。
4. **銜接首席品質長戴明 (Dr. Deming)**：每張海報執行十道安燈閘門自動掃描，未達 90 分立即安燈拉繩阻斷。
