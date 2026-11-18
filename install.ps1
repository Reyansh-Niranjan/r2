# R2 Skill Orchestration System - Windows PowerShell Installer
# Installs R2 command skills and engine into the target workspace from the private Reyansh-Niranjan/r2 repository or local source.

[CmdletBinding()]
param(
    [Parameter(Position=0)]
    [string]$TargetDirectory = (Get-Location).Path,

    [switch]$AllSpecialists,
    [switch]$Force,
    [switch]$Local,
    [switch]$SkipAuthCheck
)

$ErrorActionPreference = "Stop"

$REPO = "Reyansh-Niranjan/r2"
$REQUIRED_USER = "Reyansh-Niranjan"

if ($Local) {
    $SkipAuthCheck = $true
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   R2 Skill Orchestration System - Windows Installer     " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# ---------------------------------------------------------------------------
# 1. Pre-flight Checks & Authentication (Fail-Closed unless -Local/-SkipAuthCheck)
# ---------------------------------------------------------------------------
Write-Host "`n[1/5] Verifying prerequisites and authentication..." -ForegroundColor Yellow

if (-not $SkipAuthCheck) {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Error "Pre-flight Check Failed: 'git' is not installed or not in PATH. Please install Git for Windows and try again."
        exit 1
    }

    if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
        Write-Error "Pre-flight Check Failed: GitHub CLI ('gh') is not installed or not in PATH. Please install GitHub CLI (https://cli.github.com/) and try again."
        exit 1
    }

    # Check gh auth status
    $authStatus = gh auth status 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Authentication Failed: GitHub CLI is not authenticated. Please run 'gh auth login' to sign in and try again."
        exit 1
    }

    # Verify authenticated user
    $authUser = (gh api user -q .login 2>&1).Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($authUser)) {
        Write-Error "Authentication Failed: Could not retrieve authenticated username via 'gh api user'."
        exit 1
    }

    if ($authUser -ne $REQUIRED_USER) {
        Write-Error "Access Denied: Authenticated user '$authUser' does not match authorized repository owner '$REQUIRED_USER'. Run 'gh auth switch' or 'gh auth login' with the correct account."
        exit 1
    }

    # Verify access to private repository
    $repoCheck = gh repo view $REPO --json name,isPrivate 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Access Denied: Authenticated account '$authUser' cannot access private repository '$REPO'. Check repository permissions."
        exit 1
    }
    Write-Host "  [OK] Authenticated as authorized user '$authUser' with verified access to '$REPO'." -ForegroundColor Green
} else {
    Write-Host "  [WARN] Authentication check skipped by request (Local/SkipAuthCheck mode)." -ForegroundColor Magenta
}

# ---------------------------------------------------------------------------
# 2. Target Workspace & Git Tracking Policies
# ---------------------------------------------------------------------------
Write-Host "`n[2/5] Preparing target workspace and Git tracking policies..." -ForegroundColor Yellow

if (-not (Test-Path $TargetDirectory)) {
    New-Item -ItemType Directory -Path $TargetDirectory -Force | Out-Null
}
$TargetDirectory = (Resolve-Path $TargetDirectory).Path
Write-Host "  Target directory: $TargetDirectory"

$skillsDir = Join-Path $TargetDirectory ".agents\skills"
$r2ConfigDir = Join-Path $TargetDirectory ".r2"
$gitignoreFile = Join-Path $TargetDirectory ".gitignore"

# Ensure .gitignore exists and properly ignores .agents/skills/ while tracking .r2/
$ignorePattern = ".agents/skills/"
$altPattern = ".agents/skills"

if (-not (Test-Path $gitignoreFile)) {
    [System.IO.File]::WriteAllText($gitignoreFile, "$ignorePattern`n", [System.Text.UTF8Encoding]::new($false))
    Write-Host "  Created .gitignore with '$ignorePattern'." -ForegroundColor Green
} else {
    $ignoreContent = Get-Content -Path $gitignoreFile -Raw -ErrorAction SilentlyContinue
    if ($null -eq $ignoreContent) { $ignoreContent = "" }

    # Check if .r2 is mistakenly in .gitignore
    if ($ignoreContent -match "(?m)^\s*\.r2/?\s*$") {
        Write-Host "  [WARNING] Detected '.r2/' in .gitignore! Removing it because .r2/ must be Git-tracked." -ForegroundColor Yellow
        $newIgnore = ($ignoreContent -split "`r?`n" | Where-Object { $_ -notmatch "^\s*\.r2/?\s*$" }) -join "`n"
        [System.IO.File]::WriteAllText($gitignoreFile, $newIgnore, [System.Text.UTF8Encoding]::new($false))
        $ignoreContent = $newIgnore
    }

    # Ensure .agents/skills/ is present
    if ($ignoreContent -notmatch "(?m)^\s*\.agents/skills/?\s*$") {
        Add-Content -Path $gitignoreFile -Value "`n$ignorePattern" -Encoding UTF8
        Write-Host "  Added '$ignorePattern' to existing .gitignore." -ForegroundColor Green
    } else {
        Write-Host "  [OK] '$ignorePattern' is already present in .gitignore." -ForegroundColor Green
    }
}

