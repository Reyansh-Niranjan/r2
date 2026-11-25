---
name: r2:init
description: "R2 Workspace Initialization & Onboarding Orchestrator. Audits environment, populates R2 specialist skills without touching root skills, registers Graphify hooks, configures Impeccable live mode, scaffolds AGENTS.md, locks requirements in .r2/project-profile.json via /grill-me, and sets up .r2/ project rules and REVIEW.md tracking. Does NOT load reference reasoning prompts."
---

# /r2:init — R2 Workspace Initialization

Orchestrates complete environment setup and skill onboarding for the R2 Skill Orchestration System.

> [!IMPORTANT]
> **Prompt Injection Policy & Mandatory Pagination Rule:**
> - `/r2:init` does **NOT** load `claude-fable-5.2.md` or `claude-opus-5.5.md`. Reference files are part of R2 directly and are installed and synchronized by `install.ps1` and `update.ps1`. `/r2:init` is strictly focused on workspace onboarding, technology detection, and `.r2/` project state only.
> - **Mandatory Pagination Rule:** If any `view_file` call stops at line 800, you MUST immediately call `view_file` with `StartLine: 801` before proceeding.

### 📋 Native Task Tracking (No Markdown Checkpoint Files)
- Use Antigravity's native **TODO / Task List tool (`update_steps`)** directly in the conversation UI for multi-step tracking.
- Keep task items short (2-6 words), action-oriented, and updated live as each step starts (`in_progress`) and finishes (`done`).
- **PROHIBITION:** NEVER create, read, or update `TASKS.md`, `tasks.md`, or any markdown checkpoint files on disk. All task tracking lives strictly in the conversation UI via the native tool.

---

## Execution Sequence

Follow this strict step-by-step pipeline when `/r2:init` is invoked:

### Step 1: Project & Skill Audit (Non-Destructive)
1. Inspect the target workspace root for package managers (`package.json`, `pnpm-workspace.yaml`, `pyproject.toml`), framework configurations, CAD assets (`cad/`, `model.py`), and Git repository metadata.
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
Ensure all 45 specialist skills reside in [.agents/skills/r2/skills/](.agents/skills/r2/skills/):
- **Core & Engineering (21):** `arena`, `codebase-design`, `context7`, `diagnosing-bugs`, `domain-modeling`, `graphify`, `grill-me`, `grim-prompter`, `humanizer`, `improve-codebase-architecture`, `karpathy-guidelines`, `persona-critique`, `ponytail`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, `ponytail-help`, `ponytail-review`, `research`, `slopmonster`, `superpowers`.
- **Frontend & Motion (19):** `animate`, `animation-vocabulary`, `apple-design`, `awwwards`, `brag-slim`, `design-taste-frontend`, `emil-design-eng`, `find-animation-opportunities`, `impeccable`, `jury`, `minimalist-ui`, `mobile-native`, `motion`, `refero-design`, `review-animations`, `setup-matt-pocock-skills`, `shieldcn-badges`, `video-analyzer`, `watch`.
- **CAD & 3D Printing (5):** `3d-print-skill`, `cad-agent`, `cadquery-modeling`, `cad-skill`, `three-d-printer`.
- **Constraint:** Keep root `.agents/skills/` clean (only the 9 command skills: `/r2`, `/r2:init`, `/r2:code`, `/r2:debug`, `/r2:bug`, `/r2:plan`, `/r2:motion`, `/r2:web`, `/r2:3d`). All specialist implementations stay strictly inside `.agents/skills/r2/skills/`. Verify registry synchronization in [.agents/skills/r2/registry/skills.json](.agents/skills/r2/registry/skills.json).

