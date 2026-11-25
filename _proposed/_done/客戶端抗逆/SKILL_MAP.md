# 🗺️ 極星宇宙全內閣技能全景地圖 (SKILL MAP)

> ⚠️ **本檔由 `skill_scanner.py` 自動產生，請勿手改**  
> 執行者：**執行長 雪 (Yuki)** ｜ 依據：《00-00 極星格式規範 v1.0》  
> 現役技能總數：**3** 份（已排除鏡像 **0** 份、封存 **0** 份）  
> 技能組總數：**1** 組 ｜ 未歸類技能：**0** 份

---

## 📑 技能組索引目錄 (Group Directory)

1. [客戶端抗逆](#客戶端抗逆) (3 個技能)
2. [未歸類技能組（獨立/未標註技能）](#未歸類技能組獨立未標註技能) (0 個技能)

---

<a id="客戶端抗逆"></a>
## 🧩 技能組：客戶端抗逆

| 技能名稱 (Name) | 狀態 | 相對路徑 (Path) | 一句話用途 (Description) | 原技能母體 |
| :--- | :--- | :--- | :--- | :--- |
| **`atom-client-offline-heartbeat`** | `draft` | [atom-client-offline-heartbeat/SKILL.md](atom-client-offline-heartbeat/SKILL.md) | 生成離線 Service Worker 心跳、本地優先存證與雙層快取。在前端建立離線韌性與本地存證機制時使用；網路傳輸隊列重放時不用。只由 polaris-client-architect 呼叫，不單獨使用。 | `polaris-client-architect` |
| **`atom-client-resilient-transport`** | `draft` | [atom-client-resilient-transport/SKILL.md](atom-client-resilient-transport/SKILL.md) | 管理極限弱網傳輸、離線待發隊列與冪等靜默重放狀態機。在暴雨弱網斷線排隊與網路恢復依序上傳時使用；本地 UI 渲染時不用。只由 polaris-client-architect 呼叫，不單獨使用。 | `polaris-client-architect` |
| **`polaris-client-architect`** | `draft` | [polaris-client-architect/SKILL.md](polaris-client-architect/SKILL.md) | 建構前端極限抗逆架構、離線心跳與斷線隊列重放機制。在開發與架構 WebApp、PWA 與 LIFF 客戶端時使用；後端伺服器運維時不用。 | - |

---

<a id="未歸類技能組獨立未標註技能"></a>
## 📦 未歸類技能組（獨立/未標註技能）

| 技能名稱 (Name) | 狀態 | 相對路徑 (Path) | 一句話用途 (Description) |
| :--- | :--- | :--- | :--- |
