---
name: persona-critique
description: "Zero-dependency adversarial pre-ship stress test capturing MiroFish's multi-persona evaluation without heavy swarms. Evaluates UI, copy, or architecture through 3 distinct lenses (Target End-User, Skeptical Senior Engineer, First-Time/Low-Context User) and outputs only concrete, actionable fixes."
---

# /persona-critique

A lightweight, zero-dependency adversarial pre-ship stress test capturing the essence of MiroFish's multi-persona evaluation without requiring heavy runtime swarms, Zep, or complex daemon processes.

Runs 3 concise, adversarial critique lenses before finalizing any feature, UI, copy, API, or architectural implementation.

---

## The 3 Critique Lenses

Every critique executes all three lenses sequentially against the exact implementation or proposed diff:

### 1. Target End-User Lens
- **Focus:** Value delivery, usability friction, visual hierarchy, copy tone, onboarding flow, and perceived polish.
- **Key Questions:**
  - Does this immediately solve my core problem without making me think?
  - Where is the interaction friction, clunkiness, or unnecessary cognitive load?
  - Does the copy communicate clearly and humanly, or does it sound like synthetic corporate placeholder?
  - Is the primary call to action obvious within 1 second?

### 2. Skeptical Senior Engineer Lens
- **Focus:** Over-engineering, edge cases, security boundaries, error recovery, performance bottlenecks, and technical debt.
- **Key Questions:**
  - Is this solving a real problem with the simplest possible approach (YAGNI / Ponytail check)?
  - What happens when network fails, latency spikes, inputs are invalid, or state desynchronizes?
  - Are there security oversights (untrusted inputs, permission leaks, exposed secrets)?
  - Will this break six months from now when another developer modifies it?

### 3. First-Time / Low-Context User Lens
- **Focus:** Jargon, hidden assumptions, missing empty/loading/error states, and discoverability.
- **Key Questions:**
  - What terms or UI affordances assume prior knowledge I don't have?
  - What does the screen look like when there is no data, zero items, or during the initial load?
  - If something fails, does the user know what happened and how to recover?
  - Are touch targets, keyboard navigation, and responsive constraints respected?

---

## Output Protocol: Actionable Findings Only

The output must NOT produce vague praise or filler. Structure findings as a prioritized scorecard:

```markdown
### 🎯 Target End-User Findings
- **[Severity: High/Med/Low]** <Concrete friction or clarity defect>
  - *Fix:* <Exact prescriptive change>

### 🛠️ Skeptical Senior Engineer Findings
- **[Severity: High/Med/Low]** <Edge case, over-engineering, or failure mode>
  - *Fix:* <Exact prescriptive change>

### 👁️ First-Time / Low-Context User Findings
- **[Severity: High/Med/Low]** <Jargon, hidden assumption, or missing state>
  - *Fix:* <Exact prescriptive change>

### ⚡ Critical Pre-Ship Remediation Plan
1. [ ] <Step 1: Immediate blocker fix>
2. [ ] <Step 2: Polish / refinement fix>
```


---

## 📐 ECC Rule Compliance & Precedence

This specialist skill operates under the **R2 Private Rules Provider** framework. Before generating code or proposing architectural decisions, consult the applicable read-only rules from `.agents/skills/r2/rules/ecc/`:

- **Relevant Rule Packs:** `common/` (testing, security), `web/` (accessibility, performance, responsive), `react/`
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
