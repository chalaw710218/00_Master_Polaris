r"""創辦人主權密碼學驗簽核心 (Founder Cryptographic Sovereignty · Master v6.5 中性路徑與反盲簽版)

解決「最大權限 Agent (如幕僚長雪) 自簽、自轉正、刪鎖或手寫 JSONL 偽造事件」之零信任密碼學模組：
  1. 信任錨中性化（遵守紅線 3）：
     - 廢除雪的專屬路徑與專屬標籤，統一儲存於 `bionic_core/vaults/founder_vault.meta.json`。
     - KCV 標籤改為中性之 `polaris-founder-kcv-v65`。
  2. 創辦人公鑰指紋 (Public Key Fingerprint)：
     - 提供 `get_fingerprint()`：計算 `sha256(pub_y)[:16]`。
     - 每次終端機互動簽章或公鑰驗簽時明確顯示指紋，供創辦人手機備查防替換。
  3. 反盲簽明細展示 (Anti-Blind-Signing)：
     - 在終端機要求輸入口令前，強制完整列印待簽操作之全量審批明細（規則型態、Pattern、N、With/Without 指標、資料集雜湊、審計掃描結果），拒絕盲簽。
  4. 確定性 Schnorr 公鑰驗簽 (RFC 3526 Group 14 2048-bit)：
     - 私鑰純量 $x$ 由創辦人口令唯一推導（不落地、不進環境變數）。
     - 公鑰 $y = g^x \bmod p$ 存入 `meta.json`。
     - `fold()` / `is_locked()` 免口令直接驗算 $g^s \cdot y^{q-e} \bmod p$！
"""
from __future__ import annotations

import getpass
import hashlib
import hmac
import json
import secrets
import sys
from pathlib import Path

CORE_DIR = Path(__file__).resolve().parent
VAULT_DIR = CORE_DIR / "vaults"
DEFAULT_META_PATH = VAULT_DIR / "founder_vault.meta.json"
PIN_PATH: Path | None = None
DEFAULT_PIN_PATH = VAULT_DIR / "founder_pin.txt"
PBKDF2_ITER = 200_000
KCV_LABEL = b"polaris-founder-kcv-v65"

# RFC 3526 Group 14 (2048-bit MODP Safe Prime p = 2q + 1)
_RFC3526_P_HEX = (
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
    "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
    "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
    "E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
    "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D"
    "C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
    "83655D23DCA3AD961C62F356208552BB9ED529077096966D"
    "670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
    "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9"
    "DE2BCBF6955817183995497CEA956AE515D2261898FA0510"
    "15728E5A8AACAA68FFFFFFFFFFFFFFFF"
)
P = int(_RFC3526_P_HEX, 16)
Q = (P - 1) // 2
G = 4  # 4 = 2^2 為模安全質數 P 之二次剩餘，階數嚴格為質數 Q


def _canon(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def require_tty() -> None:
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        raise PermissionError("此高風險操作需創辦人在真實終端機 (TTY) 親自輸入口令；非互動環境一律拒絕")


def derive_key(passphrase: str, salt_hex: str, iters: int = PBKDF2_ITER) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), bytes.fromhex(salt_hex), iters)


def compute_kcv(key: bytes) -> str:
    return hmac.new(key, KCV_LABEL, hashlib.sha256).hexdigest()


def derive_keypair(key: bytes) -> tuple[int, int]:
    """由 PBKDF2 金鑰推導 Schnorr 私鑰純量 x 與公鑰 y = G^x mod P。"""
    x_raw = hmac.new(key, b"polaris-founder-schnorr-priv-v65", hashlib.sha256).digest()
    x = (int.from_bytes(x_raw, "big") % (Q - 1)) + 1
    y = pow(G, x, P)
    return x, y


def compute_fingerprint(pub_y_hex: str) -> str:
    return hashlib.sha256(pub_y_hex.strip().lower().encode("utf-8")).hexdigest()[:16]


def get_pin_path() -> Path:
    return PIN_PATH or DEFAULT_PIN_PATH


def pin_meta(meta_path: Path | None = None) -> str:
    """將指定 meta 檔案的公鑰指紋釘死到 PIN 檔案中，作為硬性信任錨。"""
    mp = meta_path or DEFAULT_META_PATH
    if not mp.exists():
        raise ValueError(f"找不到 meta 檔案，無法鎖定 PIN：{mp}")
    meta = json.loads(mp.read_text(encoding="utf-8"))
    fg = meta.get("fingerprint", compute_fingerprint(meta["pub_y"]))
    pp = get_pin_path()
    pp.parent.mkdir(parents=True, exist_ok=True)
    pp.write_text(fg.strip() + "\n", encoding="utf-8")
    return fg


