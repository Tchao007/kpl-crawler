param(
    [string]$HostName = "127.0.0.1",
    [int]$Port = 80,
    [string]$Python = "D:\python\python.exe"
)

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$server = Join-Path $repo "generated\scenario_api_server.py"
$outLog = Join-Path $repo "server.out.log"
$errLog = Join-Path $repo "server.err.log"

function Get-ListeningPids {
    param([int]$LocalPort)
    $result = @()
    $lines = netstat -ano | Select-String ":$LocalPort\s+.*LISTENING\s+(\d+)"
    foreach ($line in $lines) {
        $match = [regex]::Match($line.Line, "LISTENING\s+(\d+)")
        if ($match.Success) {
            $result += [int]$match.Groups[1].Value
        }
    }
    return $result | Sort-Object -Unique
}

foreach ($pidToStop in Get-ListeningPids -LocalPort $Port) {
    Stop-Process -Id $pidToStop -Force -ErrorAction SilentlyContinue
}

for ($i = 0; $i -lt 20; $i++) {
    if (-not @(Get-ListeningPids -LocalPort $Port).Count) {
        break
    }
    Start-Sleep -Milliseconds 100
}

if (@(Get-ListeningPids -LocalPort $Port).Count) {
    Write-Error "port $Port is still occupied"
    exit 1
}

Start-Process -FilePath $Python `
    -ArgumentList @($server, "--host", $HostName, "--port", [string]$Port) `
    -WorkingDirectory $repo `
    -RedirectStandardOutput $outLog `
    -RedirectStandardError $errLog `
    -WindowStyle Hidden

$healthUrl = "http://${HostName}:${Port}/api/health"
for ($i = 0; $i -lt 50; $i++) {
    try {
        $response = Invoke-WebRequest -UseBasicParsing -Uri $healthUrl -TimeoutSec 1
        if ($response.StatusCode -eq 200) {
            Write-Output "started $healthUrl"
            exit 0
        }
    } catch {
        Start-Sleep -Milliseconds 100
    }
}

Write-Error "server did not become healthy within 5 seconds; see $errLog"
exit 1
