# R2 Architecture Specification

## 1. Directory Structure

```text
.agents/
└── skills/
    ├── r2/                       # Primary index & engine root
    │   ├── SKILL.md              # Informs the agent; never executes specialist work
    │   ├── references/           # Scoped reasoning prompts
    │   │   ├── claude-fable-5.2.md
    │   │   ├── claude-opus-5.5.md
    │   │   └── claude-design/
    │   ├── registry/             # Master catalogs
    │   │   ├── skills.json       # 45 specialist catalog definitions
    │   │   └── dependencies.json # Dependency graph & routing rules
    │   ├── rules/                # ECC rules-only provider
    │   │   ├── RULE_PROTOCOL.md
    │   │   ├── manifest.json
    │   │   ├── loader.py
    │   │   └── ecc/              # Local, Git-ignored rule files
    │   └── skills/               # Specialist skill collection (45 skills)
    ├── r2-init/                  # /r2:init (scaffolding & installation)
    ├── r2-code/                  # /r2:code (engineering orchestrator)
    ├── r2-debug/                 # /r2:debug (triage & diagnostic orchestrator)
    ├── r2-web/                   # /r2:web (frontend anti-slop orchestrator)
    ├── r2-motion/                # /r2:motion (motion & animation orchestrator)
    └── r2-3d/                    # /r2:3d (parametric CadQuery & 3D printing orchestrator)

.r2/                              # Project-Specific Configuration (GIT-TRACKED)
├── config.json                   # Version & installation metadata
├── project-profile.json          # Socratic interview profile locked via /grill-me
├── rules.md                      # Workspace-specific architectural invariants & overrides
├── REVIEW.md                     # Continuous 1-line bug prevention rules captured by /r2:debug
└── hardware-profile.json         # Physical printer bounds, nozzle & filament specs for /r2:3d
```

## 2. Core Architectural Invariants

1. **Separation of Meta-Orchestration from Implementation:**
   None of the seven command skills implement specialist work directly. They parse tasks, load reasoning models, enforce boundaries, resolve dependencies, and delegate bounded subtasks to specialist skills.
2. **Clean Root Directory:**
   The root `.agents/skills/` directory contains strictly the 7 command skill folders (`r2`, `r2-init`, `r2-code`, `r2-debug`, `r2-web`, `r2-motion`, `r2-3d`). All specialist implementations reside inside `.agents/skills/r2/skills/`.
3. **Scoped Reasoning Injection:**
   Reference prompts (`claude-fable-5.2.md` and `claude-opus-5.5.md`) are never loaded by `/r2` or `/r2:init`. They are loaded explicitly at the start of `/r2:code`, `/r2:debug`, `/r2:web`, `/r2:motion`, and `/r2:3d` turns.
4. **Git-Tracked State Separation & Zero Duplication:**
   All project configuration, overrides, and locked requirements reside strictly in `.r2/` (e.g. `.r2/config.json`, `.r2/project-profile.json`, `.r2/rules.md`, `.r2/REVIEW.md`). Project-specific overrides are NEVER duplicated or forked into the global `specialists/` catalog.
5. **3-Round Maximum Review Cap:**
   All execution pipelines (`/r2:code`, `/r2:web`, `/r2:motion`, `/r2:3d`) strictly cap Builder <-> Critique iteration loops at a maximum of 3 rounds. If convergence is not achieved after 3 rounds, execution halts and escalates the remaining trade-offs to the user.
6. **Continuous Bug Prevention (`.r2/REVIEW.md`):**
   Whenever `/r2:debug` resolves an issue, it appends an actionable 1-line rule to `.r2/REVIEW.md`. All future runs of `/r2:code`, `/r2:web`, `/r2:motion`, and `/r2:3d` verify `.r2/REVIEW.md` at startup, guaranteeing zero regression.
