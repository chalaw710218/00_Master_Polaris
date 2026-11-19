# 🛠️ 48 小時超高速全自動團購閉環系統代碼庫 (scripts/)

> **架構總監**：工程長 林納斯 (Linus, CTO)  
> **系統使命**：實現從「臉書商品抓取 ➔ 顧客秒開下單 ➔ 秒級拋單店家 ➔ 客服推播通知取貨」的 100% 全自動化管線！

---

## ⚙️ 核心腳本規劃清單

1. `fetch_facebook_groupbuy_products.py`：
   - 抓取指定臉書粉專/社團商品圖文與報價，自動結構化解析為 JSON 資料庫。
2. `render_groupbuy_post_matrix.py`：
   - 串接泰勒絲文案與約瑟夫 4:5 圖卡，一鍵產出發布排程矩陣。
3. `order_dispatcher_to_merchants.py`：
   - 截單時自動匯總訂單，透過 Telegram Bot / LINE Notify / 雲端出單機自動拋送採購清單給合作店家與產地。
4. `pickup_notification_sentinel.py`：
   - 貨物抵達掃碼入庫後，自動觸發 LINE 官方帳號私訊，向顧客發送取貨代碼與外送進度。