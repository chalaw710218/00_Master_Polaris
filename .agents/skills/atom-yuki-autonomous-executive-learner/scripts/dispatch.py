"""雪的派工帳本 (dispatch.py · Master v6.5 中性信任錨與反盲簽版)

雪每次分派由程式寫入帳本；結果訊號只有「創辦人以口令簽章的簽收詞」：
收 / 退 / 改派:<閣員代號>

設計重點
  1. 信任錨中性化：金鑰推導與公鑰存儲統一採用母版中性之 `bionic_core/vaults/founder_vault.meta.json`。
  2. 帳本 Append-Only，每筆帶 prev/hash（雜湊鏈），中途竄改會被偵測。
  3. 簽收以 HMAC-SHA256 簽章，金鑰由創辦人口令推導；口令不落地、不進環境變數。
  4. init / signoff / stats / export-verified 一律要求真實終端機；agent 的非互動環境會被拒絕。
  5. export-verified：印出待匯出結案明細（反盲簽），由創辦人簽署附帶 Schnorr+HMAC 之 `founder_sig` 供母版 route 驗算。
  6. status 命令若偵測雜湊鏈斷裂或竄改，立即回傳 Exit Code 1。
"""
from __future__ import annotations

import argparse
import getpass
import hashlib
import hmac
import json
import re
import secrets
import sys
import tempfile
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

VAULT_DIR = Path(__file__).resolve().parent.parent / "vaults"
META_PATH: Path | None = None
BIONIC_CORE_DIR = Path(__file__).resolve().parent.parent.parent / "bionic-learning-system" / "bionic_core"
if str(BIONIC_CORE_DIR) not in sys.path:
    sys.path.insert(0, str(BIONIC_CORE_DIR))
import founder_auth  # noqa: E402

ROSTER = {"kage", "taylor", "josef", "deming", "abacus", "falcon",
          "linus", "neo", "ada", "raven", "meow"}
SIGN_RE = re.compile(r"^(收|退|改派:([a-z]+))$")
PBKDF2_ITER = 200_000
MIN_N = 5
ZERO = "0" * 64


def _ledger() -> Path:
    return VAULT_DIR / "yuki_dispatch.jsonl"


def _meta() -> Path:
    return META_PATH or founder_auth.DEFAULT_META_PATH


def _verified_samples_path() -> Path:
    return VAULT_DIR / "yuki_verified_route_samples.jsonl"


