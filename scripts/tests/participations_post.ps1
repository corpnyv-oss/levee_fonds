# Script de test: création d'une participation (utilisateur authentifié)
# Usage: powershell -ExecutionPolicy Bypass -File .\participations_post.ps1
# Expected:
#  - HTTP 201 Created
#  - Response JSON: objet Participation créé (id, montant, statut, reference)
#  - Signification: permet à l'utilisateur d'initier une participation pour une cagnotte donnée.

$token = Read-Host "JWT Token"
$uri = 'http://127.0.0.1:8000/participations/'
$body = @{
    cagnotte = 1
    montant = "10.00"
}
try {
    $resp = Invoke-RestMethod -Uri $uri -Method Post -Headers @{ Authorization = "Bearer $token" } -Body ($body | ConvertTo-Json) -ContentType 'application/json' -UseBasicParsing
    Write-Output "OK: participation créée id=$($resp.id)"
    $resp | ConvertTo-Json -Depth 3 | Write-Output
} catch {
    Write-Error "Erreur HTTP: $($_.Exception.Response.StatusCode) — $($_.Exception.Message)"
}
