# R2 Specialist Manager
# Manages discovery, selection, installation, and skills.sh integration for R2 specialist skills.

import os
import re
import sys
import json
import shutil
import subprocess
import tempfile
import argparse

REPO = "Reyansh-Niranjan/r2"

# Strict R2 exclusion list — NEVER install, register, or route these packages/skills
EXCLUDED_SKILLS = {
    "skillspector",
    "omniroute",
    "agent-vault",
    "claude-auto-handoff",
    "gemini-flash-tts",
    "reanimate",
    "unslop",
    "hallmark",
    "scrapling",
    "strix",
    "stitch-skills",
}

DOMAIN_ORDER = ["web", "motion", "code", "3d", "plan", "bug"]

CATEGORY_TO_DOMAIN = {
    "frontend": "web",
    "design-system": "web",
    "qa": "web",
    "content": "web",
    "motion": "motion",
    "media": "motion",
    "cad": "3d",
    "3d": "3d",
    "debugging": "bug",
    "security": "bug",
    "onboarding": "plan",
    "workflow": "plan",
    "core": "code",
    "architecture": "code",
    "documentation": "code",
    "testing": "code",
    "engineering": "code",
}

KNOWN_SKILL_DOMAINS = {
    "persona-critique": "code",
    "arena": "code",
    "graphify": "plan",
    "grill-me": "plan",
    "superpowers": "plan",
    "diagnosing-bugs": "bug",
    "grim-prompter": "bug",
}


def normalize_token(value):
    return re.sub(r"[\s_]+", "-", value.strip().lower())


def is_excluded(value):
    if not value:
        return False
    norm = normalize_token(value)
    if norm in EXCLUDED_SKILLS:
        return True
    parts = [p for p in re.split(r"[/@:\\]+", norm) if p]
    return any(part in EXCLUDED_SKILLS for part in parts)


def get_npx_executable():
    return shutil.which("npx") or shutil.which("npx.cmd") or "npx"


def get_repo_root():
    cur = os.path.abspath(__file__)
    while True:
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        if os.path.isdir(os.path.join(parent, ".agents")):
            return parent
        if os.path.isdir(os.path.join(parent, "engine", "registry")) and os.path.isdir(os.path.join(parent, "specialists")):
            return parent
        cur = parent
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(script_dir))


def resolve_context(workspace):
    installed_registry = os.path.join(workspace, ".agents", "skills", "r2", "registry", "skills.json")
    source_registry = os.path.join(workspace, "engine", "registry", "skills.json")

    if os.path.exists(installed_registry):
        return {
            "mode": "workspace",
            "registry_file": installed_registry,
            "dest_dir": os.path.join(workspace, ".agents", "skills", "r2", "skills"),
            "cache_dir": os.path.join(workspace, ".agents", "skills", "r2", "specialists_cache"),
            "r2_skill_md": os.path.join(workspace, ".agents", "skills", "r2", "SKILL.md"),
            "lock_file": os.path.join(workspace, ".agents", "skills", "r2", "registry", "skills-sh-lock.json"),
        }
    if os.path.exists(source_registry):
        return {
            "mode": "source",
            "registry_file": source_registry,
            "dest_dir": os.path.join(workspace, "specialists"),
            "cache_dir": os.path.join(workspace, "specialists"),
            "r2_skill_md": os.path.join(workspace, "commands", "r2", "SKILL.md"),
            "lock_file": os.path.join(workspace, "engine", "registry", "skills-sh-lock.json"),
        }
    return {
        "mode": "workspace",
        "registry_file": installed_registry,
        "dest_dir": os.path.join(workspace, ".agents", "skills", "r2", "skills"),
        "cache_dir": os.path.join(workspace, ".agents", "skills", "r2", "specialists_cache"),
        "r2_skill_md": os.path.join(workspace, ".agents", "skills", "r2", "SKILL.md"),
        "lock_file": os.path.join(workspace, ".agents", "skills", "r2", "registry", "skills-sh-lock.json"),
    }


def check_gh_auth():
    try:
        res = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
        if res.returncode != 0:
            return False, "gh is not authenticated. Run 'gh auth login' first."
        user_res = subprocess.run(["gh", "api", "user", "-q", ".login"], capture_output=True, text=True)
        username = user_res.stdout.strip()
        if username != "Reyansh-Niranjan":
            return False, f"Authenticated username '{username}' does not match required owner 'Reyansh-Niranjan'."
        return True, username
    except Exception as e:
        return False, str(e)


