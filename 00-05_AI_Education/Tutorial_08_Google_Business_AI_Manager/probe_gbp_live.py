import os
import sys
import json
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(CURRENT_DIR, "token.json")
SCOPES = ["https://www.googleapis.com/auth/business.manage"]

def probe():
    if not os.path.exists(TOKEN_FILE):
        print("❌ token.json does not exist!")
        return

    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if creds.expired and creds.refresh_token:
        print("🔄 Refreshing credentials...")
        creds.refresh(Request())
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }

    print("🔑 Token valid! Querying Google Business Profile Accounts...")
    url = "https://mybusinessaccountmanagement.googleapis.com/v1/accounts"
    resp = requests.get(url, headers=headers)
    print(f"Status Code: {resp.status_code}")
    print("Response JSON:")
    try:
        data = resp.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # Check locations under each account
        accounts = data.get("accounts", [])
        for acc in accounts:
            acc_name = acc.get("name")
            print(f"\n🏢 Checking Locations under Account: {acc_name} ({acc.get('accountName')})")
            loc_url = f"https://mybusinessbusinessinformation.googleapis.com/v1/{acc_name}/locations?readMask=name,title,storefrontAddress,metadata"
            loc_resp = requests.get(loc_url, headers=headers)
            print(f"   Locations Status: {loc_resp.status_code}")
            try:
                loc_data = loc_resp.json()
                print("   Locations Data:", json.dumps(loc_data, indent=2, ensure_ascii=False))
            except Exception as e:
                print("   Locations parse error:", e, loc_resp.text)
                
    except Exception as e:
        print("Parse error:", e, resp.text)

if __name__ == "__main__":
    probe()
