# 🛡️ 參考卷二｜全域安全機制：三態熔斷器、無鎖追加、十輪衝突審計與 RFC 協議

> **定位**：本文件為 `bionic-learning-system` 母版之附屬安全規範（`references/02_rfc_and_circuit_breaker_spec.md`），定義跨進程熔斷、Append-Only 雜湊鏈、十輪審計與母版 RFC 升級程序。

---

## 1. 磁碟持久化三態熔斷器 (Persistent Circuit Breaker · RFC #001)
實作於 `bionic_core/perceive_web.py`，狀態儲存於 `vaults/_circuit_breaker.json`：
- **CLOSED（正常通行）**：失敗計數 `< 3`。
- **HALF-OPEN（警戒試探）**：單次或兩次連線失敗，記錄失敗計數。
- **OPEN（強制熔斷）**：同一網域連續失敗 `>= 3` 次，立即鎖定 `open_until = now + 60s`，跨 CLI 進程強制阻斷連線，防止無限重試卡死。

---

## 2. 無鎖 Append-Only 雜湊鏈帳本 (Lock-Free Hash-Chained JSONL)
所有規則庫（`{office}_rules.jsonl`）、輪次帳本（`{office}_cycles.jsonl`）與派工帳本（`yuki_dispatch.jsonl`）：
- **嚴禁覆寫歷史行**：一律以 `"a"` 模式追加單行 JSON。
- **防竄改雜湊鏈**：每筆事件攜帶前一筆之 `prev` 雜湊與當前規範化內容之 `hash`（SHA-256）。任何事後改動中間行之行為皆會導致 `verify_chain` 斷鏈報警。

---

## 3. 十輪強制停機與程式化衝突大審計 (Decadal Conflict Audit)
實作於 `bionic_core/cycle_ledger.py`：
1. **去時間戳防刷輪次**：`tick()` 對 JSON 憑證自動剝離 `executed_at`, `ts`, `learned_at` 等時間戳欄位後計算規範化 SHA-256；若實質內容未變，拒絕入帳。
2. **滿 10 輪強制停機**：每滿 10 輪自動寫入 `{office}.AUDIT_REQUIRED.lock`，期間 `enforce.gate` 與 `tick` 全面阻斷（Fail-Closed）。
3. **程式化掃描解鎖 (`audit-scan` & `audit-done`)**：
   - 必須執行 `audit_scan(office)` 檢查：
     - **矛盾比對**：同一詞彙是否同時出現在 `forbid_phrase` 與 `prefer_phrase`。
     - **互斥掃描**：`prefer_phrase` 是否被 `regex_forbid` 攔截，或同指標 `metric_min > metric_max`。
     - **淘汰清單**：列出 `tampered_rejected`、TTL 到期或驗算轉負之規則。
   - 規則庫存在未解決之矛盾或互斥時，`audit_done` 強制拒絕解鎖。

---

## 4. 母版 RFC 向心升級協議 (Master RFC Protocol)
- 母版（`SKILL.md` 與 `bionic_core/`）為唯讀通用底座，任何閣員子版不得直接覆寫。
- 若子版在實戰中驗證出可通用於全閣的底層機制，須提交《Master RFC 升級提案》，經創辦人（陳先生 / 品碩 / 董事長）批准後，始得將舊版封存至 `_master_history/` 並發布新版本號。
