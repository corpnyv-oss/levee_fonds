# Vérifier si PostgreSQL est installé
$postgresPath = "C:\Program Files\PostgreSQL\17\bin\pg_ctl.exe"

if (-not (Test-Path $postgresPath)) {
    Write-Host "❌ PostgreSQL n'est pas installé dans le chemin par défaut"
    exit 1
}

# Vérifier si le service est en cours d'exécution
$service = Get-Service -Name "postgresql*" -ErrorAction SilentlyContinue

if (-not $service) {
    Write-Host "❌ Aucun service PostgreSQL trouvé"
    exit 1
}

Write-Host "✅ Services PostgreSQL trouvés :"
$service | Format-Table -Property Name, Status -AutoSize

# Essayer de se connecter à la base de données
$env:PGPASSWORD = "Root@FAPAG@2025"
$connectionTest = & "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -c "SELECT version();" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Connexion à PostgreSQL réussie :"
    $connectionTest | Select-Object -Skip 2 | Select-Object -SkipLast 2 | ForEach-Object { $_.Trim() }
} else {
    Write-Host "❌ Échec de la connexion à PostgreSQL"
    Write-Host "Message d'erreur :"
    $connectionTest
}

# Afficher les bases de données existantes
Write-Host "`n📊 Bases de données existantes :"
& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -c "\l" 2>&1 | Select-Object -Skip 2 | Select-Object -SkipLast 1 | ForEach-Object { $_.Trim() }
