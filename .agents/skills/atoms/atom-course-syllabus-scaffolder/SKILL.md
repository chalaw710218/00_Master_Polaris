---
name: atom-course-syllabus-scaffolder
description: 裝配實體小班工作坊 4 大硬參數、雙核課綱與 10 題防呆表單。在工作坊開課規格規劃與建表時使用；報名名冊審查與分流時不用。只由 polaris-course-master 呼叫，不單獨使用。
metadata:
  group: 開課營運
  parent: polaris-course-master
  owner: 雪
  status: draft
  version: "1.0"
---

# 🎓 實體工作坊教案規格與 10 題防呆表單裝配原子技能 (Course Syllabus & Form Scaffolder Atom)

> **核心職責**：專精於「實體小班工作坊 4 大硬參數設定 (每堂限額 6 席)、120m 雙核課綱裝配、10 題防呆 Google 表單 Schema 生成、招生文案與第一則留言置頂閉環」。  

---

## 核心功能與深度特性
1. **創辦人最新法旨：每堂嚴格限額 6 席 (Strict 6-Seat Cohort)**：
   - 拒絕大拜拜式走馬看花，確立「純實體 6 席極致手把手小班制」，確保每位學員 100% 解決自身業務資料痛點。
2. **四大硬參數與雙核課綱 (Four Hard Specs & Dual-Core 120m)**：
   - 席次：【純實體小班 · 每堂嚴格限額 6 席】。
   - 定價：全新夥伴單堂 NT$ 500 元 / 老學員勾選享 0 元免單回娘家。
   - 地點：生活管家家宅總部（台東市正氣北路166巷90號）。
   - 雙核課綱：14:00~15:00 核心精講 ＋ 15:00~16:00 巡桌手把手實作排錯（沒做出成品不准下課）。
3. **10 道防呆報名審查表單 Schema (10-Question Form Spec)**：
   - 自動生成標準 Google 表單結構：基本資料 ➔ 硬體環境必勾 (自備筆電/記得帳密/Chrome/充電器) ➔ 業務資料痛點 (菜單/進貨單/公文) ➔ 入席承諾 ＆ 額滿加開場意願。
4. **社群招生長文與第一則留言置頂 (Copy & First Comment Chaining)**：
   - 生成溫暖專業招生文案，第一則留言自動附載報名表單連結與正氣北路門市導航，零外連避免 FB 降權。

---

## 執行腳本
```bash
python scripts/course_syllabus_scaffolder.py --title "AI 實戰提效工作坊" --date "2026-11-25" --dry-run
```
