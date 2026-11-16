---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

Interview the user relentlessly about every aspect of their plan until you reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.

## How to ask questions

Use the **AskUserQuestion tool** for every question you ask. Never pose questions as plain text in your response — always use the multiple-choice popup so the user can quickly select an answer or type a custom one.

Ask **one question at a time**. Wait for the user's answer before moving to the next question. This keeps the conversation focused and prevents overwhelm.

For each question, provide 2–4 concrete multiple-choice options representing the most likely answers or directions. Think about what the user would realistically choose — generic options like "Yes" / "No" aren't helpful unless the question is genuinely binary. The user always has the "Other" field available to write something custom.

## Flow

1. After receiving an answer, briefly acknowledge the decision (1–2 sentences max), then immediately ask the next question via AskUserQuestion.
2. If a question can be answered by exploring the codebase or files, explore them yourself instead of asking the user.
3. Continue until all branches of the design tree are resolved.
4. When finished, provide a concise summary of all decisions made.


---

## 📐 ECC Rule Compliance & Precedence

This specialist skill operates under the **R2 Private Rules Provider** framework. Before generating code or proposing architectural decisions, consult the applicable read-only rules from `.agents/skills/r2/rules/ecc/`:

- **Relevant Rule Packs:** `common/` (documentation, principles)
- **Rule Precedence Hierarchy:**
  1. System & Developer Instructions
  2. User Instructions
  3. Existing R2 Safety & Architectural Constraints
  4. Project-Specific Instructions & Configuration (`AGENTS.md`, `package.json`, etc.)
  5. Applicable ECC Rules (`.agents/skills/r2/rules/ecc/`)
  6. Individual Specialist Guidance (this skill)
- **Immutability:** Rule files in `.agents/skills/r2/rules/ecc/` are strictly read-only upstream assets. Never edit, reformat, or commit them.
- **On-Demand Rule Acquisition:** For technologies without local rule packs (e.g. `golang`, `rust`, `docker`), discover and install on demand:
  ```powershell
  python .agents/skills/r2/rules/loader.py get-rules <tech>
  ```
- **Rule Protocol Reference:** [.agents/skills/r2/rules/RULE_PROTOCOL.md](.agents/skills/r2/rules/RULE_PROTOCOL.md)
