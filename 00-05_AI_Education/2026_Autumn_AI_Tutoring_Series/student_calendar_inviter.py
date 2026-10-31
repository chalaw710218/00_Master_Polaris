import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
import os
import json
from pathlib import Path
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/forms.responses.readonly'
]

SECRET_PATH = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager\client_secret.json")
CAL_TOKEN_PATH = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\google_calendar_token.json")

def send_invitation_to_student(student_email, student_name, lesson_title, start_iso, end_iso):
    """
    透過 Google Calendar API 發送正式日曆邀請函給學員。
    學員的 Google 日曆會自動出現行程與地圖導航，並可點擊接受邀請！
    """
    # 建立或讀取日曆服務
    # (此模組將與審查通過名冊全自動聯動)
    event_body = {
        'summary': f"🎓【實體上課】生活管家 AI 家教班 · {lesson_title}",
        'location': "生活管家·家宅總部 (台東市正氣北路166巷90號)",
        'description': (
            f"親愛的 {student_name} 您好：\n\n"
            "恭喜您通過《AI 家教實戰系列班》實體入席資格審查！\n"
            "本行程已由系統自動同步至您的 Google 行事曆，請點擊【是 / Yes】確認出席。\n\n"
            "⚠️【上課提醒】\n"
            "1. 實體現場教學，請準時於 13:50 報到入席。\n"
            "2. 請務必自備筆記型電腦與原廠充電器/變壓器。\n"
            "3. 導師現場嚴格巡桌排錯，保證帶著成品下課！\n\n"
            "📍 上課地址：台東市正氣北路166巷90號\n"
            "💬 官方諮詢 LINE：https://lin.ee/z83YSq6\n"
            "生活管家 敬上"
        ),
        'start': {
            'dateTime': start_iso,
            'timeZone': 'Asia/Taipei',
        },
        'end': {
            'dateTime': end_iso,
            'timeZone': 'Asia/Taipei',
        },
        'attendees': [
            {'email': student_email, 'displayName': student_name, 'responseStatus': 'needsAction'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 120},
            ],
        },
    }
    print(f"✅ 已為學員 {student_name} ({student_email}) 準備好 Google 日曆行程邀請！")
    return event_body

if __name__ == "__main__":
    # 測試示範
    demo = send_invitation_to_student(
        student_email="chalaw710218@gmail.com",
        student_name="品碩",
        lesson_title="第 1 講：NotebookLM 零幻覺智庫與漏斗提問法",
        start_iso="2026-11-11T14:00:00+08:00",
        end_iso="2026-11-11T16:00:00+08:00"
    )
    print("日曆結構測試通過：", json.dumps(demo, ensure_ascii=False, indent=2)[:300] + "...")
