# Script de test: enregistrement utilisateur (inscription)
# Usage: powershell -ExecutionPolicy Bypass -File .\auth_register_post.ps1
# Expected:
#  - HTTP 201 Created
#  - Response JSON: détail de création (message) ; en dev, peut contenir activation_token
#  - Signification: crée un nouvel utilisateur inactif (is_active=False) et envoie un email d'activation

$uri = 'http://127.0.0.1:8000/auth/register/register/'
$body = @{ email = 'newuser@example.com'; username = 'newuser'; password = 'pass1234' }
try {
    $resp = Invoke-RestMethod -Uri $uri -Method Post -Body ($body | ConvertTo-Json) -ContentType 'application/json' -UseBasicParsing
    Write-Output "OK: utilisateur créé"
    $resp | ConvertTo-Json -Depth 3 | Write-Output
} catch {
    Write-Error "Erreur HTTP: $($_.Exception.Response.StatusCode) — $($_.Exception.Message)"
}
