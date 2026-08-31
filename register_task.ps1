$batPath = "c:\Users\Administrator\Desktop\260814_AI 챔피언\5. 블루 실전 시험 문제\문제3\run_keep_alive.bat"
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$batPath`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 30)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -TaskName "SurgeKeepAlive_VolunteerHub" -Description "Keep Surge Website alive and auto-redeploy if down" -Force
