import os
import sys
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/drive.file'
]

FORM_ID = "1mzDnnKdGgh8o73gN1S9vxWJDW8ixLEuVgLtXQCsFSRA"
SECRET_PATH = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager\client_secret.json")
TOKEN_PATH = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\google_forms_token.json")

def get_service():
    creds = None
    if TOKEN_PATH.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
        except Exception as e:
            print("Token read error:", e)
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("Token refreshed successfully!")
            except Exception as e:
                print("Token refresh failed, re-authenticating:", e)
                creds = None
                
        if not creds:
            print("Starting OAuth local server flow...")
            flow = InstalledAppFlow.from_client_secrets_file(str(SECRET_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
            with open(TOKEN_PATH, 'w', encoding='utf-8') as f:
                f.write(creds.to_json())
            print(f"New credentials saved to {TOKEN_PATH}")

    return build('forms', 'v1', credentials=creds)

def update_form():
    service = get_service()
    if not service:
        print("Cannot get Google Forms service.")
        return

    print("Fetching current form structure...")
    form_data = service.forms().get(formId=FORM_ID).execute()
    items = form_data.get("items", [])
    print(f"Current items count: {len(items)}")

    # 檢查是否已經有講次選擇題目
    has_lecture_choice = False
    for item in items:
        if "實戰講次" in item.get("title", ""):
            has_lecture_choice = True
            break

    updated_description = (
        "【限額 10 席 · 純實體現場教學 · 解決真實生意難題】\n\n"
        "各位好朋友、老夥伴您好：\n"
        "歡迎申請由生活管家創辦人 陳品碩（闆仔）親自授權主講之「2026 秋季 AI 家教實戰系列班」。\n\n"
        "📅【秋季三週完整實戰課表】（每週三 14:00 - 16:00 ｜ 台東市正氣北路166巷90號家宅）：\n"
        "• 第 1 講 ｜ 11/11 (週三)：NotebookLM 數位大腦 ✕ 漏斗式深挖提問法（🔥 10 席已過半，僅剩最後 5 席！）\n"
        "• 第 2 講 ｜ 11/18 (週三)：Antigravity 操作 ✕ Meta 官方自動發文串接 (FB / Threads API 自動排程與秒回)\n"
        "• 第 3 講 ｜ 11/25 (週三)：資料架構管理 ✕ Antigravity 擬人化工程 (心智逆向工程 ＋ 24H 店長分身)\n\n"
        "⚠️【入席重要須知】\n"
        "1. 本課程堅持 100% 純實體現場教學，絕無線上同步！導師手把手巡桌排錯，保證做出專屬成果。\n"
        "2. 現場嚴格限額 10 席，多一張椅子都不加。\n"
        "3. 若申請人數超額，未排入本梯次者將優先為您保留至【第二梯次加開場】。\n\n"
        "📍 上課地點：生活管家·家宅（台東市正氣北路166巷90號）\n"
        "⏰ 上課時間：每週三下午 14:00 - 16:00\n"
        "💰 學費政策：老學員免收學費（0元免單回娘家特權）｜ 全新夥伴單堂實戰 NT$ 500 元（可單選或三堂完整聯報，審查通過後通知付款）\n"
        "💬 官方諮詢 LINE：https://lin.ee/z83YSq6"
    )

    requests = [
        # 1. 更新表單說明文字與標題
        {
            "updateFormInfo": {
                "info": {
                    "description": updated_description
                },
                "updateMask": "description"
            }
        }
    ]

    # 2. 如果尚未加入講次勾選題，則新增題目
    if not has_lecture_choice:
        # 找到學員身分（第 4 或 5 題）的位置插入
        insert_idx = 5
        requests.append({
            "createItem": {
                "item": {
                    "title": "5. 您預計報名參加的實戰講次（可複選，每堂 $500 / 老學員全免單）",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "CHECKBOX",
                                "options": [
                                    {"value": "【第 1 講】11/11 (週三) 14:00-16:00 ｜ NotebookLM 數位大腦 ✕ 漏斗深挖提問法（🔥 僅剩最後 5 席！）"},
                                    {"value": "【第 2 講】11/18 (週三) 14:00-16:00 ｜ Antigravity 操作 ✕ Meta 官方自動發文串接 (FB / Threads API)"},
                                    {"value": "【第 3 講】11/25 (週三) 14:00-16:00 ｜ 資料架構管理 ✕ 擬人化店長分身工程 (心智逆向工程 ＋ AI 分身)"},
                                    {"value": "👑 三堂完整聯報（優先鎖定三週實體固定席次）"}
                                ]
                            }
                        }
                    }
                },
                "location": {
                    "index": insert_idx
                }
            }
        })

    print(f"Applying {len(requests)} update requests to Google Form...")
    res = service.forms().batchUpdate(formId=FORM_ID, body={"requests": requests}).execute()
    print("🎉 Google 表單線上即時更新成功！")
    print(f"🔗 表單前台填寫網址: https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform")

if __name__ == "__main__":
    update_form()
