---
name: atom-threads-neighbor-crm
description: 🤝 Threads 在地友店聯盟與登門回禮原子微技能。專精管理台東在地 185 家友店名冊與常客互動帳本 (`friend_interactions.json`)。執行「80% 點亮微光足跡 + 20% 看見店家苦心深度走心留言」，並主動登門常客最新貼文留下真摯回訪禮，沉澱長效生活關係人口。
---

# 🤝 atom-threads-neighbor-crm · 在地友店聯盟與登門回禮原子

> **首長主政**：生活管家 影 (Kage)  
> **技術監製**：CTO 林納斯 (Linus)  
> **品質安燈**：首席品質長 戴明博士 (Dr. Deming)  
> **原屬解剖來源**：`threads-autonomous-walker` 【第二步：訪鄰居 + 2.3 登門回訪】  
> **單一核心責任**：**台東在地 185 家友店巡邏維護、常客回禮與好友互動帳本 (Social CRM) 沉澱**  

---

## 🎯 為什麼將其獨立為專精原子？
極星在台東深耕的根基，在於跟在地店家的「真實鄰里關係」。
本原子將所有公域推廣、原創發文徹底隔離開來，**專精且僅專注於「經營好友關係」**：
1. **好友帳本關係階梯**：管理 `data/friend_interactions.json`，精確記錄每一次拜訪的時間、累積互動次數與熟客等級。
2. **看見店家苦心**：拒絕空洞讚美，由生活管家視角針對烘焙發酵、慢火燉湯、手作紋理給予「懂行的人才說得出的敬佩」。
3. **登門回訪禮尚往來**：對常來自帳留言的讀者，主動前往對方客廳留言回禮，絕不讓善意落單。

---

## 💻 物理調用介面 (CLI Interface)

```bash
# 巡邏友店並更新好友帳本 (支援 dry-run)
python .agents/skills/atoms/atom-threads-neighbor-crm/scripts/neighbor_crm.py --dry-run
```
