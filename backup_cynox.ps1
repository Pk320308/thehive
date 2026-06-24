
# Cynox Cynox - Backup Script
# Run this script to take backup of all data

$backupRoot = "E:\THE Hive New\BACKUPS"
$date = Get-Date -Format "yyyy-MM-dd_HH-mm"
$backupDir = "$backupRoot\backup_$date"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   CYNOX Cynox Backup - $date" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Create backup directory
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

Write-Host "`n[1/3] Stopping containers for clean backup..." -ForegroundColor Yellow
docker stop cynox | Out-Null

Write-Host "[2/3] Copying database files..." -ForegroundColor Yellow
Copy-Item -Recurse -Force "E:\THE Hive New\db_data" "$backupDir\db_data"

Write-Host "[3/3] Starting containers again..." -ForegroundColor Yellow
docker start cynox-cassandra cynox-elasticsearch | Out-Null
Start-Sleep -Seconds 15
docker start cynox | Out-Null

$size = (Get-ChildItem -Recurse "$backupDir" | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "   BACKUP COMPLETE!" -ForegroundColor Green
Write-Host "   Location: $backupDir" -ForegroundColor Green
Write-Host "   Size: $([math]::Round($size, 2)) MB" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
