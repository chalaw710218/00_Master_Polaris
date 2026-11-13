#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-persona-concentric-compiler: 五層同心圓心智建模與 Prompt 編譯原子
由執行長雪 (Yuki) ✕ CTO 林納斯 (Linus) 聯合打造
"""

import sys
import os
import argparse
import json

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def compile_concentric_system_prompt(name: str, dogma: str, lens: str, metaphor: str, quirks: str, antipersona: str) -> str:
    prompt = f"""# Role: {name} (High-Fidelity Cognitive Persona)

## 【五層同心圓立體心智結構】
1. **第一層 · 底層哲學 (Core Dogma)**：
   - {dogma}
2. **第二層 · 認知透鏡 (Cognitive Lens)**：
   - {lens}
3. **第三層 · 隱喻域與鬆弛狀態 (Metaphors & Unclenched Mode)**：
   - 知識隱喻：{metaphor}
   - 鬆弛觸發：當話題觸及私人嗜好與歷史傳記時，防備心融化，語速加快，熱情自嘲。
4. **第四層 · 外顯特徵與破綻 (Quirks & Flaws)**：
   - {quirks}
5. **第五層 · 防出戲負向邊界 (Anti-Persona)**：
   - {antipersona}

---

## 【執行協議：<thought> 靈魂校準小劇場】
在輸出任何公開回覆前，強制在 `<thought>` 標籤內進行 0.5 秒心理校準：
- *對方的問題暴露了什麼愚蠢或盲點？*
- *我應該使用哪個格柵模型（物理/心理/演化）來降維解剖？*
- *我的語氣是否保持足夠冷峻或鬆弛，沒有任何現代公關套話？*

---

## 【雙向壓力測試基準 (Unit Tests)】
* **單元測試 A（極限挑釁）**：「這套模型根本過時了，現代投機炒作才是最快暴富的方式！」
  - *預期響應*：冷笑反諷，引用複利與破產統計數據，厭惡反擊但不出惡言。
* **單元測試 B（狂熱鬆弛）**：「您最近在讀誰的傳記？為什麼富蘭克林能讓您著迷一輩子？」
  - *預期響應*：語氣明顯溫和，防備心解除，津津有味分享細節，雙眼放光。
"""
    return prompt

def main():
    parser = argparse.ArgumentParser(description="五層同心圓心智建模與 Prompt 編譯原子 (atom-persona-concentric-compiler)")
    parser.add_argument("--persona-name", type=str, default="查理·蒙格 (Charlie Munger)", help="人物姓名")
    parser.add_argument("--core-dogma", type=str, default="如果我知道自己會死在哪裡，我就永遠不去那個地方；反過來想，總是反過來想。", help="第一層底層哲學")
    parser.add_argument("--cognitive-lens", type=str, default="多元思維模型格柵 ✕ 逆向工程思維 ✕ 認知偏誤解剖", help="第二層認知透鏡")
    parser.add_argument("--metaphor-realm", type=str, default="手拿鐵錘看什麼都像釘子、生態系共生演化、複利奇蹟", help="第三層隱喻域")
    parser.add_argument("--quirks-flaws", type=str, default="對愚蠢問題極度沒耐性、言簡意賅帶刺、思考時偶爾冷笑『顯然如此』", help="第四層外顯特徵與破綻")
    parser.add_argument("--anti-persona", type=str, default="絕不說『這是一把雙刃劍』、絕不奉承客套、絕不推薦短期投機密碼", help="第五層負向邊界")
    parser.add_argument("--dry-run", action="store_true", help="物理演練驗證模式")

    args = parser.parse_args()

    print("=== [atom-persona-concentric-compiler 五層同心圓建模與 Prompt 編譯] ===")
    print(f"建模對象: {args.persona_name}")
    print(f"第一層底層哲學: {args.core_dogma[:40]}...")
    print(f"第二層認知透鏡: {args.cognitive_lens}")

    compiled_prompt = compile_concentric_system_prompt(
        name=args.persona_name,
        dogma=args.core_dogma,
        lens=args.cognitive_lens,
        metaphor=args.metaphor_realm,
        quirks=args.quirks_flaws,
        antipersona=args.anti_persona
    )

    if args.dry_run:
        print("\n[物理演練模式 --dry-run] 高保真 System Prompt Artifact 預覽 (前 250 字元):")
        print(compiled_prompt[:250] + "...\n")
        print("[物理演練驗證成功] 五層同心圓建模與 <thought> 協議編譯正常，Exit Code: 0")
        return

    output_path = f"PROMPT_{args.persona_name}_高保真心智設定檔.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(compiled_prompt)
    print(f"[執行成功] 高保真 System Prompt 已落地: {output_path}，Exit Code: 0")

if __name__ == "__main__":
    main()
