# R2 Mandatory Specialist Skill Proof-of-Read Gate

**ALWAYS-ON WORKSPACE RULE FOR ALL `/r2:*` ORCHESTRATOR INVOCATIONS**

Soft instructions inside `SKILL.md` files are frequently bypassed under context pressure. This workspace rule enforces a hard **Proof-of-Read Gate** before any workspace inspection or file modification on `/r2:code`, `/r2:web`, `/r2:motion`, `/r2:3d`, `/r2:debug`, `/r2:bug`, `/r2:plan`, and `/r2:init`.

---

## 1. Hard Blocking Gate (Before Code Reads or Edits)

Whenever ANY `/r2:*` command or R2 workflow is triggered, you MUST complete these exact steps **BEFORE** reading workspace source code, modifying any file, or running implementation commands:

1. **Discover Installed Specialists:**
   - Check `.agents/skills/r2/skills/` (directory listing) AND `.agents/skills/r2/registry/skills.json` (or `engine/registry/skills.json` when working inside the canonical R2 repo).
   - Consult the **Specialist Skill Registry** in `.agents/skills/r2/SKILL.md` to map the active command/domain (`web`, `motion`, `code`, `3d`, `plan`, `bug`) to all relevant installed skills (including any dynamically added `skills.sh` specialists).

2. **Full Tool-Trace Reads (`view_file` / `read_file`):**
   - Call `view_file` / `read_file` on **EVERY** domain-matching downloaded specialist `SKILL.md` inside `.agents/skills/r2/skills/<skill-name>/SKILL.md`.
   - **Mandatory Pagination Rule:** If any `SKILL.md` or reference file read is capped at line 800, you MUST immediately call `view_file` / `read_file` with `StartLine: 801` (continuing until EOF) before proceeding.
   - **Zero Recall Policy:** Never assume, paraphrase, or reconstruct a specialist skill's rules from memory. Every applied rule must originate from a `view_file` / `read_file` call in the current session trace.

3. **Load Scoped Reasoning Prompt (Single Prompt Only):**
   - Only AFTER reading the domain specialist `SKILL.md` files, load the single matching prompt in `.agents/skills/r2/references/` (never both):
     - `/r2:web` and `/r2:motion` -> `claude-fable-5.2.md` ONLY
     - `/r2:code`, `/r2:debug`, `/r2:bug`, `/r2:plan`, and `/r2:3d` -> `claude-opus-5.5.md` ONLY
     - `/r2` and `/r2:init` -> NO reference prompt

---

## 2. Mandatory `SKILLS LOADED` Proof-of-Read Receipt

Before making your first code read, file write, or file edit on a `/r2:*` task, you **MUST** emit a `SKILLS LOADED` receipt listing every loaded specialist `SKILL.md` path paired with **one verbatim rule quoted directly from that file**:

```text
SKILLS LOADED:
- .agents/skills/r2/skills/<skill-1>/SKILL.md :: "<exact verbatim quote from file>"
- .agents/skills/r2/skills/<skill-2>/SKILL.md :: "<exact verbatim quote from file>"
```

### Enforcement Invariant
- **No `SKILLS LOADED` receipt = NO workspace file edits allowed.**
- Quotes MUST be exact substrings observed in the `view_file` / `read_file` output during this session.
- If a domain specialist needed for the task is missing from `.agents/skills/r2/skills/`, offer to discover/install it cleanly via `skills.sh` using:
  - `python .agents/skills/r2/scripts/specialist-manager.py find "<query>"`
  - `python .agents/skills/r2/scripts/specialist-manager.py add <owner/repo>`
