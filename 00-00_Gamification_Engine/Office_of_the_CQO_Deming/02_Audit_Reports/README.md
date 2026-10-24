# 🗃️ 戴明品質審計報告歸檔庫 (Deming Audit Reports Vault)

> **定位**：極星全域重大交付物之結構化品質審計報告實體歸檔目錄。  
> **規範**：每一份通過戴明質檢的產物，皆在此存有唯一流水編號之 Markdown 審計憑證。

---

## 📋 命名規範

`AUD-YYYYMMDD-XXX_[業務領域]_[專案縮寫].md`

例如：
* `AUD-20261025-001_Pricing_MealDelivery.md`
* `AUD-20261025-002_Social_EdamameLaunch.md`
* `AUD-20261025-003_Code_CalendarSync.md`

---

## 🛡️ 審計狀態標記
* `[PASSED] ✅`：綜合評分 $\ge 90$ 分，無觸犯任何致命紅線，准予發布或合併。
* `[ANDON BLOCKED] 🚨`：綜合評分 $< 90$ 分，或觸犯致命紅線，觸發安燈繩物理阻斷，強制整改。
