---
name: atom-client-offline-heartbeat
description: "客戶端本地優先存證與 Service Worker 離線心跳原子技能。由尼奧與林納斯監製，專門為 WebApp、PWA 與 LINE LIFF 應用，一鍵生成具備『本地優先 (Local-First) 寫入即確認』與『雙層 SLRU 緩存 Service Worker (sw.js)』之離線抗逆套件。當裝置斷網時，自動攔截請求並渲染生活管家溫潤安撫介面（『別擔心，交代的事都妥妥記在手機裡了』），徹底終結白屏崩潰，並嚴格遵循品牌法定名稱零洩漏防火牆。"
---

# 🛡️ 客戶端本地優先存證與 Service Worker 離線心跳原子技能 (Client Offline Heartbeat Atom)

> **所屬技能組**：客戶端抗逆 / 尼奧前端工匠  
> **核心職責**：專精於「本地優先 (Local-First) 寫入即確認、雙層 SLRU 緩存 Service Worker 套件生成、斷網溫暖安撫介面、品牌法定名稱零洩漏防火牆」。  
> **原技能母體**：`polaris-client-architect`

---

## 核心功能與深度特性
1. **本地優先寫入即確認 (Local-First Persistence Guarantee)**：
   - 用戶提交委託或下單時，優先寫入 IndexedDB / OPFS 本地專屬私有存儲，寫入耗時 $\le 16\text{ ms}$。
   - 本地存證成功即在 UI 呈現「已妥善記錄」，將網路延遲與超時徹底排除在第一線體驗路徑之外。
2. **雙層 SLRU 緩存架構 Service Worker (`sw.js`)**：
   - **Protected Cache (核心命脈)**：核心離線靜態資源、生活管家徽章、字體永久駐留。
   - **Probationary Cache (動態內容)**：商品圖片、動態資訊自適應汰換。
3. **溫暖斷網生還介面 (`offline.html`)**：
   - 當 `navigator.onLine === false` 時，自動優雅接管，呈現溫潤常民安撫語句：
     > **「別擔心，您交代的事管家都妥妥記在手機裡了。等風雨停了、訊號通了，第一時間替您送出。」**
4. **品牌法定名稱零洩漏防火牆 (Brand Red Line Gate)**：
   - 審查 Service Worker 註冊資訊、頁面 Title 與離線安撫文案，絕對禁止出現「極星」內部代號，全稱強制為「生活的一部分，就醬點！」。

---

## 執行腳本
```bash
python scripts/offline_heartbeat.py --app-name "生活管家 點餐與預約" --output-dir "pwa_dist" --dry-run
```
