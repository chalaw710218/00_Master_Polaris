# 🔤 字體階層與光學比例尺 (Typography Scale)
## Optical Gray Balance & Inclusive Readability

> **主政首長**：約瑟夫·米勒-布羅克曼 (Josef) ✕ 尼奧 (Neo) ✕ 戴明 (Deming)  
> **核心標準**：繁體漢字光學灰度平衡 ✕ WCAG 2.1 AAA 級長輩平權對比度。

---

## 一、 字體家族規範 (Font Stack)

### 1. 中文字體標準
* **主要指定字型**：**思源黑體 (Source Han Sans TW / Noto Sans TC)**
  * 開源、跨平台一致、筆畫骨架均稱、字重齊全（ExtraLight 至 Heavy）。
* **系統替代字型（Fallbacks）**：
  * Windows：微軟正黑體 (Microsoft JhengHei)
  * macOS / iOS：PingFang TC (蘋方-繁)
  * Android：Noto Sans CJK TC

### 2. 西文與數字專用字型
* **主要指定字型**：**DIN Next / Barlow Semi-Condensed / Inter**
  * 數字修長俐落、千分位逗點分明、價格衝擊力強。

---

## 二、 光學比例尺矩陣 (Modular Type Scale · 1.250 Major Third)

本比例尺採用古典音樂調和比例 $1.250$ 倍率（大三度階梯），確保字級跳躍自然且具備鮮明節奏感：

| 階層層級 | 標記名稱 | 印刷字級 (A4) | 數位字級 (Web/App) | 字重 (Weight) | 行距 (Line Height) | 應用情境與任務 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Hero / H0** | 巨幅標題 | $48\text{ pt}$ | $48\text{ px}~(3\text{ rem})$ | Heavy (900) | $1.20$ | 3公尺吸睛主標、特大數字 |
| **Title / H1** | 大標題 | $36\text{ pt}$ | $36\text{ px}~(2.25\text{ rem})$ | Heavy (900) | $1.25$ | 海報主標題、活動核心口號 |
| **Section / H2**| 中標題 | $24\text{ pt}$ | $24\text{ px}~(1.5\text{ rem})$ | Bold (700) | $1.35$ | 區塊分類、產品名稱、三大好處 |
| **Subhead / H3**| 小標題 | $18\text{ pt}$ | $18\text{ px}~(1.125\text{ rem})$ | Bold (700) | $1.40$ | 卡片標題、重要提醒、表格欄頭 |
| **Body / P** | 正文內文 | $12\text{ pt}$ | $15\text{ px}~(0.9375\text{ rem})$ | Medium (500) | **$1.70$ (長輩呼吸)** | 產品描述、長文說明、服務介紹 |
| **Caption / C** | 輔助說明 | $9\text{ pt}$ | $12\text{ px}~(0.75\text{ rem})$ | Regular (400) | $1.50$ | 法律免責、備註、營養成分微字 |
| **Price / Num** | 價格專用 | $28\text{ pt}$ | $32\text{ px}~(2\text{ rem})$ | DIN Bold (800) | $1.10$ | 醒目價格標籤（加 $ 符號微縮） |

---

## 三、 約瑟夫微排版三大光學戒律

1. **菲克垂直水平錯覺補償（橫細豎粗）**：
   * 繁體漢字的橫向筆畫在肉眼感知上會比豎直筆畫顯得粗重。排版大標時，筆畫較密之漢字（如「靈、醬、罐」）需給予更多內部負空間，嚴防大墨塊死黑。
2. **懸掛標點避頭尾（Hanging Punctuation）**：
   * 逗點、句號、冒號嚴禁出現在行首！
   * 標點符號統一採用半形空格微調，避免全形標點在版面右緣留下突兀的大空洞。
3. **行距是長輩的救命氧氣**：
   * 內文中文行距嚴禁低於 $1.65$ 倍！字距稍微外放 $+50\text{ pt}$，徹底消除長輩視線跳行與疲倦感。

---

## 四、 前端開發者 Tokens (CSS Variables by Neo)

```css
:root {
  /* Font Families */
  --font-sans: 'Source Han Sans TW', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif;
  --font-mono: 'DIN Next', 'Barlow Semi-Condensed', 'Inter', monospace;

  /* Font Sizes */
  --text-h0: clamp(2.5rem, 5vw, 3.5rem);
  --text-h1: clamp(1.875rem, 3.5vw, 2.5rem);
  --text-h2: clamp(1.25rem, 2vw, 1.75rem);
  --text-h3: 1.125rem;
  --text-body: 1rem;
  --text-caption: 0.8125rem;

  /* Line Heights */
  --leading-tight: 1.2;
  --leading-normal: 1.4;
  --leading-relaxed: 1.75; /* 常民友善行距 */
}
```
