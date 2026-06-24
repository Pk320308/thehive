
# Cynox Cynox - Health Monitor + Auto Heal Script
# Yeh script har 5 minute mein check karta hai sab chal raha hai ya nahi

$logFile = "E:\THE Hive New\BACKUPS\health_log.txt"

function Write-Log {
    param($msg, $color = "White")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$timestamp] $msg"
    Add-Content -Path $logFile -Value $line
}

function Check-And-Heal {
    param($containerName, $waitSeconds = 10)
    
    $status = docker inspect $containerName --format "{{.State.Status}}" 2>&1
    
    if ($status -ne "running") {
        Write-Log "WARNING: $containerName chal nahi raha (Status: $status) - Restart kar raha hoon..."
        docker start $containerName 2>&1 | Out-Null
        Start-Sleep -Seconds $waitSeconds
        
        $newStatus = docker inspect $containerName --format "{{.State.Status}}" 2>&1
        if ($newStatus -eq "running") {
            Write-Log "OK: $containerName successfully restart hua!"
        } else {
            Write-Log "ERROR: $containerName restart fail hua! Manual check karo."
        }
        return $false
    }
    return $true
}

Write-Log "--- Health Check ---"

# Check order: pehle databases, phir Cynox
$cassOk = Check-And-Heal "cynox-cassandra" 20
$esOk   = Check-And-Heal "cynox-elasticsearch" 20

# Agar databases theek hain to Cynox check karo
if ($cassOk -and $esOk) {
    $hiveOk = Check-And-Heal "cynox" 5
    if ($hiveOk) {
        # API bhi check karo
        try {
            $resp = Invoke-WebRequest -Uri "http://localhost:9001/api/status" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
            Write-Log "HEALTHY: Sab containers chal rahe hain. API: OK"
        } catch {
            Write-Log "WARNING: Containers chal rahe hain but API respond nahi kar raha - startup ho raha hoga"
        }
    }
} else {
    Write-Log "INFO: Databases restart hue, Cynox ka wait kar raha hoon..."
    Start-Sleep -Seconds 30
    Check-And-Heal "cynox" 10
}