# Ensure .r2 state directory exists (Git-tracked!)
if (-not (Test-Path $r2ConfigDir)) {
    New-Item -ItemType Directory -Path $r2ConfigDir -Force | Out-Null
}

$configFile = Join-Path $r2ConfigDir "config.json"
$existingConfig = @{}
if (Test-Path $configFile) {
    try {
        $existingConfig = Get-Content -Path $configFile -Raw | ConvertFrom-Json -AsHashtable
    } catch {
        $existingConfig = @{}
    }
}

# ---------------------------------------------------------------------------
# 3. Resolve Canonical R2 Engine & Commands Source
# ---------------------------------------------------------------------------
Write-Host "`n[3/5] Resolving R2 canonical engine and specialist source..." -ForegroundColor Yellow

$tempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("r2-install-" + [System.Guid]::NewGuid().ToString("N"))
try {
    # Check if installer is running inside a local cloned repository
    $scriptPath = $MyInvocation.MyCommand.Path
    $scriptDir = if ($scriptPath -and (Test-Path $scriptPath)) { Split-Path -Parent $scriptPath } else { $PSScriptRoot }
    $isLocalSource = $false
    if ($scriptDir -and (Test-Path (Join-Path $scriptDir "commands")) -and (Test-Path (Join-Path $scriptDir "engine"))) {
        $isLocalSource = $true
    } elseif (Test-Path "D:\R2\commands" -and (Test-Path "D:\R2\engine")) {
        $scriptDir = "D:\R2"
        $isLocalSource = $true
    }

    if ($Local -or ($isLocalSource -and ($Local -or $SkipAuthCheck -or (-not $Force)))) {
        Write-Host "  Using local canonical R2 source files from: $scriptDir"
        $sourceDir = $scriptDir
    } else {
        Write-Host "  Cloning $REPO (shallow)..."
        gh repo clone $REPO $tempDir -- --depth 1 --quiet
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to clone repository $REPO. Aborting."
            exit 1
        }
        $sourceDir = $tempDir
    }

    # Discover valid specialists from source
    $specialistsSource = Join-Path $sourceDir "specialists"
    $validSpecialists = @()
    if (Test-Path $specialistsSource) {
        $validSpecialists = Get-ChildItem -Path $specialistsSource -Directory | Select-Object -ExpandProperty Name
    }

    # ---------------------------------------------------------------------------
    # 4. Cleanup Stale R2 Folders & Install Commands/Engine
    # ---------------------------------------------------------------------------
    Write-Host "`n[4/5] Installing R2 command skills and engine runtime..." -ForegroundColor Yellow

    # Ensure target .agents/skills directory exists
    if (-not (Test-Path $skillsDir)) {
        New-Item -ItemType Directory -Path $skillsDir -Force | Out-Null
    }

    # 1. Clean stale R2 command skills (.agents/skills/r2-*)
    Get-ChildItem -Path $skillsDir -Directory | Where-Object { $_.Name -like "r2-*" } | ForEach-Object {
        Write-Host "  -> Removing stale R2 command skill: /$($_.Name)" -ForegroundColor Yellow
        Remove-Item -Path $_.FullName -Recurse -Force
    }

    # 2. Clean .agents/skills/r2 (engine & specialists container)
    $r2TargetDir = Join-Path $skillsDir "r2"
    if (Test-Path $r2TargetDir) {
        # Prune orphan specialist skills inside .agents/skills/r2/skills/
        $r2SkillsDir = Join-Path $r2TargetDir "skills"
        if (Test-Path $r2SkillsDir) {
            $orphanSkills = Get-ChildItem -Path $r2SkillsDir -Directory | Where-Object { $_.Name -notin $validSpecialists }
            foreach ($orphan in $orphanSkills) {
                Write-Host "  -> Removing orphan specialist skill: r2/skills/$($orphan.Name)" -ForegroundColor Yellow
                Remove-Item -Path $orphan.FullName -Recurse -Force
            }
        }

        # Remove previous engine runtime folders and caches to ensure a clean slate (leave skills/ intact)
        Get-ChildItem -Path $r2TargetDir | Where-Object { $_.Name -ne "skills" } | ForEach-Object {
            Remove-Item -Path $_.FullName -Recurse -Force
        }
    } else {
        New-Item -ItemType Directory -Path $r2TargetDir -Force | Out-Null
    }

    # 3. Log and verify non-R2 skills preservation
    $nonR2Skills = Get-ChildItem -Path $skillsDir -Directory | Where-Object { $_.Name -ne "r2" -and $_.Name -notlike "r2-*" }
    if ($nonR2Skills) {
        Write-Host "  [OK] Preserving non-R2 skills in .agents/skills/: $(($nonR2Skills | Select-Object -ExpandProperty Name) -join ', ')" -ForegroundColor Green
    }

    # 4. Verify project state in .r2/ is preserved (never deleted or overwritten)
    $preservedStateFiles = @("project-profile.json", "rules.md", "hardware-profile.json", "REVIEW.md")
    $foundState = @()
    foreach ($f in $preservedStateFiles) {
        if (Test-Path (Join-Path $r2ConfigDir $f)) {
            $foundState += $f
        }
    }
    if ($foundState.Count -gt 0) {
        Write-Host "  [OK] Preserving target project .r2/ state: $($foundState -join ', ')" -ForegroundColor Green
    }

    # Install the 7 command skills into .agents/skills/
    $commandsSource = Join-Path $sourceDir "commands"
    if (Test-Path $commandsSource) {
        Get-ChildItem -Path $commandsSource -Directory | ForEach-Object {
            $cmdName = $_.Name
            $targetCmdDir = Join-Path $skillsDir $cmdName
            if (-not (Test-Path $targetCmdDir)) {
                New-Item -ItemType Directory -Path $targetCmdDir -Force | Out-Null
            }
            Copy-Item -Path (Join-Path $_.FullName "*") -Destination $targetCmdDir -Recurse -Force
            Write-Host "  -> Installed command skill: /$cmdName" -ForegroundColor Cyan
        }
    }

    # Install engine runtime assets into .agents/skills/r2/
    $engineSource = Join-Path $sourceDir "engine"
    if (Test-Path $engineSource) {
        Copy-Item -Path (Join-Path $engineSource "*") -Destination $r2TargetDir -Recurse -Force
        Write-Host "  -> Installed R2 engine runtime & synced reference prompts (claude-fable-5.2.md, claude-opus-5.5.md, registry, rules, scripts)." -ForegroundColor Cyan
    }

    # Cache specialists so /r2:init can deploy offline or on-demand
    if (Test-Path $specialistsSource) {
        $cacheDir = Join-Path $r2TargetDir "specialists_cache"
        Copy-Item -Path $specialistsSource -Destination $cacheDir -Recurse -Force
        Write-Host "  -> Cached specialist catalog for on-demand onboarding." -ForegroundColor Cyan

        # If -AllSpecialists requested, populate .agents/skills/r2/skills/ immediately
        if ($AllSpecialists) {
            $specialistDest = Join-Path $r2TargetDir "skills"
            if (-not (Test-Path $specialistDest)) {
                New-Item -ItemType Directory -Path $specialistDest -Force | Out-Null
            }
            Copy-Item -Path (Join-Path $specialistsSource "*") -Destination $specialistDest -Recurse -Force
            Write-Host "  -> Installed all $($validSpecialists.Count) specialist skills into $specialistDest" -ForegroundColor Green
        }
    }

    # Update .r2/config.json
    $version = "2.2.0"
    $versionFile = Join-Path $sourceDir "VERSION"
    if (Test-Path $versionFile) {
        $version = (Get-Content $versionFile -Raw).Trim()
    }

    $now = (Get-Date).ToString("o")
    $newConfig = @{
        "version" = $version
        "repository" = $REPO
        "installed_at" = if ($existingConfig.ContainsKey("installed_at")) { $existingConfig["installed_at"] } else { $now }
        "updated_at" = $now
        "commands" = @("r2", "r2-init", "r2-code", "r2-debug", "r2-web", "r2-motion", "r2-3d")
        "specialists_mode" = if ($AllSpecialists) { "all" } else { "on_demand" }
        "status" = "ready"
    }

    [System.IO.File]::WriteAllText($configFile, ($newConfig | ConvertTo-Json -Depth 5), [System.Text.UTF8Encoding]::new($false))
    Write-Host "  -> Updated Git-tracked configuration at .r2/config.json" -ForegroundColor Green

} finally {
    if (Test-Path $tempDir) {
        Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# ---------------------------------------------------------------------------
# 5. Summary & Next Steps
# ---------------------------------------------------------------------------
Write-Host "`n[5/5] R2 Installation Complete!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "R2 Commands Installed:" -ForegroundColor White
Write-Host "  - /r2         : Central ecosystem overview & routing table"
Write-Host "  - /r2:init    : Project inspection, onboarding & ECC rules setup"
Write-Host "  - /r2:code    : Full-stack engineering & Karpathy constraints"
Write-Host "  - /r2:debug   : Precision triage & causal graph tracing"
Write-Host "  - /r2:web     : Anti-slop creative web frontend design"
Write-Host "  - /r2:motion  : 120fps GPU animations & spring physics"
Write-Host "  - /r2:3d      : Parametric CadQuery solid modeling & 3D printing DfM"
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "`nNEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. In Google Antigravity / Gemini chat, run:" -ForegroundColor White
Write-Host "     /r2:init" -ForegroundColor Green
Write-Host "2. /r2:init will inspect your project, install matching specialist skills," -ForegroundColor White
Write-Host "   and automatically download required immutable ECC rule packs.`n" -ForegroundColor White
