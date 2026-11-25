---
name: r2
description: "R2 Skill Orchestration System — Central ecosystem overview, routing table, and discovery hub. Informs the agent of available R2 pipelines (/r2:init, /r2:code, /r2:motion, /r2:web, /r2:debug, /r2:3d) and architectural constraints. Never executes specialist work directly."
---

# /r2 — R2 Skill Orchestration System

Welcome to the **R2 Skill Orchestration System**, a high-performance orchestration architecture designed for Antigravity and Gemini.

R2 separates **meta-orchestration** from **specialist implementation**. The 9 commands coordinate workflows, resolve dependency graphs, and delegate bounded tasks to specialist skills.

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
| `/r2:bug` | `.agents/skills/r2-bug/SKILL.md` | Systematic bug diagnosis, root cause isolation, regression prevention |
| `/r2:plan` | `.agents/skills/r2-plan/SKILL.md` | Socratic requirements lock, milestone planning, TDD blueprints |
| `/r2:3d` | `.agents/skills/r2-3d/SKILL.md` | Parametric CadQuery solid modeling, Slant 3D DfM, 3D printing verification |

---

## Architectural Rules

1. **Orchestration, Not Implementation:** None of the R2 orchestrator `SKILL.md` files execute specialist work themselves. They classify, enforce constraints, resolve dependencies, and delegate to specialist skills.
2. **Clean Root Directory:** ALL specialist skills managed by R2 reside strictly in `.agents/skills/r2/skills/`. NEVER duplicate or install specialist skills into the root `.agents/skills/` folder.
3. **Non-Destructive Discovery:** Never overwrite existing project-native skills in `.agents/skills/`, native `/plan`, or existing `AGENTS.md` rules without explicit user approval.
4. **Scoped Reasoning Injection & Pagination:** Reference prompts (`claude-fable-5.2.md` and `claude-opus-5.5.md`) are located in `.agents/skills/r2/references/`. They are **NEVER** loaded by `/r2` or `/r2:init`. Each orchestrator loads ONLY ONE matching prompt (never both): `/r2:web` and `/r2:motion` load ONLY `claude-fable-5.2.md`; `/r2:code`, `/r2:debug` (`/r2:bug`), `/r2:plan`, and `/r2:3d` load ONLY `claude-opus-5.5.md`. If any `view_file` call stops at line 800, you MUST immediately call `view_file` with `StartLine: 801` before proceeding.
5. **Private Rules Provider (ECC):** Coding rules are sourced exclusively from `affaan-m/ECC/rules/`, stored privately in `.agents/skills/r2/rules/ecc/` (Git-ignored), and governed by [.agents/skills/r2/rules/RULE_PROTOCOL.md](.agents/skills/r2/rules/RULE_PROTOCOL.md). Rule files are byte-for-byte immutable and adhere strictly to the 6-tier precedence hierarchy (System > User > R2 Safety > Project > ECC Rules > Specialist).
6. **Strict 3-Round Review Cap & Continuous Rule Memory:** All execution orchestrators (`/r2:code`, `/r2:web`, `/r2:motion`, `/r2:3d`) cap Builder <-> Critique review iterations at a maximum of 3 rounds. Bugs diagnosed by `/r2:debug` append a 1-line rule to `.r2/REVIEW.md`, which all future runs enforce automatically.
7. **Native Task Tracking (Zero Markdown File Workarounds):** Multi-step task progress MUST be tracked directly in the conversation UI using Antigravity's native TODO / Task List tool (`update_steps`). Agents MUST NEVER create, read, or write to `TASKS.md`, `tasks.md`, or any markdown checkpoint files on disk.
8. **Mandatory Proof-of-Read Gate (`.agents/rules/r2-skill-gate.md`):** Before reading workspace code or editing any file on any `/r2:*` command, agents MUST read EVERY domain-matching specialist `SKILL.md` inside `.agents/skills/r2/skills/` (paginating past line 800 if needed) and emit a `SKILLS LOADED` receipt quoting one verbatim rule from each file. No receipt = no edits allowed.

---

## Specialist Skill Registry

Antigravity auto-indexes one directory level deep (`.agents/skills/<name>/SKILL.md`). Specialist skills located inside `.agents/skills/r2/skills/` are skipped unless explicitly listed and read by orchestrators. Every orchestrator enforces a **Step 1 Blocking Gate** requiring tool-trace reads of matching specialist `SKILL.md` files from this registry before reading system prompts or workspace code:

