import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/drive.file'
]
token_path = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\google_forms_token.json")
creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

forms_service = build('forms', 'v1', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

res = drive_service.files().list(
    q="mimeType = 'application/vnd.google-apps.form' and trashed = false",
    orderBy="createdTime desc",
    pageSize=5,
    fields="files(id, name, createdTime, webViewLink)"
).execute()

forms = res.get('files', [])
print(f"Total forms found: {len(forms)}")
for f in forms:
    form_id = f.get('id')
    form_meta = forms_service.forms().get(formId=form_id).execute()
    print("---")
    print("Name:", f.get("name"))
    print("Form ID:", form_id)
    print("Edit Link:", f.get("webViewLink"))
    print("Responder Link:", form_meta.get("responderUri"))
