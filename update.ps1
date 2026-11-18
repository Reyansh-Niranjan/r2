# R2 Skill Orchestration System - Windows PowerShell Updater
# Checks for newer versions of R2 in the private Reyansh-Niranjan/r2 repository and safely updates local skills.

[CmdletBinding()]
param(
    [Parameter(Position=0)]
    [string]$TargetDirectory = (Get-Location).Path,

    [switch]$Force
)

$ErrorActionPreference = "Stop"
$REPO = "Reyansh-Niranjan/r2"
$REQUIRED_USER = "Reyansh-Niranjan"

Write-Host "Checking for R2 updates for target: $TargetDirectory" -ForegroundColor Cyan

# Check GitHub auth
$authUser = (gh api user -q .login 2>&1).Trim()
if ($authUser -ne $REQUIRED_USER) {
    Write-Error "Access Denied: Authenticated GitHub user '$authUser' does not match required owner '$REQUIRED_USER'."
    exit 1
}

$r2Config = Join-Path $TargetDirectory ".r2\config.json"
if (-not (Test-Path $r2Config)) {
    Write-Error "No existing R2 installation found at $TargetDirectory. Run install.ps1 first."
    exit 1
}

$localConfig = Get-Content $r2Config -Raw | ConvertFrom-Json
$localVersion = $localConfig.version

# Check upstream version
$remoteVersion = (gh api -H "Accept: application/vnd.github.raw+json" "repos/$REPO/contents/VERSION" 2>&1).Trim()
Write-Host "Local Version:    $localVersion"
Write-Host "Upstream Version: $remoteVersion"

if ($localVersion -eq $remoteVersion -and (-not $Force)) {
    Write-Host "R2 is already up to date (version $localVersion)." -ForegroundColor Green
    exit 0
}

Write-Host "Updating R2 to version $remoteVersion..." -ForegroundColor Yellow

# Run installer in update mode
$installScript = Join-Path $PSScriptRoot "install.ps1"
if (Test-Path $installScript) {
    & $installScript -TargetDirectory $TargetDirectory -Force
} else {
    & ([scriptblock]::Create((gh api -H "Accept: application/vnd.github.raw+json" "repos/$REPO/contents/install.ps1"))) -TargetDirectory $TargetDirectory -Force
}

Write-Host "Deployed 7 command skills (/r2, /r2:init, /r2:code, /r2:motion, /r2:web, /r2:debug, /r2:3d) to .agents/skills/." -ForegroundColor Cyan
Write-Host "R2 successfully updated to $remoteVersion!" -ForegroundColor Green
