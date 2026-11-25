# R2 Skill Orchestration System (`v2.3.0`)

**R2** is a modular skill orchestration architecture built for **Google Antigravity** and **Gemini**. It separates command routing from specialist implementation across 9 commands and 45+ specialist skills, coordinating software engineering, 120fps GPU motion design, Awwwards-standard web builds, systematic debugging, and parametric CadQuery 3D printing.

---

## ⚡ Quickstart: One-Line Installation (Windows)

Open PowerShell in your target project directory and run:

### Massgrave-Style (`irm | iex`):
```powershell
irm -H @{Authorization="Bearer $(gh auth token)"} https://raw.githubusercontent.com/Reyansh-Niranjan/r2/main/install.ps1 | iex
```

### GitHub CLI Native Pipeline:
```powershell
(gh api -H "Accept: application/vnd.github.raw+json" repos/Reyansh-Niranjan/r2/contents/install.ps1 | Out-String) | iex
```

*Or pass a target directory explicitly:*
```powershell
& ([scriptblock]::Create((gh api -H "Accept: application/vnd.github.raw+json" repos/Reyansh-Niranjan/r2/contents/install.ps1))) -TargetDirectory "C:\Projects\MyApp"
```

Once installed, switch to Google Antigravity or Gemini chat and run:
```text
/r2:init
```

---

## 🏛️ Architecture Overview

R2 organizes its pipeline into **9 Command Orchestrators**, a **Specialist Collection** (45 bundled skills plus `skills.sh` packages), the `.agents/rules/r2-skill-gate.md` rule, and the **ECC Rules Provider**.

```text
Target Project/
├── .agents/
│   ├── rules/
│   │   └── r2-skill-gate.md        # Always-on Proof-of-Read Specialist Skill Gate
│   └── skills/
│       ├── r2/                     # /r2 (Informational index & discovery hub)
│       │   ├── SKILL.md
│       │   ├── VERSION             # Live deployed R2 version (2.3.0)
│       │   ├── references/         # Fable 5.2, Opus 5.5, Claude Design suites (<700 lines each)
│       │   ├── registry/           # Master catalog (45+ skills, skills.sh) & dependency graph
│       │   ├── rules/              # Private rules engine (ECC provider)
│       │   │   ├── RULE_PROTOCOL.md
│       │   │   ├── manifest.json
│       │   │   ├── loader.py
│       │   │   └── .gitignore      # Ignores ecc/ rule directory
│       │   └── skills/             # Onboarded & skills.sh specialist skills
│       ├── r2-init/                # /r2:init (Workspace onboarding & rules setup)
│       ├── r2-code/                # /r2:code (Engineering orchestrator)
│       ├── r2-debug/               # /r2:debug (Systematic triage & causal tracing)
│       ├── r2-bug/                 # /r2:bug (Bug diagnosis & causal triage)
│       ├── r2-plan/                # /r2:plan (Socratic requirements lock & planning)
│       ├── r2-web/                 # /r2:web (Anti-slop creative frontend design)
│       ├── r2-motion/              # /r2:motion (120fps motion & spring physics)
│       └── r2-3d/                  # /r2:3d (Parametric CadQuery & 3D printing DfM)
├── .r2/                            # Project-Specific Configuration (GIT-TRACKED)
│   ├── config.json                 # Installation metadata & version tracking
│   ├── project-profile.json        # Project profile locked via /grill-me
│   ├── rules.md                    # Project-specific architectural invariants & overrides
│   ├── REVIEW.md                   # Continuous bug-prevention rules from /r2:debug
│   └── hardware-profile.json       # Printer bed volume & nozzle constraints for /r2:3d
└── .gitignore                      # Includes .agents/skills/ (MUST NOT include .r2/)
```

### The Command Orchestrators

