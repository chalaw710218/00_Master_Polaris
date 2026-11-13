---
name: atom-learning-spin-tone-discriminator
description: SPIN 內部自對弈去 AI 腔與創辦人神韻對齊原子 (Self-Play Tone Discrimination & Founder Voice Alignment Atom)。專門執行 UCLA SPIN 內部自對弈盲測，一票否決 AI 說教套話與農場宣傳虛詞，確保對外與對內產出 100% 對齊創辦人品碩（闆仔）的實幹商人底色。
---

# 🎭 atom-learning-spin-tone-discriminator (SPIN 內部自對弈去 AI 腔與創辦人神韻對齊原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-learning-system`（第三章｜SPIN 內部自對弈判別機制）  
> **核心職責**：專門執行「內部自對弈判別器盲測（SPIN）、AI 說教腔與農場垃圾詞過濾、以及創辦人（品碩 · 闆仔）實幹神韻對齊審查」。

---

## 核心設計哲學：UCLA ICML 2024 SPIN (Self-Play Fine-Tuning)

1. **零和博弈判別機制**：
   * 生成器（Generator）產出初版草案 ➔ 內部判別器（Discriminator）以「創辦人品碩真實發言分佈」為標竿進行嚴苛盲測。
   * 若判斷為「像 AI 模板、浮誇說教、農場叫賣」 ➔ 立即打回強制重寫，修剪虛浮形容詞。
   * 若判斷為「像品碩認可的真實實幹神韻」 ➔ 方准正式放行出廠。
2. **創辦人品碩（闆仔）的三大核心神韻基線**：
   * **真誠質樸**：零過度修飾、零廉價表情符號堆砌、不講官腔假話。
   * **商人信譽與算大帳**：講清楚跑腿費、成本結構與損耗，明白算帳不玩套路。
   * **拒絕農場話術**：一票否決「在當今瞬息萬變的世界中」、「總之」、「保證穩賺」、「震撼揭秘」等粗劣垃圾詞。

---

## 執行腳本與參數

專屬腳本位於 `scripts/spin_tone_discriminator.py`。

### 命令行介面 (CLI)

```bash
python scripts/spin_tone_discriminator.py --input-text "這是一份極具前瞻性且改變世界的方案..."
python scripts/spin_tone_discriminator.py --file-path "draft.txt" --strict-founder-mode
```

### 核心參數
- `--input-text`：待審查之草案文字。
- `--file-path`：待審查之文字檔案路徑。
- `--strict-founder-mode`：嚴格闆仔模式（提高對形容詞與表情符號的懲罰門檻）。
- `--dry-run`：預演模式，輸出評分與敏感詞檢測細節。