### `skills.sh` Missing Domain Specialist Discovery (Optional On-Demand)
If Step 1 detects a stack or workflow (e.g., Supabase, Next.js, Stripe, Expo, Rust) that lacks a matching specialist in `.agents/skills/r2/skills/`, offer to search and install from [skills.sh](https://www.skills.sh/) (`vercel-labs/skills` `find-skills`) for Antigravity:
```powershell
python .agents/skills/r2/scripts/specialist-manager.py find "<detected-tech>"
python .agents/skills/r2/scripts/specialist-manager.py add <owner/repo>
```
`specialist-manager.py` runs `npx skills add ... -a antigravity -y --copy` in an isolated staging dir, routes files verbatim into `.agents/skills/r2/skills/<skill-name>/SKILL.md`, registers metadata in `skills.json` (`source: "skills.sh"`), syncs `.agents/skills/r2/SKILL.md`, and enforces R2's exclusion list (`SkillSpector`, `OmniRoute`, `Agent Vault`, `claude-auto-handoff`, `Gemini Flash TTS`, `reanimate`, `unslop`, `hallmark`, `scrapling`, `strix`, `stitch-skills`).

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

4. **Lock Project Requirements & Rules via `.r2/` (Strict State Isolation):**
   - **Zero Specialist Duplication:** Project-specific rules, constraints, and overrides are stored strictly inside `.r2/` (e.g., `.r2/project-profile.json` and `.r2/rules.md`). NEVER duplicate or fork specialist skills into global `specialists/`.
   - Check if project profile exists at `.r2/project-profile.json`:
     - **If the profile already exists:** Skip interrogation and read cached requirements.
     - **If the project is unconfigured:** Run the Socratic interview via `.agents/skills/r2/skills/grill-me/` to clarify scope, constraints, and non-negotiables. Persist answers to:
       ```json
       .r2/project-profile.json
       ```
   - Scaffold project-specific guidelines in `.r2/rules.md` for workspace architectural invariants, technology overrides, and custom constraints.
   - Initialize `.r2/REVIEW.md` for bug prevention rules. Whenever `/r2:debug` resolves an issue, it appends a 1-line rule to `.r2/REVIEW.md` that all future orchestrators check automatically.
   - If CAD / 3D printing is detected, initialize `.r2/hardware-profile.json` with printer bed boundaries, nozzle dimensions, and material shrinkage preferences for `/r2:3d`.

### Step 4: ECC Rule Initialization & Integrity Verification
1. **Detect Project Technologies:**
   Inspect workspace for active technology indicators (`package.json`, `tsconfig.json`, `pyproject.toml`, CAD files, file extensions).
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

### Step 5: Verify & Update Registry + Active Gate Rule
1. **Read Live R2 Version:** Read the active installed version dynamically from [.agents/skills/r2/VERSION](.agents/skills/r2/VERSION) (falling back to `.r2/config.json` `"version"` field). **NEVER** hardcode or guess a version string.
2. **Verify Installed Specialists:** Run `python .agents/skills/r2/scripts/specialist-manager.py verify` to confirm every specialist in `.agents/skills/r2/skills/` has a valid `SKILL.md`.
3. **Verify Always-On Proof-of-Read Gate:** Confirm [.agents/rules/r2-skill-gate.md](.agents/rules/r2-skill-gate.md) exists on disk and is active so every `/r2:*` command emits a `SKILLS LOADED` receipt before workspace code reads or edits.
4. **Sync Registry & Table:** Run `python .agents/skills/r2/scripts/specialist-manager.py sync` to synchronize [.agents/skills/r2/registry/skills.json](.agents/skills/r2/registry/skills.json) and [.agents/skills/r2/SKILL.md](.agents/skills/r2/SKILL.md).

### Step 6: Print Live Initialization Summary
Conclude `/r2:init` by reporting the live status using ONLY the dynamically read version, verified `.agents/rules/r2-skill-gate.md` state, and the exact **9-command** 1:1 reasoning routing table:
- **Installed R2 Version:** `<live value from .agents/skills/r2/VERSION or .r2/config.json>`
- **Proof-of-Read Gate:** `.agents/rules/r2-skill-gate.md` (`ACTIVE` / `MISSING`)
- **Available R2 Commands (9):**
  | Command | Role | Reasoning Injection (1:1) |
  | :--- | :--- | :--- |
  | `/r2` | Central index & discovery hub | *None* |
  | `/r2:init` | Workspace onboarding & `.r2/` state setup | *None* |
  | `/r2:code` | Full-stack engineering & simplicity constraints | `Opus 5.5` (`claude-opus-5.5.md`) |
  | `/r2:web` | Anti-slop creative frontend design | `Fable 5.2` (`claude-fable-5.2.md`) |
  | `/r2:motion` | 120fps GPU animation & spring physics | `Fable 5.2` (`claude-fable-5.2.md`) |
  | `/r2:debug` | Empirical triage, root-cause tracing & routing | `Opus 5.5` (`claude-opus-5.5.md`) |
  | `/r2:bug` | Systematic bug diagnosis & regression prevention | `Opus 5.5` (`claude-opus-5.5.md`) |
  | `/r2:plan` | Socratic requirements lock & TDD milestones | `Opus 5.5` (`claude-opus-5.5.md`) |
  | `/r2:3d` | Parametric CadQuery solid modeling & 3D printing DfM | `Opus 5.5` (`claude-opus-5.5.md`) |
