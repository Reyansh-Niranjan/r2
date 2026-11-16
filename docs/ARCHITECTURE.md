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
    │   │   ├── skills.json
    │   │   └── dependencies.json
    │   ├── rules/                # ECC rules-only provider
    │   │   ├── RULE_PROTOCOL.md
    │   │   ├── manifest.json
    │   │   ├── loader.py
    │   │   └── ecc/              # Local, Git-ignored rule files
    │   └── skills/               # Specialist skill collection (59 skills)
    ├── r2-init/                  # /r2:init (scaffolding & installation)
    ├── r2-code/                  # /r2:code (engineering orchestrator)
    ├── r2-debug/                 # /r2:debug (triage & diagnostic orchestrator)
    ├── r2-web/                   # /r2:web (frontend anti-slop orchestrator)
    └── r2-motion/                # /r2:motion (motion & animation orchestrator)
```

## 2. Core Architectural Invariants

1. **Separation of Meta-Orchestration from Implementation:**
   None of the six command skills implement specialist work directly. They parse tasks, load reasoning models, enforce boundaries, resolve dependencies, and delegate bounded subtasks to specialist skills.
2. **Clean Root Directory:**
   The root `.agents/skills/` directory contains strictly the 6 command skill folders (`r2`, `r2-init`, `r2-code`, `r2-debug`, `r2-web`, `r2-motion`). All specialist implementations reside inside `.agents/skills/r2/skills/`.
3. **Scoped Reasoning Injection:**
   Reference prompts (`claude-fable-5.2.md` and `claude-opus-5.5.md`) are never loaded by `/r2` or `/r2:init`. They are loaded explicitly by `/r2:code`, `/r2:debug`, `/r2:web`, and `/r2:motion`.
4. **Git-Tracked State Separation:**
   All project configuration and locked requirements reside in `.r2/` (e.g. `.r2/config.json`, `.r2/project-profile.json`). `.r2/` MUST NOT be added to `.gitignore`.
