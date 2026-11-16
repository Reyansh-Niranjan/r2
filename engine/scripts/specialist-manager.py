# R2 Specialist Manager
# Manages discovery, selection, and installation of specialist skills from the private R2 repository.

import os
import sys
import json
import shutil
import subprocess
import tempfile
import argparse

REPO = "Reyansh-Niranjan/r2"

def get_repo_root():
    cur = os.path.abspath(__file__)
    while True:
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        if os.path.isdir(os.path.join(parent, ".agents")):
            return parent
        cur = parent
    cur = os.path.abspath(__file__)
    for _ in range(5):
        cur = os.path.dirname(cur)
    return cur

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
    # Check package.json
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

    # Check python
    if os.path.exists(os.path.join(workspace_root, "pyproject.toml")) or os.path.exists(os.path.join(workspace_root, "requirements.txt")):
        techs.add("python")
    else:
        # Check if python files exist in workspace
        for root, dirs, files in os.walk(workspace_root):
            if any(f.endswith(".py") for f in files):
                techs.add("python")
                break

    # Check go, rust, c++
    if os.path.exists(os.path.join(workspace_root, "go.mod")):
        techs.add("golang")
    if os.path.exists(os.path.join(workspace_root, "Cargo.toml")):
        techs.add("rust")

    return sorted(list(techs))

def determine_relevant_specialists(techs, all_specialists):
    # Core specialists always installed
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

    selected = set(core)
    if "web" in techs or "react" in techs or "vue" in techs or "nextjs" in techs or "typescript" in techs:
        selected.update(frontend)

    # Filter to existing in all_specialists
    valid_selected = [s for s in all_specialists if s in selected or s.replace("novaslate-", "") in selected]
    return sorted(valid_selected)

def download_specialists_from_gh(target_specialists, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    temp_dir = tempfile.mkdtemp(prefix="r2_specialists_")
    try:
        print(f"Fetching specialist definitions from {REPO}...")
        # Clone with depth 1
        clone_cmd = ["gh", "repo", "clone", REPO, temp_dir, "--", "--depth", "1"]
        res = subprocess.run(clone_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Failed to clone {REPO}: {res.stderr}")

        src_specialists = os.path.join(temp_dir, "specialists")
        if not os.path.exists(src_specialists):
            raise RuntimeError(f"Repository {REPO} does not contain specialists/ directory.")

        installed = []
        for s in target_specialists:
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

def main():
    parser = argparse.ArgumentParser(description="R2 Specialist Skill Manager")
    parser.add_argument("action", choices=["install", "install-all", "list", "verify"], help="Action to perform")
    parser.add_argument("--tech", nargs="*", help="Override detected technologies")
    args = parser.parse_args()

    workspace = get_repo_root()
    dest_dir = os.path.join(workspace, ".agents", "skills", "r2", "skills")
    cache_dir = os.path.join(workspace, ".agents", "skills", "r2", "specialists_cache")
    registry_file = os.path.join(workspace, ".agents", "skills", "r2", "registry", "skills.json")

    with open(registry_file, "r", encoding="utf-8") as f:
        reg = json.load(f)
    all_known_specialists = sorted(list(reg.get("skills", {}).keys()))

    if args.action == "list":
        print(f"Total catalog specialists: {len(all_known_specialists)}")
        for s in all_known_specialists:
            installed = os.path.exists(os.path.join(dest_dir, s))
            print(f"  [{'INSTALLED' if installed else 'AVAILABLE'}] {s}")
        return

    if args.action == "verify":
        installed = [s for s in os.listdir(dest_dir) if os.path.isdir(os.path.join(dest_dir, s))] if os.path.exists(dest_dir) else []
        print(f"Verified {len(installed)} installed specialist skills in {dest_dir}.")
        return

    auth_ok, auth_msg = check_gh_auth()
    if not auth_ok:
        print(f"Error: Authentication failed: {auth_msg}", file=sys.stderr)
        sys.exit(1)

    if args.action == "install-all":
        target_specialists = all_known_specialists
    else:
        techs = args.tech if args.tech else inspect_project_tech(workspace)
        print(f"Detected project technologies: {techs}")
        target_specialists = determine_relevant_specialists(techs, all_known_specialists)

    print(f"Installing {len(target_specialists)} specialist skills into {dest_dir}...")
    
    # Check if local cache exists
    if os.path.exists(cache_dir):
        print("Using local cache...")
        os.makedirs(dest_dir, exist_ok=True)
        installed = []
        for s in target_specialists:
            src_s = os.path.join(cache_dir, s)
            dest_s = os.path.join(dest_dir, s)
            if os.path.exists(src_s):
                if os.path.exists(dest_s):
                    shutil.rmtree(dest_s)
                shutil.copytree(src_s, dest_s)
                installed.append(s)
    else:
        installed = download_specialists_from_gh(target_specialists, dest_dir)

    print(f"Successfully installed {len(installed)} specialist skills.")

if __name__ == '__main__':
    main()
