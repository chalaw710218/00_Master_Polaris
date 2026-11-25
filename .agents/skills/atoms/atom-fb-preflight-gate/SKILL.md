---
name: atom-fb-preflight-gate
description: 審查臉書內文零外部連結、抽離第一留言導流與品牌紅線。在臉書發布前防降權質檢與排程窗口驗證時使用；API 實際推送時不用。只由 facebook-publisher 呼叫，不單獨使用。
metadata:
  group: 發臉書
  parent: facebook-publisher
  owner: 戴明
  status: draft
  version: "1.0"
---

# 🛑 Facebook 貼文防降權與品牌紅線安燈原子技能 (FB Post Preflight & Anti-Downgrade Gate Atom)

> **核心職責**：專精於臉書發文前的「貼文內文防降權審計 (零外部 URL)、第一留言導流自動抽離封裝、品牌法定名稱零洩漏防火牆、排程時間窗口合規性」。  

---

## 核心功能與深度特性
1. **內文零外連防降權機制 (Anti-Downgrade Gate)**：
   - Meta 演算法對內文含有外部網址 (`http://`, `https://`, `bit.ly`, `lin.ee`) 的貼文會施加 50%~80% 曝光懲罰。
   - 本原子自動檢測並將文案中的所有外部網址抽離，同時在內文末端置換為高情商引導詞：「👉 預約訂購與門市資訊，管家已整理在【第一則留言】中，點擊即可直達！」。
2. **第一則留言 (First Comment) 導流自動封裝**：
   - 將抽離出的 LINE 官方帳號、門市自取地址與訂購網址，標準化封裝為專屬的第一則留言 Payload，確保貼文發布後能被秒級派發。
3. **品牌法定名稱零洩漏防火牆 (Brand Red Line Gate)**：
   - 出廠前強制掃描文案與留言，嚴禁對外出現內部代號「極星」或「Polaris」；官方品牌名稱強制維持「生活管家，就醬點！」或自稱「生活管家」。
4. **排程時間合規審查 (Schedule Window Check)**：
   - 若為預約排程，驗證時間是否符合 Meta 規定之「當前時間 10 分鐘以上，且不超過 75 天」。支援自然語言或 ISO 時戳。

---

## 執行腳本
```bash
python scripts/fb_preflight_gate.py --text "新鮮夏雪芒果直送！訂購請點 https://lin.ee/z83YSq6" --dry-run
```
