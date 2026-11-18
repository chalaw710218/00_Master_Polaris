import subprocess
import json

cmd = ['powershell', '-Command', 'Get-Process chrome -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count']
res = subprocess.run(cmd, capture_output=True, text=True)
print("Chrome process count:", res.stdout.strip())

# Check with wmic or powershell CIM
cmd2 = ['powershell', '-Command', 'Get-CimInstance Win32_Process | Where-Object { $_.Name -eq "chrome.exe" } | Select-Object -Property CommandLine | Select-Object -First 2 | ForEach-Object { $_.CommandLine }']
res2 = subprocess.run(cmd2, capture_output=True, text=True)
print("Chrome CommandLine sample:\n", res2.stdout.strip())
