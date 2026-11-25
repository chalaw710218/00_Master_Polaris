---
name: atom-persona-utterance-miner
description: 🧠 極星心智逆向·非受迫性發言採礦與公關話術過濾原子 (Polaris Persona Unforced Utterance Miner Atom v1.0)。由執行長雪 (Yuki) 心智監製、首席視覺長約瑟夫 (Josef) 神韻協同。專門粉碎公關新聞通稿與客套祝詞，透過四維定向情報矩陣（長訪談逐字稿、即興論戰反擊、私人狂熱嗜好、習慣隱喻），精確提煉人物「下意識反問、語速放鬆、自嘲與講話帶刺」之真實非受迫性發言 (Unforced Utterances) 切片。
---

# 🧠 極星非受迫性發言採礦與公關話術過濾原子 (atom-persona-utterance-miner)

由執行長雪 (Yuki) 心智主政、首席視覺長約瑟夫 (Josef) 人格調校、CTO 林納斯 (Linus) 代碼驗收。

## 核心定位與職責
專門解決 AI 人格建模時「原料被公關通訊稿、官方演講或維基百科的假大空套話污染，導致生成的 AI 人格如廉價機器人般說話毫無靈魂」之致命痛點。
本原子作為真實人味情報採礦終端，提供：
1. **時代認知地平線鎖定**：鎖定人物最具代表性的歷史黃金階段，剔除時代之後的現代新名詞，防止時代穿幫。
2. **公關廢話無情洗滌**：自動識別並過濾演講稿、祝賀詞、經公關審核的宣傳通稿。
3. **非受迫性發言 (Unforced Utterances) 提取**：精準捕獲即興反擊、爭端下的情緒反問、聊到狂熱嗜好時防備心融化的鬆弛狀態、以及習慣性的語言破綻。

## 輸入參數規範
- `--persona-name`: 目標人物姓名（如「史蒂夫·賈伯斯」、「查理·蒙格」）
- `--era-horizon`: 時代認知地平線（如 `1997-2011 蘋果巔峰期`、`1980-2023 伯克夏成熟期`）
- `--raw-transcript-sample`: 訪談逐字稿或言論樣品
- `--dry-run`: 物理演練模式，輸出過濾分析與真性情語料切片

## 執行腳本
```bash
python scripts/utterance_miner.py --persona-name "CharlieMunger" --era-horizon "1980-2023" --dry-run
```
