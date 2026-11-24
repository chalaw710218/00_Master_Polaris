$action = New-ScheduledTaskAction -Execute 'C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager\run_midnight_autopilot.bat' -WorkingDirectory 'C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager'
Set-ScheduledTask -TaskName 'Polaris_GBP_Midnight_Autopilot' -Action $action
Start-ScheduledTask -TaskName 'Polaris_GBP_Midnight_Autopilot'
Start-Sleep -Seconds 5
$info = Get-ScheduledTaskInfo -TaskName 'Polaris_GBP_Midnight_Autopilot'
Write-Output "LastRunTime: $($info.LastRunTime)"
Write-Output "LastTaskResult: $($info.LastTaskResult)"
Write-Output "NextRunTime: $($info.NextRunTime)"