def read_pinned_fingerprint() -> str | None:
    pp = get_pin_path()
    if pp.exists():
        content = pp.read_text(encoding="utf-8").strip()
        if content:
            return content
    return None


def build_meta_dict(passphrase: str, salt_hex: str | None = None, iters: int = PBKDF2_ITER) -> dict:
    salt = salt_hex or secrets.token_hex(16)
    key = derive_key(passphrase, salt, iters)
    kcv = compute_kcv(key)
    _, y = derive_keypair(key)
    pub_y_hex = format(y, "x")
    return {
        "salt": salt,
        "iter": iters,
        "kcv": kcv,
        "pub_y": pub_y_hex,
        "fingerprint": compute_fingerprint(pub_y_hex),
    }


def init_meta_file(passphrase: str, meta_path: Path | None = None) -> dict:
    mp = meta_path or DEFAULT_META_PATH
    if mp.exists():
        raise ValueError(f"創辦人金鑰設定檔已存在，拒絕覆蓋：{mp}")
    mp.parent.mkdir(parents=True, exist_ok=True)
    meta = build_meta_dict(passphrase)
    mp.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def load_verified_key(passphrase: str, meta_path: Path | None = None) -> tuple[bytes, dict]:
    mp = meta_path or DEFAULT_META_PATH
    if not mp.exists():
        raise ValueError(f"尚未初始化創辦人簽收口令設定檔 ({mp})，請先由創辦人執行 dispatch.py init")
    meta = json.loads(mp.read_text(encoding="utf-8"))
    key = derive_key(passphrase, meta["salt"], int(meta["iter"]))
    if not hmac.compare_digest(compute_kcv(key), meta["kcv"]):
        raise ValueError("創辦人口令錯誤")
    if "pub_y" not in meta:
        _, y = derive_keypair(key)
        pub_y_hex = format(y, "x")
        meta["pub_y"] = pub_y_hex
        meta["fingerprint"] = compute_fingerprint(pub_y_hex)
        mp.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return key, meta


def print_anti_blind_signing_dossier(payload: dict, fingerprint: str) -> None:
    """在終端機列印待審批之完整明細，防創辦人被騙盲簽。"""
    act = payload.get("action", "unknown")
    print("\n" + "=" * 65)
    print(f"🛡️  創辦人主權密碼學審批台 (Anti-Blind-Signing) · 指紋: [{fingerprint}]")
    print("=" * 65)
    if act == "promote":
        print(f"📌 操作類型：高風險規則轉正 (Promote Rule)")
        print(f"🏛️  辦公室代號：{payload.get('office')}  ｜  規則單號：{payload.get('rule_id')}")
        print(f"📐 規則型態：{payload.get('kind')} (scope={payload.get('scope')})")
        print(f"🎯 語義模式：{payload.get('pattern')}")
        print(f"📊 真值指標：遵守組={payload.get('with_metric')} vs 對照組={payload.get('without_metric')} (N={payload.get('n')})")
        print(f"🧪 留出集檢驗 (Holdout Split)：{'PASS (優於對照)' if payload.get('holdout_passed') else 'FAIL'}")
        print(f"📦 資料集快照簽章：{str(payload.get('trial_sha256', ''))[:16]}...")
        print(f"📜 物理論述證據：{payload.get('evidence')}")
    elif act == "audit_done":
        print(f"📌 操作類型：十輪強制衝突審計解鎖 (Audit-Done Release)")
        print(f"🏛️  辦公室代號：{payload.get('office')}  ｜  解鎖關卡：第 {payload.get('cycle')} 輪")
        print(f"🔗 前置 Tick 雜湊：{str(payload.get('last_tick_hash', ''))[:16]}...")
        print(f"🔍 程式化掃描簽章：{payload.get('scan_digest')}")
        print(f"📝 審計報告雜湊：{str(payload.get('report_sha256', ''))[:16]}...")
    elif act == "route_samples":
        print(f"📌 操作類型：匯出已驗簽幕僚長路由樣本 (Export Verified Route Samples)")
        print(f"📊 結案任務筆數：{payload.get('count')} 筆")
        print(f"📦 樣本列標準雜湊：{str(payload.get('samples_sha256', ''))[:16]}...")
    else:
        print(f"📌 操作類型：{act}")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    print("-" * 65)
    print("⚠️  請親自核對上述數值無誤後，於下方輸入口令簽署授權（口令不落地、不進環境變數）：")


