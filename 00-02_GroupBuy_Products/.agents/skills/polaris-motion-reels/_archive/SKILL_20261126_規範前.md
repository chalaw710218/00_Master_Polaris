---
name: polaris-motion-reels
description: >-
  極星微動態短影音自動合成引擎。以 Python 與 FFmpeg 為底層，將靜態高清食材照、生活攝影與 AI 角色定裝照，自動轉譯為具備 Ken Burns 視差緩動、微光呼吸感、氛圍漸層與動態字卡之 5~15 秒直式 9:16 短影音（MP4），專為 Threads、Instagram Reels 與 TikTok 高頻發布而生。
---

# 🎬 極星微動態短影音自動合成引擎 (Polaris Motion Reels)

> **版本**：v1.0 (影專屬視覺動態版)  
> **所屬模組**：北極星全域社群矩陣 (Polaris Social Matrix)  
> **核心使命**：突破靜態圖文的演算法天花板，將極星高精度的生鮮食材照、小編生活照與產地風土紀實，全自動合成為具備好萊塢推軌運鏡與環境呼吸感的 9:16 直式微短影音（MP4）。

---

## 🎯 什麼時候使用本技能？

當創辦人（品碩）或小編需要：
1. **靜態轉短影音**：「把剛才生成的這張煎午仔魚照片做成 6 秒的 Reels 短影音！」
2. **多運鏡動態展示**：對同一張圖片進行 `zoom_in`（緩慢推近特寫）、`zoom_out`（拉遠全景）、`pan_up`（向上搖鏡）、或 `breathing`（微光呼吸節奏）。
3. **自動壓上文字與品牌浮水印**：自動生成底部暗角漸變、精美中文標題與 `@hellotaitung` 官方品牌標識。

---

## 💻 執行指南與命令

核心合成腳本位於 `scripts/generate_motion_reel.py`：

### 1. 基礎直式 Reels 合成 (9:16，預設緩慢推鏡)
```powershell
python ".agents/skills/polaris-motion-reels/scripts/generate_motion_reel.py" --image "圖片路徑.jpg" --duration 6.0 --text "台東的海風，今天也是安靜的陪著大家 ☕"
```

### 2. 煎魚特寫呼吸感運鏡 (微動呼吸)
```powershell
python ".agents/skills/polaris-motion-reels/scripts/generate_motion_reel.py" --image "午仔魚.jpg" --motion "breathing" --duration 5.0 --text "起鍋前的一圈米酒，是整個廚房最迷人的時刻 🔥"
```

### 3. 正方形貼文影音 (1:1，適合 Threads / IG 走心隨筆)
```powershell
python ".agents/skills/polaris-motion-reels/scripts/generate_motion_reel.py" --image "生活照.jpg" --aspect "1:1" --motion "zoom_out" --duration 5.0
```

---

## 🛠️ 支援運鏡模式 (Motion Presets)

* `zoom_in`：Ken Burns 緩慢推近（放大 15%），極適合美食香氣、細節特寫。
* `zoom_out`：緩慢拉遠，營造從細節展開至廣闊台東風景的豁然開朗感。
* `pan_up`：由下往上搖鏡，適合人物立繪與直式建築/老屋視角。
* `breathing`：細微的正弦波呼吸縮放，讓靜止畫面呈現彷彿正在呼吸的生命力。

---

## 📁 影音產出規範

* **解析度規格**：
  * 直式 `9:16`：1080 × 1920（高相容性 MP4）
  * 正方形 `1:1`：1080 × 1080
  * 橫式 `16:9`：1920 × 1080
* **編碼規格**：H.264 (yuv420p)，確保各廠牌手機與所有社群平台秒速加載播放。
* **產出歸檔**：`output/` 目錄。