def inspect_project_tech(workspace_root):
    techs = set()
    pkg_path = os.path.join(workspace_root, "package.json")
    if os.path.exists(pkg_path):
        techs.add("web")
        techs.add("javascript")
        try:
            with open(pkg_path, "r", encoding="utf-8") as f:
                d = json.load(f)
            deps = {**d.get("dependencies", {}), **d.get("devDependencies", {})}
            if "typescript" in deps or os.path.exists(os.path.join(workspace_root, "tsconfig.json")):
                techs.add("typescript")
            if "react" in deps:
                techs.add("react")
            if "vue" in deps:
                techs.add("vue")
            if "next" in deps:
                techs.add("nextjs")
            if "astro" in deps:
                techs.add("astro")
            if "tailwindcss" in deps:
                techs.add("tailwind")
            if "framer-motion" in deps or "motion" in deps:
                techs.add("motion")
        except Exception:
            pass

    if os.path.exists(os.path.join(workspace_root, "pyproject.toml")) or os.path.exists(os.path.join(workspace_root, "requirements.txt")):
        techs.add("python")
    else:
        for root, dirs, files in os.walk(workspace_root):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
            if any(f.endswith(".py") for f in files):
                techs.add("python")
                break

    if os.path.isdir(os.path.join(workspace_root, "cad")) or os.path.exists(os.path.join(workspace_root, ".r2", "hardware-profile.json")):
        techs.add("cad")
        techs.add("3d")
    for root, dirs, files in os.walk(workspace_root):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
        if any(f.endswith((".step", ".stl", ".3mf", ".scad")) for f in files):
            techs.add("cad")
            techs.add("3d")
            break

    if os.path.exists(os.path.join(workspace_root, "go.mod")):
        techs.add("golang")
    if os.path.exists(os.path.join(workspace_root, "Cargo.toml")):
        techs.add("rust")

    return sorted(list(techs))


def determine_relevant_specialists(techs, reg):
    all_specialists = sorted(list(reg.get("skills", {}).keys()))
    core = {
        "graphify", "ponytail", "ponytail-debt", "ponytail-audit", "ponytail-review",
        "ponytail-gain", "ponytail-help", "karpathy-guidelines", "persona-critique",
        "superpowers", "grill-me", "codebase-design", "domain-modeling",
        "improve-codebase-architecture", "diagnosing-bugs", "context7",
        "humanizer", "slopmonster", "arena", "research", "grim-prompter"
    }
    frontend = {
        "animate", "animation-vocabulary", "apple-design", "awwwards", "brag-slim",
        "design-taste-frontend", "emil-design-eng", "find-animation-opportunities",
        "impeccable", "jury", "minimalist-ui", "mobile-native", "motion",
        "refero-design", "review-animations", "setup-matt-pocock-skills",
        "shieldcn-badges", "video-analyzer", "watch"
    }
    cad = {
        "3d-print-skill", "cad-agent", "cadquery-modeling", "cad-skill", "three-d-printer"
    }

    selected = set(core)
    if any(t in techs for t in ("web", "react", "vue", "nextjs", "astro", "typescript", "tailwind", "motion")):
        selected.update(frontend)
    if any(t in techs for t in ("cad", "3d", "cadquery", "3d-printing")):
        selected.update(cad)

    # Always include non-excluded skills.sh skills already registered in this workspace/catalog
    for name, meta in reg.get("skills", {}).items():
        if meta.get("source") == "skills.sh" and not is_excluded(name):
            selected.add(name)

    return sorted([s for s in all_specialists if s in selected and not is_excluded(s)])


