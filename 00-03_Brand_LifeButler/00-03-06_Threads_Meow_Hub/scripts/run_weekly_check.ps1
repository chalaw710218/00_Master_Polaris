$HubDir = "c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub"
Set-Location $HubDir

$LogDir = Join-Path $HubDir "logs"
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

$LogFile = Join-Path $LogDir "weekly_gate_check.log"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

"==========================================" | Out-File -FilePath $LogFile -Append -Encoding utf8
"[$Timestamp] 開始執行生活管家影每週知識門禁審計 (Weekly Gate Check)" | Out-File -FilePath $LogFile -Append -Encoding utf8
"==========================================" | Out-File -FilePath $LogFile -Append -Encoding utf8

python scripts/bionic_knowledge_gate.py check *>> $LogFile

$ExitCode = $LASTEXITCODE
"[$Timestamp] 審計結束，Exit Code: $ExitCode" | Out-File -FilePath $LogFile -Append -Encoding utf8
"------------------------------------------`n" | Out-File -FilePath $LogFile -Append -Encoding utf8

exit $ExitCode
