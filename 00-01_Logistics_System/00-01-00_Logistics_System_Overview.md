# 🚚 00-01 寶桑物流與車隊交付系統 (Logistics System) 總綱

> **戰略定位**：生活管家「三端一體」之**物流交付端 (The Delivery Terminal)**  
> **最高母法遵循**：[`00-03-03 營運白皮書 V3.0`](file:///C:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-03_Brand_LifeButler/00-03-03_Core_Whitepaper/00-03-03_LifeButler_Operations_Whitepaper_V3.0.md) 第 3.3 節  
> **法定組織實體**：寶桑物流生活商行（合規承攬車隊）  
> **主管幕僚與技術支持**：工程長 林納斯 (Linus CTO) ✕ 市場情報長 獵鷹 (Falcon CIO) ✕ 創辦人陳品碩親率

---

## 🌊 零、 核心使命與 Bawsa 精神

寶桑物流不是普通的跑腿車隊，而是深深植根於台東土地的**「生活動脈與最後一哩路履約網絡」**。
* **文化根基**：傳承阿美族「Bawsa」海祭慰勞男子的包容、分享與關懷精神，把剛起鍋的熱便當、安心新鮮的生鮮好食材，親手送進每位台東鄉親家門。
* **社會價值**：落實白皮書四大理念之**「好營生」**（保障在地司機合理彈性收入）與**「同質等價」**（消滅偏鄉外送被加價剝削的不平等）。

---

## 🏛️ 一、 系統架構與外部雲端資產指針 (External Resource Pointers)

為避免跨對話框資訊孤島，本戰區核心技術與營運資產完整映射如下：

1. **📱 寶桑車隊 AppSheet 派單與結算系統 (原型)**：
   * 🔗 [Google Doc 企劃與資料結構全紀錄](https://docs.google.com/document/d/1VGpsUDVcteloUXf8NGK92rNRHVXkdx60Q4nUWCuiew8/edit?usp=sharing)
   * **功能範疇**：AI 自動進件、GPS 經緯度座標追蹤、外送員薪資與代墊款自動核銷、公司抽成試算。
2. **📦 家宅＋團購落地計劃書 (原始定稿版)**：
   * 🔗 [Google Doc 計畫書全文](https://docs.google.com/document/d/16gIJYl4QAKjxukbYu6LuuiEA87LZnNuy/edit?usp=sharing)
   * **功能範疇**：冷鏈集單交付、站點合單與保冷箱配給規範。
3. **⚖️ 外送專法合規與解耦防線 (林納斯 ✕ 獵鷹推演定案)**：
   * 🔗 [外送專法合規母法與施行細則指針](file:///C:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-00_External_Resource_Index.md#L101-L108)
   * **戰略避險決策**：在法律架構上，生活管家脫離「外送平台業者」框架，將點餐 SaaS（`00-09`）部署於店家端，寶桑物流定位為「傳統第三方物流 (3PL) ＋ 免費 SaaS 供應商」，免除 45 元底薪與非自願失業金沉重法遵成本。

---

## 📂 二、 轄下分支與執行重點 (Sub-Branches)

```
00-01_Logistics_System/
├── 00-01-00_Logistics_System_Overview.md      # [本文件] 車隊總綱與外鏈指針
├── 📁 00-01-01_Branch_Tariff_Update            # 4/1 起收費標準調整專案 (市區里程、梯級定價與疊單規則)
├── 📁 00-01-02_Branch_Route_Dulan              # 東海岸都蘭路線擴展 (定時定點巡迴配送與鄉鎮中繼站)
└── 📁 00-01-03_Branch_Vehicle_Dispatch         # 外送車次與即時調度系統 (AppSheet / LINE 通知 / 雲端出單機)
```

1. **`00-01-01_Branch_Tariff_Update`**：
   * 專注於定價透明化。打破傳統雙平台高抽成，制定市區基本運費、跨區里程加價與社區集單減免方案。
2. **`00-01-02_Branch_Route_Dulan`**：
   * 專注於城鄉動脈串聯。台東市區 $\leftrightarrow$ 都蘭/東河之固定班次班車，解決沿海偏鄉居民採買不易痛點。
3. **`00-01-03_Branch_Vehicle_Dispatch`**：
   * 串接 `00-09` 林納斯的 ESC/POS 出單機硬體驅動，店家接單即時印出兩聯派工單，司機掃碼領單起跑。

---

## 🔗 三、 跨戰區協作流向 (Inter-Project Workflows)

* **上游輸入源**：`00-09` (店家線上點餐訂單) ＋ `00-02` (團購生鮮到貨分裝通知)。
* **下游交付點**：`00-08` (家宅實體站點自取 / 集中配送) ＋ 消費者住家門前。
* **發布與宣傳**：`00-03-05` 內容母庫（調度 `#寶桑物流代送中` 喵編文案）。
