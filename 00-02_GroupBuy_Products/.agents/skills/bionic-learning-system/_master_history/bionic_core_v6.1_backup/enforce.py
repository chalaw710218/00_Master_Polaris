"""強制層：先讀後寫閘門 (Enforce · Master v6.1 第十一章 ⑤)

v6.1 零信任硬化升級：
  • 支援 6 種結構化規則型態：
    1. `forbid_phrase`：禁止出現指定字串
    2. `prefer_phrase`：提示詞約束優先採用指定結構/詞彙
    3. `max_count`：指定字元/詞彙出現上限（格式 `詞:上限`，如 `？:2`）
    4. `regex_forbid`：正則表達式命中即阻斷
    5. `metric_min`：數值指標下限檢查（格式 `指標名:下限`，如 `contrast_ratio:7.0`）
    6. `metric_max`：數值指標上限檢查（格式 `指標名:上限`，如 `fcp_ms:500`）
  • 十輪停機鎖未解除 ➔ 拒絕放行。
  • 對草稿文字與數值指標逐條檢查 ➔ 違規即 Exit Code 1。

用法：
  python enforce.py constraints --office kage
  python enforce.py gate --office kage --text "草稿內容"
  python enforce.py gate --office josef --text "海報文案" --metrics "{\"contrast_ratio\": 4.5}"
"""
from __future__ import annotations

import argparse
import json
import re
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
    lines = ["### 🧠 仿生閉環約束（來自 bionic_core 已驗證轉正規則，非模型臆測）"]
    for r in rules:
        tag = f"[{r['rule_id']} 來源{r['source_tier']}級 信心{r['confidence']}]"
        kind = r["kind"]
        pat = r["pattern"]
        ev = r["evidence"]
        if kind == "forbid_phrase":
            lines.append(f"🚫 禁止使用「{pat}」 {tag}｜{ev}")
        elif kind == "prefer_phrase":
            lines.append(f"⭐ 優先採用「{pat}」 {tag}｜{ev}")
        elif kind == "max_count":
            lines.append(f"⚖️ 次數上限：{pat} {tag}｜{ev}")
        elif kind == "regex_forbid":
            lines.append(f"🚫 禁止正則型態 `{pat}` {tag}｜{ev}")
        elif kind == "metric_min":
            lines.append(f"📐 指標下限：{pat} {tag}｜{ev}")
        elif kind == "metric_max":
            lines.append(f"📐 指標上限：{pat} {tag}｜{ev}")
    return "\n".join(lines)


def check_text(text: str, rules: list[dict]) -> list[str]:
    violations = []
    for r in rules:
        kind = r["kind"]
        pat = r["pattern"]
        rid = r["rule_id"]
        if kind == "forbid_phrase" and pat in text:
            violations.append(f"違反 {rid}：出現禁用語「{pat}」")
        elif kind == "max_count":
            try:
                word, lim = pat.rsplit(":", 1)
                if text.count(word) > int(lim):
                    violations.append(f"違反 {rid}：「{word}」出現 {text.count(word)} 次，超過上限 {lim} 次")
            except ValueError:
                violations.append(f"規則 {rid} 格式錯誤（須為 詞:上限）")
        elif kind == "regex_forbid":
            try:
                if re.search(pat, text):
                    violations.append(f"違反 {rid}：命中禁用正則 `{pat}`")
            except re.error as e:
                violations.append(f"規則 {rid} 正則語法錯誤：{e}")
    return violations


def check_metrics(metrics: dict[str, float], rules: list[dict]) -> list[str]:
    violations = []
    for r in rules:
        kind = r["kind"]
        pat = r["pattern"]
        rid = r["rule_id"]
        if kind in ("metric_min", "metric_max"):
            try:
                key, threshold_s = pat.rsplit(":", 1)
                threshold = float(threshold_s)
            except ValueError:
                violations.append(f"規則 {rid} 格式錯誤（須為 指標名:數值）")
                continue
            if key not in metrics:
                continue
            val = float(metrics[key])
            if kind == "metric_min" and val < threshold:
                violations.append(f"違反 {rid}：指標 `{key}` = {val} 低於下限 {threshold}")
            elif kind == "metric_max" and val > threshold:
                violations.append(f"違反 {rid}：指標 `{key}` = {val} 高於上限 {threshold}")
    return violations


def gate(office: str, text: str = "", metrics: dict[str, float] | None = None) -> tuple[bool, list[str]]:
    if cycle_ledger.is_locked(office):
        return False, [f"停機鎖未解除（{office}）：滿 10 輪須先提交包含『矛盾比對/互斥掃描/淘汰清單』之審計報告"]
    rules = load_active_rules(office)
    v = check_text(text, rules)
    if metrics:
        v.extend(check_metrics(metrics, rules))
    return (not v), v


def main() -> None:
    ap = argparse.ArgumentParser(description="先讀後寫閘門 (v6.1)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("constraints")
    c.add_argument("--office", required=True)
    g = sub.add_parser("gate")
    g.add_argument("--office", required=True)
    g.add_argument("--text", default="")
    g.add_argument("--metrics", help="JSON 字串，例如 '{\"contrast_ratio\": 7.5}'")
    a = ap.parse_args()
    if a.cmd == "constraints":
        print(compile_constraints(load_active_rules(a.office)))
    else:
        metrics_dict = None
        if a.metrics:
            try:
                metrics_dict = json.loads(a.metrics)
            except Exception as e:
                print(f"🛑 --metrics JSON 解析錯誤：{e}")
                sys.exit(1)
        ok, v = gate(a.office, a.text, metrics_dict)
        if ok:
            print("🟢 放行")
        else:
            print("🛑 閘門阻斷：" + "；".join(v))
            sys.exit(1)


if __name__ == "__main__":
    main()
