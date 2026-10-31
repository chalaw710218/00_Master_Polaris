import os
import sys
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# 包含 Google Forms 與 Google Drive 權限
SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/drive.file'
]

SECRET_PATH = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager\client_secret.json")
TOKEN_PATH = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\google_forms_token.json")

def get_forms_service():
    creds = None
    if TOKEN_PATH.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        if not creds:
            if not SECRET_PATH.exists():
                print(f"錯誤：找不到 {SECRET_PATH}")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(str(SECRET_PATH), SCOPES)
            # 使用本地固定端口進行授權
            creds = flow.run_local_server(port=0)
            with open(TOKEN_PATH, 'w', encoding='utf-8') as f:
                f.write(creds.to_json())
            print(f"憑證已成功保存至 {TOKEN_PATH}")

    return build('forms', 'v1', credentials=creds)

def create_polaris_form():
    service = get_forms_service()
    if not service:
        print("無法取得 Google Forms 服務！")
        return

    # 1. 建立空表單
    form_body = {
        "info": {
            "title": "2026 秋季 AI 家教實戰系列班 · 第 1 講【實體入席申請表】",
            "documentTitle": "2026 秋季 AI 家教實戰系列班 · 第 1 講【實體入席申請表】"
        }
    }
    created_form = service.forms().create(body=form_body).execute()
    form_id = created_form["formId"]
    responder_uri = created_form.get("responderUri", "")
    print(f"表單建立成功！Form ID: {form_id}")
    print(f"填寫網址 (Published URL): {responder_uri}")

    # 2. 批量寫入說明、題目與設定
    description = (
        "【限額 10 席 · 純實體現場教學 · 解決真實生意難題】\n\n"
        "各位好朋友、老夥伴您好：\n"
        "歡迎申請由生活管家創辦人 陳品碩（闆仔）親自授權主講之「AI 家教實戰系列班 · 第 1 講」。\n\n"
        "⚠️【入席重要須知】\n"
        "1. 本課程堅持 100% 純實體現場教學，絕無線上同步！導師極度嚴厲，現場手把手巡桌排錯，保證做出專屬成果。\n"
        "2. 為了確保「每人一台螢幕個別指導」的最高教學品質，現場嚴格限額 10 席，多一張椅子都不加。\n"
        "3. 若申請人數超過 10 名，將依「硬體準備完整度」與「業務情境契合度」進行審查分流；未排入本梯次之夥伴，將優先為您保留至【第二梯次加開場】，敬請理解與體諒。\n\n"
        "📍 上課地點：生活管家·家宅總部（台東市正氣北路166巷90號）\n"
        "⏰ 上課時間：每週三下午 14:00 - 16:00\n"
        "💰 學費政策：老學員免收學費（0元免單回娘家特權）｜ 全新夥伴單堂實戰 NT$ 500 元（審查通過後通知付款）\n"
        "💬 官方諮詢 LINE：https://lin.ee/z83YSq6 （加入後可直接私訊管家）"
    )

    requests = [
        # 更新說明文字
        {
            "updateFormInfo": {
                "info": {
                    "description": description
                },
                "updateMask": "description"
            }
        },
        # 題目 1: 真實姓名
        {
            "createItem": {
                "item": {
                    "title": "1. 您的真實姓名",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {}
                        }
                    }
                },
                "location": {"index": 0}
            }
        },
        # 題目 2: Email (核心驗證與日曆同步)
        {
            "createItem": {
                "item": {
                    "title": "2. 您的常用 Email 信箱（Google 帳號佳）",
                    "description": "【核心聯繫憑證】審查通過後，系統將發送報到通知信，並直接將上課行程寫入您的 Google 行事曆！",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {}
                        }
                    }
                },
                "location": {"index": 1}
            }
        },
        # 題目 3: 手機號碼
        {
            "createItem": {
                "item": {
                    "title": "3. 您的聯絡電話 / 手機號碼",
                    "description": "用於突發狀況聯繫與上課當日簡訊提醒",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {}
                        }
                    }
                },
                "location": {"index": 2}
            }
        },
        # 題目 4: LINE ID
        {
            "createItem": {
                "item": {
                    "title": "4. 您的 LINE ID 或 稱呼",
                    "description": "便於加入教學即時群與個別指導（亦可加入官方 LINE：https://lin.ee/z83YSq6 私訊我們）",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {}
                        }
                    }
                },
                "location": {"index": 3}
            }
        },
        # 題目 5: 學員身分
        {
            "createItem": {
                "item": {
                    "title": "5. 您的學員身分",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [
                                    {"value": "👑 生活管家老學員（享有回娘家 0 元免收學費特權）"},
                                    {"value": "🌟 全新夥伴（單堂實戰 NT$ 500 元，通過審查後提供付款資訊）"}
                                ]
                            }
                        }
                    }
                },
                "location": {"index": 4}
            }
        },
        # 題目 6: 攜帶設備
        {
            "createItem": {
                "item": {
                    "title": "6. 上課當天您預計攜帶的設備",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [
                                    {"value": "筆記型電腦 (Windows 系統)"},
                                    {"value": "筆記型電腦 (Mac / Apple 系統)"},
                                    {"value": "⚠️ 平板電腦 (iPad / Android 平板) —— 建議自備外接鍵盤以利檔案操作"}
                                ]
                            }
                        }
                    }
                },
                "location": {"index": 5}
            }
        },
        # 題目 7: 軟硬體環境勾選
        {
            "createItem": {
                "item": {
                    "title": "7. 軟體環境與前置準備勾選（請全數確認）",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "CHECKBOX",
                                "options": [
                                    {"value": "已確認電腦安裝有 Google Chrome 瀏覽器"},
                                    {"value": "確定記得自己的 Google 帳號與密碼（現場需登入 NotebookLM 實作）"},
                                    {"value": "筆電可正常連接 Wi-Fi 無線網路"},
                                    {"value": "確定當天會攜帶筆電原廠充電器 / 電源線"}
                                ]
                            }
                        }
                    }
                },
                "location": {"index": 6}
            }
        },
        # 題目 8: 行業
        {
            "createItem": {
                "item": {
                    "title": "8. 您目前從事的行業或主要業務內容",
                    "description": "例如：早午餐店、伴手禮電商、長照服務、社區營造、接案業務等",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {}
                        }
                    }
                },
                "location": {"index": 7}
            }
        },
        # 題目 9: 想解決的資料
        {
            "createItem": {
                "item": {
                    "title": "9. 本次上課，您最想帶哪種資料丟進 AI 幫您解決問題？（可複選）",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "CHECKBOX",
                                "options": [
                                    {"value": "店內菜單、商品規格或歷史進貨報價單（精算與自動答覆）"},
                                    {"value": "密密麻麻的活動企劃案、長篇補助案公文（快速摘要與深挖）"},
                                    {"value": "顧客常見疑難雜症、客服問答紀錄（打造零幻覺客服庫）"},
                                    {"value": "店鋪營運規章、員工教育訓練手冊（打造數位店長）"},
                                    {"value": "其他個人研究資料或筆記"}
                                ]
                            }
                        }
                    }
                },
                "location": {"index": 8}
            }
        },
        # 題目 10: 入席意願
        {
            "createItem": {
                "item": {
                    "title": "10. 入席承諾與候補加開意願",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [
                                    {"value": "我已確認時間（每週三 14:00-16:00），審查通過我一定準時出席！"},
                                    {"value": "若本週 10 名正取已滿，我非常希望參加【第二梯次加開場】，請第一時間通知我！"}
                                ]
                            }
                        }
                    }
                },
                "location": {"index": 9}
            }
        }
    ]

    service.forms().batchUpdate(formId=form_id, body={"requests": requests}).execute()
    print("✅ 全數題目與設定寫入成功！")
    print(f"🔗 學員報名填寫網址：{responder_uri}")
    print(f"🛠️ 講師後台編輯網址：https://docs.google.com/forms/d/{form_id}/edit")

if __name__ == "__main__":
    create_polaris_form()
