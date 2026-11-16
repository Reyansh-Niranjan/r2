# Authentication & Access Control

R2 is distributed via the private GitHub repository `Reyansh-Niranjan/r2`.

## Prerequisites
1. **Git for Windows:** Installed and available in PATH.
2. **GitHub CLI (`gh`):** Installed and authenticated.

## Authentication Verification Steps
Before any file is created, downloaded, or modified, `install.ps1` executes:

1. `gh auth status` -> Verifies active token and connectivity.
2. `gh api user -q .login` -> Confirms authenticated user equals `Reyansh-Niranjan`.
3. `gh repo view Reyansh-Niranjan/r2` -> Confirms read access to the private repository.

## Fail-Closed Behavior
If any check fails:
- Execution terminates with exit code 1.
- No files are created or modified.
- No unauthenticated or public fallbacks are attempted.
