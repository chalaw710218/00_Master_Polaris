---
name: atom-flywheel-launch-cockpit
description: "創辦人極簡決策卡組裝與一鍵審批發射台原子技能。專門將各流水線產出之文案、5D 定價、海報與工單成果，精煉組裝為創辦人（品碩）專用之『3 秒極簡決策卡』(含業務類型、預覽文案、單元經濟/利潤、戴明出廠狀態)。內建品牌法定名稱零洩漏出廠熔斷閘門 (嚴禁對外出現極星)，創辦人僅需回覆『核准』或『批准』，即可秒級直連全網自動推播。"
---

# 🚀 創辦人極簡決策卡組裝與一鍵審批發射台原子技能 (Flywheel Launch Cockpit Atom)

> **所屬技能組**：飛輪總控 / 創辦人決策總樞紐  
> **核心職責**：專精於「流水線戰果極簡提煉、創辦人三秒決策卡組裝、品牌法定名稱零洩漏出廠熔斷、一鍵批准全網派發閉環」。  
> **原技能母體**：`polaris-flywheel-orchestrator`

---

## 核心功能與深度特性
1. **消滅發散碎碎念 · 創辦人 3 秒極簡決策卡 (3-Second Executive Card)**：
   - 拒絕向創辦人丟出動輒數千字的混亂長文。
   - 嚴格標準化四欄位展示：
     - 📌 **業務類別**：管家選品 / 生活服務 / AI 教育 / 商業調查。
     - 📝 **對外文案預覽**：前 100 字核心金句與第一則留言導流。
     - 💰 **單元經濟與利潤**：進貨底價、定價、單份毛利率、代墊風控等級。
     - 🛡️ **戴明出廠門禁**：安燈質檢分數 (100/100)、品牌防火牆 (通過)。
2. **品牌法定名稱零洩漏出廠熔斷閘門 (Zero-Leakage Brand Redline)**：
   - 出廠前強制做全域掃描，若對外預覽文案出現「極星」或「Polaris」，**立即拉繩熔斷 (Exit Code 1)**，嚴禁半成品或違規品推到創辦人面前。
3. **一鍵審批全網派發閉環 (One-Click Launch Dispatcher)**：
   - 當創辦人輸入「核准」或「批准」時，自動分發至對應發布原子：
     - 選品/文案 ➔ 直連 `atom-fb-preflight-gate` ➔ `atom-fb-feed-dispatcher` 與 Threads。
     - 孝親/跑腿 ➔ 直連 `atom-care-order-dispatcher` 派單。
4. **乾跑防呆 (Dry-Run Support)**：
   - 支援 `--dry-run` 模擬全流程驗證，輸出標準決策卡與 Exit Code 0 擔保。

---

## 執行腳本
```bash
python scripts/flywheel_launch_cockpit.py --pipeline "groupbuy" --title "越臺鹽焗帶皮腰果 500g" --price 340 --profit 92 --copy "天然低溫慢焗，保留原果薄皮與酥脆口感..." --dry-run
```
