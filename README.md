# R2 Skill Orchestration System

**R2** is a modular, high-performance skill orchestration architecture built for **Google Antigravity** and **Gemini**. It separates meta-orchestration from specialist implementation, coordinating complex software engineering, 120fps GPU motion design, award-winning frontend experiences, systematic causal debugging, and parametric CadQuery 3D printing through a clean command hierarchy.

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

R2 separates responsibilities into **Command Orchestrators**, a **Master Specialist Collection** (45 skills), and a **Private On-Demand Rules Provider (ECC)**.

```text
Target Project/
├── .agents/
│   ├── rules/
│   │   └── r2-skill-gate.md        # Always-on Proof-of-Read Specialist Skill Gate
│   └── skills/
│       ├── r2/                     # /r2 (Informational index & discovery hub)
│       │   ├── SKILL.md
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

1. **3-Round Maximum Review Cap:**
   All execution pipelines (`/r2:code`, `/r2:web`, `/r2:motion`, `/r2:3d`) strictly cap the iteration loop between the Builder and Critique/Reviewer at **3 rounds**. If consensus, passing scores, or resolution cannot be achieved after Round 3, execution halts immediately and documents unresolved trade-offs directly to the user.
2. **Continuous Rule Memory (`.r2/REVIEW.md`):**
   Whenever `/r2:debug` diagnoses and resolves a defect, it appends a concise 1-line rule to `.r2/REVIEW.md`. All future runs of `/r2:code`, `/r2:web`, `/r2:motion`, and `/r2:3d` check `.r2/REVIEW.md` at startup, guaranteeing zero regression.
3. **Strict `.r2/` Project State Isolation:**
   Project-specific rules, hardware configurations, and requirement locks reside strictly inside `.r2/` (`.r2/project-profile.json`, `.r2/rules.md`, `.r2/hardware-profile.json`). Specialists are **never duplicated** into global `specialists/`.

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
- Authenticates access to the private repository.
- Safely updates the project's `.gitignore` to ignore `.agents/skills/`.
- Verifies that `.r2/` is NOT ignored, ensuring configuration is shareable with collaborators.
- Deploys all 9 command skills, `.agents/rules/r2-skill-gate.md`, engine runtime assets, and specialists into `.agents/`.
- Creates `.r2/config.json`.

### Phase 2: First-Time Project Setup (`/r2:init`)
- Invoked inside Google Antigravity or Gemini chat.
- Inspects project dependencies (`package.json`, `tsconfig.json`, `pyproject.toml`, CAD files, etc.).
- Installs the project-relevant specialist skills from the 45-skill catalog into `.agents/skills/r2/skills/`.
- Initializes ECC rules: downloads `common/` and detected technology packs from upstream `affaan-m/ECC` at pinned commit `d2ef2680594f9a17526a6e1a2e18b3d242c5d17b`.
- Verifies all downloaded rules byte-for-byte using SHA-256 hashes against `manifest.json`.
- Runs Socratic requirements alignment via `/grill-me` (caching answers in `.r2/project-profile.json`).

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
To update R2 to the latest release while preserving project `.r2/` state:
```powershell
& ([scriptblock]::Create((gh api -H "Accept: application/vnd.github.raw+json" repos/Reyansh-Niranjan/r2/contents/update.ps1)))
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
