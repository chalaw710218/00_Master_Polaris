# 🎨 品牌全域標準色票 (Color Palette SSOT)
## Color System, Printing Limits & Design Tokens

> **主政首長**：約瑟夫·米勒-布羅克曼 (Josef) ✕ 尼奧 (Neo) ✕ 戴明 (Deming)  
> **適用載體**：健豪/藍格印刷送印、LINE OA 圖文選單、Tailwind CSS / 網頁 UI、FB/Threads 社群。

---

## 一、 品牌色彩矩陣一覽

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ 寶桑暖陽黃       │  │ 太平洋暖褐       │  │ 常民生活米白     │
│ #F5A623         │  │ #8B572A         │  │ #FAF8F3         │
│ C0 M38 Y95 K0   │  │ C30 M65 Y90 K25 │  │ C2 M2 Y4 K0     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ 墨黑直壓         │  │ 蔬果翠綠 (生鮮)  │  │ 炙熱熟成紅 (活動)│
│ #1A1A1A         │  │ #2E7D32         │  │ #D32F2F         │
│ C0 M0 Y0 K100   │  │ C80 M20 Y100 K15│  │ C15 M95 Y90 K5  │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## 二、 印刷物理鐵律 (Print Physics & TAC Limits)

### 1. 嚴禁四色黑，文字強制 K100 直壓
* ❌ **絕對禁止**：使用 Photoshop 預設的黑（如 `C75 M68 Y67 K90`）。在合版印刷下，四色套印會有微小物理震動，導致細小文字邊緣產生「彩虹重影」與模糊！
* ⭕ **唯一標準**：內文與標題黑字，印刷色值必須設定為 **`C:0 M:0 Y:0 K:100`**，並開啟「黑色直壓（Overprint Black）」，底色不挖空，字跡如刀削般銳利。

### 2. 總油墨覆蓋率（TAC）天花板
* **合版印刷最大極限**：$\text{TAC} = C + M + Y + K \le 250\%$。
* 當深色背景大面積超過 250% 時，印刷廠的油墨無法及時乾燥，裁切堆疊時會直接印染到上一張的背面，造成整箱印件報廢！

---

## 三、 數位開發者 Tokens (CSS & Tailwind Config)

### 1. CSS Custom Properties
```css
:root {
  /* Brand Core Colors */
  --color-brand-primary: #F5A623;    /* 寶桑暖陽黃 */
  --color-brand-secondary: #8B572A;  /* 太平洋暖褐 */
  --color-brand-ink: #1A1A1A;        /* 墨黑直壓 */
  --color-brand-canvas: #FAF8F3;     /* 常民生活米白 */

  /* Functional Accents */
  --color-brand-fresh: #2E7D32;      /* 蔬果翠綠 */
  --color-brand-alert: #D32F2F;      /* 炙熱熟成紅 */

  /* Surface & Border Neutrals */
  --color-border-subtle: #E8E4DA;
  --color-card-bg: #FFFFFF;
}
```

### 2. Tailwind CSS Config (tailwind.config.js)
```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#F5A623',
          secondary: '#8B572A',
          ink: '#1A1A1A',
          canvas: '#FAF8F3',
          fresh: '#2E7D32',
          alert: '#D32F2F',
        }
      }
    }
  }
}
```
