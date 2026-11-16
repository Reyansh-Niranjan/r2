# ECC Rules Integration (Private Rules-Only Provider)

R2 incorporates programming rules from `https://github.com/affaan-m/ECC` (`rules/` directory).

## Core Principles
1. **Rules Only:** No ECC skills, agents, commands, hooks, scripts, or workflows.
2. **Byte-for-Byte Immutability:** Rule files remain unmodified upstream source material.
3. **Local & Git-Ignored:** Stored in `.agents/skills/r2/rules/ecc/` and excluded by `.agents/skills/r2/rules/.gitignore`.
4. **Precedence Hierarchy:**
   1. System & Developer Instructions
   2. User Instructions
   3. Existing R2 Safety & Architectural Constraints
   4. Project-Specific Instructions & Configuration
   5. Applicable ECC Rules
   6. Individual Specialist Guidance

## Usage via CLI
```bash
# List available upstream packs
python .agents/skills/r2/rules/loader.py list

# Get paths for detected technologies (downloads on-demand if missing)
python .agents/skills/r2/rules/loader.py get-rules react typescript

# Verify SHA-256 integrity
python .agents/skills/r2/rules/loader.py verify
```
