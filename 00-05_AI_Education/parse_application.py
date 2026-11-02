import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

token_path = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\google_forms_token.json")
form_id = "1mzDnnKdGgh8o73gN1S9vxWJDW8ixLEuVgLtXQCsFSRA"

try:
    with open(token_path, "r", encoding="utf-8") as f:
        creds = Credentials.from_authorized_user_file(str(token_path))
    service = build("forms", "v1", credentials=creds)

    form_info = service.forms().get(formId=form_id).execute()
    q_map = {}
    for item in form_info.get("items", []):
        title = item.get("title")
        q_item = item.get("questionItem", {})
        q_id = q_item.get("question", {}).get("questionId")
        if q_id:
            q_map[q_id] = title

    res = service.forms().responses().list(formId=form_id).execute()
    responses = res.get("responses", [])
    print(f"=== 報名總人數：{len(responses)} 人 ===")
    for idx, r in enumerate(responses):
        print(f"\n【申請者 #{idx+1}】")
        print(f"填表時間：{r.get('createTime')}")
        answers = r.get("answers", {})
        # Sort by question order if possible
        for item in form_info.get("items", []):
            q_item = item.get("questionItem", {})
            q_id = q_item.get("question", {}).get("questionId")
            if q_id and q_id in answers:
                title = item.get("title")
                vals = [a.get("value") for a in answers[q_id].get("textAnswers", {}).get("answers", [])]
                print(f"• {title}: {', '.join(vals)}")
except Exception as e:
    print("Error:", e)
