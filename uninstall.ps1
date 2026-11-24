# R2 Skill Orchestration System - Windows PowerShell Uninstaller
# Safely uninstalls R2 command skills and engine, optionally purging .r2/ state.

[CmdletBinding()]
param(
    [Parameter(Position=0)]
    [string]$TargetDirectory = (Get-Location).Path,

    [switch]$PurgeState,
    [switch]$Confirm
)

$TargetDirectory = (Resolve-Path $TargetDirectory).Path
Write-Host "Uninstalling R2 from: $TargetDirectory" -ForegroundColor Yellow

$skillsDir = Join-Path $TargetDirectory ".agents\skills"
$commands = @("r2", "r2-init", "r2-code", "r2-debug", "r2-bug", "r2-plan", "r2-web", "r2-motion", "r2-3d")

foreach ($cmd in $commands) {
    $cmdPath = Join-Path $skillsDir $cmd
    if (Test-Path $cmdPath) {
        Remove-Item -Path $cmdPath -Recurse -Force
        Write-Host "Removed /$cmd" -ForegroundColor Cyan
    }
}

if ($PurgeState) {
    $r2Dir = Join-Path $TargetDirectory ".r2"
    if (Test-Path $r2Dir) {
        Remove-Item -Path $r2Dir -Recurse -Force
        Write-Host "Purged .r2/ configuration and state directory." -ForegroundColor Yellow
    }
} else {
    Write-Host "Preserved .r2/ configuration directory (pass -PurgeState to remove)." -ForegroundColor Green
}

Write-Host "R2 has been safely uninstalled." -ForegroundColor Green
