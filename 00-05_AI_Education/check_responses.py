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
    res = service.forms().responses().list(formId=form_id).execute()
    responses = res.get("responses", [])
    print(f"TOTAL_RESPONSES: {len(responses)}")
    for idx, r in enumerate(responses):
        created_time = r.get("createTime")
        answers = r.get("answers", {})
        print(f"[{idx+1}] Time: {created_time}, Answers Count: {len(answers)}")
except Exception as e:
    print("ERROR:", e)
