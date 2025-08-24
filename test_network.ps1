# Test de connexion réseau vers le serveur PostgreSQL
$hostname = "dpg-d2l2ir95pdvs73a92fog-a.frankfurt-postgres.render.com"
$port = 5432

Write-Host "=== Test de connectivité réseau ==="
Write-Host "Cible: $hostname`:$port"

# Vérifier la résolution DNS
try {
    $ipAddresses = [System.Net.Dns]::GetHostAddresses($hostname) | Select-Object -ExpandProperty IPAddressToString
    Write-Host "✅ Résolution DNS réussie: $($ipAddresses -join ', ')"
} catch {
    Write-Host "❌ Échec de la résolution DNS pour $hostname"
    exit 1
}

# Tester la connexion TCP
$tcpClient = New-Object System.Net.Sockets.TcpClient
$connection = $tcpClient.BeginConnect($hostname, $port, $null, $null)
$success = $connection.AsyncWaitHandle.WaitOne(5000, $false)  # Timeout de 5 secondes

if ($tcpClient.Connected) {
    Write-Host "✅ Connexion TCP réussie sur le port $port"
    $tcpClient.EndConnect($connection)
} else {
    Write-Host "❌ Échec de la connexion TCP sur le port $port"
    Write-Host "Vérifiez que:"
    Write-Host "1. Le serveur est en cours d'exécution"
    Write-Host "2. Le port $port n'est pas bloqué par un pare-feu"
    Write-Host "3. Le service est accessible depuis votre réseau"
    exit 1
}

# Tester avec Test-NetConnection
Write-Host "`n=== Test avec Test-NetConnection ==="
$testResult = Test-NetConnection -ComputerName $hostname -Port $port -InformationLevel Detailed
$testResult | Format-List *

if ($testResult.TcpTestSucceeded) {
    Write-Host "✅ Test de connexion réussi avec Test-NetConnection"
} else {
    Write-Host "❌ Échec du test de connexion avec Test-NetConnection"
    exit 1
}
