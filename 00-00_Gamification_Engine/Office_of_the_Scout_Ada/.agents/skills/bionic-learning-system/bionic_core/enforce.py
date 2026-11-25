"""強制層：先讀後寫閘門 (Enforce · Master v6.4 純數學核心與指標缺席阻斷版)

v6.4 核心升級（100% 消除角色私貨與缺席放行漏洞）：
  • 100% 純數學規則解析：移除任何寫死之角色指標名稱，統一呼叫 `rule_store.parse_metric_pattern(pat, kind)` 解析 `>=`、`<=`、`:` 算子。
  • 數值指標缺席硬阻斷 (Fail-Closed)：若某子版存在 active 之數值規則 (`metric_min` / `metric_max` / `baseline_standard`)，呼叫 `gate()` 時若未傳入 `metrics` 或缺少該指標鍵名，直接判定違規阻斷，絕不缺席放行！
  • 十輪停機鎖未解除 ➔ 拒絕放行。
  • 對草稿文字與數值指標逐條檢查 ➔ 違規即 Exit Code 1。
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
        scope = r.get("scope", "any")
        scope_label = "（開頭鉤子）" if scope == "prefix" else ""
        ev = r["evidence"]
        if kind == "forbid_phrase":
            lines.append(f"🚫 禁止使用{scope_label}「{pat}」 {tag}｜{ev}")
        elif kind == "prefer_phrase":
            lines.append(f"⭐ 優先採用{scope_label}「{pat}」 {tag}｜{ev}")
        elif kind == "max_count":
            lines.append(f"⚖️ 次數上限：{pat} {tag}｜{ev}")
        elif kind == "regex_forbid":
            lines.append(f"🚫 禁止正則型態 `{pat}` {tag}｜{ev}")
        elif kind == "metric_min":
            lines.append(f"📐 指標下限：{pat} {tag}｜{ev}")
        elif kind == "metric_max":
            lines.append(f"📐 指標上限：{pat} {tag}｜{ev}")
        elif kind == "baseline_standard":
            lines.append(f"🏛️ 合規基準標準：{pat} {tag}｜{ev}")
        elif kind == "route":
            lines.append(f"🧭 幕僚長派工路由建議：{pat} {tag}｜{ev}")
    return "\n".join(lines)


def _count_token(text: str, word: str) -> int:
    if word.lower() == "emoji":
        return len(re.findall(r"[\U00010000-\U0010ffff\u2600-\u27bf]", text))
    if word in ("?", "？"):
        return text.count("？") + text.count("?")
    return text.count(word)


def check_text(text: str, rules: list[dict]) -> list[str]:
    violations = []
    for r in rules:
        kind = r["kind"]
        pat = r["pattern"]
        scope = r.get("scope", "any")
        rid = r["rule_id"]
        if kind == "forbid_phrase":
            if rule_store._match_phrase(text, pat, scope):
                loc = "開頭鉤子" if scope == "prefix" else "內文"
                violations.append(f"違反 {rid}：{loc}出現禁用語「{pat}」")
        elif kind == "max_count":
            try:
                word, lim_s = pat.rsplit(":", 1)
                lim = int(lim_s)
                cnt = _count_token(text, word)
                if cnt > lim:
                    violations.append(f"違反 {rid}：「{word}」出現 {cnt} 次，超過上限 {lim} 次")
            except ValueError:
                violations.append(f"規則 {rid} 格式錯誤（須為 詞:上限）")
        elif kind == "regex_forbid":
            try:
                if re.search(pat, text):
                    violations.append(f"違反 {rid}：命中禁用正則 `{pat}`")
            except re.error as e:
                violations.append(f"規則 {rid} 正則語法錯誤：{e}")
    return violations


def check_metrics(metrics: dict[str, float] | None, rules: list[dict]) -> list[str]:
    violations = []
    for r in rules:
        kind = r["kind"]
        pat = r["pattern"]
        rid = r["rule_id"]
        if kind in ("metric_min", "metric_max", "baseline_standard"):
            try:
                key, op, threshold = rule_store.parse_metric_pattern(pat, kind)
            except ValueError:
                violations.append(f"規則 {rid} 格式錯誤（須為 key>=val, key<=val 或 key:val）")
                continue
            if metrics is None or key not in metrics or metrics[key] is None:
                violations.append(f"違反 {rid}：缺少必檢數值指標 `{key}`（Fail-Closed 拒絕缺席放行）")
                continue
            val = float(metrics[key])
            if op == ">=" and val < threshold:
                violations.append(f"違反 {rid}：指標 `{key}` = {val} 低於下限 {threshold}")
            elif op == "<=" and val > threshold:
                violations.append(f"違反 {rid}：指標 `{key}` = {val} 高於上限 {threshold}")
    return violations


def gate(office: str, text: str = "", metrics: dict[str, float] | None = None) -> tuple[bool, list[str]]:
    if cycle_ledger.is_locked(office):
        return False, [f"停機鎖未解除（{office}）：滿 10 輪須先提交包含『矛盾比對/互斥掃描/淘汰清單』並通過程式化掃描與簽章之審計報告"]
    rules = load_active_rules(office)
    v = check_text(text, rules)
    v.extend(check_metrics(metrics, rules))
    return (not v), v


def main() -> None:
    ap = argparse.ArgumentParser(description="先讀後寫閘門 (v6.4 純數學核心與指標缺席阻斷版)")
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
