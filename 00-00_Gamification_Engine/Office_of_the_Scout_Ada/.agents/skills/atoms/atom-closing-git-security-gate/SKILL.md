---
name: atom-closing-git-security-gate
description: 🌙 極星收工閉環·資安脫敏審查與 Git 閉環推送原子 (Polaris EOD Git Security Gate Atom v1.0)。由 CTO 林納斯 (Linus) 代碼主政、首席品質長戴明 (Dr. Deming) 安燈監製。專門在每日收工時盤點 Git 異動檔案，嚴格審查未授權明文 API Token 與個人私密資訊，確認機密目錄 (00-07, 00-11) 受 .gitignore 隔離保護，並組裝標準 chore(daily) 格式化 Commit 訊息完成遠端同步閉環。
---

# 🌙 極星收工資安脫敏審查與 Git 閉環推送原子 (atom-closing-git-security-gate)

由 CTO 林納斯 (Linus) 業務主政、首席品質長戴明 (Dr. Deming) 安燈監製、執行長雪 (Yuki) 營運協同。

## 核心定位與職責
專門解決每日收工提交代碼時「不慎將含有 API 金鑰、客戶私密資料或內部機密代號（如 00-11 逆向實驗室）推送到 GitHub 雲端」之重大資安事故。
本原子作為收工前的終極物理安全閘門，提供：
1. **未受保護敏感檔案盤點**：檢查 `git status`，確保商業機密專案（`00-07`、`00-11`）未脫離 `.gitignore` 的防護罩。
2. **明文金鑰與 Token 脫敏掃描**：以正則表達式快速掃描當日異動內容，攔截任何明文憑證（如 Google API Key, GitHub Token, 私密金鑰）。
3. **優雅 Commit 訊息組裝**：自動提煉今日核心推進成果，組裝格式如 `chore(daily): YYYY-MM-DD daily closing - [里程碑摘要]`，確保 GitHub 時間軸乾淨專業。

## 輸入參數規範
- `--check-only`: 僅執行資安掃描，不執行提交
- `--custom-summary`: 自訂今日核心成果摘要（留空則自動提煉）
- `--dry-run`: 物理演練模式，輸出資安查核結果與預擬 Commit 訊息

## 執行腳本
```bash
python scripts/git_security_gate.py --dry-run
```
