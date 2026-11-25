---
name: atom-neo-web-vitals-autophagy
description: 首席前端與客戶端架構師尼奧·前端效能遙測與肥大依賴自噬原子 (Neo Web Vitals & Dependency Autophagy Protocol v1.0)。落實創辦人親授「這是讓尼奧自主學習的唷！學習前端工程的」法旨！以客觀物理效能指標（FCP < 0.5s、INP < 100ms、CLS == 0、Bundle < 50KB）為學習真值天平；啟動溶酶體代謝自噬機制，自主掃描並殘酷剃除肥大無用的 npm 依賴（如 moment.js、全量 lodash），死守極端輕量化與 280ms 首屏加載！
role_key: neo
type: atomic_skill
parent_skill: bionic-learning-neo
version: v1.0
exit_code_verified: true
---

# ⚡ 尼奧前端效能遙測與依賴自噬原子 (Neo Web Vitals Autophagy)

> 🕶️ **原子使命**：貫徹創辦人親授心法——**「這是讓尼奧自主學習的唷！學習前端工程的。」** 一個優秀的前端工程師不是看他裝了多少套件，而是看他在面對任何功能時，能否用最精簡、甚至零依賴的原生代碼實現！本原子落實極星溶酶體代謝自噬機制：以 Google Core Web Vitals 為冷酷物理法官，主動獵殺肥大 npm 套件，守死首屏 280ms 載入與極端低碳低耗！

---

## 🏛️ 效能物理指標與依賴自噬架構 (Performance & Autophagy)

```mermaid
flowchart TD
    ClientApp["前端專案 / 依賴套件庫 (package.json)"] --> AuditEngine{"⚡ 尼奧效能與依賴審計引擎 (web_vitals_autophagy.py)"}
    
    AuditEngine --> M1["1. Core Web Vitals 物理指標審查\n• FCP < 0.5s (首屏秒現)\n• LCP < 1.2s (最大內容渲染)\n• INP < 100ms (點擊互動無延遲)\n• CLS == 0.0 (版面零跳動位移)"]
    
    AuditEngine --> M2["2. 溶酶體依賴自噬獵殺 (Dependency Autophagy)\n• 偵測肥大套件 (例: moment.js 72KB)\n• 推薦原生替代 (例: 原生 Intl.DateTimeFormat 0KB)\n• 偵測全量 import (例: lodash 24KB ➔ 原生 Array 0KB)"]
    
    M1 & M2 --> Action["✂️ 自動執行依賴自噬剪枝，挽回客戶端載入效能！"]
```

---

## 🧭 肥大套件自噬替代對照表 (Autophagy Replacement Table)

| 肥大待自噬套件 | 體積 (gzip) | **尼奧原生自噬替代方案** | 節省體積 (Savings) |
| :--- | :--- | :--- | :--- |
| `moment.js` | ~ 72 KB | **原生 `Intl.DateTimeFormat`** | **- 72 KB (100% 降解)** |
| `lodash` (全量) | ~ 25 KB | **現代 ES6+ 原生方法 (Map/Filter/Set)** | **- 25 KB (100% 降解)** |
| `axios` | ~ 13 KB | **原生 `fetch` API** | **- 13 KB (100% 降解)** |
| `uuid` | ~ 3 KB | **原生 `crypto.randomUUID()`** | **- 3 KB (100% 降解)** |

---

## 🛠️ 命令列工具 (CLI Usage)

```powershell
# 審查前端效能指標與套件依賴自噬機會
python scripts/web_vitals_autophagy.py --audit-performance '{"fcp_sec": 0.45, "lcp_sec": 1.1, "inp_ms": 68, "cls": 0.0, "dependencies": ["moment", "lodash", "react", "tailwindcss"]}'
```
