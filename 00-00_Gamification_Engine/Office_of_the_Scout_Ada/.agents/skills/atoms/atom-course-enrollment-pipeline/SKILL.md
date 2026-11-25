---
name: atom-course-enrollment-pipeline
description: 審查名額三軌分流、發送日曆邀請、24h RSVP 點名與現場驗收。在學員報名後名額調度與課前課後履約時使用；初期課綱規劃時不用。只由 polaris-course-master 呼叫，不單獨使用。
metadata:
  group: 開課營運
  parent: polaris-course-master
  owner: 雪
  status: draft
  version: "1.0"
---

# 🎟️ 學員名額審查分流與 24h-RSVP 履約閉環底座原子技能 (Course Enrollment Pipeline Atom)

> **核心職責**：專精於「報名名冊三軌分流 (正取 6 名 / 備取 2 名 / 第二梯次加開庫)、Google 日曆邀請 Payload 生成、課前 24h RSVP 點名機制、備取自動遞補、現場 DOD 驗收閉環」。  

---

## 核心功能與深度特性
1. **名額三軌精確分流 (Strict 6-Seat Pipeline)**：
   - 輸入表單報名學員清單，依「硬體準備度全勾」與「資料代表性」排序：
     - **第 1~6 名**：【正取 6 席】（發送 Google 日曆正式邀請函）。
     - **第 7~8 名**：【備取 2 席】（發送備取就緒通知，進入 24h 遞補隊列）。
     - **第 9 名以後**：【第二梯次加開庫】（自動歸檔為加開場 VIP 優先保證名單）。
2. **Google Calendar API 邀請 Payload 自動生成**：
   - 提取正取 6 名之 Email 核心憑證，自動封裝為 `attendees=[{"email": "..."}]`。
   - 活動地點自動設定為「台東市正氣北路166巷90號 (生活管家總部)」，自動開啟 24 小時與 2 小時前推播提醒。
3. **課前 24 小時 RSVP 點名與無痛遞補 (RSVP Check-in & Auto-Fill)**：
   - 課前一天上午 11:00 發送點名確認，若有正取學員請假或逾時未確認，系統自動將備取 1 號無痛升級為正取，發送即刻進場通知，保證現場 6 席 100% 滿座率。
4. **現場 DOD (Definition of Done) 驗收標準**：
   - 現場實作 60 分鐘：沒做出完整自動化成品不准下課，當場拍照存證並預約下一講席位。

---

## 執行腳本
```bash
python scripts/course_enrollment_pipeline.py --input-csv "applicants_sample.csv" --dry-run
```
