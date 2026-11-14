"""雪的派工帳本 (dispatch.py)

雪每次分派由程式寫入帳本；結果訊號只有「創辦人以口令簽章的簽收詞」：
收 / 退 / 改派:<閣員代號>

設計重點
  1. 帳本 Append-Only，每筆帶 prev/hash（雜湊鏈），中途竄改會被偵測。
  2. 簽收以 HMAC-SHA256 簽章，金鑰由創辦人口令推導；口令不落地、不進環境變數。
  3. 簽章綁定派工內容的雜湊：事後改派工紀錄，簽收即失效。
  4. init / signoff / stats 一律要求真實終端機；agent 的非互動環境會被拒絕。
  5. 統計只計入簽章有效的簽收；樣本 < MIN_N 一律標示資料不足。

用法
  python dispatch.py init                 # 創辦人一次性，自己在終端機執行
  python dispatch.py dispatch --category 文案 --assign taylor [--mode serial|parallel] [--note ..] [--parent T-..]
  python dispatch.py signoff --task T-... --word 收     # 創辦人親自執行；退；改派:kage
  python dispatch.py stats                # 創辦人親自執行（需口令）
  python dispatch.py status               # 任何人可執行：只驗鏈、列未驗證計數
  python dispatch.py selftest
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
ROSTER = {"kage", "taylor", "josef", "deming", "abacus", "falcon",
          "linus", "neo", "ada", "raven", "meow"}   # 可自行增刪；雪不可派給自己
SIGN_RE = re.compile(r"^(收|退|改派:([a-z]+))$")
PBKDF2_ITER = 200_000
MIN_N = 5
ZERO = "0" * 64


def _ledger() -> Path:
    return VAULT_DIR / "yuki_dispatch.jsonl"


def _meta() -> Path:
    return VAULT_DIR / "yuki_signoff.meta.json"


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


def _derive_key(passphrase: str, salt_hex: str, iters: int) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), bytes.fromhex(salt_hex), iters)


def _kcv(key: bytes) -> str:
    return hmac.new(key, b"yuki-dispatch-kcv", hashlib.sha256).hexdigest()


def init_vault(passphrase: str) -> None:
    if _meta().exists() or _ledger().exists():
        raise ValueError("已初始化，拒絕覆蓋")
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    salt = secrets.token_hex(16)
    kcv = _kcv(_derive_key(passphrase, salt, PBKDF2_ITER))
    _meta().write_text(json.dumps({"salt": salt, "iter": PBKDF2_ITER, "kcv": kcv}, indent=2),
                       encoding="utf-8")
    append_event({"type": "genesis", "kcv": kcv})


def load_key(passphrase: str) -> bytes:
    meta = json.loads(_meta().read_text(encoding="utf-8"))
    events = read_events()
    genesis = events[0] if events else {}
    if genesis.get("type") != "genesis" or genesis.get("kcv") != meta.get("kcv"):
        raise ValueError("meta 與帳本創世紀錄不符，可能被替換")
    key = _derive_key(passphrase, meta["salt"], int(meta["iter"]))
    if not hmac.compare_digest(_kcv(key), meta["kcv"]):
        raise ValueError("口令錯誤")
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


def signoff(task_id: str, word: str, passphrase: str) -> dict:
    m = SIGN_RE.match(word)
    if not m:
        raise ValueError("簽收詞僅限：收 / 退 / 改派:<閣員代號>")
    if word.startswith("改派") and m.group(2) not in ROSTER:
        raise ValueError(f"改派對象不在名冊：{m.group(2)}")
    key = load_key(passphrase)
    d = _find_dispatch(read_events(), task_id)
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


def compute_stats(events: list[dict], signoffs: list[dict]) -> dict:
    disp = {e["task_id"]: e for e in events if e.get("type") == "dispatch"}
    by_task: dict[str, list[dict]] = {}
    for s in signoffs:
        by_task.setdefault(s["task_id"], []).append(s)
    rows: dict = {}
    for tid, ss in by_task.items():
        last = ss[-1]
        if last["word"] == "退":          # 仍在返工，尚未結案
            continue
        d = disp[tid]
        rework = sum(1 for s in ss if s["word"] == "退")
        for a in d["assigned"]:           # 並行任務：每位閣員各計一次
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
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        raise PermissionError("此操作需創辦人在真實終端機親自輸入口令；非互動環境一律拒絕")


def selftest() -> None:
    global VAULT_DIR
    VAULT_DIR = Path(tempfile.mkdtemp(prefix="yuki_dispatch_test_"))
    fails: list[str] = []

    def check(name: str, cond: bool) -> None:
        print(("OK   " if cond else "FAIL ") + name)
        if not cond:
            fails.append(name)

    def raises(fn) -> bool:
        try:
            fn()
        except ValueError:
            return True
        return False

    pw = "correct horse battery staple"
    check("未 init 不得派工", raises(lambda: dispatch("文案", ["taylor"], "serial")))
    init_vault(pw)
    check("重複 init 被拒", raises(lambda: init_vault(pw)))
    t1 = dispatch("文案", ["taylor"], "serial")
    t2 = dispatch("文案", ["taylor"], "serial")
    check("不在名冊不得派工", raises(lambda: dispatch("文案", ["nobody"], "serial")))
    check("非法簽收詞被拒", raises(lambda: signoff(t1, "好", pw)))
    check("改派對象不在名冊被拒", raises(lambda: signoff(t1, "改派:nobody", pw)))
    check("錯誤口令被拒", raises(lambda: signoff(t1, "收", "wrong passphrase 123")))

    signoff(t1, "收", pw)
    signoff(t2, "退", pw)
    signoff(t2, "收", pw)
    # 偽造：沒有金鑰的 agent 寫入假簽章
    append_event({"type": "signoff", "task_id": t1, "word": "收",
                  "dispatch_hash": "x", "nonce": "aa", "sig": "0" * 64})
    # 重放：複製一筆有效簽收
    last = [e for e in read_events() if e.get("type") == "signoff" and e["task_id"] == t2][-1]
    append_event({k: v for k, v in last.items() if k not in ("ts", "prev", "hash")})

    events = read_events()
    vs = verified_signoffs(events, load_key(pw))
    check("偽造與重放不計入（有效簽收應為 3）", len(vs) == 3)
    rows = compute_stats(events, vs)
    r = rows[("文案", "taylor")]
    check("結案 2、一次過 1", r["closed"] == 2 and r["first_pass"] == 1)
    check("樣本不足被標示", "資料不足" in format_stats(rows, MIN_N)[0])
    check("雜湊鏈完整", verify_chain(events)[0])

    p = _ledger()
    p.write_text(p.read_text(encoding="utf-8").replace("文案", "定價", 1), encoding="utf-8")
    check("竄改派工內容被偵測", not verify_chain()[0])

    print("結果：" + ("全數通過" if not fails else f"失敗 {len(fails)} 項"))
    sys.exit(1 if fails else 0)


def main() -> None:
    ap = argparse.ArgumentParser(description="雪的派工帳本")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    d = sub.add_parser("dispatch")
    d.add_argument("--category", required=True)
    d.add_argument("--assign", required=True, help="逗號分隔，如 taylor,kage")
    d.add_argument("--mode", default="serial", choices=["serial", "parallel"])
    d.add_argument("--note", default="")
    d.add_argument("--parent", default="")
    s = sub.add_parser("signoff")
    s.add_argument("--task", required=True)
    s.add_argument("--word", required=True)
    st = sub.add_parser("stats")
    st.add_argument("--min-n", type=int, default=MIN_N)
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
            print("鏈頭雜湊（建議抄到 agent 寫不到的地方）：" + events[-1]["hash"][:16])
        elif a.cmd == "status":
            events = read_events()
            print("鏈檢查：" + verify_chain(events)[1])
            print(f"派工 {sum(1 for e in events if e.get('type') == 'dispatch')} 筆；"
                  f"帳上簽收 {sum(1 for e in events if e.get('type') == 'signoff')} 筆（未驗證）")
        elif a.cmd == "selftest":
            selftest()
    except (ValueError, PermissionError, OSError) as e:
        print(f"阻斷：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
