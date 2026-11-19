# 台東垃圾車即時雷達 · 全新視覺與互動工程落地規範 (TRASH RADAR REDESIGN SPEC)

> **設計主政**：首席視覺長 約瑟夫 (Josef)  
> **落地實作**：首席前端與客戶端架構師 尼奧 (Neo)  
> **決策依據**：創辦人（品碩）親定雷達大改版裁示 ✕ 常民風土色彩學 ✕ 戴明安燈出廠門禁  
> **對外法定品牌**：「生活管家，就醬點！」  
> **服務自稱**：「生活管家」  
> **文件版本**：v2.0-Production-Ready  
> **交付目標**：提供尼奧 100% 忠實還原、零歧義、可直接複製套用之 Design Tokens 與 CSS/HTML 互動架構。

---

## 1. 設計哲學與三大核心公理

### 公理一：乾淨一屏，拒絕 AI 塑料套版 (One Screen, Anti-Slop)
- **初始狀態絕對淨空**：開啟頁面時映入眼簾的是純淨、呼吸感充足的一屏空間。卡片區完全空白，**嚴禁**預載雜亂預設值、**嚴禁**自動跳出瀏覽器定位權限彈窗嚇阻長輩。
- **去除一切偽科技噪聲**：徹底摒棄廉價漸層、浮誇發光、無意義 3D 垃圾桶圖標與雜亂的儀表板。回歸 Figma 級精湛極簡排版，以純粹的文字階層與幾何秩序傳遞可靠感。

### 公理二：極限減法，零操作摩擦 (Zero-Friction Ergonomics)
- **大刀闊斧移除冗餘控件**：
  1. ❌ 移除時間輸入框、就是現在按鈕、快速時間按鈕（台東常民倒垃圾就是當下，無需複雜跨時段排程）。
  2. ❌ 移除「走路/騎車」切換開關（卡片直接同時運算「走路約 X 分 ｜ 騎車約 Y 分」，一目了然）。
  3. ❌ 移除手動打字地址輸入框（強光與顛簸下打字極具挫折感，改以一鍵定位＋8大生活圈兜底按鈕完全涵蓋）。
- **單一核心呼叫**：全屏視覺重心只有一顆極致醒目、熱區飽滿的「📍 幫我找垃圾車」主按鈕。

### 公理三：深色微縮，真實物理觸感 (Tactile Physics Feedback)
- 每一顆可點擊元件（按鈕、兜底標籤、導航卡）皆注入即時深色微縮（Darken & Scale Down）物理反饋，消除數位觸控的虛浮飄動感，給予使用者如實體機械開關般的清脆按壓反饋。

---

## 2. 全域 Design Tokens (常民風土色彩學與幾何和聲)

尼奧請將以下 CSS Custom Properties 直接置於全域樣式表頂層：

