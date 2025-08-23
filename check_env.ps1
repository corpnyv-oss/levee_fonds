Write-Host "=== Vérification de l'environnement ==="

# Vérifier Python
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if ($pythonPath) {
    Write-Host "✅ Python trouvé: $pythonPath"
    $pythonVersion = python --version 2>&1
    Write-Host "   Version: $pythonVersion"
} else {
    Write-Host "❌ Python n'est pas dans le PATH"
}

# Vérifier pip
$pipPath = (Get-Command pip -ErrorAction SilentlyContinue).Source
if ($pipPath) {
    Write-Host "✅ pip trouvé: $pipPath"
    $pipVersion = pip --version 2>&1
    Write-Host "   $pipVersion"
} else {
    Write-Host "❌ pip n'est pas dans le PATH"
}

# Vérifier PostgreSQL
$psqlPath = (Get-Command psql -ErrorAction SilentlyContinue).Source
if ($psqlPath) {
    Write-Host "✅ PostgreSQL trouvé: $psqlPath"
    $psqlVersion = psql --version 2>&1
    Write-Host "   $psqlVersion"
} else {
    Write-Host "❌ PostgreSQL (psql) n'est pas dans le PATH"
}

# Vérifier les variables d'environnement
Write-Host "`n=== Variables d'environnement ==="
$envVars = @('PATH', 'PYTHONPATH', 'DJANGO_SETTINGS_MODULE')
foreach ($var in $envVars) {
    $value = [Environment]::GetEnvironmentVariable($var)
    if ($value) {
        Write-Host "$var = $value"
    } else {
        Write-Host "$var = (non défini)"
    }
}

# Vérifier les services PostgreSQL
Write-Host "`n=== Services PostgreSQL ==="
$postgresServices = Get-Service -Name postgresql* -ErrorAction SilentlyContinue
if ($postgresServices) {
    $postgresServices | Format-Table -Property Name, Status, DisplayName
} else {
    Write-Host "Aucun service PostgreSQL trouvé"
}

# Vérifier les connexions réseau
Write-Host "`n=== Connexions réseau PostgreSQL ==="
$pgConnections = Get-NetTCPConnection -LocalPort 5432 -ErrorAction SilentlyContinue
if ($pgConnections) {
    $pgConnections | Format-Table -Property LocalAddress, LocalPort, State, OwningProcess
} else {
    Write-Host "Aucune connexion sur le port 5432"
}
