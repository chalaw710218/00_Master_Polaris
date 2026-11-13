---
name: atom-groupbuy-cost-auditor
description: "商品供應鏈底價逆推與食安背調底座原子技能。專門在管家選品前，依據商品零售市價或廠商報價，精確拆解產地出貨價、大宗原料、冷鏈物流與耗損摩擦成本，逆推廠商真實毛利率與極限底價，排查負面食安背景，並生成老闆專用之高情商談判議價話術。"
---

# 🔬 商品供應鏈底價逆推與食安背調底座原子技能 (Groupbuy Cost Auditor Atom)

> **所屬技能組**：選品審計 / 算盤財務工匠  
> **核心職責**：專精於「市場批發/零售行情審計、供應鏈極限成本逆推、廠商真實毛利拆解、食安合規檢驗、高情商議價籌碼話術」。  
> **原技能母體**：`sharp-groupbuy-analyzer`

---

## 核心功能與深度特性
1. **供應鏈摩擦成本逆向拆解 (Supply Chain Cost Decomposition)**：
   - 輸入商品報價或市價（如生鮮、腰果、肉品），自動拆解：產地出貨價 (40%~55%)、大宗原料與包材損耗 (10%~15%)、冷鏈物流與倉儲 (8%~12%)、廠商大盤毛利 (25%~35%)。
   - 計算極限進貨底價 (Floor Price) 與安全議價空間 (Negotiation Buffer)。
2. **高情商採購談判話術 (High-EQ Supplier Negotiation Script)**：
   - 提供老闆在面對供應商時的專業話術：以台東實體門市通路、固定週週結清、冷鏈完整與高回購社群影響力為籌碼，爭取第一線大盤底價。
3. **食安與廠商合規檢核 (Food Safety Compliance Check)**：
   - 檢核工廠登記、產銷履歷、SGS 檢驗與負面新聞排查，確保生活管家嚴選品質。
4. **乾跑防呆 (Dry-Run Support)**：
   - 支援 `--dry-run` 模擬成本拆解與報告生成，提供完整 JSON 與 CLI 輸出。

---

## 執行腳本
```bash
python scripts/groupbuy_cost_auditor.py --product-name "越臺鹽焗帶皮腰果 500g" --retail-price 380 --quote-price 250 --dry-run
```
