---
name: atom-neo-ergonomic-spin-tester
description: 首席前端與客戶端架構師尼奧·常民人機摩擦自對弈挑刺與自癒原子 (Neo Ergonomic Self-Play & Friction Triage Protocol v1.0)。落實創辦人親授「這是讓尼奧自主學習的唷！學習前端工程的」法旨！在前端交互設計中主動分裂出「75歲台東長輩」與「烈日機車外送員」極端視角，無情挑刺按鍵熱區（<48px）、強光對比度（<7:1）與繁瑣流程；並自主推導 PRM 狀態機與樂觀 UI（Optimistic UI）修復補丁！
role_key: neo
type: atomic_skill
parent_skill: bionic-learning-neo
version: v1.0
exit_code_verified: true
---

# 🎭 尼奧常民人機摩擦自對弈挑刺與自癒原子 (Neo Ergonomic SPIN Tester)

> 🕶️ **原子使命**：貫徹創辦人親授心法——**「這是讓尼奧自主學習的唷！學習前端工程的。」** 如果工程師只在冷氣房裡用最新款 iPhone 測試介面，做出來的前端在台東鄉間就是一場災難！本原子落實 UCLA SPIN 自對弈機制，尼奧自主化身挑剔的常民使用者，對自己的 UI 進行魔鬼挑刺，並自主合成出自動修復與狀態機補丁，讓介面真正實現零摩擦！

---

## 🏛️ 雙重極端常民自對弈視角 (Dual Extreme Personas)

```mermaid
flowchart TD
    UIComponent["前端組件 / 互動頁面 / LINE LIFF 流程"] --> SPIN{"🎭 尼奧 SPIN 自對弈挑刺法官 (ergonomic_spin_tester.py)"}
    
    SPIN --> P1["👵 視角 1: 75 歲台東獨居阿嬤\n• 手指微顫抖，眼力花，畏懼複雜設定\n• 挑刺: 『按鈕小於 48px 我按不到！』\n• 挑刺: 『字體小於 18px 我看不清！』"]
    
    SPIN --> P2["🛵 視角 2: 烈日下機車外送車手\n• 正午 12,000 Lux 烈日反光，機車把手震動\n• 挑刺: 『強光下白底淺灰字根本反白失明！』\n• 挑刺: 『防誤觸邊距小於 12dp 一震就誤點！』"]
    
    P1 & P2 --> Triage{"是否檢測到任何人機摩擦？"}
    Triage -->|發現摩擦缺陷| Patch["✨ 尼奧自主合成自癒補丁 (Self-Healing Patch)\n• 自動重設 min-h-[48px] 與 text-lg\n• 注入烈日 APCA 高對比度 Token 與 12dp slop"]
    Triage -->|零摩擦零缺陷| Pass["👑 人機工程 100% 驗收放行！"]
```

---

## 🧭 自對弈挑刺量化門禁 (Quantitative Thresholds)

| 檢驗指標 | 一般商業前端 | **極星常民人機自癒標準** | 違規自癒處置 |
| :--- | :--- | :--- | :--- |
| **觸控熱區** | 32px ~ 40px | **$\ge 48\times 48\text{dp}$** | 強制補正 `min-h-[48px] min-w-[48px]` |
| **正文字級** | 14px ~ 16px | **$\ge 18\text{px}$ (動作按鈕 $\ge 20\text{px}$)** | 提升至 `text-lg` / `text-xl` |
| **對比敏感度** | 4.5 : 1 (AA) | **$\ge 7.0 : 1$ (AAA) / APCA Lc $\ge 90$** | 色彩自動拉深至 `#1E1E1E` 炭黑 |
| **完成步數** | 5 ~ 7 步 | **$\le 3$ 步 (零多餘表單)** | 合併壓縮為三步極簡 Flow |

---

## 🛠️ 命令列工具 (CLI Usage)

```powershell
# 執行組件人機工程自對弈挑刺與自癒補丁生成
python scripts/ergonomic_spin_tester.py --audit-ui '{"component_name": "即時呼叫生活管家按鈕", "touch_target_dp": 38, "font_size_px": 15, "contrast_ratio": 5.2, "flow_steps": 4, "is_outdoor_sun": true}'
```
