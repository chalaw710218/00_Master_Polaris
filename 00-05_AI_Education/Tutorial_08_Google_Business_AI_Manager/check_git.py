import subprocess
import os

repo_dir = r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager\clients\01_Taitung_Shokunin_Diner\website"
res = subprocess.run(["git", "remote", "-v"], cwd=repo_dir, capture_output=True, text=True)
print("Git remote:", res.stdout, res.stderr)

res_status = subprocess.run(["git", "status"], cwd=repo_dir, capture_output=True, text=True)
print("Git status:", res_status.stdout)
