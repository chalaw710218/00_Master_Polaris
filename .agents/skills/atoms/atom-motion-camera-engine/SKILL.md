---
name: atom-motion-camera-engine
description: 精算電影級運鏡軌跡、平滑緩動曲線與視差逐幀渲染。在微動態短影音運鏡設計與 MP4 編碼輸出時使用；安全區排版時不用。只由 polaris-motion-reels 呼叫，不單獨使用。
metadata:
  group: 做短影音
  parent: polaris-motion-reels
  owner: 約瑟夫
  status: draft
  version: "1.0"
---

# 🎥 短影音微動態鏡頭運鏡軌跡與逐幀渲染原子技能 (Motion Reels Camera Engine Atom)

> **核心職責**：專精於短影音之「電影級運鏡軌跡精算、Ease-In-Out 平滑緩動、多比例智能裁切、逐幀 LANCZOS 高清視差採樣與 MP4 編碼」。  

---

## 核心功能與深度特性
1. **電影級 Ease-In-Out 緩動軌跡 (Kinetic Trajectory Interpolation)**：
   - 拒絕死板等速平移，採用三次多項式或正弦波緩動，實現開頭緩慢啟動、中間流暢過渡、結尾優雅收尾的專業推軌運鏡。
2. **四重專業運鏡預設 (Motion Presets)**：
   - `zoom_in`：香氣與細節推鏡（放大 15%~25%），適合美食特寫與職人手藝。
   - `zoom_out`：風景與格局拉遠，從微觀細節展開至廣闊風土全景。
   - `pan_up`：垂直由下往上搖鏡，適合直式人物立繪、建築與職人身影。
   - `breathing`：低頻正弦波微光呼吸節奏，賦予靜態人物或食材活生生的生命力。
3. **多比例智能畫布裁切 (Canvas Aspect Ratio)**：
   - 直式 `9:16` (1080x1920) 專為 IG Reels、Threads 與 TikTok。
   - 正方形 `1:1` (1080x1080) 專為貼文卡片。
   - 橫式 `16:9` (1920x1080) 專為 YouTube 與大螢幕展示。
4. **工業級編碼與乾跑防呆 (Encoding & Dry-Run)**：
   - 支援 `--dry-run` 毫秒級預算每幀坐標與縮放倍率，驗證軌跡連續性。
   - 實體編碼使用 H.264 (yuv420p)，確保各廠牌行動裝置零黑屏、零延遲。

---

## 執行腳本
```bash
python scripts/camera_engine.py --image "input.jpg" --motion "zoom_in" --duration 5.0 --aspect "9:16" --dry-run
```
