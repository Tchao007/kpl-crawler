param(
  [string]$HostName = "127.0.0.1",
  [int]$Port = 8765,
  [int]$StopTimeoutMs = 2000,
  [int]$HealthTimeoutSec = 3,
  [switch]$WithLogs
)

$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$pidPath = Join-Path $root "server.pid"
$serverScript = Join-Path $root "generated\scenario_api_server.py"

function Stop-OldServer {
  $serverScriptPattern = [regex]::Escape($serverScript)
  $currentPid = $PID
  Get-CimInstance Win32_Process -Filter "name='python.exe'" |
    Where-Object {
      $_.ProcessId -ne $currentPid -and
      $_.CommandLine -and
      $_.CommandLine -match $serverScriptPattern
    } |
    ForEach-Object {
      Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    }

  if (-not (Test-Path -LiteralPath $pidPath)) {
    return
  }

  $rawPid = (Get-Content -LiteralPath $pidPath -ErrorAction SilentlyContinue | Select-Object -First 1)
  if (-not $rawPid) {
    return
  }

  $oldPid = [int]$rawPid
  $oldProcess = Get-Process -Id $oldPid -ErrorAction SilentlyContinue
  if (-not $oldProcess) {
    return
  }

  Stop-Process -Id $oldPid -Force -ErrorAction SilentlyContinue
  $watch = [Diagnostics.Stopwatch]::StartNew()
  while ($watch.ElapsedMilliseconds -lt $StopTimeoutMs) {
    if (-not (Get-Process -Id $oldPid -ErrorAction SilentlyContinue)) {
      return
    }
    Start-Sleep -Milliseconds 100
  }
}

function Start-NewServer {
  $arguments = @("-B", $serverScript, "--host", $HostName, "--port", [string]$Port)
  $startArgs = @{
    FilePath = "python"
    ArgumentList = $arguments
    WorkingDirectory = $root
    WindowStyle = "Hidden"
    PassThru = $true
  }

  if ($WithLogs) {
    $startArgs.RedirectStandardOutput = Join-Path $root "server.out.log"
    $startArgs.RedirectStandardError = Join-Path $root "server.err.log"
  }

  $process = Start-Process @startArgs
  Set-Content -LiteralPath $pidPath -Value $process.Id -Encoding ASCII
  return $process
}

function Test-ServerHealth {
  param([int]$ProcessId)

  $url = "http://${HostName}:${Port}/"
  try {
    $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec $HealthTimeoutSec
    return "ok pid=$ProcessId status=$($response.StatusCode) url=$url"
  } catch {
    return "started pid=$ProcessId health=pending url=$url error=$($_.Exception.Message)"
  }
}

$total = [Diagnostics.Stopwatch]::StartNew()
Stop-OldServer
$newProcess = Start-NewServer
Start-Sleep -Milliseconds 300
$result = Test-ServerHealth -ProcessId $newProcess.Id
$total.Stop()
"$result elapsed_ms=$($total.ElapsedMilliseconds)"
