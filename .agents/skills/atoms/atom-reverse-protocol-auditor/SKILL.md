---
name: atom-reverse-protocol-auditor
description: 🔬 北極星核心技術研究室·網路通訊協議簽名逆向與硬證據審計原子 (Polaris Reverse Engineering Protocol Auditor Atom v1.0)。由 CTO 林納斯 (Linus) 確定性架構主政。專門解析 API 或 HAR 網路請求頭之 Timestamp、Nonce、Authorization 與動態簽名 (X-Sign/Signature)，精確逆推出雜湊加密拼裝算法 (如 HMAC-SHA256 / MD5 Salt)，並產出具備代碼與封包佐證之標準七章節《00-11-XX 逆向拆解審計報告.md》。
---

# 🔬 極星網路通訊協議簽名逆向與硬證據審計原子 (atom-reverse-protocol-auditor)

由 CTO 林納斯 (Linus) 業務主政、首席黑色調查官渡鴉 (Raven) 情報協同。

## 核心定位與職責
專門解決調研第三方系統、私域通訊協定或競品 API 時「請求帶有防篡改簽名無法重放、參數混淆看不清、分析報告缺乏硬證據空談架構」之痛點。
本原子作為協議逆向與審計報告產出終端，提供：
1. **簽名演算法逆推推演**：輸入 Headers 樣品與 Payload，自動對比測試 MD5、SHA256、HMAC 拼裝字典，還原加密公式（如 `sign = md5(appKey + nonce + ts + body)`）。
2. **端點路由與未混淆參數萃取**：提取 API Endpoints、鑑權模式（Bearer / Cookie / Custom Header）與狀態碼映射。
3. **七大章節硬證據報告編譯**：導出嚴格格式化、具備真實代碼佐證的《00-11-XX 逆向拆解審計報告.md》，包含可直接執行的 Python 重放腳本原型。

## 輸入參數規範
- `--target-id`: 標的編號（如 `00-11-14_SampleTarget`）
- `--sample-headers-json`: 請求頭樣品 JSON（含 `X-Sign`, `X-Timestamp`, `X-Nonce`）
- `--output-report`: 產出審計報告路徑（預設在標的根目錄）
- `--dry-run`: 物理演練模式，模擬簽名還原推演並輸出審計報告預覽

## 執行腳本
```bash
python scripts/protocol_auditor.py --target-id 00-11-14_SampleTarget --dry-run
```
