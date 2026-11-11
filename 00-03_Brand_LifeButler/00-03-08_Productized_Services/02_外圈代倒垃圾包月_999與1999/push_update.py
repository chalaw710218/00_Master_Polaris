import subprocess
import os
import shutil
import tempfile

temp_dir = os.path.join(tempfile.gettempdir(), 'taitung-trash-radar')
engine_dir = os.path.abspath('05_Trash_Radar_Engine')

shutil.copy2(os.path.join(engine_dir, 'index.html'), os.path.join(temp_dir, 'index.html'))
shutil.copy2(os.path.join(engine_dir, 'taitung_trash_routes_seed.json'), os.path.join(temp_dir, 'taitung_trash_routes_seed.json'))

subprocess.run(["git", "add", "."], cwd=temp_dir, check=True)
commit_proc = subprocess.run(["git", "commit", "-m", "feat: add KEH-5109 Zhongxing Rd 16:20 vanguard stop"], cwd=temp_dir, capture_output=True, text=True)
print("Commit:", commit_proc.stdout)
push_proc = subprocess.run(["git", "push", "origin", "main"], cwd=temp_dir, capture_output=True, text=True)
print("Push stdout:", push_proc.stdout)
print("Push stderr:", push_proc.stderr)
print("Deploy success!")
