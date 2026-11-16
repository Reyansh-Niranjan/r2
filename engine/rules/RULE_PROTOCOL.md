# R2 Rule Protocol: ECC Rules-Only On-Demand Provider

This document establishes the binding protocol for the ECC (Everything-Claude-Code) private rules-only provider integrated into the R2 Skill Orchestration System.

---

## 1. Architectural Scope & Boundary

- **Source Repository:** `https://github.com/affaan-m/ECC`
- **Pinned Commit SHA:** `d2ef2680594f9a17526a6e1a2e18b3d242c5d17b`
- **Target Boundary:** `rules/` directory ONLY.
  - NEVER download, clone, or install ECC skills, agents, commands, hooks, scripts, workflows, or configurations.
  - NEVER clone the root ECC repository.
- **Local Storage:** `.agents/skills/r2/rules/ecc/`
  - Kept strictly private and uncommitted via `.agents/skills/r2/rules/.gitignore`.
  - Master manifest maintained at `.agents/skills/r2/rules/manifest.json`.
  - Automation & discovery engine: `.agents/skills/r2/rules/loader.py`.

---

## 2. Absolute Rule Immutability

All rule files residing in `.agents/skills/r2/rules/ecc/` are third-party upstream source material.
- **Zero Modifications:** Files must remain 100% byte-for-byte identical to their ECC source versions.
- **No Refactoring:** Never edit, reformat, rename, translate, or merge rule files.
- **Integrity Validation:** Validated via SHA-256 hashes recorded in `manifest.json`. Integrity can be audited at any time using:
  ```bash
  python .agents/skills/r2/rules/loader.py verify
  ```

---

## 3. Strict Precedence Hierarchy

When resolving conflicts or applying instructions, every R2 command orchestrator and specialist skill MUST adhere to the following strict precedence ranking:

1. **System & Developer Instructions**
   Platform guardrails, system prompts, Antigravity core constraints.
2. **User Instructions**
   Active conversation prompt, explicit user requirements, project-specific overrides.
3. **Existing R2 Safety & Architectural Constraints**
   Command skill separation, hardware safety, anti-slop rules, Windows compatibility, non-mutating audit rules.
4. **Project-Specific Instructions & Configuration**
   Workspace `AGENTS.md`, `package.json`, `tsconfig.json`, existing codebase architecture.
5. **Applicable ECC Rules**
   Read-only coding standards, language conventions, framework best practices, style guides from `.agents/skills/r2/rules/ecc/`.
6. **Individual Specialist Guidance**
   Internal recommendations, heuristics, or prompt text within individual specialist `SKILL.md` files.

*Note:* ECC rules guide quality and idiomatic code formatting/structure, but they NEVER override user prompt directives, R2 safety boundaries, or project architectural standards.

---

## 4. Rule Consumption Matrix

R2 orchestrators and specialists query and load rules based on their domain:

| Orchestrator / Role | Default Rule Packs | Purpose |
|---------------------|--------------------|---------|
| `/r2:init` | Discovery & Verification | Runs tech detection, verifies rule integrity, triggers loader |
| `/r2:code` | `common/`, `typescript/`, `python/` | Code implementation, refactoring, API integration |
| `/r2:web` | `common/`, `typescript/`, `react/`, `web/` | Web frontend, components, DOM/CSS, responsive UI |
| `/r2:motion` | `common/`, `typescript/`, `react/`, `web/` | Motion design, GPU animations, interactive UI |
| `/r2:debug` | `common/` + failing tech stack | Root-cause analysis, defect remediation |
| **All Specialists** | `common/` + domain tech stack | Specialist domain execution adhering to standard conventions |

### Standard Baseline Rules (`common/`):
- `coding-style.md`: Clean, idiomatic syntax and formatting.
- `git.md`: Branching, commit conventions, hygiene.
- `patterns.md`: Idiomatic architectural patterns.
- `performance.md`: Algorithmic efficiency, resource management.
- `security.md`: Secure coding practices, vulnerability avoidance.
- `testing.md`: Unit, integration, and assertion testing standards.
- `documentation.md`: Comments, docstrings, technical documentation.
- `principles.md`: Core software engineering principles.

---

## 5. On-Demand Dynamic Acquisition

For technologies not included in the initial installation (e.g. `golang`, `rust`, `cpp`, `csharp`, `php`, `docker`, `astro`, `vue`, `angular`, `swift`, `kotlin`), R2 dynamically discovers and installs rule packs on demand.

### Commands:

1. **List all available rule packs:**
   ```bash
   python .agents/skills/r2/rules/loader.py list
   ```

2. **Retrieve rule paths for given technologies (auto-downloads if missing):**
   ```bash
   python .agents/skills/r2/rules/loader.py get-rules <tech1> <tech2> ...
   ```
   *Example:*
   ```bash
   python .agents/skills/r2/rules/loader.py get-rules rust docker
   ```

3. **Explicitly install a specific rule pack:**
   ```bash
   python .agents/skills/r2/rules/loader.py install <pack_name>
   ```

4. **Verify SHA-256 hash integrity of all local rules:**
   ```bash
   python .agents/skills/r2/rules/loader.py verify
   ```

Rule acquisition is purely additive: it downloads immutable `.md` files directly from GitHub into `.agents/skills/r2/rules/ecc/<pack>/`, verifies byte lengths and SHA-256 hashes, and records them in `manifest.json`.
