---
name: atom-fb-feed-dispatcher
description: 上傳多圖暫存池、組合貼文矩陣並執行即時或排程發布。在貼文通過安燈質檢後派發與第一留言秒發時使用；貼文內容質檢時不用。只由 facebook-publisher 呼叫，不單獨使用。
metadata:
  group: 發臉書
  parent: facebook-publisher
  owner: 林納斯
  status: draft
  version: "1.0"
---

# 🚀 Facebook 粉絲專頁多圖暫存與 Feed 派發底座原子技能 (FB Feed Dispatcher Atom)

> **核心職責**：專精於臉書粉專之「多圖 published=false 暫存池上傳、attached_media 矩陣組合、即時/排程雙模發布、第一留言秒發、貼文歷程自動歸檔」。  

---

## 核心功能與深度特性
1. **多圖暫存池與媒體附載 (Media Staging Pool)**：
   - 支援 1~10 張高清實拍照，以 `published=false` 模式平行或循序推播至粉專暫存池取得 `media_fbid`。
   - 自動將其封裝為 `attached_media[{i}]={"media_fbid":"..."}` 陣列，隨 Feed 貼文一次性優雅展開。
2. **即時發布與預約排程雙模 (Immediate & Scheduled Modes)**：
   - 即時模式：`published=True` 毫秒級推播至粉絲專頁。
   - 排程模式：`published=False` 搭配 `scheduled_publish_time` UNIX 時戳，由 Meta 伺服器精準定時公開。
3. **首留言秒級導流閉環 (First Comment Chaining)**：
   - 貼文成功取得 `post_id` 後，立即調用 `/comments` 端點發表 First Comment，確保顧客第一時間看見 LINE 訂單與門市資訊。
4. **自動歸檔與冪等防呆 (Archive Hook & Idempotency)**：
   - 每次成功發布或排程，自動向 `00-03_Brand_LifeButler/00-03-05_Brand_Content_Hub/00_Social_Posts_Master_Archive.md` 追加時戳、Post ID 與文案存證。
   - 支援 `--dry-run` 模式，在不耗損 API 配額下完整驗證請求 Payload 與歸檔邏輯。

---

## 執行腳本
```bash
python scripts/fb_feed_dispatcher.py --message "生活管家，就醬點！" --images "sample1.jpg" "sample2.jpg" --dry-run
```