```css
:root {
  /* ==========================================================================
     常民風土色彩學 (Hyperlocal Palette) - WCAG AAA / AA 高對比規範 (>= 7:1)
     ========================================================================== */
  --color-primary: #0F2537;         /* 黑潮深藍：太平洋深海沉靜底色，主品牌標題、主按鈕、重點強調 */
  --color-primary-active: #081520;  /* 黑潮深藍 (按壓態)：微暗沈穩 */
  --color-accent: #E5A93B;          /* 池上金：熟成縱谷金黃稻穗，狀態標籤、重要數值突顯 */
  --color-accent-light: #FDF6E9;    /* 池上金淡背景：警示或提醒底色 */
  --color-alert: #D84A38;           /* 太麻里日出紅：晨曦高警示色，時間緊迫、預警、緊急備案 */
  --color-alert-light: #FDF0EE;     /* 太麻里日出紅淡背景：警示卡片底色 */
  --color-bg-base: #F8F9FA;         /* 暖米白：陽光曬過之石灰白地坪，柔和不刺眼，作為主背景 */
  --color-bg-card: #FFFFFF;         /* 純白：卡片實體表面，搭配高精細無階層微陰影 */
  --color-text-main: #1A1A1A;       /* 炭墨黑：正文、主要數值、深色清晰可讀 */
  --color-text-muted: #555555;      /* 次要字灰：輔助說明、站點距離、表定時間 (對比度 >= 5.5:1) */
  --color-border-subtle: #E2E8F0;   /* 微結構邊框：分隔線、無干擾弱邊界 */
  --color-focus-ring: #0F253733;    /* 焦點環：外光暈，輔助無障礙鍵盤/螢幕閱讀焦點 */

  /* ==========================================================================
     字階和聲 (Modular Scale 1.25 - Major Third)
     基線：16px / 1rem，台東長輩人因視力平權字級
     ========================================================================== */
  --font-family-base: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif;
  
  --font-size-xs: 0.8rem;     /* 12.8px：微型標籤、次要時間備註 (長輩介面絕對下限) */
  --font-size-sm: 0.875rem;   /* 14px：輔助描述、次要狀態、小按鈕 */
  --font-size-base: 1.0625rem;/* 17px：內文標準字級，高於市面 14/15px，兼顧老花視力 */
  --font-size-md: 1.25rem;    /* 20px：卡片副標題、次級站點名稱 */
  --font-size-lg: 1.5625rem;  /* 25px：主答案「去 [站名]」、核心時間倒數 */
  --font-size-xl: 1.953rem;   /* 31.25px：極限倒數分鐘、重要狀態宣告 */

  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-bold: 700;
  --font-weight-heavy: 800;

  /* ==========================================================================
     空間節奏與網格 (Spacing & Elevation Tokens)
     8px 基線步長，黃金留白率
     ========================================================================== */
  --space-xxs: 4px;
  --space-xs: 8px;
  --space-sm: 12px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;

  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --radius-full: 9999px;

  /* 物理深度：精緻無髒感雙層微陰影 */
  --shadow-card: 0 4px 16px -2px rgba(15, 37, 55, 0.06), 0 2px 6px -1px rgba(15, 37, 55, 0.04);
  --shadow-card-elevated: 0 12px 28px -4px rgba(15, 37, 55, 0.12), 0 4px 10px -2px rgba(15, 37, 55, 0.06);
  --shadow-button-primary: 0 6px 18px -2px rgba(15, 37, 55, 0.25);

  /* ==========================================================================
     微動態物理參數 (Micro-Kinetic Tokens)
     ========================================================================== */
  --transition-tactile: transform 0.08s cubic-bezier(0.2, 0, 0.13, 1), filter 0.08s ease;
  --transition-card-in: opacity 0.28s ease-out, transform 0.28s cubic-bezier(0.16, 1, 0.3, 1);
}
```

---

## 3. 視圖佈局與結構規範 (Layout & Grid Hierarchy)

