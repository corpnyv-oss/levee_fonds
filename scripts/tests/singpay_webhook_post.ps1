# Script de test: envoi d'un webhook SingPay simulé
# Usage: powershell -ExecutionPolicy Bypass -File .\singpay_webhook_post.ps1
# Expected:
#  - HTTP 200 OK si transaction trouvée et traitée
#  - HTTP 404 si transaction inconnue
#  - HTTP 401 si signature invalide
#  - Signification: teste la logique de verification HMAC, anti-replay, idempotence et mapping des statuts

$webhookUrl = 'http://127.0.0.1:8081/webhooks/singpay/'
$payload = @{ status = 'paid'; provider_ref = 'webhook-12345'; reference_psp = 'psp-1' } | ConvertTo-Json
# calcule la signature HMAC-SHA256 (dev: on peut remplacer par header X-Signature invalide)
$secret = Read-Host "Webhook secret"
$hmac = [System.Convert]::ToBase64String((New-Object System.Security.Cryptography.HMACSHA256([System.Text.Encoding]::UTF8.GetBytes($secret))).ComputeHash([System.Text.Encoding]::UTF8.GetBytes($payload)))

try {
    $resp = Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $payload -ContentType 'application/json' -Headers @{ 'X-Signature' = $hmac; 'X-Timestamp' = [int][double]::Parse((Get-Date -UFormat %s)) }
    Write-Output "OK: $($resp | ConvertTo-Json -Depth 3)"
} catch {
    Write-Error "Erreur HTTP: $($_.Exception.Response.StatusCode) — $($_.Exception.Message)"
}
