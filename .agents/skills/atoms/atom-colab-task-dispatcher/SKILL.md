---
name: atom-colab-task-dispatcher
description: ⚡ 極星 Google Colab 遠端任務脫敏封裝與成果回傳原子 (Polaris Colab Task Dispatcher & Ingest Atom v1.0)。由 CTO 林納斯 (Linus) 確定性架構主政、首席視覺長約瑟夫 (Josef) 圖像協同。專門將本地 Python 計算腳本或 ComfyUI/Flux 生圖任務，進行本機絕對路徑與機敏資訊自動脫敏，封裝為標準 Colab 遠端執行單元 (IPython Cell Payload)，並於雲端渲染完成後安全拉取至本地目錄且完成 SHA-256 完整性校驗。
---

# ⚡ 極星 Colab 遠端任務脫敏封裝與成果回傳原子 (atom-colab-task-dispatcher)

由 CTO 林納斯 (Linus) 業務主政、首席視覺長約瑟夫 (Josef) 視覺協同、首席科技偵察官艾達 (Ada) 算力調度。

## 核心定位與職責
專門解決調用雲端運算時「本機絕對路徑無法在雲端執行、腳本含有私密 Token 或極星內部代號、雲端輸出圖片/數據無法安全自動回傳本機」之痛點。
本原子作為任務傳送與成果接引管線，提供：
1. **任務代碼自動脫敏**：替換 Windows 絕對路徑為雲端容器路徑，擦除敏感金鑰與品牌內部代號。
2. **IPython Cell Payload 打包**：將生圖 Prompt 或矩陣計算算法封裝為合規之執行單元。
3. **成果接引與雜湊校驗**：模擬或接引雲端生成的 PNG / JSON，下載存入本地目標資料夾，並計算 SHA-256 雜湊值確保傳輸完整無損。

## 輸入參數規範
- `--task-type`: 任務類型 (`image_flux` 或 `compute_matrix`，預設 `image_flux`)
- `--prompt-or-code`: 生圖提示詞或欲執行之 Python 代碼
- `--output-local-dir`: 本地下載存檔目錄（預設 `00-03_Brand_Dynamics` 或指定目錄）
- `--dry-run`: 物理演練模式，輸出脫敏 Payload 與回傳模擬報告

## 執行腳本
```bash
python scripts/task_dispatcher.py --task-type image_flux --dry-run
```
