import subprocess
import os
import shutil

temp_clone = r"C:\Users\lenovo\AppData\Local\Temp\shokunin-taitung"
if os.path.exists(temp_clone):
    shutil.rmtree(temp_clone)

res = subprocess.run(["git", "clone", "https://github.com/chalaw710218/shokunin-taitung.git", temp_clone], capture_output=True, text=True)
print("Clone:", res.stdout, res.stderr)

if os.path.exists(temp_clone):
    print("Files:", os.listdir(temp_clone))
