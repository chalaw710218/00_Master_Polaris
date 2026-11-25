---
name: atom-care-telehealth-card
description: 生成瑞士網格外地兒女 3 分鐘安心聽診圖卡與醫囑速記。在長輩陪診或巡檢完畢回報家屬時使用；服務前派工排程時不用。只由 lifebutler-care-artisan 呼叫，不單獨使用。
metadata:
  group: 生活管家
  parent: lifebutler-care-artisan
  owner: 約瑟夫
  status: draft
  version: "1.0"
---

# 📱 外地兒女 3 分鐘孝親安心聽診圖卡生成原子技能 (Care Telehealth Card Atom)

> **核心職責**：專精於「瑞士網格行動端安心圖卡排版、核心醫囑結構化速記、生命徵象視覺化、醫療法規免責宣告、品牌法定名稱零洩漏防火牆」。  

---

## 核心功能與深度特性
1. **外地兒女 3 分鐘快速閱讀架構 (3-Minute Reassurance Grid)**：
   - 拒絕冗長報告，專為遠距上班族兒女設計行動端卡片：
     - 💚 **長輩狀態快速定錨**：今日氣色良好、精神飽滿。
     - 🩺 **生命體徵儀表板**：收縮壓/舒張壓 (mmHg)、脈搏心率 (bpm)、血糖/血氧。
     - 📝 **醫師關鍵叮嚀**：藥量微調、飲食禁忌、生活作息叮嚀。
     - ⏰ **重要時程提醒**：下次門診預約時間、健保慢性病連續處方箋領藥日期。
2. **醫療法規合規與免責條款 (Medical Regulatory Guardrail)**：
   - 底部強制標註法定免責宣告：「本報告由生活管家協助陪伴記錄，內容均為醫師現場口述與藥袋標示之忠實速記，管家不具醫療診斷行為，任何醫療決定請遵照主治醫師指示。」
3. **品牌法定名稱零洩漏防火牆 (Brand Red Line Gate)**：
   - 署名強制為「生活管家，就醬點！ 生活管家團隊」，嚴禁對外出現內部代號「極星」。
4. **乾跑防呆 (Dry-Run Support)**：
   - 支援 `--dry-run` 輸出結構化圖卡預覽與 Markdown/HTML 文本。

---

## 執行腳本
```bash
python scripts/care_telehealth_card.py --order-id CARE-20261113-01 --elder "陳阿公" --bp "128/82" --pulse 72 --doctor "台東馬偕 心臟內科 陳醫師" --notes "血壓控制理想，降血壓藥維持原劑量，叮嚀天氣變冷早起加件外套" --dry-run
```