| Command | Physical Path | Primary Role | Reference Injections |
| :--- | :--- | :--- | :--- |
| `/r2` | `.agents/skills/r2/SKILL.md` | Pure informational discovery hub & routing table | *None* |
| `/r2:init` | `.agents/skills/r2-init/SKILL.md` | Workspace onboarding, environment scaffolding, requirement lock | *None* (Deterministic) |
| `/r2:code` | `.agents/skills/r2-code/SKILL.md` | Full-stack engineering, Graphify navigation, Ponytail simplicity | Opus 5.5 only |
| `/r2:motion` | `.agents/skills/r2-motion/SKILL.md` | 120fps motion design, spring physics, video pipelines | Fable 5.2 only, Claude Design |
| `/r2:web` | `.agents/skills/r2-web/SKILL.md` | Anti-slop creative web design, Awwwards bar, Playwright/axe QA | Fable 5.2 only |
| `/r2:debug` | `.agents/skills/r2-debug/SKILL.md` | Triage, root-cause path tracing, conditional domain routing | Opus 5.5 only |
| `/r2:bug` | `.agents/skills/r2-bug/SKILL.md` | Systematic bug diagnosis, root cause isolation, regression prevention | Opus 5.5 only |
| `/r2:plan` | `.agents/skills/r2-plan/SKILL.md` | Socratic requirements lock, milestone planning, TDD blueprints | Opus 5.5 only |
| `/r2:3d` | `.agents/skills/r2-3d/SKILL.md` | Parametric CadQuery solid modeling, Slant 3D DfM, 3D printing verification | Opus 5.5 only |

---

## 🛑 Orchestration Guardrails

1. **Always-On Proof-of-Read Gate (`.agents/rules/r2-skill-gate.md`):**
   Before reading workspace code or editing any file on any `/r2:*` command, the agent must inspect `.agents/skills/r2/skills/` and `skills.json`, call `view_file` / `read_file` on every matching specialist `SKILL.md` (paginating past line 800 if truncated), and emit a `SKILLS LOADED` receipt quoting one verbatim rule from each loaded file.
2. **1:1 Scoped Reasoning Injection (< 700 Lines):**
   Each orchestrator loads only its matching reference prompt: `/r2:web` and `/r2:motion` load `claude-fable-5.2.md`; `/r2:code`, `/r2:debug`, `/r2:bug`, `/r2:plan`, and `/r2:3d` load `claude-opus-5.5.md`. `/r2` and `/r2:init` load neither.
3. **3-Round Maximum Review Cap:**
   All execution pipelines (`/r2:code`, `/r2:web`, `/r2:motion`, `/r2:3d`) cap the iteration loop between Builder and Critique/Reviewer at **3 rounds**. If unresolved trade-offs remain after Round 3, execution halts and reports directly to the user.
4. **Continuous Rule Memory (`.r2/REVIEW.md`):**
   Whenever `/r2:debug` or `/r2:bug` diagnoses and resolves a defect, it appends a concise 1-line rule to `.r2/REVIEW.md`. Future runs check `.r2/REVIEW.md` at startup to prevent regressions.
5. **Native UI Task Tracking (`update_steps`, Zero `TASKS.md`):**
   Multi-step task progress runs directly in Antigravity's native UI checklist tool (`update_steps`). Agents must never write task state to `TASKS.md`, `tasks.md`, or markdown checkpoint files on disk.
6. **Strict `.r2/` Project State Isolation:**
   Project-specific rules, hardware configurations, and requirement locks reside strictly inside `.r2/` (`.r2/project-profile.json`, `.r2/rules.md`, `.r2/hardware-profile.json`). Specialists are never duplicated into global `specialists/`.

---

## 🔒 Authentication & Private Repository Protection

`Reyansh-Niranjan/r2` is a **strictly private** repository. The installer operates under a **fail-closed** policy:

1. **Prerequisites Verification:** Ensures `git` and `gh` (GitHub CLI) are installed and accessible in `$env:PATH`.
2. **Session Verification:** Executes `gh auth status` to confirm active authentication.
3. **Identity Verification:** Retrieves authenticated user via `gh api user -q .login` and strictly enforces an exact match with `Reyansh-Niranjan`.
4. **Access Verification:** Validates that the authenticated session possesses read permissions for `Reyansh-Niranjan/r2`.

If any check fails, the installer aborts immediately without modifying any files or downloading content.

---

## 🚀 Two-Phase Installation Lifecycle

### Phase 1: Initial Windows Installer (`install.ps1`)
- Authenticates access to the private repository (or runs locally via `-Local`).
- Safely updates the project's `.gitignore` to ignore `.agents/skills/`, `TASKS.md`, and `tasks.md`, while keeping `.r2/` Git-tracked.
- Deploys all 9 command skills, `.agents/rules/r2-skill-gate.md`, `.agents/skills/r2/VERSION`, engine runtime assets, and all 45 specialists into `.agents/skills/r2/skills/` by default without manual cache steps (pass `-OnDemand` for cache-only setup).
- Preserves any `skills.sh`-installed specialists and `.r2/` project state across installs and updates.
- Creates or updates `.r2/config.json`.