### 3.1 視口約束與容器 (Mobile-First Shell)
- **最大寬度鎖定**：`max-width: 480px`，居中於桌面端，全滿適配手機端（左右邊界 padding: `20px`）。
- **背景底色**：全域底色 `--color-bg-base` (#F8F9FA)，確保戶外強光下具備足夠的紙本磨砂質感，防止眩光。

```html
<main class="radar-app-shell">
  <!-- 頂部品牌標題區 -->
  <header class="radar-header">
    <div class="brand-badge">生活管家</div>
    <h1 class="brand-title">生活管家，就醬點！｜ 台東垃圾車雷達</h1>
    <p class="brand-tagline">不追車、不空等 · 一鍵掌握到站倒數</p>
  </header>

  <!-- 核心觸控英雄區 (Hero Trigger) -->
  <section class="radar-hero-trigger">
    <!-- 主按鈕 min-height: 56px -->
  </section>

  <!-- 動態載入/狀態反饋區 -->
  <div id="radar-loading-container" class="radar-loading-container" aria-live="polite"></div>

  <!-- 主答案展示區 (Result Area - 初始完全淨空) -->
  <section id="radar-result-container" class="radar-result-container" aria-live="polite"></section>

  <!-- 8大生活圈兜底按鈕區 (Fallback Area) -->
  <section id="radar-fallback-container" class="radar-fallback-container"></section>

  <!-- 今日已收工 / 生活管家 999 包月卡片區 -->
  <aside id="radar-promo-container" class="radar-promo-container"></aside>
</main>
```

---

## 4. 關鍵互動狀態與元件視覺階層 (State Machine & Visual Flow)

### 狀態 0：開啟初始畫面 (State: Clean Screen)
- **畫面狀態**：卡片區與下方結果區為空白，乾淨清爽。
- **核心主按鈕**：
  - 文字：「📍 幫我找垃圾車」
  - 尺寸：高度 `min-height: 58px`，寬度 `100%`，圓角 `--radius-full`（或 `--radius-md` 16px）。
  - 色彩：底色 `--color-primary`（#0F2537），文字純白（#FFFFFF），字級 `--font-size-base`（17px）加粗。
  - 陰影：`--shadow-button-primary`。

### 狀態 1：按壓與載入中 (State: Pressed & Locating)
- **瞬間物理反饋**：
  ```css
  .btn-tactile:active {
    transform: scale(0.97);
    filter: brightness(0.9);
  }
  ```
- **過渡文字切換**：
  - 點擊後主按鈕立即設為 `disabled`，滑鼠游標設為 `wait`。
  - **階段 1（0 ~ 1.2 秒）**：按鈕內部文字轉換為「📡 定位中…」。
  - **階段 2（1.2 秒以上）**：按鈕內部文字切換為「🔍 搜尋附近垃圾車…」。
  - 載入指示：按鈕前方顯示簡潔 SVG 單色旋轉微環（禁止使用花俏彩虹進度條）。

---

### 狀態 2：主答案卡片成功呈現 (State: Master Answer Card)
> 💡 **這是使用者第一眼看見的核心結論，必須具備極高視覺穿透力（1.5 秒內完成「站名 ➔ 倒數 ➔ 導航」認知）。**

```html
<article class="master-answer-card">
  <!-- 頂部狀態列 -->
  <div class="card-status-bar">
    <span class="badge-status-live">● 即時動態連線</span>
    <span class="badge-distance">距您約 320 公尺</span>
  </div>

  <!-- 主目標站名 (視覺穿透點 A) -->
  <h2 class="target-station-title">
    去 <span class="station-name">鐵花文創聚落站</span>
  </h2>
  <p class="station-address">台東市鐵花路 371 號對面</p>

  <!-- 即時倒數與交通耗時 (視覺穿透點 B) -->
  <div class="arrival-time-block">
    <div class="primary-countdown">
      車約 <span class="countdown-num">6</span> 分鐘後抵達
    </div>
    <div class="transit-metric-row">
      <span class="metric-item">🚶 走路約 <strong>4</strong> 分</span>
      <span class="metric-divider">・</span>
      <span class="metric-item">🛵 騎車約 <strong>2</strong> 分</span>
    </div>
  </div>

  <!-- Google 地圖導航大按鈕 (視覺穿透點 C) -->
  <div class="card-action-block">
    <a href="https://www.google.com/maps/dir/?api=1&destination=22.753123,121.147890" 
       target="_blank" 
       rel="noopener noreferrer" 
       class="btn-nav-primary btn-tactile">
      🗺️ Google 地圖導航
    </a>
  </div>
</article>
```

#### 視覺樣式規範：
1. **站名階層**：`--font-size-lg`（25px），字重 `800`，字色 `--color-primary`。
2. **倒數分鐘**：數字部分採用 `--font-size-xl`（31px）或加粗，字色 `--color-alert`（太麻里日出紅，高能見度）。
3. **交通並列呈現**：**完全摒棄切換器**。以灰色字體同時列出「🚶 走路約 X 分・🛵 騎車約 Y 分」，讓使用者一眼判定要步行前往還是發動機車。
4. **導航按鈕**：
   - 樣式：底色 `--color-primary`（黑潮深藍），高度 `min-height: 52px`，圓角 `--radius-md`，字體純白 16px 加粗。
   - 連結格式：直接對齊標準 URL Schema `https://www.google.com/maps/dir/?api=1&destination={latitude},{longitude}`。

---

### 狀態 3：雙收情境卡片 (State: Dual Collection - 垃圾車 ✕ 回收車)
> 依據創辦人（品碩）親定裁示 B：卡片**直接並列兩時間**，清晰明白，嚴禁使用任何 Checkbox 或篩選折疊！

```html
<div class="dual-collection-banner">
  <div class="dual-stream-item stream-trash">
    <div class="stream-label">🗑️ 一般垃圾</div>
    <div class="stream-eta highlight">約 6 分鐘到</div>
    <div class="stream-source">GPS 即時連線</div>
  </div>
  <div class="dual-stream-divider"></div>
  <div class="dual-stream-item stream-recycle">
    <div class="stream-label">♻️ 資源回收車</div>
    <div class="stream-eta">表定 17:47 到</div>
    <div class="stream-source">定點表定班次</div>
  </div>
</div>
```
- **設計細節**：以雙欄並列排版，左右以細邊框 `--color-border-subtle` 分隔。
- 具備即時定位的車輛顯示深藍高亮與「約 X 分到」，非即時車輛顯示「表定 HH:mm」並標註資料來源。

---

### 狀態 4：裕度吃緊與無即時訊號警告 (State: Margin & Warning Triggers)

#### 4.1 裕度吃緊勉強備案 (Margin <= 3 分鐘)
當（垃圾車預估到站時間 － 使用者騎車抵達時間）<= 3 分鐘：
- 插入黃紅雙色警戒卡：
  ```html
  <div class="urgency-warning-card">
    <div class="warning-header">
      <span class="warning-icon">⚠️</span>
      <strong>這站時間有點緊迫！</strong>
    </div>
    <p class="warning-desc">您騎車前往約需 3 分鐘，車輛約 4 分鐘到站，裕度不足 1 分鐘。</p>
    <div class="alternative-station-box">
      <div class="alt-title">💡 建議從容考慮下一站：</div>
      <div class="alt-station-name">南京路市民廣場站</div>
      <div class="alt-time-meta">還有 <strong>16</strong> 分鐘 ｜ 騎車約 4 分鐘</div>
      <a href="https://www.google.com/maps/dir/?api=1&destination=22.756123,121.149890" 
         target="_blank" class="btn-alt-nav btn-tactile">
        改去這站導航 ➔
      </a>
    </div>
  </div>
  ```

#### 4.2 無 GPS 即時狀態警告
若該路線車輛未開啟 GPS 或處於訊號盲區：
- 卡片頂部置入太麻里日出紅醒目提示：
  > 「⚠️ 本班次目前為預估時間，台東市垃圾車可能因車流提早 10~15 分鐘抵達，**強烈建議提早 15 分鐘出門**至站點等候。」

---

### 狀態 5：定位失敗 / 拒絕之 8 大生活圈兜底按鈕 (State: 8 District Fallbacks)
當使用者瀏覽器阻擋 GPS 或定位逾時：
- 隱藏 loading，在主按鈕下方展開「8 大生活圈兜底按鈕矩陣」。
- 標題：「📍 點選您所在的生活圈，直接為您查車」
- 排版：雙欄 2 欄式網格（2 Columns Grid），按鈕高度 `min-height: 48px`。

```html
<div class="district-fallback-matrix">
  <div class="fallback-matrix-title">請選擇您目前所在的台東生活圈：</div>
  <div class="district-grid">
    <button type="button" class="btn-district btn-tactile" data-lat="22.755" data-lng="121.152">
      市區 / 寶桑
    </button>
    <button type="button" class="btn-district btn-tactile" data-lat="22.751" data-lng="121.146">
      鐵花 / 體育場
    </button>
    <button type="button" class="btn-district btn-tactile" data-lat="22.738" data-lng="121.139">
      東海 / 漢陽
    </button>
    <button type="button" class="btn-district btn-tactile" data-lat="22.744" data-lng="121.132">
      豐榮 / 豐谷
    </button>
    <button type="button" class="btn-district btn-tactile" data-lat="22.763" data-lng="121.121">
      豐年 / 康樂
    </button>
    <button type="button" class="btn-district btn-tactile" data-lat="22.772" data-lng="121.135">
      馬蘭 / 榮民醫院
    </button>
    <button type="button" class="btn-district btn-tactile" data-lat="22.788" data-lng="121.124">
      卑南 / 南王
    </button>
    <button type="button" class="btn-district btn-tactile" data-lat="22.705" data-lng="121.078">
      知本 / 建農
    </button>
  </div>
</div>
```

---

### 狀態 6：收工卡與 999 包月代倒入口卡 (State: EOD & Butler Promo Card)
當今日所有定點班次已全數收工離線（如晚間 21:00 後）：
1. **收工預報列表**：
   - 標題：「🌙 今日垃圾清運已結束」
   - 呈現明日或下一清運日的「前 5 筆早班/定點預報」。
2. **生活管家商業服務入口卡**（極致優雅、不唐突、直擊台東常民痛點）：

```html
<aside class="butler-service-card">
  <div class="service-pill">生活管家，就醬點！專屬服務</div>
  <h3 class="service-title">不想追垃圾車？讓生活管家替你天天搞定</h3>
  <p class="service-subtitle">
    下班太晚趕不上？長輩提重物不方便？台東市區專人定時到府收運。
  </p>

  <div class="service-tier-row">
    <div class="tier-box">
      <div class="tier-name">外圈彈性包月</div>
      <div class="tier-price">NT$ 999 <span>/月</span></div>
      <div class="tier-feat">週收 2~3 次 · 門前免等待</div>
    </div>
    <div class="tier-box highlighted">
      <div class="tier-badge">熱門首選</div>
      <div class="tier-name">全區專屬管家</div>
      <div class="tier-price">NT$ 1,999 <span>/月</span></div>
      <div class="tier-feat">週收 5 次 · 垃圾+回收全包</div>
    </div>
  </div>

  <div class="service-cta-block">
    <a href="https://lin.ee/example" target="_blank" rel="noopener noreferrer" class="btn-service-cta btn-tactile">
      💬 加 LINE 預約生活管家代倒
    </a>
    <p class="service-guarantee">✨ 經專業背景查核 ｜ 門前無接觸代倒 ｜ 安心守護</p>
  </div>
</aside>
```

---

## 5. 實體按鍵微動態與物理反饋規範 (Kinetic Engineering)

尼奧在實作 CSS 樣式時，請完整導入以下類別，確保全系統手感一致：

```css
/* ==========================================================================
   實體按鍵物理反饋規範 (Physical Tactile Tokens)
   ========================================================================== */
.btn-tactile {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-family-base);
  border-radius: var(--radius-md);
  cursor: pointer;
  border: none;
  text-decoration: none;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
  transition: var(--transition-tactile);
}

/* 按壓觸發：瞬間縮小 3% 並微降亮度 10%，模擬實體按鍵反饋 */
.btn-tactile:active {
  transform: scale(0.97) !important;
  filter: brightness(0.90) !important;
}

/* 焦點狀態 (無障礙) */
.btn-tactile:focus-visible {
  outline: 3px solid var(--color-accent);
  outline-offset: 2px;
}

/* 核心主按鈕 (Hero Button) */
.btn-hero-find {
  width: 100%;
  min-height: 58px;
  background-color: var(--color-primary);
  color: #FFFFFF;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-heavy);
  box-shadow: var(--shadow-button-primary);
  border-radius: var(--radius-full);
  padding: 0 var(--space-lg);
  letter-spacing: 0.5px;
}

.btn-hero-find:disabled {
  opacity: 0.85;
  cursor: wait;
}

/* 導航按鈕 (Navigation Button) */
.btn-nav-primary {
  width: 100%;
  min-height: 52px;
  background-color: var(--color-primary);
  color: #FFFFFF;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-bold);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
}

/* 8 大生活圈兜底按鈕 */
.btn-district {
  min-height: 48px;
  background-color: #FFFFFF;
  color: var(--color-text-main);
  border: 1px solid var(--color-border-subtle);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  padding: var(--space-xs) var(--space-sm);
  text-align: center;
}

.btn-district:hover {
  border-color: var(--color-primary);
  background-color: #F8FAFC;
}
```

---

## 6. 戴明品質驗收紅線 (Deming Andon Gatekeeper Checkpoints)

尼奧在發布代碼與部署前，請以本清單逐項驗收，未達標禁止出廠：

| 驗收項目 | 戴明品質標準 | 檢查方法 |
| :--- | :--- | :--- |
| **首屏一區塊** | 初次進入頁面時，卡片區 100% 空白，不可有虛構預設站點。 | 重新整理清空快取確認 |
| **物理反饋** | 所有按鈕在 `:active` 時必須有 `scale(0.97)` 與 `brightness(0.9)`。 | 行動裝置真機長按測試 |
| **按鍵熱區** | 所有可點擊按鈕高度必須 `>= 48px`（主按鈕 `>= 56px`）。 | DevTools Box-sizing 檢驗 |
| **文字對比度** | 主文字、站名與按鈕對比度嚴格 `>= 7:1`（次要文字 `>= 4.5:1`）。 | Chrome Lighthouse / Axe 檢驗 |
| **雙收呈現** | 回收日情境卡片直接並列兩時間，嚴禁 Checkbox。 | Mock API 資料確認 |
| **外部品牌合規** | 頁面抬頭及文案嚴格鎖定「生活管家，就醬點！」與「生活管家」，嚴禁洩漏極星內部字眼。 | 全文字串檢索 |
| **Google 導航** | 點擊導航必須精確帶入目標站點之經緯度座標。 | 真機點擊跳轉驗證 |

---

> **約瑟夫簽署結語**：  
> 本規範以台東常民在日烈天熱或夜暮下騎車、倒垃圾的第一視角鍛造。尼奧兄請完全以本規範為骨架，將目前舊引擎中瑣碎的輸入框、時間選取器與交通工具開關乾淨俐落地切除，重塑 Figma 級簡潔純粹的極致體驗！
