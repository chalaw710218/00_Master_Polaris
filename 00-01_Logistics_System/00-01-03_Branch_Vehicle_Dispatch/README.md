# 📱 00-01-03 外送車次與即時調度系統 (Branch Vehicle Dispatch)

> **上級指針**：[`00-01-00 物流系統總綱`](../00-01-00_Logistics_System_Overview.md) ｜ [`00-03-03 營運白皮書 V3.0`](file:///C:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-03_Brand_LifeButler/00-03-03_Core_Whitepaper/00-03-03_LifeButler_Operations_Whitepaper_V3.0.md)  
> **核心目標**：整合 AppSheet、LINE 派單與林納斯 ESC/POS 雲端出單機，實現極簡高效率派單。

## 📌 規劃中核心模組：
1. **AppSheet 派單管理後台**：
   * 🔗 [Google Doc 原型紀錄](https://docs.google.com/document/d/1VGpsUDVcteloUXf8NGK92rNRHVXkdx60Q4nUWCuiew8/edit?usp=sharing)
   * 司機接單介面、訂單狀態回報（已取餐/配送中/已送達）。
2. **司機代墊款與薪資結算流水線**：
   * 現金收付每日核銷機制、油資與每單配送費自動累計。
3. **軟硬體閉環通訊**：
   * 對接 `00-09` 點餐後台，訂單成立秒級驅動後台熱感應印表機輸出工單。
