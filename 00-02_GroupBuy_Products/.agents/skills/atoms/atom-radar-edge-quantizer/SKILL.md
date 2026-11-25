---
name: atom-radar-edge-quantizer
description: 🛰️ 極星科技雷達·端側邊緣量化評估與無感化轉譯原子 (Polaris Radar Edge Quantizer & Gentle Translation Atom v1.0)。由首席科技偵察官艾達 (Ada) 業務主政、首席前端架構師尼奧 (Neo) 體驗協同。專門評審 0.5B~1.8B 小型開源邊緣權重 (Edge-SLM)，精算 BitNet 1.58b / INT4 極限混合量化之 RAM 占用 (<500MB) 與首字推論延遲 (<50ms)，並堅守零攝像頭常民尊嚴防線 (全面改以毫米波/壓電微震無感感知)，導出結構化之《科技審查卷宗 (RAD-Report)》。
---

# 🛰️ 極星端側邊緣量化評估與無感化轉譯原子 (atom-radar-edge-quantizer)

由首席科技偵察官艾達 (Ada) 業務主政、首席前端架構師尼奧 (Neo) 體驗協同、CTO 林納斯 (Linus) 代碼驗收。

## 核心定位與職責
專門解決大型雲端模型體積臃腫、在邊緣小板卡（如樹莓派、微控制器）無法運行，以及傳統居家安防強制安裝攝影鏡頭、嚴重侵害常民與長輩隱私尊嚴之痛點。
本原子作為端側邊緣選型與無感人性化轉譯終端，提供：
1. **開源邊緣小模型選型與量化評審**：評估 0.5B~1.8B 開源權重（如 Qwen2.5-0.5B, SmolLM2），精算 W3A8、BitNet 1.58-bit 或 INT4 量化後的顯存/RAM 占用（嚴格 $\le 500\text{MB}$）與推論延遲（$\le 50\text{ms}$）。
2. **和光同塵無感化轉譯與零攝像頭防線**：將侵入式影像識別轉化為地面微振動感知、毫米波雷達或地墊壓力矩陣，讓科技於無聲處守護。
3. **結構化絕密科技卷宗導出**：產出包含硬體選型 BOM 清單、量化參數與 Python 評估腳本之標準《RAD-Report 卷宗》。

## 輸入參數規範
- `--model-id`: 邊緣模型名稱（如 `Qwen2.5-0.5B-Instruct`）
- `--param-billions`: 參數量（十億 B，如 `0.5`）
- `--quant-precision`: 量化精度 (`bitnet_158`, `int4`, `w3a8`, `fp16`，預設 `int4`)
- `--sensor-modality`: 感知模態 (`piezo_vibration`, `mmwave_fmcw`, `camera_slop`，預設 `piezo_vibration`)
- `--dry-run`: 物理演練模式，輸出量化評估與 RAD-Report 卷宗預覽

## 執行腳本
```bash
python scripts/edge_quantizer.py --model-id "Qwen2.5-0.5B" --param-billions 0.5 --quant-precision int4 --dry-run
```
