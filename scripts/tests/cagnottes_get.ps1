# Script de test: récupération de la liste des cagnottes
# Usage: powershell -ExecutionPolicy Bypass -File .\cagnottes_get.ps1
# Expected:
#  - HTTP 200 OK
#  - Response JSON: liste d'objets. Chaque objet contient au minimum: id, titre, description, objectif, statut
#  - Signification: la route GET /cagnottes/ liste les cagnottes publiques accessibles.

$uri = 'http://127.0.0.1:8000/cagnottes/'
try {
    $resp = Invoke-RestMethod -Uri $uri -Method Get -UseBasicParsing
    Write-Output "OK: reçu $(($resp | Measure-Object).Count) éléments"
    $resp | ConvertTo-Json -Depth 3 | Write-Output
} catch {
    Write-Error "Erreur HTTP: $($_.Exception.Response.StatusCode) — $($_.Exception.Message)"
}
