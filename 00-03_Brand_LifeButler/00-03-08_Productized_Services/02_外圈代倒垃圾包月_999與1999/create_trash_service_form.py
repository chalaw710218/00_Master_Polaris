import os
import sys
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/drive.file'
]

ROOT_DIR = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris")
TOKEN_PATH = ROOT_DIR / "00-05_AI_Education" / "2026_Autumn_AI_Tutoring_Series" / "google_forms_token.json"

def get_forms_service():
    if not TOKEN_PATH.exists():
        print(f"❌ 找不到 Token: {TOKEN_PATH}")
        return None
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build('forms', 'v1', credentials=creds)

def main():
    service = get_forms_service()
    if not service:
        sys.exit(1)

    print("🚀 正在調用 Google Forms API 建立【生活管家】代倒垃圾包月服務預約表單...")

    # 1. 建立表單本體
    form_body = {
        "info": {
            "title": "【生活管家】代倒垃圾包月服務｜需求登記與到府服務預約單",
            "documentTitle": "【生活管家】代倒垃圾包月服務預約表單"
        }
    }
    created = service.forms().create(body=form_body).execute()
    form_id = created["formId"]
    responder_uri = created.get("responderUri", "")
    print(f"✅ 表單建立成功！Form ID: {form_id}")
    print(f"🔗 填寫網址 (Published URL): {responder_uri}")

    # 2. 說明文案與題目
    description = (
        "您好！感謝您對「生活管家」代倒垃圾包月服務的關注。\n\n"
        "從今天起，您不用再為了追垃圾車中斷晚餐、狼狽狂奔！\n"
        "為了替您安排最流暢的機車清運路線與專屬服務時段，請協助填寫以下資訊（只需 1~2 分鐘）。\n\n"
        "🛵【我們的服務承諾】：\n"
        "• 機車專車出勤，每次限 20L 兩包（一般生活垃圾＋回收各一包，可自由搭配）。\n"
        "• 100% 物理隔離：倒垃圾出勤全車嚴禁攜帶食品保溫箱，徹底杜絕交叉污染。\n"
        "• 每次清運拍照 LINE 回傳留痕，回到家門前永遠乾淨清爽。\n\n"
        "【填表後的服務流程】：\n"
        "1. 填寫本表單 ➔ 2. 管家在 LINE 與您確認需求與路線 ➔ 3. 約定時間到府確認放置點 ➔ 4. 正式啟動清運！"
    )

    requests = [
        {"updateFormInfo": {"info": {"description": description}, "updateMask": "description"}},
        
        # Q1: 稱謂
        {"createItem": {"item": {"title": "1. 您的稱謂（姓名或先生/小姐）", "questionItem": {"question": {"required": True, "textQuestion": {}}}}, "location": {"index": 0}}},
        
        # Q2: 電話
        {"createItem": {"item": {"title": "2. 聯絡電話（手機）", "description": "例如：0912-345-678，專員確認路線時聯繫使用", "questionItem": {"question": {"required": True, "textQuestion": {}}}}, "location": {"index": 1}}},
        
        # Q3: LINE ID
        {"createItem": {"item": {"title": "3. LINE ID 或 LINE 顯示名稱", "description": "【極重要】清運完成拍照回傳、通知專員到府均透過官方 LINE 聯繫", "questionItem": {"question": {"required": True, "textQuestion": {}}}}, "location": {"index": 2}}},
        
        # Q4: 服務地址
        {"createItem": {"item": {"title": "4. 服務清運地址", "description": "請填寫完整地址（例如：台東市新生路OO號，店家請備註店名）", "questionItem": {"question": {"required": True, "textQuestion": {}}}}, "location": {"index": 3}}},
        
        # Q5: 居住型態
        {"createItem": {"item": {"title": "5. 您的建築 / 居住型態", "questionItem": {"question": {"required": True, "choiceQuestion": {"type": "RADIO", "options": [
            {"value": "獨棟透天（門前有一樓空地或騎樓）"},
            {"value": "社區華廈 / 電梯大樓（有管理室 / 可放指定暫存區）"},
            {"value": "傳統公寓（無電梯 / 需約定一樓大門旁放置）"},
            {"value": "臨街實體店面 / 微型工作室（早午餐、咖啡、手作等）"},
            {"value": "其他"}
        ]}}}}, "location": {"index": 4}}},
        
        # Q6: 預計放置位置
        {"createItem": {"item": {"title": "6. 預計垃圾放置位置", "questionItem": {"question": {"required": True, "choiceQuestion": {"type": "RADIO", "options": [
            {"value": "自家一樓大門口（遮雨棚下）"},
            {"value": "自家私人車庫角落"},
            {"value": "大樓 / 社區管理室指定放置處"},
            {"value": "店面後門 / 側門約定點"},
            {"value": "尚未確定，希望能與管家現場約定討論"}
        ]}}}}, "location": {"index": 5}}},
        
        # Q7: 方案選擇
        {"createItem": {"item": {"title": "7. 您希望預約的包月方案", "questionItem": {"question": {"required": True, "choiceQuestion": {"type": "RADIO", "options": [
            {"value": "🌱【輕量雙享包】NT$ 999 /月（每週 2 次，每次限 20L 兩包含回收，適合兩人小家庭、上班族）"},
            {"value": "👑【尊榮旗艦包】NT$ 1,999 /月（每週 5 次全收運日天天清不積累，適合育兒家庭、店家工作室）"},
            {"value": "🤔 還在考慮中（希望能與管家專員通話討論後再決定）"}
        ]}}}}, "location": {"index": 6}}},
        
        # Q8: 999 偏好日
        {"createItem": {"item": {"title": "8. 若選擇「999 輕量方案」，您偏好的清運日組合", "questionItem": {"question": {"required": False, "choiceQuestion": {"type": "RADIO", "options": [
            {"value": "【週二、週五】組合（適合平日小開伙、週末前清空）"},
            {"value": "【週一、週四】組合（適合清空週末外帶垃圾）"},
            {"value": "聽從管家最佳化路線安排皆可"},
            {"value": "（我選擇 1,999 方案，全收運日 5 天皆出勤）"}
        ]}}}}, "location": {"index": 7}}},
        
        # Q9: 垃圾型態
        {"createItem": {"item": {"title": "9. 家中日常主要的垃圾類型（多選，讓專員預先準備裝備）", "questionItem": {"question": {"required": False, "choiceQuestion": {"type": "CHECKBOX", "options": [
            {"value": "一般外帶餐盒、家庭常態廚餘（已瀝乾密封）"},
            {"value": "嬰幼兒尿布（每日固定產出）"},
            {"value": "網購紙箱、包材、寶特瓶等資源回收"},
            {"value": "店家營業耗材（咖啡渣、鮮奶盒、手作耗材）"},
            {"value": "寵物貓砂 / 墊料"}
        ]}}}}, "location": {"index": 8}}},
        
        # Q10: 希望開始日期
        {"createItem": {"item": {"title": "10. 您希望從哪一天開始享受服務？", "description": "例如：下週一開始，管家小隊將於開工日前為您安排專員就緒", "questionItem": {"question": {"required": True, "textQuestion": {}}}}, "location": {"index": 9}}},
        
        # Q11: 方便聯絡時段
        {"createItem": {"item": {"title": "11. 方便管家專員與您電話 / LINE 確認細節的時段？", "questionItem": {"question": {"required": True, "choiceQuestion": {"type": "CHECKBOX", "options": [
            {"value": "上午時段 (09:00 ~ 12:00)"},
            {"value": "下午時段 (14:00 ~ 17:00)"},
            {"value": "傍晚時段 (17:00 ~ 19:30)"},
            {"value": "任何時間只要傳 LINE 留言即可"}
        ]}}}}, "location": {"index": 10}}},
        
        # Q12: 是否需現場打照面
        {"createItem": {"item": {"title": "12. 是否需要管家專員提前到府「現場勘查約定點與打個照面」？", "questionItem": {"question": {"required": True, "choiceQuestion": {"type": "RADIO", "options": [
            {"value": "需要：希望能提前約個時間（約 3~5 分鐘），當面確認門口放置點與溝通細節"},
            {"value": "不需要：我會將門口照片拍下來傳 LINE，確認路線後直接於指定日開始出勤！"}
        ]}}}}, "location": {"index": 11}}},
        
        # Q13: 服務規範與超量加收條款
        {"createItem": {"item": {"title": "13. 服務規範與超量加收條款確認", "description": "【服務規範摘要】：\n1. 機車出勤每次上限 20L 兩包（含回收，可自由調配）。\n2. 超量加收（併入下月帳單）：若單次超過 2 包，專員在安全允許下順手清運並拍照存證，費用一律併入下月帳單結算，現場不經手現金。\n3. 安全紅線：嚴禁夾帶瓦斯罐、未熄香灰、未包紮針頭與裝潢廢棄物。\n4. 一樓平面交接：垃圾放置於一樓指定點，專員不持鑰匙、不進室內私領域。", "questionItem": {"question": {"required": True, "choiceQuestion": {"type": "CHECKBOX", "options": [
            {"value": "我已詳閱並充分理解上述服務規範，同意每次清運以 20L 兩包為基準，若有超量將依規定併入下月帳單結算。"}
        ]}}}}, "location": {"index": 12}}},
        
        # Q14: 個資保護同意書
        {"createItem": {"item": {"title": "14. 個人資料蒐集、處理與利用同意書", "description": "【個資保護承諾】：\n1. 蒐集目的：本表單所填姓名、電話、地址、LINE ID 僅供生活管家排程派工、到府履約與帳單對帳使用。\n2. 絕不對外公開：嚴格遵守個資法，絕不外洩、不販售、不作任何第三方行銷使用。\n3. 資料保障：受數位加密保護，終止服務後可隨時要求刪除銷毀。", "questionItem": {"question": {"required": True, "choiceQuestion": {"type": "CHECKBOX", "options": [
            {"value": "本人已詳閱上述個資聲明，同意生活管家將本人所填之地址、電話與 LINE 資料僅用於代倒垃圾服務之履約與聯繫，並確認本資料受嚴密保護、絕不對外公開。"}
        ]}}}}, "location": {"index": 13}}},
        
        # Q15: 其他備註
        {"createItem": {"item": {"title": "15. 其他備註或特殊叮嚀事項", "description": "例如：「家門口有養狗請先按門鈴」、「請避開右側盆栽」等", "questionItem": {"question": {"required": False, "textQuestion": {}}}}, "location": {"index": 14}}}
    ]

    service.forms().batchUpdate(formId=form_id, body={"requests": requests}).execute()
    print("✨ 所有題目、說明、超量條款與個資保護同意書已全數成功寫入表單！")
    
    # 儲存結果
    output = {
        "formId": form_id,
        "responderUri": responder_uri
    }
    with open("google_form_live_info.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
