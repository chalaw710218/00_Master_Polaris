"""Threads 閉環安全發布器 (Threads Closed-Loop Safe Publisher)

核心原則：
未經仿生學習閉環守門員 (bionic_closed_loop_gatekeeper.py) 審計通過者，
物理層面絕對禁止調用 Meta Graph API 發布！

用法：
  python publish_with_gatekeeper.py --text "貼文內容" [--dry-run]
  python publish_with_gatekeeper.py --file draft.txt [--image path_or_url]
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def find_workspace_root() -> Path:
    cur = Path(__file__).resolve()
    for p in [cur] + list(cur.parents):
        if (p / ".git").exists() or (p / "00-01_Master_Polaris_Map.md").exists():
            return p
    return Path.cwd()


ROOT = find_workspace_root()
GATEKEEPER = (
    ROOT
    / ".agents"
    / "skills"
    / "threads-growth-auditor"
    / "scripts"
    / "bionic_closed_loop_gatekeeper.py"
)


def load_env() -> dict:
    """由根目錄 .secrets.env 讀取金鑰。"""
    env_file = ROOT / ".secrets.env"
    env_vars = {}
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip()
    return env_vars


def preflight_check(text: str, persona: str = "meow", threshold: int = 90) -> bool:
    """調用閉環守門員進行物理質檢。"""
    if not GATEKEEPER.exists():
        sys.stderr.write(f"[WARN] 找不到守門員腳本: {GATEKEEPER}，無法進行閉環質檢！\n")
        return False

    cmd = [
        sys.executable,
        str(GATEKEEPER),
        "--text",
        text,
        "--persona",
        persona,
        "--threshold",
        str(threshold),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(proc.stdout)
    if proc.returncode != 0:
        if proc.stderr:
            sys.stderr.write(proc.stderr)
        return False
    return True


def publish_thread(text: str, image_url: str | None = None, dry_run: bool = False) -> str | None:
    """直連 Meta Threads API 執行發布。"""
    env = load_env()
    user_id = env.get("THREADS_USER_ID")
    token = env.get("THREADS_ACCESS_TOKEN")

    if dry_run:
        print("🧪 [DRY-RUN 模擬發布模式] 質量閘門已放行，模擬成功，不產生真實網路請求。")
        return "dry_run_success_post_id_99999"

    if not user_id or not token:
        print("❌ 錯誤：尚未於 .secrets.env 設定 THREADS_USER_ID 或 THREADS_ACCESS_TOKEN")
        return None

    try:
        import requests
    except ImportError:
        print("❌ 錯誤：未安裝 requests 套件")
        return None

    api_base = "https://graph.threads.net/v1.0"

    # 1. 建立容器
    payload = {
        "access_token": token,
        "text": text,
        "media_type": "IMAGE" if image_url else "TEXT",
    }
    if image_url:
        payload["image_url"] = image_url

    r1 = requests.post(f"{api_base}/{user_id}/threads", data=payload).json()
    creation_id = r1.get("id")
    if not creation_id:
        print(f"❌ 建立容器失敗: {r1}")
        return None

    time.sleep(2)

    # 2. 正式發布
    r2 = requests.post(
        f"{api_base}/{user_id}/threads_publish",
        data={"access_token": token, "creation_id": creation_id},
    ).json()

    post_id = r2.get("id")
    if post_id:
        print(f"🎉 發布成功！Post ID: {post_id}")
        print(f"🔗 貼文網址: https://www.threads.net/@/post/{post_id}")
        return post_id
    else:
        print(f"❌ 發布失敗: {r2}")
        return None


def main():
    ap = argparse.ArgumentParser(description="Threads 閉環安全發布器")
    ap.add_argument("--file", help="草稿檔案路徑")
    ap.add_argument("--text", help="草稿內容文字")
    ap.add_argument("--persona", default="meow", choices=["meow", "shadow"])
    ap.add_argument("--threshold", type=int, default=90)
    ap.add_argument("--image", help="附帶圖片路徑或 URL")
    ap.add_argument("--dry-run", action="store_true", help="演練模式，通過審查但不實際發送")
    a = ap.parse_args()

    if a.file:
        with open(a.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif a.text:
        text = a.text
    else:
        text = sys.stdin.read()

    print("🚀 [Step 1/2] 啟動仿生學習出廠質量安燈檢驗...")
    passed = preflight_check(text, a.persona, a.threshold)

    if not passed:
        print("\n🛑 [發布中斷] 貼文未通過仿生學習出廠標準，硬性阻斷 Meta API 調用！請修正後重試。")
        sys.exit(1)

    print("📡 [Step 2/2] 質量驗收合格，開始調用 Meta Threads API 發布...")
    post_id = publish_thread(text, a.image, a.dry_run)
    if not post_id:
        sys.exit(1)


if __name__ == "__main__":
    main()
