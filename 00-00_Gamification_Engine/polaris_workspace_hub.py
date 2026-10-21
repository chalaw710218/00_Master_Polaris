"""
Polaris Workspace Hub (北極星 Google Workspace 統一中樞)
為全體內閣夥伴（雪、算盤、泰勒絲、林納斯、獵鷹、特務影）提供對 Google 試算表與 Google 文件的完整操作能力：
- 新建 (Create)
- 讀取 (Read)
- 修改 / 更新 (Update / Replace)
- 追加 (Append)
- 權限管理 (Share / Move)
"""

import os
import json
from typing import List, Dict, Any, Optional

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    import gspread
except ImportError:
    pass

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive'
]

DEFAULT_KEY_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "google_service_account.json")

class PolarisWorkspaceHub:
    def __init__(self, key_path: Optional[str] = None):
        self.key_path = key_path or DEFAULT_KEY_PATH
        if not os.path.exists(self.key_path):
            # Check current working directory as fallback
            if os.path.exists("google_service_account.json"):
                self.key_path = os.path.abspath("google_service_account.json")
            else:
                self.credentials = None
                self.drive_service = None
                self.sheets_service = None
                self.docs_service = None
                self.gc = None
                return

        self.credentials = service_account.Credentials.from_service_account_file(
            self.key_path, scopes=SCOPES
        )
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
        self.sheets_service = build('sheets', 'v4', credentials=self.credentials)
        self.docs_service = build('docs', 'v1', credentials=self.credentials)
        try:
            self.gc = gspread.authorize(self.credentials)
        except Exception:
            self.gc = None

    def is_connected(self) -> bool:
        return self.credentials is not None

    # =========================================================================
    # 1. Google 試算表操作 (Google Sheets)
    # =========================================================================

    def create_spreadsheet(self, title: str, folder_id: Optional[str] = None) -> Dict[str, str]:
        """新建一張全新的 Google 試算表"""
        if not self.is_connected():
            raise FileNotFoundError(f"找不到服務帳號金鑰：{self.key_path}")

        file_metadata = {
            'name': title,
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
        if folder_id:
            file_metadata['parents'] = [folder_id]

        file = self.drive_service.files().create(
            body=file_metadata,
            fields='id, name, webViewLink'
        ).execute()

        return {
            "id": file.get('id'),
            "title": file.get('name'),
            "url": file.get('webViewLink')
        }

    def append_sheet_row(self, spreadsheet_id: str, range_name: str, row_values: List[Any]):
        """在試算表指定範圍末端追加一行資料"""
        body = {'values': [row_values]}
        return self.sheets_service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()

    def update_sheet_range(self, spreadsheet_id: str, range_name: str, values: List[List[Any]]):
        """修改試算表指定區間（如 A1:D10）"""
        body = {'values': values}
        return self.sheets_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

    def read_sheet_range(self, spreadsheet_id: str, range_name: str) -> List[List[Any]]:
        """讀取試算表指定區間內容"""
        result = self.sheets_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        return result.get('values', [])

    # =========================================================================
    # 2. Google 文件操作 (Google Docs)
    # =========================================================================

    def create_document(self, title: str, folder_id: Optional[str] = None) -> Dict[str, str]:
        """新建一份全新的 Google 文件 (Docs)"""
        if not self.is_connected():
            raise FileNotFoundError(f"找不到服務帳號金鑰：{self.key_path}")

        file_metadata = {
            'name': title,
            'mimeType': 'application/vnd.google-apps.document'
        }
        if folder_id:
            file_metadata['parents'] = [folder_id]

        file = self.drive_service.files().create(
            body=file_metadata,
            fields='id, name, webViewLink'
        ).execute()

        return {
            "id": file.get('id'),
            "title": file.get('name'),
            "url": file.get('webViewLink')
        }

    def append_doc_text(self, document_id: str, text: str):
        """在 Google 文件末尾追加文字段落"""
        doc = self.docs_service.documents().get(documentId=document_id).execute()
        content = doc.get('body', {}).get('content', [])
        end_index = 1
        if content:
            end_index = content[-1].get('endIndex', 1) - 1

        requests = [
            {
                'insertText': {
                    'location': {'index': max(1, end_index)},
                    'text': text + "\n"
                }
            }
        ]
        return self.docs_service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()

    def replace_doc_text(self, document_id: str, old_text: str, new_text: str):
        """在 Google 文件中全文替換指定文字 (Find & Replace)"""
        requests = [
            {
                'replaceAllText': {
                    'containsText': {
                        'text': old_text,
                        'matchCase': True
                    },
                    'replaceText': new_text
                }
            }
        ]
        return self.docs_service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()

    # =========================================================================
    # 3. 雲端硬碟共用與搜尋 (Google Drive)
    # =========================================================================

    def share_file_with_user(self, file_id: str, email: str, role: str = 'writer'):
        """將建立的試算表或文件共用給指定的使用者 (如品碩的個人信箱)"""
        permission = {
            'type': 'user',
            'role': role,
            'emailAddress': email
        }
        return self.drive_service.permissions().create(
            fileId=file_id,
            body=permission,
            fields='id'
        ).execute()
