# R2 Skill Orchestration System - Windows PowerShell Updater
# Checks for newer versions of R2 and safely updates local skills. Supports GitHub and -Local mode.

[CmdletBinding()]
param(
    [Parameter(Position=0)]
    [string]$TargetDirectory = (Get-Location).Path,

    [switch]$Local,
    [switch]$Force,
    [switch]$AllSpecialists
)

$ErrorActionPreference = "Stop"
$REPO = "Reyansh-Niranjan/r2"
$REQUIRED_USER = "Reyansh-Niranjan"

# Resolve target directory
if (-not (Test-Path $TargetDirectory)) {
    Write-Error "Target directory '$TargetDirectory' does not exist."
    exit 1
}
$TargetDirectory = (Resolve-Path $TargetDirectory).Path
Write-Host "Checking for R2 updates for target: $TargetDirectory" -ForegroundColor Cyan

$r2Config = Join-Path $TargetDirectory ".r2\config.json"
if (-not (Test-Path $r2Config)) {
    Write-Error "No existing R2 installation found at $TargetDirectory. Run install.ps1 first."
    exit 1
}

$localConfig = Get-Content $r2Config -Raw | ConvertFrom-Json
$localVersion = $localConfig.version

# Detect local R2 repository candidate ($PSScriptRoot or D:\R2)
$localRepo = $null
if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "VERSION")) -and (Test-Path (Join-Path $PSScriptRoot "commands"))) {
    $localRepo = $PSScriptRoot
} elseif (Test-Path "D:\R2\VERSION") {
    $localRepo = "D:\R2"
}

$useLocal = $Local.IsPresent
$targetVersion = $null

if (-not $useLocal) {
    # Default: Try GitHub check first
    Write-Host "Checking for upstream R2 updates on GitHub ($REPO)..." -ForegroundColor Cyan
    try {
        if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
            throw "GitHub CLI ('gh') is not installed or not in PATH."
        }
        $authStatus = gh auth status 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "GitHub CLI is not authenticated."
        }
        $authUser = (gh api user -q .login 2>&1).Trim()
        if ($authUser -ne $REQUIRED_USER) {
            throw "Authenticated user '$authUser' does not match required owner '$REQUIRED_USER'."
        }
        $remoteVersion = (gh api -H "Accept: application/vnd.github.raw+json" "repos/$REPO/contents/VERSION" 2>&1).Trim()
        if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($remoteVersion)) {
            throw "Failed to fetch remote VERSION from GitHub."
        }
        Write-Host "Local Installed Version: $localVersion"
        Write-Host "Upstream Remote Version: $remoteVersion"

        if ($localVersion -eq $remoteVersion -and (-not $Force)) {
            Write-Host "R2 is already up to date (version $localVersion)." -ForegroundColor Green
            exit 0
        }
        $targetVersion = $remoteVersion
    } catch {
        if ($localRepo) {
            Write-Host "  [WARN] GitHub check failed: $($_.Exception.Message)" -ForegroundColor Yellow
            Write-Host "  [WARN] Falling back cleanly to local R2 repository at $localRepo..." -ForegroundColor Yellow
            $useLocal = $true
        } else {
            Write-Error "Update Failed: $($_.Exception.Message)"
            exit 1
        }
    }
}

if ($useLocal) {
    if (-not $localRepo) {
        Write-Error "Local update failed: No local R2 repository found at '$PSScriptRoot' or 'D:\R2'."
        exit 1
    }
    $localRepoVersion = (Get-Content (Join-Path $localRepo "VERSION") -Raw).Trim()
    Write-Host "Local Update Mode: using repository at $localRepo (v$localRepoVersion)" -ForegroundColor Cyan
    Write-Host "Local Installed Version: $localVersion"
    Write-Host "Local Repository Version: $localRepoVersion"

    if ($localVersion -eq $localRepoVersion -and (-not $Force)) {
        Write-Host "R2 is already up to date (version $localVersion)." -ForegroundColor Green
        exit 0
    }
    $targetVersion = $localRepoVersion
}

Write-Host "Updating R2 to version $targetVersion..." -ForegroundColor Yellow

# Run installer in update mode
$installParams = @{
    TargetDirectory = $TargetDirectory
    Force = $true
}
if ($AllSpecialists) {
    $installParams["AllSpecialists"] = $true
}

if ($useLocal) {
    $installParams["Local"] = $true
    $installParams["SkipAuthCheck"] = $true
    $localInstallScript = Join-Path $localRepo "install.ps1"
    & $localInstallScript @installParams
} else {
    $installScript = Join-Path $PSScriptRoot "install.ps1"
    if (Test-Path $installScript) {
        & $installScript @installParams
    } else {
        & ([scriptblock]::Create((gh api -H "Accept: application/vnd.github.raw+json" "repos/$REPO/contents/install.ps1"))) @installParams
    }
}

Write-Host "Deployed 7 command skills and synced reference prompts into .agents/skills/." -ForegroundColor Cyan
Write-Host "R2 successfully updated to $targetVersion!" -ForegroundColor Green
