---
name: atom-linus-security-sandbox
description: 資安金庫隔離與進程沙盒獵殺原子 (Zero-Trust Secret Vault & Process Sandbox Atom)。專門為工程長林納斯 (Linus) 執行資安與進程治理終極鐵律（Laws 11~15）：本地金庫 AES-256-GCM 隔離、Git Pre-Commit 私鑰零洩漏門禁、Google RE2 線性正則 DFA（根除 ReDoS）、爬蟲 Playwright 30s 獵殺與 85MB 記憶體硬限制、以及 Wasm 權能隔離。
---

# 🛡️ atom-linus-security-sandbox (資安金庫隔離與進程沙盒獵殺原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-learning-linus`（第六章資安與進程治理防線 · Laws 11~15）  
> **核心職責**：專門執行「零信任本機私鑰隔離、Git Commit 提交前機密物理防漏門禁、RE2 線性時間正則檢驗（杜絕 ReDoS 回溯漏洞）、無頭爬蟲進程獵殺（SIGKILL ✕ 85MB 內存限制）、以及 Wasm 模組沙盒隔離」。

---

## 核心設計哲學：林納斯資安與治理五大鐵律 (Laws 11~15)

1. **本機金庫隔離律 (Zero-Trust Secret Vault Law)**：
   * 配置以 AES-256-GCM 本地加密儲存；Pre-Commit 檢查在提交前 100% 物理阻斷私鑰、API Token 外洩。
2. **cgroups v2 容器硬限制 (Rootless Container Law)**：
   * 外部不可信腳本在 Rootless 容器中運行，記憶體硬限制鎖死在 250MB，爆炸半徑 100% 受控。
3. **Google RE2 正則律 (Deterministic Regular Expression Law)**：
   * 正則表達式全面遷移至 RE2 / 線性時間 DFA 引擎，杜絕指數級回溯（ReDoS）癱瘓 CPU。
4. **爬蟲進程獵殺律 (Headless Process Killer Law)**：
   * 瀏覽器 Context 週期重啟，子進程 30 秒逾時強制獵殺（SIGKILL），常駐記憶體鎖死在 85MB 以內。
5. **Wasm 模組沙盒律 (Wasm Edge Sandbox Law)**：
   * 三方插件運行於 Wasm 沙盒，0.05ms 極速啟動，嚴格權能 (Capability) 隔離。

---

## 執行腳本與參數

專屬腳本位於 `scripts/linus_security_sandbox.py`。

### 命令行介面 (CLI)

```bash
python scripts/linus_security_sandbox.py --scan-secrets "sample_code.py"
python scripts/linus_security_sandbox.py --audit-regex "(a+)+b"
```

### 核心參數
- `--scan-secrets`：掃描指定檔案或字串，檢查是否存在 API 金鑰、私鑰或敏感 Token。
- `--audit-regex`：審計特定正則表達式，檢測是否存在災難性回溯（ReDoS）隱患。
- `--dry-run`：預演模式。
