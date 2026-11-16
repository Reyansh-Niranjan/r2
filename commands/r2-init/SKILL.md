---
name: r2:init
description: "R2 Workspace Initialization & Onboarding Orchestrator. Audits environment, populates R2 specialist skills without touching root skills, registers Graphify hooks, configures Impeccable live mode, scaffolds AGENTS.md, and locks requirements via /grill-me. Does NOT load reference reasoning prompts."
---

# /r2:init — R2 Workspace Initialization

Orchestrates complete environment setup and skill onboarding for the R2 Skill Orchestration System.

> [!IMPORTANT]
> **Prompt Injection Policy:** `/r2:init` does **NOT** load `claude-fable-5.2.md` or `claude-opus-5.5.md`. It runs as a clean, deterministic orchestration engine.

---

## Execution Sequence

Follow this strict step-by-step pipeline when `/r2:init` is invoked:

### Step 1: Project & Skill Audit (Non-Destructive)
1. Inspect the target workspace root for package managers (`package.json`, `pnpm-workspace.yaml`, `pyproject.toml`), framework configurations, and Git repository metadata.
2. Check existing native skills in `.agents/skills/`.
3. **Never overwrite** existing native skills or project-specific configurations without explicit user authorization. Reuse compatible local skills where available.

### Step 2: Populate & Verify R2 Specialist Skills
Install and verify the appropriate specialist skills for the target project:
```powershell
python .agents/skills/r2/scripts/specialist-manager.py install
```
Or to install all available catalog specialists:
```powershell
python .agents/skills/r2/scripts/specialist-manager.py install-all
```
All specialist skills reside strictly in [.agents/skills/r2/skills/](.agents/skills/r2/skills/):
Ensure all 59 specialist skills reside in [.agents/skills/r2/skills/](.agents/skills/r2/skills/):
- **Original R2 Specialists (34):** `animate`, `animation-vocabulary`, `apple-design`, `awwwards`, `brag-slim`, `codebase-design`, `context7`, `design-taste-frontend`, `diagnosing-bugs`, `domain-modeling`, `emil-design-eng`, `find-animation-opportunities`, `graphify`, `grill-me`, `grim-prompter`, `humanizer`, `impeccable`, `improve-codebase-architecture`, `jury`, `karpathy-guidelines`, `minimalist-ui`, `mobile-native`, `motion`, `persona-critique`, `ponytail`, `ponytail-debt`, `refero-design`, `research`, `review-animations`, `setup-matt-pocock-skills`, `shieldcn-badges`, `slopmonster`, `superpowers`, `watch`.
- **Integrated NovaSlate Specialists (25):**
  - *Non-colliding (6):* `arena`, `ponytail-audit`, `ponytail-gain`, `ponytail-help`, `ponytail-review`, `video-analyzer`.
  - *Conflict-resolved (19):* `novaslate-animate`, `novaslate-animation-vocabulary`, `novaslate-codebase-design`, `novaslate-design-taste-frontend`, `novaslate-diagnosing-bugs`, `novaslate-domain-modeling`, `novaslate-emil-design-eng`, `novaslate-find-animation-opportunities`, `novaslate-improve-codebase-architecture`, `novaslate-karpathy-guidelines`, `novaslate-minimalist-ui`, `novaslate-mobile-native`, `novaslate-ponytail`, `novaslate-ponytail-debt`, `novaslate-research`, `novaslate-review-animations`, `novaslate-setup-matt-pocock-skills`, `novaslate-shieldcn-badges`, `novaslate-slopmonster`.
  - *Consolidated Canonical (1):* `impeccable` (fully unified into canonical `.agents/skills/r2/skills/impeccable/`).
- **Constraint:** Keep root `.agents/skills/` clean (only the 6 command skills). All 59 specialist implementations stay strictly inside `.agents/skills/r2/skills/`. Verify registry synchronization in [.agents/skills/r2/registry/skills.json](.agents/skills/r2/registry/skills.json).

### Step 3: Setup & Onboarding Workflows
Execute the standard scaffolding tasks in order:

1. **Configure Impeccable Live Mode:**
   - On Windows 11 PowerShell, ensure the copy agent environment variable is set:
     ```powershell
     $env:IMPECCABLE_LIVE_COPY_AGENT = "chat"
     ```
   - Prepare `.agents/skills/r2/skills/impeccable/` for live visual variant generation.

2. **Register Graphify Antigravity Hooks:**
   - Verify `graphify` availability or install if required:
     ```powershell
     uv tool install graphifyy
     graphify antigravity install
     graphify hook install
     ```
   - Build initial graph if none exists: `/graphify .`

3. **Scaffold Project Instructions via `setup-matt-pocock-skills`:**
   - Delegate to `.agents/skills/r2/skills/setup-matt-pocock-skills/` to configure issue tracker conventions (`gh issue create` or local markdown) and domain doc locations (`GLOSSARY.md`, `docs/adr/`).
   - Update `AGENTS.md` with concise agent instructions without overwriting existing user guidelines.

4. **Lock Project Requirements via `/grill-me` (One-Time Execution):**
   - Check if project profile exists at `.agents/skills/r2/registry/project-profile.json`.
   - **If the profile already exists:** Skip interrogation and read cached requirements.
   - **If the project is unconfigured:** Run the Socratic interview via `.agents/skills/r2/skills/grill-me/` to clarify scope, constraints, and non-negotiables. Persist answers to:
     ```json
     .agents/skills/r2/registry/project-profile.json
     ```
   - Future `/r2:init` runs will reuse this profile without re-prompting the user.

### Step 4: ECC Rule Initialization & Integrity Verification
1. **Detect Project Technologies:**
   Inspect workspace for active technology indicators (`package.json`, `tsconfig.json`, `pyproject.toml`, file extensions).
2. **Verify Installed Rule Integrity:**
   Verify byte-for-byte fidelity and SHA-256 hashes of installed rule files against [.agents/skills/r2/rules/manifest.json](.agents/skills/r2/rules/manifest.json):
   ```powershell
   python .agents/skills/r2/rules/loader.py verify
   ```
3. **Ensure Core Rule Packs Installed:**
   Ensure project-detected technology rule packs (`common`, `typescript`, `react`, `web`, `python`) are present under `.agents/skills/r2/rules/ecc/`.
4. **On-Demand Rule Acquisition:**
   If new languages or frameworks are detected that are not currently installed, download their immutable rule packs on demand:
   ```powershell
   python .agents/skills/r2/rules/loader.py get-rules <detected_tech>
   ```
5. **Git Privacy Verification:**
   Ensure `.agents/skills/r2/rules/.gitignore` contains `ecc/` so rule files remain strictly private and uncommitted.

### Step 5: Verify & Update Registry
- Verify every skill in `.agents/skills/r2/skills/` has a valid `SKILL.md`.
- Update [.agents/skills/r2/registry/skills.json](.agents/skills/r2/registry/skills.json) with current scan status and timestamps.