def sign_founder_action(
    payload: dict,
    meta_path: Path | None = None,
    _test_passphrase: str | None = None,
    prompt_label: str = "創辦人授權口令：",
) -> dict:
    mp = meta_path or DEFAULT_META_PATH
    if _test_passphrase is not None:
        try:
            mp.resolve().relative_to(VAULT_DIR.resolve())
            raise PermissionError("安全阻斷：正式 vaults 嚴禁傳入 _test_passphrase，必須於真實終端機輸入口令")
        except ValueError:
            pass
        passphrase = _test_passphrase
    else:
        require_tty()
        # 讀取 meta 中的公鑰指紋供創辦人核對
        meta_init = json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else {}
        fg = meta_init.get("fingerprint", "UNINITIALIZED")
        print_anti_blind_signing_dossier(payload, fg)
        passphrase = getpass.getpass(prompt_label)

    key, meta = load_verified_key(passphrase, mp)
    x, _ = derive_keypair(key)
    nonce = secrets.token_hex(8)
    bound_payload = {**payload, "nonce": nonce, "kcv": meta["kcv"]}
    msg_bytes = _canon(bound_payload).encode("utf-8")

    hmac_sig = hmac.new(key, msg_bytes, hashlib.sha256).hexdigest()

    k_raw = hmac.new(key, b"schnorr-k:" + msg_bytes, hashlib.sha256).digest()
    k = (int.from_bytes(k_raw, "big") % (Q - 1)) + 1
    r = pow(G, k, P)
    r_bytes = r.to_bytes(256, "big")
    e = int.from_bytes(hashlib.sha256(r_bytes + msg_bytes).digest(), "big") % Q
    s = (k + x * e) % Q

    return {
        "nonce": nonce,
        "kcv": meta["kcv"],
        "fingerprint": meta.get("fingerprint", compute_fingerprint(meta["pub_y"])),
        "hmac_sig": hmac_sig,
        "schnorr_e": format(e, "x"),
        "schnorr_s": format(s, "x"),
    }


def verify_founder_action(
    payload: dict,
    sig_bundle: dict | None,
    meta_path: Path | None = None,
    expected_fingerprint: str | None = None,
) -> tuple[bool, str]:
    """驗證高風險操作簽章。以公鑰 pub_y 驗證 Schnorr 簽章；若提供 expected_fingerprint 則額外核對指紋。"""
    if not isinstance(sig_bundle, dict):
        return False, "缺少創辦人密碼學簽章 (founder_sig)"
    mp = meta_path or DEFAULT_META_PATH
    if not mp.exists():
        return False, f"找不到創辦人金鑰設定檔 ({mp})，無法驗簽"
    try:
        meta = json.loads(mp.read_text(encoding="utf-8"))
        if sig_bundle.get("kcv") != meta.get("kcv"):
            return False, "簽章 kcv 與設定檔不符"
        if "pub_y" not in meta:
            return False, "設定檔缺少公鑰 pub_y"

        calc_fg = compute_fingerprint(meta["pub_y"])
        if "fingerprint" in meta and meta["fingerprint"] != calc_fg:
            return False, f"設定檔內記載之指紋遭竄改 (meta={meta['fingerprint']} vs 實算={calc_fg})"
        meta_fg = calc_fg
        pinned_fg = read_pinned_fingerprint()
        if pinned_fg and meta_fg != pinned_fg:
            return False, f"公鑰已被更換（指紋與 PIN 錨定檔案不符：meta={meta_fg} vs pin={pinned_fg}）"
        if expected_fingerprint and meta_fg != expected_fingerprint:
            return False, f"公鑰指紋不相符（預期 {expected_fingerprint} vs 檔案 {meta_fg}）"

        pub_y = int(meta["pub_y"], 16)
        e = int(str(sig_bundle.get("schnorr_e", "")), 16)
        s = int(str(sig_bundle.get("schnorr_s", "")), 16)
        if not (0 < e < Q and 0 < s < Q):
            return False, "Schnorr 簽章參數超出有限域範圍"

        bound_payload = {**payload, "nonce": sig_bundle["nonce"], "kcv": sig_bundle["kcv"]}
        msg_bytes = _canon(bound_payload).encode("utf-8")

        r_calc = (pow(G, s, P) * pow(pub_y, Q - e, P)) % P
        r_bytes = r_calc.to_bytes(256, "big")
        e_calc = int.from_bytes(hashlib.sha256(r_bytes + msg_bytes).digest(), "big") % Q
        if e_calc != e:
            return False, "Schnorr 公鑰驗簽失敗（偽造簽章或內容遭竄改）"

        return True, f"創辦人密碼學簽章驗證通過 (指紋: {meta_fg})"
    except Exception as ex:
        return False, f"驗簽異常：{ex}"
