---
name: atom-client-resilient-transport
description: 管理極限弱網傳輸、離線待發隊列與冪等靜默重放狀態機。在暴雨弱網斷線排隊與網路恢復依序上傳時使用；本地 UI 渲染時不用。只由 polaris-client-architect 呼叫，不單獨使用。
metadata:
  group: 客戶端抗逆
  parent: polaris-client-architect
  owner: 林納斯
  status: draft
  version: "1.0"
---

# ⚡ 極限弱網穿透傳輸與斷線重放隊列原子技能 (Client Resilient Transport & Outbox WAL Atom)

> **核心職責**：專精於「離線 Outbox WAL 狀態機、斷網自動排隊防丟單、網絡恢復靜默依序重放、冪等防重扣機制、弱網傳輸遙測」。  

---

## 核心功能與深度特性
1. **離線待發隊列 WAL 狀態機 (Write-Ahead Logging Outbox)**：
   - 狀態流轉：`QUEUED (本地已排隊)` ➔ `SYNCING (同步中)` ➔ `COMMITTED (雲端確認入庫)` / `RETRY_BACKOFF (指數退避等待)`。
   - 保證斷網期間用戶連續提交 10 筆操作，無一丟失，按時間戳嚴格 FIFO 排隊。
2. **冪等性防重複機制 (Idempotent Key Engine)**：
   - 每筆事務自帶唯一客戶端生成的 `idempotency_key = sha256(order_id + timestamp)`。
   - 雲端即便重複接收到重試封包，保證只執行一次扣款與派工，徹底消除弱網重複發射風險。
3. **網絡心跳感知與自動重放 (Auto-Replay on Reconnect)**：
   - 監聽 `online` 事件，當網絡信號恢復時，不需用戶手動刷新，自動在背景啟動隊列重放，完成平滑同步。
4. **乾跑防呆 (Dry-Run Support)**：
   - 支援 `--dry-run` 模擬「正常在線 ➔ 突發斷網 ➔ 離線累計 3 筆訂單 ➔ 網絡恢復 ➔ 隊列自動重放清空」全生命週期，Exit Code 0 擔保。

---

## 執行腳本
```bash
python scripts/resilient_transport.py --simulate-offline --queue-items 3 --dry-run
```