### Phase 2: First-Time Project Setup (`/r2:init`)
- Invoked inside Google Antigravity or Gemini chat.
- Inspects project dependencies (`package.json`, `tsconfig.json`, `pyproject.toml`, CAD files, etc.) and reads the live R2 version from `.agents/skills/r2/VERSION` (or `.r2/config.json`).
- Verifies `.agents/skills/r2/skills/` and `.agents/rules/r2-skill-gate.md` are present and active.
- Offers on-demand `skills.sh` discovery (`find` / `add`) for any missing domain specialists.
- Initializes ECC rules: downloads `common/` and detected technology packs from upstream `affaan-m/ECC` at pinned commit `d2ef2680594f9a17526a6e1a2e18b3d242c5d17b`, verified via SHA-256 against `manifest.json`.
- Runs Socratic requirements alignment via `/grill-me` (caching answers in `.r2/project-profile.json`).

---

## 🌐 `skills.sh` Ecosystem Integration

R2 integrates directly with [skills.sh](https://www.skills.sh/) (`vercel-labs/skills`) through `specialist-manager.py`, routing external packages into `.agents/skills/r2/skills/<skill-name>/` while keeping root `.agents/skills/` limited to the 9 R2 commands:

```powershell
# Search skills.sh (supports --owner <org>)
python .agents/skills/r2/scripts/specialist-manager.py find "react"

# Install verbatim from <owner/repo> or <owner/repo>/<skill>
python .agents/skills/r2/scripts/specialist-manager.py add vercel-labs/agent-skills
python .agents/skills/r2/scripts/specialist-manager.py add vercel-labs/skills/find-skills --domain plan

# Update skills.sh packages and re-sync skills.json + r2/SKILL.md
python .agents/skills/r2/scripts/specialist-manager.py update
```

Every `add` and `update` copies the package verbatim (never rewritten from memory), registers metadata in `skills.json` (`source: "skills.sh"`), syncs the Specialist Skill Registry table in `r2/SKILL.md`, and blocks excluded packages (`SkillSpector`, `OmniRoute`, `Agent Vault`, `claude-auto-handoff`, `Gemini Flash TTS`, `reanimate`, `unslop`, `hallmark`, `scrapling`, `strix`, `stitch-skills`).

---

## 📐 ECC Rules Provider (Rules-Only, Immutable, On-Demand)

- **Source:** Upstream `https://github.com/affaan-m/ECC` (`rules/` directory ONLY).
- **Zero Extraneous Components:** Never installs ECC agents, skills, workflows, or scripts.
- **Byte-for-Byte Immutability:** Rules are never reformatted, renamed, edited, or committed.
- **Strict Precedence Hierarchy:**
  1. System & Developer Instructions
  2. User Instructions
  3. Existing R2 Safety & Architectural Constraints
  4. Project-Specific Instructions & Configuration (`AGENTS.md`, `package.json`, `.r2/rules.md`, `.r2/REVIEW.md`)
  5. Applicable ECC Rules (`.agents/skills/r2/rules/ecc/`)
  6. Individual Specialist Guidance
- **On-Demand Acquisition:** Orchestrators dynamically fetch rules for newly encountered stacks:
  ```powershell
  python .agents/skills/r2/rules/loader.py get-rules <tech1> <tech2>
  ```

---

## 🔄 Updates & Maintenance

### Check & Apply Updates
To update R2 from GitHub while preserving `.r2/` project state and `skills.sh` packages:
```powershell
& ([scriptblock]::Create((gh api -H "Accept: application/vnd.github.raw+json" repos/Reyansh-Niranjan/r2/contents/update.ps1)))
```

Or update directly from a local canonical clone (`D:\R2`):
```powershell
D:\R2\update.ps1 -Local -Force
```

### Safe Uninstallation
To remove R2 commands while preserving project `.r2/` configuration:
```powershell
powershell -File .agents/skills/r2/uninstall.ps1
```
Or to purge everything including `.r2/`:
```powershell
powershell -File .agents/skills/r2/uninstall.ps1 -PurgeState
```

---

## 📚 Documentation Index

- [Architecture Reference](docs/ARCHITECTURE.md)
- [Authentication & Access Control](docs/AUTHENTICATION.md)
- [ECC Rules Integration](docs/ECC_RULES.md)
- [Troubleshooting & Recovery](docs/TROUBLESHOOTING.md)
