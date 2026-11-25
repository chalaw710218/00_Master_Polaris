"""threads-growth-auditor 共用模組：金鑰載入與 Windows UTF-8 輸出。"""
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

API_BASE = "https://graph.threads.net/v1.0"
SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"


def load_env():
    """由本檔位置向上回溯尋找 .secrets.env（極星根目錄）。"""
    for parent in Path(__file__).resolve().parents:
        env_file = parent / ".secrets.env"
        if env_file.exists():
            env = {}
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env[k.strip()] = v.strip()
            return env
    return {}
