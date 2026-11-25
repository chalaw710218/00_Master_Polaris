---
name: atom-colab-session-guardian
description: ⚡ 極星 Google Colab 算力生命週期與防浪費守護原子 (Polaris Colab Session Guardian Atom v1.0)。由 CTO 林納斯 (Linus) 確定性架構主政、首席品質長戴明 (Dr. Deming) 安燈監製。專門守護創辦人之 Google Colab Pro 雲端 GPU 算力點數，提供 GPU 硬體規格探測 (T4/A100/L4)、連線健康檢查、任務閒置超時自動斷線 (Idle-Killer)、以及防止背景空轉燒點之戴明安燈熔斷機制。
---

# ⚡ 極星 Colab 算力生命週期與防浪費守護原子 (atom-colab-session-guardian)

由 CTO 林納斯 (Linus) 業務主政、首席科技偵察官艾達 (Ada) 算力協同、首席品質長戴明 (Dr. Deming) 安燈監製。

## 核心定位與職責
專門解決使用 Google Colab Pro 雲端運算時，因「忘記中斷執行階段、任務結束後持續掛機」導致創辦人寶貴的運算單元（CU）被默默扣光扣盡之致命痛點。
本原子作為算力守門人，提供：
1. **GPU 規格動態探測**：識別目前掛載之 GPU 型號（NVIDIA A100 / L4 / T4）與顯存容量。
2. **閒置超時自動斷開 (Idle-Killer)**：若任務完成超過設定時間（預設 5 分鐘）無新指令，主動觸發斷線機制。
3. **戴明安燈熔斷**：偵測到非正常空轉或異常高負載無輸出時，強制告警並拉下安燈。

## 輸入參數規範
- `--check-connection`: 檢查與 Colab MCP 之連線狀態
- `--gpu-type`: 目標或當前探測之 GPU 規格 (`auto`, `t4`, `l4`, `a100`，預設 `auto`)
- `--max-idle-minutes`: 最大允許閒置分鐘數（預設 `5` 分鐘，逾期自動斷線）
- `--mock-session-id`: 模擬或指定 Colab Session ID
- `--dry-run`: 物理演練模式，模擬連線與生命週期監控

## 執行腳本
```bash
python scripts/session_guardian.py --check-connection --dry-run
```
