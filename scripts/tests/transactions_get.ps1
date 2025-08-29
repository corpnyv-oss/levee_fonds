# Script de test: récupération d'une transaction
# Expected:
#  - HTTP 200 OK si transaction existe et appartient à l'utilisateur/admin
#  - HTTP 403 si non autorisé
#  - Signification: vérifie l'accès restreint aux transactions

$token = Read-Host "JWT Token"
$txId = Read-Host "Transaction ID"
$uri = "http://127.0.0.1:8081/transactions/$txId/"
try {
    $resp = Invoke-RestMethod -Uri $uri -Method Get -Headers @{ Authorization = "Bearer $token" } -UseBasicParsing
    Write-Output "OK: transaction trouvée"
    $resp | ConvertTo-Json -Depth 3 | Write-Output
} catch {
    Write-Error "Erreur HTTP: $($_.Exception.Response.StatusCode) — $($_.Exception.Message)"
}
