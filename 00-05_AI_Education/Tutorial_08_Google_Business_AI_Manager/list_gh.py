import subprocess

res = subprocess.run(["gh", "repo", "list", "chalaw710218"], capture_output=True, text=True)
print("GH repos:", res.stdout)
