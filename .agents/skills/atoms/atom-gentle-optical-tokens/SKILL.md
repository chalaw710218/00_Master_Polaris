---
name: atom-gentle-optical-tokens
description: 🌸 極星常民生活設計系統·光學符記與高齡對比度審計原子 (Polaris Gentle UI Optical Tokens & APCA Audit Atom v1.0)。專門將常民與高齡介面之文字對比度、光學灰度平衡 (橫細豎粗 1:1.18 補償)、風土大地色系與無感微透明度，全自動編譯並嚴格審計 APCA Lc >= 75（對應 WCAG AAA 超越標準）之 CSS 設計變數。
---

# 🌸 極星光學符記與高齡對比度審計原子 (atom-gentle-optical-tokens)

由首席前端與客戶端體驗架構師尼奧 (Neo) 業務主政、首席視覺長約瑟夫 (Josef) 光學審定、CTO 林納斯 (Linus) 確定性代碼驗收。

## 核心定位與職責
專門解決常民、長輩在強光（台東縱谷 130,000 Lux 烈日）或高齡晶狀體黃化弱光下「看字吃力、反光刺眼、字體發虛」之痛點。
以「APCA (Advanced Perceptual Contrast Algorithm) 視力平權 ✕ 菲克垂直水平錯覺補償 ✕ 台東風土大地色系」為底層，產出工業級可直接套用的 `gentle-ui.css`，並具備色彩對比度硬核物理門禁。

## 輸入參數規範
- `--primary-color`: 主色代碼（HEX，預設縱谷深稻黃金 `#4A3E1B` 或太平洋石墨藍 `#1E2B37`）
- `--bg-color`: 背景色代碼（HEX，預設暖米紙白 `#FBF9F5` 或常民柔夜黑 `#181A1B`）
- `--surface-mode`: 模式 (`light` 或 `dark`，預設 `light`)
- `--optical-ratio`: 筆畫橫細豎粗補償比（預設 `1.18`，依約瑟夫中文字型光學法典）
- `--output-css`: 產出 CSS 檔案路徑（預設 `gentle-ui-tokens.css`）
- `--dry-run`: 物理演練模式，不寫入實體檔案僅回傳驗算報告

## 執行腳本
```bash
python scripts/optical_tokens.py --surface-mode light --dry-run
```
