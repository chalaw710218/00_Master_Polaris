# 🤖 Threads 自動化發布與回覆機腳本庫 (Automation Scripts)

> **主掌幹部**：工程長 林納斯 (Linus, CTO)  
> **技術架構**：Meta Threads API 官方官方整合模組。

---

## 🛠️ 開發計畫與模組規劃

1. **`threads_publisher.py`**：
   * 支援將 Markdown 文字一鍵調用 Threads API 發布純文字脆文。
   * 與 `one-shot-photo-marketer` 全域行銷發射台進行跨平台派發整合。
2. **`threads_replier_bot.py`**：
   * Webhook 監聽貼文底下新留言。
   * 自動調用 LLM ＋ 喵編專屬 Persona，30 秒內自動產生溫暖、接梗回覆。
3. **配置指南**：
   * 需於 Meta for Developers 建立 Threads API 應用程式，並將 Access Token 安全寫入 `.secrets.env`（嚴禁上傳 GitHub）。
