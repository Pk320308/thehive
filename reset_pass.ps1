
# Try with default password first
$uri = "http://127.0.0.1:9001/api/user/admin@thehive.local/password/set"
$body = '{"password":"Admin@Cynox123"}'
$headers = @{ "Content-Type" = "application/json" }

# Try secret password
$cred1 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin@thehive.local:secret"))
$resp1 = Invoke-RestMethod -Uri $uri -Method POST -Headers @{ "Content-Type" = "application/json"; "Authorization" = "Basic $cred1" } -Body $body -ErrorAction SilentlyContinue
Write-Host "With 'secret': $resp1"

# Try with empty password
$cred2 = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin@thehive.local:"))
$resp2 = Invoke-RestMethod -Uri $uri -Method POST -Headers @{ "Content-Type" = "application/json"; "Authorization" = "Basic $cred2" } -Body $body -ErrorAction SilentlyContinue
Write-Host "With empty: $resp2"
