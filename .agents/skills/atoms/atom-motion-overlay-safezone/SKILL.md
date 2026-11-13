---
name: atom-motion-overlay-safezone
description: "短影音安全區避讓字幕與品牌動態覆層原子技能。專門針對 IG Reels、Threads 與 TikTok 嚴格精算社群 UI 安全邊界 (避開底部 350px 文案區與右側 120px 互動區)，壓制防眩暗角漸層、文字呼吸淡入淡出 (Fade In/Out)，並嚴格審查品牌法定名稱零洩漏防火牆。"
---

# 📱 短影音安全區避讓字幕與品牌動態覆層原子技能 (Motion Reels Overlay & Safe Zone Atom)

> **所屬技能組**：做短影音 / 視覺工匠  
> **核心職責**：專精於短影音之「社群 UI 安全區幾何避讓、防眩暗角覆層、字幕淡入淡出時間軸、品牌法定名稱零洩漏防火牆」。  
> **原技能母體**：`polaris-motion-reels`

---

## 核心功能與深度特性
1. **社群原生 UI 安全邊界避讓 (Social Safe Zone Guard)**：
   - 深入研究 Instagram Reels、Threads 與 TikTok 行動版 UI 覆蓋層。
   - 頂部避開 180px 狀態列與導航列、底部避開 380px 帳號與文案區、右側避開 140px 愛心/留言/轉發垂直按鈕列。
   - 保證字幕與主標題 100% 落在黃金安全矩形內，絕不被系統按鈕遮擋。
2. **防眩光暗角漸變 (Anti-Glare Dynamic Vignette)**：
   - 自動生成底部 28% 高度之平滑漸變暗角，抵抗背景明亮高光，使白字高對比清晰可讀。
3. **字卡淡入淡出動態時間軸 (Typography Fade-In/Out Timeline)**：
   - 首秒 (0~0.8s) 緩慢淡入、主體時段呼吸微震、結尾 (最後 0.5s) 溫柔淡出，提升觀看完成度與停留時長。
4. **品牌法定名稱零洩漏防火牆 (Brand Red Line Gate)**：
   - 出廠前強制文字審計，品牌署名必須為「生活管家，就醬點！ @hellotaitung」或「生活管家」，嚴禁對外出現內部代號「極星」。

---

## 執行腳本
```bash
python scripts/overlay_safezone.py --title "起鍋前的一圈米酒，是廚房最迷人的時刻" --duration 5.0 --dry-run
```