def download_specialists_from_gh(target_specialists, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    temp_dir = tempfile.mkdtemp(prefix="r2_specialists_")
    try:
        print(f"Fetching specialist definitions from {REPO}...")
        clone_cmd = ["gh", "repo", "clone", REPO, temp_dir, "--", "--depth", "1"]
        res = subprocess.run(clone_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Failed to clone {REPO}: {res.stderr}")

        src_specialists = os.path.join(temp_dir, "specialists")
        if not os.path.exists(src_specialists):
            raise RuntimeError(f"Repository {REPO} does not contain specialists/ directory.")

        installed = []
        for s in target_specialists:
            if is_excluded(s):
                print(f"Skipped excluded specialist: {s}")
                continue
            src_s = os.path.join(src_specialists, s)
            dest_s = os.path.join(dest_dir, s)
            if os.path.exists(src_s):
                if os.path.exists(dest_s):
                    shutil.rmtree(dest_s)
                shutil.copytree(src_s, dest_s)
                installed.append(s)
            else:
                print(f"Warning: Specialist '{s}' not found in upstream repository.")
        return installed
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def parse_skill_frontmatter(skill_md_path):
    """Parse YAML frontmatter (name, description) from SKILL.md without modifying the file."""
    with open(skill_md_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    meta = {"name": "", "description": ""}
    match = re.match(r"^---\s*\r?\n(.*?)\r?\n---", content, re.DOTALL)
    if not match:
        return meta

    block = match.group(1)
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^([a-zA-Z0-9_-]+)\s*:\s*(.*)$", line)
        if m:
            key = m.group(1).strip().lower()
            val = m.group(2).strip()
            if val in ("|", ">", "|-", ">-"):
                block_lines = []
                i += 1
                while i < len(lines) and (lines[i].startswith("  ") or lines[i].startswith("\t") or lines[i].strip() == ""):
                    block_lines.append(lines[i].strip())
                    i += 1
                val = " ".join(x for x in block_lines if x)
                if key in meta:
                    meta[key] = val
                continue
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            if key in meta:
                meta[key] = val
        i += 1
    return meta


def infer_category_and_domain(skill_name, description, category_override=None, domain_override=None):
    if domain_override and not category_override:
        domain_to_cat = {
            "web": "frontend",
            "motion": "motion",
            "code": "core",
            "3d": "cad",
            "plan": "workflow",
            "bug": "debugging",
        }
        return domain_to_cat.get(domain_override, "core"), domain_override

    if category_override:
        cat = category_override.strip().lower()
        dom = domain_override or CATEGORY_TO_DOMAIN.get(cat, "code")
        return cat, dom

    text = f"{skill_name} {description}".lower()
    if any(k in text for k in ("cadquery", "3d print", "filament", "nozzle", "overhang", "stl", "step")):
        return "cad", "3d"
    if any(k in text for k in ("animation", "motion", "framer-motion", "gsap", "spring physics", "keyframe", "video")):
        return "motion", "motion"
    if any(k in text for k in ("debug", "bug", "stack trace", "threat model", "vulnerability", "security audit")):
        return "debugging", "bug"
    if any(k in text for k in ("react", "next.js", "nextjs", "tailwind", "css", "frontend", "ui", "ux", "web", "accessibility", "seo", "html")):
        return "frontend", "web"
    if any(k in text for k in ("plan", "milestone", "workflow", "discovery", "find-skills", "skill")):
        return "workflow", "plan"
    return "core", "code"


def parse_skillssh_package(pkg, explicit_skills=None):
    pkg = pkg.strip().rstrip("/")
    skills = list(explicit_skills or [])

    if pkg.startswith(("http://", "https://")):
        repo = pkg
    elif "@" in pkg:
        repo, skill_part = pkg.split("@", 1)
        if skill_part:
            skills.insert(0, skill_part)
    elif pkg.count("/") == 2:
        owner, repo_name, skill_part = pkg.split("/", 2)
        repo = f"{owner}/{repo_name}"
        if skill_part:
            skills.insert(0, skill_part)
    else:
        repo = pkg

    # Deduplicate preserving order
    seen = set()
    deduped = []
    for s in skills:
        if s not in seen:
            seen.add(s)
            deduped.append(s)
    return repo, deduped


def summarize_for_table(description, max_len=95):
    clean = re.sub(r"\s+", " ", (description or "")).strip().replace("|", "/")
    if not clean:
        return "Specialist skill imported via skills.sh"
    if len(clean) <= max_len:
        return clean
    truncated = clean[: max_len - 3].rsplit(" ", 1)[0]
    return f"{truncated}..."


def resolve_skill_domain(name, meta):
    if meta.get("domain") in DOMAIN_ORDER:
        return meta["domain"]
    if name in KNOWN_SKILL_DOMAINS:
        return KNOWN_SKILL_DOMAINS[name]
    cat = (meta.get("category") or "core").lower()
    return CATEGORY_TO_DOMAIN.get(cat, "code")


def sync_r2_skill_md(r2_skill_md_path, reg, dry_run=False):
    if not os.path.exists(r2_skill_md_path):
        return False

    with open(r2_skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    skills = reg.get("skills", {})
    by_domain = {d: [] for d in DOMAIN_ORDER}
    for name in sorted(skills.keys()):
        if is_excluded(name):
            continue
        meta = skills[name]
        dom = resolve_skill_domain(name, meta)
        by_domain.setdefault(dom, []).append((name, meta))

    rows = [
        "| Domain | Specialist Skill | Relative Path | Primary Purpose |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for dom in DOMAIN_ORDER:
        entries = sorted(by_domain.get(dom, []), key=lambda x: x[0])
        for idx, (name, meta) in enumerate(entries):
            dom_cell = f"**`{dom}`**" if idx == 0 else f"`{dom}`"
            rel_path = f".agents/skills/r2/skills/{name}/SKILL.md"
            purpose = summarize_for_table(meta.get("description", ""))
            rows.append(f"| {dom_cell} | `{name}` | `{rel_path}` | {purpose} |")

    table_block = "\n".join(rows)
    table_pattern = re.compile(
        r"(\| Domain \| Specialist Skill \| Relative Path \| Primary Purpose \|\r?\n\| :--- \| :--- \| :--- \| :--- \|\r?\n)(?:\|.*\r?\n)+",
        re.MULTILINE,
    )

    if not table_pattern.search(content):
        return False

    updated = table_pattern.sub(table_block + "\n", content, count=1)
    updated = re.sub(
        r"\(\d+ specialist skills\)",
        f"({len(skills)} specialist skills)",
        updated,
    )

    if not dry_run and updated != content:
        with open(r2_skill_md_path, "w", encoding="utf-8") as f:
            f.write(updated)
    return True


def save_registry(registry_file, reg, dry_run=False):
    reg["total_skills"] = len(reg.get("skills", {}))
    reg["description"] = f"Master registry of {reg['total_skills']} specialized skills for R2 Skill Orchestration System"
    if dry_run:
        return
    os.makedirs(os.path.dirname(registry_file), exist_ok=True)
    with open(registry_file, "w", encoding="utf-8") as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)
        f.write("\n")


def load_skillssh_lock(lock_file):
    if os.path.exists(lock_file):
        try:
            with open(lock_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"version": 1, "skills": {}}


def save_skillssh_lock(lock_file, lock_data, dry_run=False):
    if dry_run:
        return
    os.makedirs(os.path.dirname(lock_file), exist_ok=True)
    with open(lock_file, "w", encoding="utf-8") as f:
        json.dump(lock_data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def run_skillssh_find(args):
    query = " ".join(args.target).strip() if args.target else ""
    npx_bin = get_npx_executable()
    cmd = [npx_bin, "--yes", "skills", "find"]
    if query:
        cmd.append(query)
    if args.owner:
        cmd.extend(["--owner", args.owner])

    print(f"Discovering skills via skills.sh (vercel-labs/skills): {' '.join(cmd)}")
    if args.dry_run:
        print("[DRY-RUN] Command not executed.")
        return 0

    if not query and not sys.stdin.isatty():
        print("Tip: Pass a search query in non-interactive shells, e.g.: specialist-manager.py find react")
        return 0

    res = subprocess.run(cmd, capture_output=True, text=True)
    output = (res.stdout or "") + ("\n" + res.stderr if res.stderr else "")
    if res.returncode != 0:
        print(output, file=sys.stderr)
        return res.returncode

    filtered_lines = []
    skip_next_url = False
    for line in output.splitlines():
        stripped = line.strip()
        if skip_next_url and stripped.startswith(("└", "http")):
            skip_next_url = False
            continue
        skip_next_url = False
        first_tok = stripped.split()[0] if stripped else ""
        if first_tok and ("/" in first_tok or "@" in first_tok) and is_excluded(first_tok):
            skip_next_url = True
            continue
        filtered_lines.append(line)

    print("\n".join(filtered_lines).strip())
    return 0


def install_via_skillssh(repo, skill_filters, ctx, reg, category=None, domain=None, dry_run=False):
    if is_excluded(repo):
        print(f"[BLOCKED] '{repo}' matches R2's exclusion list and cannot be installed.", file=sys.stderr)
        return []
    for sf in skill_filters:
        if is_excluded(sf):
            print(f"[BLOCKED] Skill '{sf}' matches R2's exclusion list and cannot be installed.", file=sys.stderr)
            return []

    npx_bin = get_npx_executable()
    cmd = [npx_bin, "--yes", "skills", "add", repo]
    if skill_filters:
        cmd.append("--skill")
        cmd.extend(skill_filters)
    cmd.extend(["-a", "antigravity", "-y", "--copy"])

    if dry_run:
        print(f"[DRY-RUN] Would run in isolated temp staging dir: {' '.join(cmd)}")
        print(f"[DRY-RUN] Would copy installed skills verbatim into: {ctx['dest_dir']}/<skill-name>/")
        print(f"[DRY-RUN] Would auto-register into: {ctx['registry_file']}")
        print(f"[DRY-RUN] Would auto-sync registry table in: {ctx['r2_skill_md']}")
        return []

    temp_cwd = tempfile.mkdtemp(prefix="r2_skillssh_")
    try:
        print(f"Fetching from skills.sh: {' '.join(cmd)}")
        res = subprocess.run(cmd, cwd=temp_cwd, capture_output=True, text=True)
        if res.returncode != 0:
            err_msg = (res.stderr or res.stdout or "").strip()
            raise RuntimeError(f"skills CLI failed for '{repo}': {err_msg}")

        staged_skills_dir = os.path.join(temp_cwd, ".agents", "skills")
        if not os.path.isdir(staged_skills_dir):
            raise RuntimeError(f"No skills installed by skills CLI for '{repo}'. Verify package/skill name.")

        staged_lock_path = os.path.join(temp_cwd, "skills-lock.json")
        staged_lock = {}
        if os.path.exists(staged_lock_path):
            try:
                with open(staged_lock_path, "r", encoding="utf-8") as lf:
                    staged_lock = json.load(lf).get("skills", {})
            except Exception:
                staged_lock = {}

        os.makedirs(ctx["dest_dir"], exist_ok=True)
        lock_data = load_skillssh_lock(ctx["lock_file"])
        installed = []

        for entry in sorted(os.listdir(staged_skills_dir)):
            src_skill_dir = os.path.join(staged_skills_dir, entry)
            if not os.path.isdir(src_skill_dir):
                continue

            skill_md = os.path.join(src_skill_dir, "SKILL.md")
            if not os.path.exists(skill_md):
                print(f"Skipping '{entry}': missing SKILL.md.")
                continue

            fm = parse_skill_frontmatter(skill_md)
            if is_excluded(entry) or is_excluded(fm.get("name", "")):
                print(f"[BLOCKED] Excluded skill '{entry}' skipped.")
                continue

            dest_skill_dir = os.path.join(ctx["dest_dir"], entry)
            if os.path.exists(dest_skill_dir):
                shutil.rmtree(dest_skill_dir)
            shutil.copytree(src_skill_dir, dest_skill_dir)

            # Mirror into specialists_cache when operating inside a target workspace
            if ctx["mode"] == "workspace" and os.path.isdir(ctx["cache_dir"]):
                cache_skill_dir = os.path.join(ctx["cache_dir"], entry)
                if os.path.exists(cache_skill_dir):
                    shutil.rmtree(cache_skill_dir)
                shutil.copytree(src_skill_dir, cache_skill_dir)

            cat, dom = infer_category_and_domain(entry, fm.get("description", ""), category, domain)
            existing = reg.get("skills", {}).get(entry, {})
            if category is None and existing.get("category"):
                cat = existing["category"]
            if domain is None and existing.get("domain"):
                dom = existing["domain"]

            reg.setdefault("skills", {})[entry] = {
                "source": "skills.sh",
                "repo": repo,
                "version": existing.get("version", "1.0.0"),
                "category": cat,
                "domain": dom,
                "security_status": "skills_sh_installed",
                "risk_score": 0,
                "risk_severity": "LOW",
                "findings_count": 0,
                "description": fm.get("description") or existing.get("description") or f"Specialist skill '{entry}' from {repo}",
                "path": f".agents/skills/r2/skills/{entry}",
            }

            if entry in staged_lock:
                lock_data.setdefault("skills", {})[entry] = staged_lock[entry]
            else:
                lock_data.setdefault("skills", {})[entry] = {
                    "source": repo,
                    "sourceType": "github",
                }
            installed.append(entry)
            print(f"  [OK] Installed '{entry}' verbatim from {repo} -> {dest_skill_dir} (domain: {dom})")

        if installed:
            save_registry(ctx["registry_file"], reg, dry_run=dry_run)
            save_skillssh_lock(ctx["lock_file"], lock_data, dry_run=dry_run)
            sync_r2_skill_md(ctx["r2_skill_md"], reg, dry_run=dry_run)

        return installed
    finally:
        shutil.rmtree(temp_cwd, ignore_errors=True)


def run_skillssh_add(args, ctx, reg):
    if not args.target:
        print("Error: 'add' requires a package (<owner/repo> or <owner/repo>/<skill>).", file=sys.stderr)
        return 1

    installed_all = []
    for pkg in args.target:
        repo, skill_filters = parse_skillssh_package(pkg, args.skill)
        installed = install_via_skillssh(
            repo=repo,
            skill_filters=skill_filters,
            ctx=ctx,
            reg=reg,
            category=args.category,
            domain=args.domain,
            dry_run=args.dry_run,
        )
        installed_all.extend(installed)

    if not args.dry_run:
        if installed_all:
            print(f"Registered {len(installed_all)} skills.sh specialist(s) in {ctx['registry_file']} and synced {ctx['r2_skill_md']}.")
        else:
            print("No skills were installed.")
    return 0


def run_skillssh_update(args, ctx, reg):
    skills_map = reg.get("skills", {})
    targets = set(args.target or [])
    skillssh_entries = {
        name: meta
        for name, meta in skills_map.items()
        if meta.get("source") == "skills.sh" and (not targets or name in targets)
    }

    if not skillssh_entries:
        msg = "No skills.sh-managed specialists registered yet."
        if targets:
            msg = f"No skills.sh-managed specialists matched: {', '.join(sorted(targets))}"
        print(msg)
        print("Install skills.sh packages via: specialist-manager.py add <owner/repo>")
        return 0

    by_repo = {}
    for name, meta in skillssh_entries.items():
        repo = meta.get("repo")
        if not repo:
            continue
        by_repo.setdefault(repo, []).append(name)

    npx_bin = get_npx_executable()
    if args.dry_run:
        print(f"[DRY-RUN] Would update {len(skillssh_entries)} skills.sh skill(s) across {len(by_repo)} repo(s) via 'npx skills update' / 'npx skills add':")
        for repo, names in sorted(by_repo.items()):
            print(f"  - {repo}: {', '.join(sorted(names))}")
        return 0

    # Also invoke native `npx skills update -y` inside an isolated staging dir if lockfile exists
    temp_upd = tempfile.mkdtemp(prefix="r2_skillssh_upd_")
    try:
        lock_data = load_skillssh_lock(ctx["lock_file"])
        if lock_data.get("skills"):
            staged_agents = os.path.join(temp_upd, ".agents", "skills")
            os.makedirs(staged_agents, exist_ok=True)
            for name in skillssh_entries:
                existing_dir = os.path.join(ctx["dest_dir"], name)
                if os.path.isdir(existing_dir):
                    shutil.copytree(existing_dir, os.path.join(staged_agents, name))
            with open(os.path.join(temp_upd, "skills-lock.json"), "w", encoding="utf-8") as lf:
                json.dump(lock_data, lf, indent=2)
            subprocess.run([npx_bin, "--yes", "skills", "update", "-y"], cwd=temp_upd, capture_output=True, text=True)
    finally:
        shutil.rmtree(temp_upd, ignore_errors=True)

    updated = []
    for repo, names in sorted(by_repo.items()):
        res = install_via_skillssh(repo=repo, skill_filters=sorted(names), ctx=ctx, reg=reg, dry_run=False)
        updated.extend(res)

    print(f"Updated {len(updated)} skills.sh specialist(s) and synchronized registry/SKILL.md.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="R2 Specialist Skill Manager (with skills.sh integration)")
    parser.add_argument(
        "action",
        choices=["install", "install-all", "list", "verify", "find", "add", "update", "sync"],
        help="Action to perform",
    )
    parser.add_argument("target", nargs="*", help="Package (<owner/repo> or <owner/repo>/<skill>), search query, or skill name(s)")
    parser.add_argument("--tech", nargs="*", help="Override detected technologies")
    parser.add_argument("--skill", "-s", nargs="*", help="Specific skill name(s) inside package")
    parser.add_argument("--owner", help="Filter skills.sh find by GitHub owner")
    parser.add_argument("--category", help="Registry category for added skills.sh skill")
    parser.add_argument("--domain", choices=DOMAIN_ORDER, help="R2 orchestrator domain table mapping")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without modifying files")
    args = parser.parse_args()

    workspace = get_repo_root()
    ctx = resolve_context(workspace)
    registry_file = ctx["registry_file"]
    dest_dir = ctx["dest_dir"]
    cache_dir = ctx["cache_dir"]

    if not os.path.exists(registry_file):
        print(f"Error: Registry file not found at {registry_file}", file=sys.stderr)
        sys.exit(1)

    with open(registry_file, "r", encoding="utf-8") as f:
        reg = json.load(f)

    all_known_specialists = sorted(list(reg.get("skills", {}).keys()))

    if args.action == "list":
        print(f"Total catalog specialists: {len(all_known_specialists)}")
        for s in all_known_specialists:
            installed = os.path.exists(os.path.join(dest_dir, s))
            meta = reg["skills"][s]
            src = meta.get("source", "local")
            cat = meta.get("category", "core")
            print(f"  [{'INSTALLED' if installed else 'AVAILABLE'}] {s} ({cat}, source={src})")
        return

    if args.action == "verify":
        installed = [
            s for s in os.listdir(dest_dir)
            if os.path.isdir(os.path.join(dest_dir, s)) and os.path.exists(os.path.join(dest_dir, s, "SKILL.md"))
        ] if os.path.exists(dest_dir) else []
        excluded_present = [s for s in installed if is_excluded(s)]
        if excluded_present:
            print(f"Warning: Excluded skills present: {excluded_present}", file=sys.stderr)
            sys.exit(1)
        print(f"Verified {len(installed)} installed specialist skills in {dest_dir}.")
        return

    if args.action == "find":
        sys.exit(run_skillssh_find(args))

    if args.action == "add":
        sys.exit(run_skillssh_add(args, ctx, reg))

    if args.action == "update":
        sys.exit(run_skillssh_update(args, ctx, reg))

    if args.action == "sync":
        if args.dry_run:
            print(f"[DRY-RUN] Would sync {registry_file} -> {ctx['r2_skill_md']}")
            return
        save_registry(registry_file, reg, dry_run=False)
        synced = sync_r2_skill_md(ctx["r2_skill_md"], reg, dry_run=False)
        print(f"Synchronized registry ({len(all_known_specialists)} skills). Table synced={synced}.")
        return

    if args.action == "install-all":
        target_specialists = [s for s in all_known_specialists if not is_excluded(s)]
    else:
        techs = args.tech if args.tech else inspect_project_tech(workspace)
        print(f"Detected project technologies: {techs}")
        target_specialists = determine_relevant_specialists(techs, reg)

    if args.dry_run:
        print(f"[DRY-RUN] Would install {len(target_specialists)} specialist skills into {dest_dir}.")
        return

    print(f"Installing {len(target_specialists)} specialist skills into {dest_dir}...")

    if os.path.exists(cache_dir):
        print("Using local cache...")
        os.makedirs(dest_dir, exist_ok=True)
        installed = []
        for s in target_specialists:
            src_s = os.path.join(cache_dir, s)
            dest_s = os.path.join(dest_dir, s)
            if os.path.exists(src_s):
                if os.path.exists(dest_s) and os.path.abspath(src_s) != os.path.abspath(dest_s):
                    shutil.rmtree(dest_s)
                if os.path.abspath(src_s) != os.path.abspath(dest_s):
                    shutil.copytree(src_s, dest_s)
                installed.append(s)
            elif os.path.exists(dest_s):
                # Already present (e.g., skills.sh installed directly to dest_dir)
                installed.append(s)
    else:
        auth_ok, auth_msg = check_gh_auth()
        if not auth_ok:
            print(f"Error: Authentication failed: {auth_msg}", file=sys.stderr)
            sys.exit(1)
        installed = download_specialists_from_gh(target_specialists, dest_dir)

    print(f"Successfully installed {len(installed)} specialist skills.")


if __name__ == "__main__":
    main()
