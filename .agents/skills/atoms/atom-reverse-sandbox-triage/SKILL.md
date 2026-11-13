---
name: atom-reverse-sandbox-triage
description: 🔬 北極星核心技術研究室·逆向工程沙盒拓荒與多格式解包原子 (Polaris Reverse Engineering Sandbox Triage Atom v1.0)。由 CTO 林納斯 (Linus) 確定性架構主政。專門在 00-11 實驗室下自動偵測下一個流水號並建立獨立隔離沙盒 (00-11-XX_<目標>/target, extracted, analysis_notes)，依據標的類型 (Web/JS, Electron asar, HAR 封包, Android APK) 分流解包，堅決杜絕主倉庫 Git 污染。
---

# 🔬 極星逆向工程沙盒拓荒與多格式解包原子 (atom-reverse-sandbox-triage)

由 CTO 林納斯 (Linus) 業務主政、首席科技偵察官艾達 (Ada) 協同。

## 核心定位與職責
專門解決逆向工程實驗中「多個標的混淆在同一個目錄、解包產物過大污染 Git 主倉庫、標的格式未經檢驗直接暴力處理」之痛點。
本原子作為逆向實驗室入口總控，提供：
1. **獨立沙盒拓荒**：自動巡視 `00-11_Reverse_Engineering_Lab/`，計算下一個流水號（如 `00-11-03`），建立具備 `target/`, `extracted/`, `analysis_notes/` 之標準隔離環境。
2. **標的分類檢驗 (Triage)**：識別 Web 前端、Electron JS、HAR 網路封包或二進位 APK，輸出對應工具鏈與解包建議。
3. **主倉庫 Git 隔離防呆**：在沙盒內自動產生 `.gitignore`，防止大型解包臨時檔案進入主版本庫。

## 輸入參數規範
- `--target-name`: 目標名稱（如 `TastyIgniter`, `LocalDeliveryApp`）
- `--target-type`: 目標類型 (`web_js`, `electron`, `har_traffic`, `android_apk`, `auto`，預設 `auto`)
- `--base-lab-dir`: 實驗室目錄路徑（預設 `00-11_Reverse_Engineering_Lab`）
- `--dry-run`: 物理演練模式，不寫入實體磁碟僅輸出拓荒規格與路徑計算

## 執行腳本
```bash
python scripts/sandbox_triage.py --target-name DeliveryPartner --target-type har_traffic --dry-run
```