| Domain | Specialist Skill | Relative Path | Primary Purpose |
| :--- | :--- | :--- | :--- |
| **`web`** | `awwwards` | `.agents/skills/r2/skills/awwwards/SKILL.md` | Award-winning website design, WebGL, art direction |
| `web` | `design-taste-frontend` | `.agents/skills/r2/skills/design-taste-frontend/SKILL.md` | Anti-slop frontend taste, typography, layout aesthetics |
| `web` | `emil-design-eng` | `.agents/skills/r2/skills/emil-design-eng/SKILL.md` | Micro-interactions, UI polish, design engineering craft |
| `web` | `humanizer` | `.agents/skills/r2/skills/humanizer/SKILL.md` | Natural copy editing, de-AI writing, punchy voice |
| `web` | `impeccable` | `.agents/skills/r2/skills/impeccable/SKILL.md` | Frontend UI design systems, token architecture, audits |
| `web` | `jury` | `.agents/skills/r2/skills/jury/SKILL.md` | Rigorous Awwwards-style design scoring & UI review |
| `web` | `minimalist-ui` | `.agents/skills/r2/skills/minimalist-ui/SKILL.md` | Monochrome palettes, clean typography, editorial UI |
| `web` | `mobile-native` | `.agents/skills/r2/skills/mobile-native/SKILL.md` | Touch targets, viewport meta, mobile web polish |
| `web` | `refero-design` | `.agents/skills/r2/skills/refero-design/SKILL.md` | Proven real-world SaaS/web UI design patterns |
| `web` | `shieldcn-badges` | `.agents/skills/r2/skills/shieldcn-badges/SKILL.md` | Modern shield badges, headers, and UI status tags |
| `web` | `slopmonster` | `.agents/skills/r2/skills/slopmonster/SKILL.md` | Anti-slop copy auditing, tone refinement, clarity |
| **`motion`** | `animate` | `.agents/skills/r2/skills/animate/SKILL.md` | Ground-up animation building, purpose, and timing |
| `motion` | `animation-vocabulary` | `.agents/skills/r2/skills/animation-vocabulary/SKILL.md` | Reverse-lookup glossary of exact animation terminology |
| `motion` | `apple-design` | `.agents/skills/r2/skills/apple-design/SKILL.md` | Fluid physics, gesture interactions, Apple HIG motion |
| `motion` | `brag-slim` | `.agents/skills/r2/skills/brag-slim/SKILL.md` | Programmatic launch video generation & audio sync |
| `motion` | `find-animation-opportunities` | `.agents/skills/r2/skills/find-animation-opportunities/SKILL.md` | Codebase scanning for high-impact animation candidates |
| `motion` | `motion` | `.agents/skills/r2/skills/motion/SKILL.md` | 120fps GPU acceleration via Motion.dev / Framer Motion |
| `motion` | `review-animations` | `.agents/skills/r2/skills/review-animations/SKILL.md` | Frame-by-frame animation craft review & critique |
| `motion` | `video-analyzer` | `.agents/skills/r2/skills/video-analyzer/SKILL.md` | Video pacing, scene cut analysis, animation timing audits |
| `motion` | `watch` | `.agents/skills/r2/skills/watch/SKILL.md` | Video download, frame extraction, audio envelope analysis |
| **`code`** | `arena` | `.agents/skills/r2/skills/arena/SKILL.md` | Multi-agent competitive single-elimination code optimization |
| `code` | `codebase-design` | `.agents/skills/r2/skills/codebase-design/SKILL.md` | Deep module design, narrow interfaces, high cohesion |
| `code` | `context7` | `.agents/skills/r2/skills/context7/SKILL.md` | Up-to-date documentation & API lookups via Context7 |
| `code` | `domain-modeling` | `.agents/skills/r2/skills/domain-modeling/SKILL.md` | Domain-driven design, entity relationships, ubiquitous language |
| `code` | `improve-codebase-architecture` | `.agents/skills/r2/skills/improve-codebase-architecture/SKILL.md` | Architectural refactoring, seam deepening, visual debt reports |
| `code` | `karpathy-guidelines` | `.agents/skills/r2/skills/karpathy-guidelines/SKILL.md` | Anti-LLM coding mistakes, simplicity-first, surgical changes |
| `code` | `persona-critique` | `.agents/skills/r2/skills/persona-critique/SKILL.md` | Adversarial multi-persona code review and stress testing |
| `code` | `ponytail` | `.agents/skills/r2/skills/ponytail/SKILL.md` | Anti-overengineering, code pruning, simplicity enforcement |
| `code` | `ponytail-audit` | `.agents/skills/r2/skills/ponytail-audit/SKILL.md` | Overengineering detection, speculative code identification |
| `code` | `ponytail-debt` | `.agents/skills/r2/skills/ponytail-debt/SKILL.md` | Technical debt quantification and pruning priorities |
| `code` | `ponytail-gain` | `.agents/skills/r2/skills/ponytail-gain/SKILL.md` | Code simplification scorecards and efficiency gains |
| `code` | `ponytail-help` | `.agents/skills/r2/skills/ponytail-help/SKILL.md` | Ponytail simplicity rules and quick reference guide |
| `code` | `ponytail-review` | `.agents/skills/r2/skills/ponytail-review/SKILL.md` | Code deletion and dead-code pruning review |
| `code` | `research` | `.agents/skills/r2/skills/research/SKILL.md` | Deep technical research and evidence synthesis |
| `code` | `setup-matt-pocock-skills` | `.agents/skills/r2/skills/setup-matt-pocock-skills/SKILL.md` | Issue tracking, triage labeling, and git workflow setup |
| **`3d`** | `3d-print-skill` | `.agents/skills/r2/skills/3d-print-skill/SKILL.md` | Additive manufacturing workflow, slicer prep, DfM checks |
| `3d` | `cad-agent` | `.agents/skills/r2/skills/cad-agent/SKILL.md` | Mechanical verification, automated overhang & tolerance checks |
| `3d` | `cad-skill` | `.agents/skills/r2/skills/cad-skill/SKILL.md` | Parametric 3D printable CAD design and modeling |
| `3d` | `cadquery-modeling` | `.agents/skills/r2/skills/cadquery-modeling/SKILL.md` | Python-based CadQuery / OpenCASCADE solid geometry |
| `3d` | `three-d-printer` | `.agents/skills/r2/skills/three-d-printer/SKILL.md` | Hardware profiles, mechanical tolerances, printer databases |
| **`plan`** | `graphify` | `.agents/skills/r2/skills/graphify/SKILL.md` | Codebase knowledge graphs, structural navigation, call tracing |
| `plan` | `grill-me` | `.agents/skills/r2/skills/grill-me/SKILL.md` | Socratic requirements lock, architectural stress testing |
| `plan` | `superpowers` | `.agents/skills/r2/skills/superpowers/SKILL.md` | Structured milestone planning, TDD workflows, worktrees |
| **`bug`** | `diagnosing-bugs` | `.agents/skills/r2/skills/diagnosing-bugs/SKILL.md` | Systematic diagnosis loop, root cause isolation, repros |
| `bug` | `grim-prompter` | `.agents/skills/r2/skills/grim-prompter/SKILL.md` | Security threat modeling, vulnerability identification |

