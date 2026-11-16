---
name: r2
description: "R2 Skill Orchestration System — Central ecosystem overview, routing table, and discovery hub. Informs the agent of available R2 pipelines (/r2:init, /r2:code, /r2:motion, /r2:web, /r2:debug) and architectural constraints. Never executes specialist work directly."
---

# /r2 — R2 Skill Orchestration System

Welcome to the **R2 Skill Orchestration System**, a high-performance orchestration architecture designed for Antigravity and Gemini.

R2 separates **meta-orchestration** from **specialist implementation**. The 6 orchestrators coordinate workflows, resolve dependency graphs, and delegate bounded tasks to specialist skills.

---

## Orchestrator Directory & Command Mapping

On Windows 11 NTFS, directories are safely isolated using hyphens while YAML commands preserve exact colon syntax:

| Command | Physical Path | Primary Role |
| :--- | :--- | :--- |
| `/r2` | `.agents/skills/r2/SKILL.md` | Pure informational discovery hub & routing table |
| `/r2:init` | `.agents/skills/r2-init/SKILL.md` | Workspace onboarding, environment scaffolding, requirement lock |
| `/r2:code` | `.agents/skills/r2-code/SKILL.md` | Full-stack engineering, Graphify navigation, Ponytail simplicity |
| `/r2:motion` | `.agents/skills/r2-motion/SKILL.md` | 120fps motion design, spring physics, video pipelines |
| `/r2:web` | `.agents/skills/r2-web/SKILL.md` | Anti-slop creative web design, Awwwards bar, Playwright/axe QA |
| `/r2:debug` | `.agents/skills/r2-debug/SKILL.md` | Triage, root-cause path tracing, conditional domain routing |

---

## Architectural Rules

1. **Orchestration, Not Implementation:** None of the 6 R2 orchestrator `SKILL.md` files execute specialist work themselves. They classify, enforce constraints, resolve dependencies, and delegate to specialist skills.
2. **Clean Root Directory:** ALL specialist skills managed by R2 reside strictly in `.agents/skills/r2/skills/`. NEVER duplicate or install specialist skills into the root `.agents/skills/` folder.
3. **Non-Destructive Discovery:** Never overwrite existing project-native skills in `.agents/skills\`, native `/plan`, or existing `AGENTS.md` rules without explicit user approval.
4. **Scoped Reasoning Injection:** Reference prompts (`claude-fable-5.2.md` and `claude-opus-5.5.md`) are located in `.agents/skills/r2/references/`. They are **NEVER** loaded by `/r2` or `/r2:init`. They MUST be explicitly loaded at the start of every `/r2:code`, `/r2:motion`, `/r2:web`, and `/r2:debug` invocation.
5. **Private Rules Provider (ECC):** Coding rules are sourced exclusively from `affaan-m/ECC/rules/`, stored privately in `.agents/skills/r2/rules/ecc/` (Git-ignored), and governed by [.agents/skills/r2/rules/RULE_PROTOCOL.md](.agents/skills/r2/rules/RULE_PROTOCOL.md). Rule files are byte-for-byte immutable and adhere strictly to the 6-tier precedence hierarchy (System > User > R2 Safety > Project > ECC Rules > Specialist).

---

## Registries & References

- **Master Catalog:** [.agents/skills/r2/registry/skills.json](.agents/skills/r2/registry/skills.json)
- **Dependency Graph:** [.agents/skills/r2/registry/dependencies.json](.agents/skills/r2/registry/dependencies.json)
- **Specialist Skills Directory:** `.agents/skills/r2/skills/`
- **Rule Provider Protocol:** [.agents/skills/r2/rules/RULE_PROTOCOL.md](.agents/skills/r2/rules/RULE_PROTOCOL.md)
- **Rule Manifest:** [.agents/skills/r2/rules/manifest.json](.agents/skills/r2/rules/manifest.json)
- **On-Demand Rule Engine:** `.agents/skills/r2/rules/loader.py`