def _canon(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _h(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def read_events() -> list[dict]:
    p = _ledger()
    if not p.exists():
        return []
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def append_event(ev: dict) -> dict:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    events = read_events()
    prev = events[-1]["hash"] if events else ZERO
    body = {"ts": _now(), **ev, "prev": prev}
    body["hash"] = _h(_canon(body))
    with open(_ledger(), "a", encoding="utf-8") as f:
        f.write(json.dumps(body, ensure_ascii=False) + "\n")
    return body


def verify_chain(events: list[dict] | None = None) -> tuple[bool, str]:
    events = read_events() if events is None else events
    prev = ZERO
    for i, e in enumerate(events):
        body = {k: v for k, v in e.items() if k != "hash"}
        if body.get("prev") != prev:
            return False, f"第 {i + 1} 筆 prev 不連續"
        if _h(_canon(body)) != e.get("hash"):
            return False, f"第 {i + 1} 筆內容與雜湊不符"
        prev = e["hash"]
    return True, f"鏈完整（{len(events)} 筆）"


def init_vault(passphrase: str, meta_target: Path | None = None) -> None:
    mp = meta_target or _meta()
    if mp.exists() or _ledger().exists():
        raise ValueError("已初始化，拒絕覆蓋")
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    meta_dict = founder_auth.init_meta_file(passphrase, meta_path=mp)
    append_event({"type": "genesis", "kcv": meta_dict["kcv"], "pub_y": meta_dict["pub_y"], "fingerprint": meta_dict["fingerprint"]})


def load_key(passphrase: str, meta_target: Path | None = None) -> bytes:
    mp = meta_target or _meta()
    key, meta = founder_auth.load_verified_key(passphrase, meta_path=mp)
    events = read_events()
    genesis = events[0] if events else {}
    if genesis.get("type") != "genesis" or genesis.get("kcv") != meta.get("kcv"):
        raise ValueError("meta 與帳本創世紀錄不符，可能被替換")
    return key


def dispatch(category: str, assigned: list[str], mode: str, note: str = "", parent: str = "") -> str:
    if not _meta().exists():
        raise ValueError("尚未 init，拒絕派工")
    if not category.strip():
        raise ValueError("category 不可為空")
    bad = [a for a in assigned if a not in ROSTER]
    if not assigned or bad:
        raise ValueError(f"派工對象不在名冊：{bad or '未指定'}")
    if mode not in ("serial", "parallel"):
        raise ValueError("mode 須為 serial 或 parallel")
    tid = "T-" + datetime.now().strftime("%Y%m%d") + "-" + secrets.token_hex(3)
    append_event({"type": "dispatch", "task_id": tid, "category": category.strip(),
                  "assigned": sorted(assigned), "mode": mode, "note": note,
                  "parent": parent, "by": "yuki"})
    return tid


def _find_dispatch(events: list[dict], task_id: str) -> dict | None:
    for e in events:
        if e.get("type") == "dispatch" and e.get("task_id") == task_id:
            return e
    return None


def signoff(task_id: str, word: str, passphrase: str, meta_target: Path | None = None) -> dict:
    m = SIGN_RE.match(word)
    if not m:
        raise ValueError("簽收詞僅限：收 / 退 / 改派:<閣員代號>")
    if word.startswith("改派") and m.group(2) not in ROSTER:
        raise ValueError(f"改派對象不在名冊：{m.group(2)}")
    events = read_events()
    ok_chain, msg_chain = verify_chain(events)
    if not ok_chain:
        raise ValueError(f"帳本雜湊鏈損毀 ({msg_chain})，拒絕簽收")
    key = load_key(passphrase, meta_target=meta_target)
    d = _find_dispatch(events, task_id)
    if not d:
        raise ValueError("找不到該任務")
    payload = {"type": "signoff", "task_id": task_id, "word": word,
               "dispatch_hash": d["hash"], "nonce": secrets.token_hex(4)}
    sig = hmac.new(key, _canon(payload).encode("utf-8"), hashlib.sha256).hexdigest()
    return append_event({**payload, "sig": sig})


def verified_signoffs(events: list[dict], key: bytes) -> list[dict]:
    disp = {e["task_id"]: e for e in events if e.get("type") == "dispatch"}
    seen: set[str] = set()
    ok: list[dict] = []
    for e in events:
        if e.get("type") != "signoff":
            continue
        payload = {k: e[k] for k in ("type", "task_id", "word", "dispatch_hash", "nonce") if k in e}
        exp = hmac.new(key, _canon(payload).encode("utf-8"), hashlib.sha256).hexdigest()
        sig = str(e.get("sig", ""))
        d = disp.get(e.get("task_id"))
        if (hmac.compare_digest(exp, sig) and sig not in seen
                and d is not None and d["hash"] == e.get("dispatch_hash")):
            seen.add(sig)
            ok.append(e)
    return ok


def export_verified_samples(
    passphrase: str,
    out_path: Path | None = None,
    meta_target: Path | None = None,
    _allow_test: bool = False,
) -> Path:
    events = read_events()
    ok_chain, msg_chain = verify_chain(events)
    if not ok_chain:
        raise ValueError(f"派工帳本雜湊鏈損毀：{msg_chain}")
    mp = meta_target or _meta()
    key = load_key(passphrase, meta_target=mp)
    vs = verified_signoffs(events, key)
    disp = {e["task_id"]: e for e in events if e.get("type") == "dispatch"}
    by_task: dict[str, list[dict]] = {}
    for s in vs:
        by_task.setdefault(s["task_id"], []).append(s)

    samples: list[dict] = []
    for tid in sorted(by_task.keys()):
        ss = by_task[tid]
        last = ss[-1]
        if last["word"] == "退":
            continue
        d = disp[tid]
        rework = sum(1 for s in ss if s["word"] == "退")
        first_pass_pct = 100.0 if (last["word"] == "收" and rework == 0) else 0.0
        samples.append({
            "id": tid,
            "category": d["category"],
            "assigned": d["assigned"],
            "metric": first_pass_pct,
            "ts": last.get("ts", d.get("ts", "")),
        })

    samples_sha = _h(_canon(samples))
    sig_payload = {"action": "route_samples", "samples_sha256": samples_sha, "count": len(samples)}
    sig_bundle = founder_auth.sign_founder_action(
        sig_payload,
        meta_path=mp,
        _test_passphrase=passphrase if _allow_test else None,
    )
    target = out_path or _verified_samples_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    envelope = {
        "kind": "verified_route_samples",
        "samples_sha256": samples_sha,
        "count": len(samples),
        "founder_sig": sig_bundle,
        "samples": samples,
    }
    target.write_text(json.dumps(envelope, ensure_ascii=False) + "\n", encoding="utf-8")
    return target


def compute_stats(events: list[dict], signoffs: list[dict]) -> dict:
    disp = {e["task_id"]: e for e in events if e.get("type") == "dispatch"}
    by_task: dict[str, list[dict]] = {}
    for s in signoffs:
        by_task.setdefault(s["task_id"], []).append(s)
    rows: dict = {}
    for tid, ss in by_task.items():
        last = ss[-1]
        if last["word"] == "退":
            continue
        d = disp[tid]
        rework = sum(1 for s in ss if s["word"] == "退")
        for a in d["assigned"]:
            r = rows.setdefault((d["category"], a),
                                {"closed": 0, "accepted": 0, "first_pass": 0, "reassigned": 0})
            r["closed"] += 1
            if last["word"] == "收":
                r["accepted"] += 1
                if rework == 0:
                    r["first_pass"] += 1
            else:
                r["reassigned"] += 1
    return rows


def format_stats(rows: dict, min_n: int) -> list[str]:
    lines = []
    for (cat, a), r in sorted(rows.items()):
        n = r["closed"]
        if n < min_n:
            lines.append(f"{cat} x {a}：資料不足（已結案 {n} < {min_n}）")
        else:
            lines.append(f"{cat} x {a}：已結案 {n}，一次過 {r['first_pass'] / n:.0%}，"
                         f"收 {r['accepted']}，被改派 {r['reassigned']}")
    return lines or ["（尚無已驗證且結案的簽收）"]


def _require_tty() -> None:
    founder_auth.require_tty()


def selftest() -> None:
    global VAULT_DIR, META_PATH
    temp_dir = Path(tempfile.mkdtemp(prefix="yuki_dispatch_test_v65_"))
    VAULT_DIR = temp_dir
    meta_p = temp_dir / "test_founder.meta.json"
    META_PATH = meta_p
    fails: list[str] = []

    def check(name: str, cond: bool) -> None:
        print(("OK   " if cond else "FAIL ") + name)
        if not cond:
            fails.append(name)

    def raises(fn) -> bool:
        try:
            fn()
        except (ValueError, PermissionError):
            return True
        return False

    pw = "correct horse battery staple founder v65"
    meta_p = temp_dir / "test_founder.meta.json"
    check("未 init 不得派工", raises(lambda: dispatch("文案", ["taylor"], "serial")))
    init_vault(pw, meta_target=meta_p)
    check("重複 init 被拒", raises(lambda: init_vault(pw, meta_target=meta_p)))
    t1 = dispatch("文案", ["taylor"], "serial")
    t2 = dispatch("文案", ["taylor"], "serial")
    check("不在名冊不得派工", raises(lambda: dispatch("文案", ["nobody"], "serial")))
    check("非法簽收詞被拒", raises(lambda: signoff(t1, "好", pw, meta_target=meta_p)))
    check("改派對象不在名冊被拒", raises(lambda: signoff(t1, "改派:nobody", pw, meta_target=meta_p)))
    check("錯誤口令被拒", raises(lambda: signoff(t1, "收", "wrong passphrase 123", meta_target=meta_p)))

    signoff(t1, "收", pw, meta_target=meta_p)
    signoff(t2, "退", pw, meta_target=meta_p)
    signoff(t2, "收", pw, meta_target=meta_p)
    # 偽造與重放
    append_event({"type": "signoff", "task_id": t1, "word": "收",
                  "dispatch_hash": "x", "nonce": "aa", "sig": "0" * 64})
    last = [e for e in read_events() if e.get("type") == "signoff" and e["task_id"] == t2][-1]
    append_event({k: v for k, v in last.items() if k not in ("ts", "prev", "hash")})

    events = read_events()
    vs = verified_signoffs(events, load_key(pw, meta_target=meta_p))
    check("偽造與重放不計入（有效簽收應為 3）", len(vs) == 3)
    rows = compute_stats(events, vs)
    r = rows[("文案", "taylor")]
    check("結案 2、一次過 1", r["closed"] == 2 and r["first_pass"] == 1)
    check("雜湊鏈完整", verify_chain(events)[0])

    exp_file = export_verified_samples(pw, meta_target=meta_p, _allow_test=True)
    exp_obj = json.loads(exp_file.read_text(encoding="utf-8"))
    check("匯出標準路由樣本列只含有效結案 2 筆並附帶創辦人 Schnorr 簽章", exp_obj["count"] == 2 and "founder_sig" in exp_obj)

    p = _ledger()
    p.write_text(p.read_text(encoding="utf-8").replace("文案", "定價", 1), encoding="utf-8")
    check("竄改派工內容被偵測", not verify_chain()[0])
    check("雜湊鏈損毀時拒絕匯出路由樣本", raises(lambda: export_verified_samples(pw, meta_target=meta_p, _allow_test=True)))

    print("結果：" + ("全數通過" if not fails else f"失敗 {len(fails)} 項"))
    sys.exit(1 if fails else 0)


def main() -> None:
    ap = argparse.ArgumentParser(description="雪的派工帳本 (v6.5)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    d = sub.add_parser("dispatch")
    d.add_argument("--category", required=True)
    d.add_argument("--assign", required=True)
    d.add_argument("--mode", default="serial", choices=["serial", "parallel"])
    d.add_argument("--note", default="")
    d.add_argument("--parent", default="")
    s = sub.add_parser("signoff")
    s.add_argument("--task", required=True)
    s.add_argument("--word", required=True)
    st = sub.add_parser("stats")
    st.add_argument("--min-n", type=int, default=MIN_N)
    ev_cmd = sub.add_parser("export-verified")
    ev_cmd.add_argument("--out", help="選填：輸出路徑")
    sub.add_parser("status")
    sub.add_parser("selftest")
    a = ap.parse_args()

    try:
        if a.cmd == "init":
            _require_tty()
            p1 = getpass.getpass("設定創辦人簽收口令（建議 4 個以上隨機詞）：")
            if p1 != getpass.getpass("再輸入一次：") or len(p1) < 12:
                raise ValueError("兩次不一致，或少於 12 字元")
            init_vault(p1)
            print("已初始化。口令請自行保管，不要告訴任何 agent。")
        elif a.cmd == "dispatch":
            print(dispatch(a.category, [x.strip() for x in a.assign.split(",") if x.strip()],
                           a.mode, a.note, a.parent))
        elif a.cmd == "signoff":
            _require_tty()
            d0 = _find_dispatch(read_events(), a.task)
            if not d0:
                raise ValueError("找不到該任務")
            print(f"任務 {a.task}：{d0['category']} -> {','.join(d0['assigned'])}（{d0['mode']}）{d0['note']}")
            signoff(a.task, a.word, getpass.getpass("創辦人簽收口令："))
            print(f"已簽收：{a.word}")
        elif a.cmd == "stats":
            _require_tty()
            events = read_events()
            ok, msg = verify_chain(events)
            print("鏈檢查：" + msg)
            if not ok:
                sys.exit(1)
            vs = verified_signoffs(events, load_key(getpass.getpass("創辦人簽收口令：")))
            claimed = sum(1 for e in events if e.get("type") == "signoff")
            print(f"簽收：帳上 {claimed} 筆，簽章有效 {len(vs)} 筆")
            for line in format_stats(compute_stats(events, vs), a.min_n):
                print(line)
            print("鏈頭雜湊：" + events[-1]["hash"][:16])
        elif a.cmd == "export-verified":
            _require_tty()
            pw = getpass.getpass("創辦人簽收口令（匯出已驗簽路由樣本）：")
            out_p = export_verified_samples(pw, Path(a.out) if a.out else None)
            print(f"已驗簽並匯出標準路由樣本：{out_p}")
        elif a.cmd == "status":
            events = read_events()
            ok, msg = verify_chain(events)
            print("鏈檢查：" + msg)
            print(f"派工 {sum(1 for e in events if e.get('type') == 'dispatch')} 筆；"
                  f"帳上簽收 {sum(1 for e in events if e.get('type') == 'signoff')} 筆（未驗證）")
            if not ok:
                sys.exit(1)
        elif a.cmd == "selftest":
            selftest()
    except (ValueError, PermissionError, OSError) as e:
        print(f"阻斷：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