---

## `skills.sh` Ecosystem Integration (On-Demand Discovery & Installs)

R2 natively integrates the open [skills.sh](https://www.skills.sh/) ecosystem (`vercel-labs/skills`) via `specialist-manager.py`:

- **Search & Discover (`find-skills`):**
  ```powershell
  python .agents/skills/r2/scripts/specialist-manager.py find "<query>" [--owner <owner>]
  ```
- **Install Verbatim (`<owner/repo>` or `<owner/repo>/<skill>`):**
  ```powershell
  python .agents/skills/r2/scripts/specialist-manager.py add <owner/repo> [--domain web|motion|code|3d|plan|bug]
  python .agents/skills/r2/scripts/specialist-manager.py add <owner/repo>/<skill>
  ```
  Packages are fetched via `npx skills add ... -a antigravity -y --copy` inside an isolated staging directory, copied **verbatim** (never rewritten from memory) into `.agents/skills/r2/skills/<skill-name>/SKILL.md`, auto-registered into `skills.json` (`source: "skills.sh"`), and auto-synced into the Specialist Skill Registry table above while keeping root `.agents/skills/` uncluttered.
- **Update Installed `skills.sh` Packages:**
  ```powershell
  python .agents/skills/r2/scripts/specialist-manager.py update [skill-names...]
  ```
- **Strict Exclusion Guard:** Never installs or registers `SkillSpector`, `OmniRoute`, `Agent Vault`, `claude-auto-handoff`, `Gemini Flash TTS`, `reanimate`, `unslop`, `hallmark`, `scrapling`, `strix`, or `stitch-skills`.

---

## Registries & References

- **Always-On Skill Gate Rule:** [.agents/rules/r2-skill-gate.md](.agents/rules/r2-skill-gate.md)
- **Master Catalog:** [.agents/skills/r2/registry/skills.json](.agents/skills/r2/registry/skills.json) (45 specialist skills)
- **Dependency Graph:** [.agents/skills/r2/registry/dependencies.json](.agents/skills/r2/registry/dependencies.json)
- **Specialist Skills Directory:** `.agents/skills/r2/skills/`
- **Rule Provider Protocol:** [.agents/skills/r2/rules/RULE_PROTOCOL.md](.agents/skills/r2/rules/RULE_PROTOCOL.md)
- **Rule Manifest:** [.agents/skills/r2/rules/manifest.json](.agents/skills/r2/rules/manifest.json)
- **On-Demand Rule Engine:** `.agents/skills/r2/rules/loader.py`
