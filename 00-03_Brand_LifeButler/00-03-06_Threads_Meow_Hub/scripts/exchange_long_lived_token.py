#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exchange_long_lived_token.py — Threads 1小時短期權杖自動升級 60 天長效權杖與自動續期工具

問題根因：
Meta Graph API Explorer 產生的 THAA... 權杖預設僅有 1 小時效期 (Short-Lived Token)。
必須在 1 小時有效期限內，使用 THREADS_APP_SECRET 呼叫：
  GET https://graph.threads.net/access_token?grant_type=th_exchange_token&client_secret=...&access_token=...
換取 60 天有效之 Long-Lived Token，之後即可透過 th_refresh_token 無限自動續期。
"""

import sys
import requests
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_PATH = ROOT_DIR / ".secrets.env"


def load_env():
    env_vars = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s and not s.startswith("#") and "=" in s:
                k, v = s.split("=", 1)
                env_vars[k.strip()] = v.strip()
    return env_vars


def update_env_token(new_token: str):
    lines = ENV_PATH.read_text(encoding="utf-8").splitlines()
    new_lines = []
    updated = False
    for line in lines:
        if line.strip().startswith("THREADS_ACCESS_TOKEN="):
            new_lines.append(f"THREADS_ACCESS_TOKEN={new_token}")
            updated = True
        else:
            new_lines.append(line)
    if not updated:
        new_lines.append(f"THREADS_ACCESS_TOKEN={new_token}")
    ENV_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def exchange_or_refresh(input_token: str = None):
    env = load_env()
    secrets_to_try = [s for s in [env.get("THREADS_APP_SECRET"), env.get("FB_APP_SECRET")] if s]
    token = input_token or env.get("THREADS_ACCESS_TOKEN")

    if not token or not secrets_to_try:
        print("❌ 缺少 THREADS_ACCESS_TOKEN 或 應用程式密鑰")
        return False

    # 1. 嘗試用短期 Token 換取 60 天長效 Token
    for idx, secret in enumerate(secrets_to_try, 1):
        print(f"🔄 正在向 Meta 申請將短期權杖升級為 60 天長效權杖 (th_exchange_token, 密鑰候選 {idx}/{len(secrets_to_try)})...")
        r = requests.get(
            "https://graph.threads.net/access_token",
            params={
                "grant_type": "th_exchange_token",
                "client_secret": secret,
                "access_token": token,
            },
            timeout=15,
        )
        if r.status_code == 200 and r.json().get("access_token"):
            data = r.json()
            long_token = data["access_token"]
            expires_in = data.get("expires_in", 0)
            days = expires_in / 86400
            import datetime
            exp_dt = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
            update_env_token(long_token)
            masked_data = {k: ("***MASKED***" if k == "access_token" else v) for k, v in data.items()}
            print(f"📦 API 原始回應 (Token 已遮罩): {masked_data}")
            print(f"✅ 成功換取 60 天長效權杖 (expires_in={expires_in} 秒, 效期: {days:.2f} 天, 到期日: {exp_dt.strftime('%Y-%m-%d %H:%M:%S')}) 並已寫入 .secrets.env！")
            return True
        else:
            print(f"ℹ️ th_exchange_token 回應 ({r.status_code}): {r.text}")
        print(f"ℹ️ th_exchange_token 回應 ({r.status_code}): {r.text}")

    # 2. 若本身已是長效 Token，嘗試 refresh 續期 60 天
    print("🔄 嘗試對長效權杖執行續期 (th_refresh_token)...")
    r2 = requests.get(
        "https://graph.threads.net/refresh_access_token",
        params={"grant_type": "th_refresh_token", "access_token": token},
        timeout=15,
    )
    if r2.status_code == 200 and r2.json().get("access_token"):
        data = r2.json()
        refreshed_token = data["access_token"]
        expires_in = data.get("expires_in", 0)
        days = expires_in / 86400
        import datetime
        exp_dt = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
        update_env_token(refreshed_token)
        masked_data = {k: ("***MASKED***" if k == "access_token" else v) for k, v in data.items()}
        print(f"📦 API 原始回應 (Token 已遮罩): {masked_data}")
        print(f"✅ 成功續期 60 天長效權杖 (expires_in={expires_in} 秒, 效期: {days:.2f} 天, 到期日: {exp_dt.strftime('%Y-%m-%d %H:%M:%S')}) 並已寫入 .secrets.env！")
        return True
    else:
        print(f"❌ th_refresh_token 失敗 ({r2.status_code}): {r2.text}")
        return False


if __name__ == "__main__":
    arg_token = sys.argv[1] if len(sys.argv) > 1 else None
    exchange_or_refresh(arg_token)
