---
name: atom-yuki-hyperlocal-artisan
description: 台東微型實體生態守護與非標服務產品化原子 (Taitung Hyperlocal Ecosystem & Living Service Artisan Atom)。專門為執行長雪 (Yuki) 落實台東在地實體商業守護新律（大醫治未病紅外掃描、6分鐘到府救命、客流工具共享零成本槓桿、高齡尊嚴修容與口述傳家回憶錄、平戰結合社區儲能）。
---

# 🌸 atom-yuki-hyperlocal-artisan (台東微型實體生態守護與非標服務產品化原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-learning-yuki`（第六章第 21 至 30 律 · 台東在地守護新律十條）  
> **核心職責**：專門執行「台東微型實體生態守護工單生成、非標生活服務標準化封裝、大醫治未病紅外線配電盤預防檢測、工具共享進門接觸點槓桿、以及高齡尊嚴陪伴與傳家回憶錄裝配」。

---

## 核心設計哲學：台東微型實體商業生態學

1. **大醫治未病防護律 (Preventive Thermal Inspection)**：
   * 真正的守護在於消患於無形。生活管家到府服務時，順手以紅外熱像儀掃描配電盤與弱電箱發燙螺絲（> 60°C 預警）。
   * 賣給常民的是全家一輩子的居安無憂，而非驚心動魄的滅火。
2. **客流工具共享零成本槓桿 (Tool Sharing Leverage)**：
   * 免費出借專業電鑽、砂輪機或水電工具給鄰居友店，零成本創造實體進門接觸點。
   * 在選工具與還工具的 5 分鐘閒聊中，自然轉化高毛利生鮮與家政管家訂單。
3. **高齡尊嚴修容與口述傳家回憶錄 (Senior Dignity & Oral History)**：
   * 肉體照護有極限，心靈尊嚴無止境。清爽修容 ＋ 訪談老長輩一生事蹟裝訂成冊，昇華為家族生命史中的崇高恩人。

---

## 執行腳本與參數

專屬腳本位於 `scripts/yuki_hyperlocal_artisan.py`。

### 命令行介面 (CLI)

```bash
python scripts/yuki_hyperlocal_artisan.py --service-type "thermal" --client-name "寶桑路陳伯伯" --dry-run
python scripts/yuki_hyperlocal_artisan.py --service-type "tool_share" --tool-name "喜利得衝擊電鑽" --neighbor "光明路早午餐友店"
```

### 核心參數
- `--service-type`：在地守護服務類型（`thermal` 大醫治未病紅外檢測 / `tool_share` 工具共享客流槓桿 / `grooming_history` 尊嚴修容回憶錄 / `energy_storage` 平戰儲能）。
- `--client-name`：服務對象或住戶名稱。
- `--tool-name`：借用工具名稱（工具共享模式專用）。
- `--neighbor`：鄰里或友店名稱。
- `--dry-run`：預演模式。
