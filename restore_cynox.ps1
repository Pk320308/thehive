
# Cynox Cynox - Restore Script
# Run this to restore from a backup

$backupRoot = "E:\THE Hive New\BACKUPS"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   CYNOX Cynox - Restore Tool" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# List available backups
$backups = Get-ChildItem -Directory $backupRoot | Sort-Object Name -Descending
if ($backups.Count -eq 0) {
    Write-Host "No backups found in $backupRoot" -ForegroundColor Red
    exit
}

Write-Host "Available Backups:" -ForegroundColor Yellow
for ($i = 0; $i -lt $backups.Count; $i++) {
    Write-Host "  [$i] $($backups[$i].Name)" -ForegroundColor White
}

$choice = Read-Host "`nEnter backup number to restore"
$selectedBackup = $backups[$choice].FullName

Write-Host "`nRestoring from: $selectedBackup" -ForegroundColor Yellow

Write-Host "[1/4] Stopping all containers..." -ForegroundColor Yellow
docker stop cynox cynox-cassandra cynox-elasticsearch | Out-Null

Write-Host "[2/4] Removing current data..." -ForegroundColor Yellow
Remove-Item -Recurse -Force "E:\THE Hive New\db_data"

Write-Host "[3/4] Restoring backup..." -ForegroundColor Yellow
Copy-Item -Recurse -Force "$selectedBackup\db_data" "E:\THE Hive New\db_data"

Write-Host "[4/4] Starting containers..." -ForegroundColor Yellow
docker start cynox-cassandra cynox-elasticsearch | Out-Null
Start-Sleep -Seconds 20
docker start cynox | Out-Null

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "   RESTORE COMPLETE!" -ForegroundColor Green
Write-Host "   Open: http://localhost:9001" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
