"""創辦人主權密碼學驗簽核心 (Founder Cryptographic Sovereignty · Master v6.4)

解決「最大權限 Agent (如幕僚長雪) 自簽、自轉正、刪鎖或手寫 JSONL 偽造事件」之零信任密碼學模組：
  1. 沿用 `dispatch.py` 之 `PBKDF2-HMAC-SHA256` (200,000 次迭代) 口令推導金鑰與 `kcv` 校驗。
  2. 結合 RFC 3526 Group 14 (2048-bit 安全質數 $p = 2q + 1$) 之確定性 Schnorr 公鑰驗簽：
     - 私鑰純量 $x$ 由創辦人口令金鑰唯一推導（不落地、不進環境變數）。
     - 公鑰 $y = g^x \bmod p$ 存入 `meta.json`。
     - 簽章時：強制檢查真實終端機 (`_require_tty()`)，輸入創辦人口令後同時產出 `hmac_sig` 與 Schnorr 簽章 `(schnorr_e, schnorr_s)`。
     - 驗簽時 (`fold()` / `is_locked()` / `enforce.py`)：**無須創辦人再次輸入口令**，直接以公鑰 $y$ 驗算 $g^s \cdot y^{q-e} \bmod p$！
     - 任何 Agent 若無創辦人口令，即使直接修改 JSONL 並重算雜湊鏈，亦無法偽造有效簽章，`fold()` 當場識破並打入 `tampered_rejected`。
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
ROOT_DIR = CORE_DIR.parent.parent.parent.parent
DEFAULT_META_PATH = (
    ROOT_DIR
    / ".agents"
    / "skills"
    / "atom-yuki-autonomous-executive-learner"
    / "vaults"
    / "yuki_signoff.meta.json"
)

PBKDF2_ITER = 200_000

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
    return hmac.new(key, b"yuki-dispatch-kcv", hashlib.sha256).hexdigest()


def derive_keypair(key: bytes) -> tuple[int, int]:
    """由 PBKDF2 金鑰推導 Schnorr 私鑰純量 x 與公鑰 y = G^x mod P。"""
    x_raw = hmac.new(key, b"polaris-founder-schnorr-priv-v64", hashlib.sha256).digest()
    x = (int.from_bytes(x_raw, "big") % (Q - 1)) + 1
    y = pow(G, x, P)
    return x, y


def build_meta_dict(passphrase: str, salt_hex: str | None = None, iters: int = PBKDF2_ITER) -> dict:
    salt = salt_hex or secrets.token_hex(16)
    key = derive_key(passphrase, salt, iters)
    kcv = compute_kcv(key)
    _, y = derive_keypair(key)
    return {
        "salt": salt,
        "iter": iters,
        "kcv": kcv,
        "pub_y": format(y, "x"),
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
    # 若舊版 meta 尚無 pub_y，驗證口令通過後自動補齊公鑰欄位
    if "pub_y" not in meta:
        _, y = derive_keypair(key)
        meta["pub_y"] = format(y, "x")
        mp.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return key, meta


def sign_founder_action(
    payload: dict,
    meta_path: Path | None = None,
    _test_passphrase: str | None = None,
    prompt_label: str = "創辦人簽收口令：",
) -> dict:
    """簽署高風險操作（promote / route 驗算 / 高風險 audit-done）。
    正式環境強制檢查 TTY 並由 getpass 讀取口令；_test_passphrase 僅允許於非正式環境之暫存目錄自檢使用。
    """
    mp = meta_path or DEFAULT_META_PATH
    if _test_passphrase is not None:
        # 安全防呆：_test_passphrase 嚴禁用於正式 ROOT_DIR 下的 vaults
        try:
            mp.resolve().relative_to(ROOT_DIR.resolve())
            raise PermissionError("安全阻斷：正式工作區帳本嚴禁傳入 _test_passphrase，必須於真實終端機輸入口令")
        except ValueError:
            pass
        passphrase = _test_passphrase
    else:
        require_tty()
        passphrase = getpass.getpass(prompt_label)

    key, meta = load_verified_key(passphrase, mp)
    x, _ = derive_keypair(key)
    nonce = secrets.token_hex(8)
    bound_payload = {**payload, "nonce": nonce, "kcv": meta["kcv"]}
    msg_bytes = _canon(bound_payload).encode("utf-8")

    # 1. 對稱 HMAC-SHA256 簽章
    hmac_sig = hmac.new(key, msg_bytes, hashlib.sha256).hexdigest()

    # 2. 確定性 Schnorr 簽章 (供 fold() / is_locked() 免口令公鑰驗證)
    k_raw = hmac.new(key, b"schnorr-k:" + msg_bytes, hashlib.sha256).digest()
    k = (int.from_bytes(k_raw, "big") % (Q - 1)) + 1
    r = pow(G, k, P)
    r_bytes = r.to_bytes(256, "big")
    e = int.from_bytes(hashlib.sha256(r_bytes + msg_bytes).digest(), "big") % Q
    s = (k + x * e) % Q

    return {
        "nonce": nonce,
        "kcv": meta["kcv"],
        "hmac_sig": hmac_sig,
        "schnorr_e": format(e, "x"),
        "schnorr_s": format(s, "x"),
    }


def verify_founder_action(
    payload: dict,
    sig_bundle: dict | None,
    meta_path: Path | None = None,
    key: bytes | None = None,
) -> tuple[bool, str]:
    """驗證高風險操作簽章。無須口令即可透過 meta.json 中的公鑰 pub_y 攔截任何偽造簽章。"""
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

        pub_y = int(meta["pub_y"], 16)
        e = int(str(sig_bundle.get("schnorr_e", "")), 16)
        s = int(str(sig_bundle.get("schnorr_s", "")), 16)
        if not (0 < e < Q and 0 < s < Q):
            return False, "Schnorr 簽章參數超出有限域範圍"

        bound_payload = {**payload, "nonce": sig_bundle["nonce"], "kcv": sig_bundle["kcv"]}
        msg_bytes = _canon(bound_payload).encode("utf-8")

        # 公鑰驗證：r_calc = (G^s * y^(Q - e)) mod P
        r_calc = (pow(G, s, P) * pow(pub_y, Q - e, P)) % P
        r_bytes = r_calc.to_bytes(256, "big")
        e_calc = int.from_bytes(hashlib.sha256(r_bytes + msg_bytes).digest(), "big") % Q
        if e_calc != e:
            return False, "Schnorr 公鑰驗簽失敗（偽造簽章或內容遭竄改）"

        if key is not None:
            exp_hmac = hmac.new(key, msg_bytes, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(exp_hmac, str(sig_bundle.get("hmac_sig", ""))):
                return False, "HMAC 驗簽失敗"

        return True, "創辦人密碼學簽章驗證通過"
    except Exception as ex:
        return False, f"驗簽異常：{ex}"
