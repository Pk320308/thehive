# Cynox Cynox - Auto Backup Script (Task Scheduler version)
# Yeh script background mein chalta hai - bina containers band kiye
# Updated to use proper snapshot tools (elasticdump & nodetool snapshot) to prevent corruption

$backupRoot = "E:\THE Hive New\BACKUPS"
$logFile = "E:\THE Hive New\BACKUPS\backup_log.txt"
$maxBackups = 48  # 48 backups = 24 ghante ka data (har 30 min = 48 backups/day)

# Log function
function Write-Log {
    param($msg)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$timestamp] $msg"
    Add-Content -Path $logFile -Value $line
}

# Backup directory banana
if (-not (Test-Path $backupRoot)) {
    New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
}

Write-Log "===== BACKUP STARTED ====="

try {
    $date = Get-Date -Format "yyyy-MM-dd_HH-mm"
    $backupDir = "$backupRoot\backup_$date"
    
    # Naya backup folder banana
    New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
    
    Write-Log "Taking Cassandra Snapshot..."
    # Clear old snapshots just in case
    docker exec cynox-cassandra nodetool clearsnapshot thp 2>&1 | Out-Null
    # Take a new snapshot named 'autobackup'
    docker exec cynox-cassandra nodetool snapshot -t autobackup thp 2>&1 | Out-Null
    
    # Copy Cassandra Snapshot Data
    Write-Log "Copying Cassandra snapshot data..."
    Copy-Item -Recurse -Force "E:\THE Hive New\db_data\cassandra\data\thp\*\snapshots\autobackup\*" "$backupDir\cassandra" -ErrorAction SilentlyContinue

    Write-Log "Taking Elasticsearch Dump..."
    # Use elasticdump to export data to JSON format to prevent corruption
    docker run --rm --net host -v "$($backupDir):/backup" elasticdump/elasticsearch-dump --input=http://localhost:9200/cynox --output=/backup/elasticsearch_cynox.json --type=data 2>&1 | Out-Null
    docker run --rm --net host -v "$($backupDir):/backup" elasticdump/elasticsearch-dump --input=http://localhost:9200/cynox --output=/backup/elasticsearch_cynox_mapping.json --type=mapping 2>&1 | Out-Null
    
    Write-Log "Copying Cynox Attachment Files..."
    Copy-Item -Recurse -Force "E:\THE Hive New\db_data\cynox" "$backupDir\cynox" -ErrorAction SilentlyContinue
    
    # Size calculate karo
    $size = (Get-ChildItem -Recurse $backupDir -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Log "Backup complete: $backupDir (Size: $([math]::Round($size, 2)) MB)"
    
    # Purane backups delete karo (sirf last 48 rakhenge)
    $allBackups = Get-ChildItem -Directory $backupRoot | Where-Object { $_.Name -like "backup_*" } | Sort-Object Name -Descending
    if ($allBackups.Count -gt $maxBackups) {
        $toDelete = $allBackups | Select-Object -Skip $maxBackups
        foreach ($old in $toDelete) {
            Remove-Item -Recurse -Force $old.FullName
            Write-Log "Purana backup delete kiya: $($old.Name)"
        }
    }
    
    Write-Log "===== BACKUP SUCCESSFUL ====="
    
} catch {
    Write-Log "ERROR: $($_.Exception.Message)"
    Write-Log "===== BACKUP FAILED ====="
}
