"""
auth_google_business.py
========================
極星 Google 商家 (Google Business Profile) 官方 OAuth2 授權認證工具
主理：情報長 雪柔 (Sheryl Sandberg / 獵鷹) ✕ CTO 林納斯 (Linus)

功能：
1. 讀取 client_secret.json
2. 啟動本機授權瀏覽器視窗 (OAuth 2.0 InstalledAppFlow)
3. 取得永久 Refresh Token 並安全儲存至 token.json
4. 自動探測創辦人管理之 Google 商家帳戶 (Account Management API)
5. 列出「職人食堂」之 Location ID 與商家資訊
"""

import os
import sys
import json
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# 確保 Windows UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET_FILE = os.path.join(CURRENT_DIR, "client_secret.json")
TOKEN_FILE = os.path.join(CURRENT_DIR, "token.json")

# 請求管理權限範圍
SCOPES = [
    "https://www.googleapis.com/auth/business.manage"
]

def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception:
            creds = None

    # 如果沒有有效憑證，啟動授權登入
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 正在以 Refresh Token 自動無感續期金鑰...")
            creds.refresh(Request())
        else:
            print("🌐 正在為您開啟瀏覽器進行 Google 商家管理員授權...")
            print("👉 請在跳出的瀏覽器視窗中，登入您的管理員帳號並點選【允許】！")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0, prompt='consent')
            
        # 儲存憑證供後續 Python 代碼無限期使用
        with open(TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())
        print(f"✅ 授權憑證已成功保存至：{TOKEN_FILE}")

    print("\n🔍 正在探測創辦人管理之 Google 商家清單...")
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }
    
    # 呼叫 Account Management API
    url = "https://mybusinessaccountmanagement.googleapis.com/v1/accounts"
    resp = requests.get(url, headers=headers)
    print(f"📡 API 回應狀態碼：{resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        print("🎉 成功讀取到商家帳戶清單：")
        accounts = data.get("accounts", [])
        for acc in accounts:
            print(f"🏢 帳戶名稱：{acc.get('accountName')} | ID：{acc.get('name')}")
            
            # 探測該帳戶下的 Locations (門市清單)
            acc_id = acc.get("name")
            loc_url = f"https://mybusinessbusinessinformation.googleapis.com/v1/{acc_id}/locations?readMask=name,title,storefrontAddress"
            loc_resp = requests.get(loc_url, headers=headers)
            if loc_resp.status_code == 200:
                loc_data = loc_resp.json()
                locations = loc_data.get("locations", [])
                for loc in locations:
                    print(f"   📍 門市地標：{loc.get('title')} ({loc.get('name')})")
            else:
                print(f"   ⚠️ 讀取門市列表狀態：{loc_resp.status_code} ({loc_resp.text})")
    else:
        print("⚠️ 探測帳戶回應：", resp.status_code, resp.text)
        print("\n💡 提示：若出現 403 PERMISSION_DENIED，表示 GCP 專案尚需開啟 MyBusiness API 或申請白名單配額。")

if __name__ == "__main__":
    authenticate()
