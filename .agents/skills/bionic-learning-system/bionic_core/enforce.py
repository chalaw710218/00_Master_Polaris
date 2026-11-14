"""強制層：先讀後寫閘門 (Enforce · Master v6.0 第十一章 ⑤)

任何產出技能在輸出前呼叫本模組：
  1. 十輪停機鎖未解除 ➔ 拒絕。
  2. 載入該子版 active 規則 ➔ 編譯為約束文字（注入生成提示詞）。
  3. 對草稿逐條檢查 ➔ 違規即 Exit Code 1。

用法：
  python enforce.py constraints --office kage
  python enforce.py gate --office kage --text "草稿內容"
  from enforce import load_active_rules, compile_constraints, check_text
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cycle_ledger  # noqa: E402
import rule_store  # noqa: E402

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def load_active_rules(office: str) -> list[dict]:
    return [r for r in rule_store.fold(office).values() if r["status"] == "active"]


def compile_constraints(rules: list[dict]) -> str:
    if not rules:
        return "（目前無 active 規則：尚無經驗證的學習成果可約束本次產出）"
    lines = ["### 🧠 仿生閉環約束（來自已轉正的規則，非模型臆測）"]
    for r in rules:
        tag = f"[{r['rule_id']} 來源{r['source_tier']}級 信心{r['confidence']}]"
        if r["kind"] == "forbid_phrase":
            lines.append(f"🚫 禁止使用「{r['pattern']}」 {tag}｜{r['evidence']}")
        elif r["kind"] == "prefer_phrase":
            lines.append(f"⭐ 優先採用「{r['pattern']}」 {tag}｜{r['evidence']}")
        elif r["kind"] == "max_count":
            lines.append(f"⚖️ 規則：{r['pattern']} {tag}｜{r['evidence']}")
    return "\n".join(lines)


def check_text(text: str, rules: list[dict]) -> list[str]:
    violations = []
    for r in rules:
        if r["kind"] == "forbid_phrase" and r["pattern"] in text:
            violations.append(f"違反 {r['rule_id']}：出現禁用語「{r['pattern']}」")
        if r["kind"] == "max_count":
            # pattern 格式「詞:上限」，例如「？:2」
            try:
                word, lim = r["pattern"].rsplit(":", 1)
                if text.count(word) > int(lim):
                    violations.append(f"違反 {r['rule_id']}：「{word}」超過 {lim} 次")
            except ValueError:
                violations.append(f"規則 {r['rule_id']} 格式錯誤（須為 詞:上限）")
    return violations


def gate(office: str, text: str) -> tuple[bool, list[str]]:
    if cycle_ledger.is_locked(office):
        return False, ["停機鎖未解除：滿 10 輪須先提交衝突審計報告"]
    v = check_text(text, load_active_rules(office))
    return (not v), v


def main() -> None:
    ap = argparse.ArgumentParser(description="先讀後寫閘門")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("constraints")
    c.add_argument("--office", required=True)
    g = sub.add_parser("gate")
    g.add_argument("--office", required=True)
    g.add_argument("--text", required=True)
    a = ap.parse_args()
    if a.cmd == "constraints":
        print(compile_constraints(load_active_rules(a.office)))
    else:
        ok, v = gate(a.office, a.text)
        if ok:
            print("🟢 放行")
        else:
            print("🛑 閘門阻斷：" + "；".join(v))
            sys.exit(1)


if __name__ == "__main__":
    main()
