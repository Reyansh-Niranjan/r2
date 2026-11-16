#!/usr/bin/env python3
"""
R2 ECC Rules Engine & On-Demand Downloader
Loads, verifies, and on-demand acquires private third-party rules from:
https://github.com/affaan-m/ECC (directory: rules/)
Rules are strictly immutable, private, and Git-ignored.
"""

import sys
import os
import json
import hashlib
import urllib.request
import datetime

RULES_DIR = os.path.dirname(os.path.abspath(__file__))
ECC_DIR = os.path.join(RULES_DIR, "ecc")
MANIFEST_PATH = os.path.join(RULES_DIR, "manifest.json")
DEFAULT_COMMIT_SHA = "d2ef2680594f9a17526a6e1a2e18b3d242c5d17b"
REPO_URL = "https://github.com/affaan-m/ECC"

def load_manifest():
    if os.path.exists(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading manifest: {e}", file=sys.stderr)
    return {
        "manifest_version": "1.0.0",
        "repository": REPO_URL,
        "source_directory": "rules/",
        "source_commit_sha": DEFAULT_COMMIT_SHA,
        "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "installed_packs": [],
        "available_packs": [],
        "total_installed_files": 0,
        "rules": {}
    }

def save_manifest(manifest):
    manifest["last_updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    manifest["total_installed_files"] = len(manifest.get("rules", {}))
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

def fetch_tree(commit_sha):
    tree_url = f"https://api.github.com/repos/affaan-m/ECC/git/trees/{commit_sha}?recursive=1"
    req = urllib.request.Request(tree_url, headers={"User-Agent": "R2-ECC-Rule-Loader"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("tree", [])

def install_pack(pack_name, acquisition_mode="on_demand"):
    manifest = load_manifest()
    commit_sha = manifest.get("source_commit_sha", DEFAULT_COMMIT_SHA)
    
    pack_dir = os.path.join(ECC_DIR, pack_name)
    if pack_name in manifest.get("installed_packs", []) and os.path.exists(pack_dir) and any(os.scandir(pack_dir)):
        print(f"Pack '{pack_name}' is already installed.", file=sys.stderr)
        return True

    print(f"Discovering and installing ECC rule pack '{pack_name}' (commit {commit_sha[:8]})...", file=sys.stderr)
    tree = fetch_tree(commit_sha)
    pack_prefix = f"rules/{pack_name}/"
    matching_blobs = [item for item in tree if item["type"] == "blob" and item["path"].startswith(pack_prefix)]

    if not matching_blobs:
        print(f"Rule pack '{pack_name}' not found in ECC rules/ directory.", file=sys.stderr)
        return False

    os.makedirs(os.path.join(ECC_DIR, pack_name), exist_ok=True)
    installed_files = 0

    for item in matching_blobs:
        remote_path = item["path"]
        rel_path = remote_path[len("rules/"):]
        local_path = os.path.join(ECC_DIR, rel_path.replace("/", os.sep))
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        raw_url = f"https://raw.githubusercontent.com/affaan-m/ECC/{commit_sha}/{remote_path}"
        req = urllib.request.Request(raw_url, headers={"User-Agent": "R2-ECC-Rule-Loader"})
        with urllib.request.urlopen(req) as resp:
            content = resp.read()

        if item.get("size") is not None:
            assert len(content) == item["size"], f"Size mismatch for {remote_path}"

        sha256_hash = hashlib.sha256(content).hexdigest()

        # Write immutable byte-for-byte content
        with open(local_path, "wb") as f:
            f.write(content)

        manifest["rules"][rel_path] = {
            "pack": pack_name,
            "relative_path": rel_path,
            "installed_path": f".agents/skills/r2/rules/ecc/{rel_path}",
            "sha256": sha256_hash,
            "size_bytes": len(content),
            "installed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "acquisition_mode": acquisition_mode
        }
        installed_files += 1

    if pack_name not in manifest["installed_packs"]:
        manifest["installed_packs"].append(pack_name)
        manifest["installed_packs"].sort()

    save_manifest(manifest)
    print(f"Successfully installed pack '{pack_name}' ({installed_files} files verified).", file=sys.stderr)
    return True

def get_rule_files(tech_list):
    manifest = load_manifest()
    # Always include common rules
    needed_packs = set(["common"])
    
    # Map common aliases or tech names to ECC pack names
    alias_map = {
        "ts": "typescript",
        "typescript": "typescript",
        "react": "react",
        "reactjs": "react",
        "py": "python",
        "python": "python",
        "web": "web",
        "css": "web",
        "html": "web",
        "frontend": "web",
        "go": "golang",
        "golang": "golang",
        "rs": "rust",
        "rust": "rust",
        "cs": "csharp",
        "csharp": "csharp",
        "cpp": "cpp",
        "c++": "cpp",
        "java": "java",
        "kt": "kotlin",
        "kotlin": "kotlin",
        "swift": "swift",
        "dart": "dart",
        "flutter": "dart",
        "php": "php",
        "rb": "ruby",
        "ruby": "ruby",
        "vue": "vue",
        "angular": "angular",
        "nuxt": "nuxt"
    }

    for t in tech_list:
        key = t.lower().strip()
        pack = alias_map.get(key, key)
        needed_packs.add(pack)

    files_to_load = []
    for pack in sorted(needed_packs):
        if pack not in manifest.get("installed_packs", []):
            # Attempt on-demand installation
            success = install_pack(pack, acquisition_mode="on_demand")
            if not success:
                print(f"[Warning] Rule pack '{pack}' not available in ECC. Continuing without it.", file=sys.stderr)
                continue
            manifest = load_manifest()

        # Collect files for this pack
        pack_dir = os.path.join(ECC_DIR, pack)
        if os.path.isdir(pack_dir):
            for root, _, files in os.walk(pack_dir):
                for f in sorted(files):
                    if f.endswith(".md"):
                        rel = os.path.relpath(os.path.join(root, f), RULES_DIR)
                        files_to_load.append(f".agents/skills/r2/rules/{rel.replace(os.sep, '/')}")

    return files_to_load

def verify_all():
    manifest = load_manifest()
    rules = manifest.get("rules", {})
    if not rules:
        print("No ECC rules installed in manifest. Use loader.py get-rules <tech> to install.")
        return True
    print(f"Verifying {len(rules)} installed ECC rule files against SHA-256 hashes...")
    mismatches = []
    missing = []
    for rel_path, meta in rules.items():
        local_path = os.path.join(ECC_DIR, rel_path.replace("/", os.sep))
        if not os.path.exists(local_path):
            missing.append(rel_path)
            continue
        with open(local_path, "rb") as f:
            content = f.read()
        sha = hashlib.sha256(content).hexdigest()
        if sha != meta["sha256"]:
            mismatches.append((rel_path, meta["sha256"], sha))

    if missing:
        print(f"MISSING FILES ({len(missing)}): {missing}", file=sys.stderr)
    if mismatches:
        print(f"HASH MISMATCHES ({len(mismatches)}): {mismatches}", file=sys.stderr)
    if not missing and not mismatches:
        print(f"ALL {len(rules)} ECC RULE FILES VERIFIED 100% BYTE-FOR-BYTE IDENTICAL!")
        return True
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: loader.py [list|install <pack>|get-rules <tech...>|verify]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "list":
        manifest = load_manifest()
        print("Installed packs:", manifest.get("installed_packs", []))
        print("Available in ECC:", manifest.get("available_packs", []))
    elif cmd == "install":
        if len(sys.argv) < 3:
            print("Usage: loader.py install <pack_name>")
            sys.exit(1)
        pack_name = sys.argv[2]
        install_pack(pack_name, acquisition_mode="manual")
    elif cmd == "get-rules":
        techs = sys.argv[2:]
        rule_files = get_rule_files(techs)
        for rf in rule_files:
            print(rf)
    elif cmd == "verify":
        success = verify_all()
        sys.exit(0 if success else 1)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
