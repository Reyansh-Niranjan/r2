# Troubleshooting & Recovery

## 1. Authentication Failure
**Symptom:** `Authentication Failed: GitHub CLI is not authenticated.`
**Resolution:**
```powershell
gh auth login
```
Select GitHub.com, HTTPS, and authenticate with user `Reyansh-Niranjan`.

## 2. Access Denied (Wrong User)
**Symptom:** `Access Denied: Authenticated user '...' does not match authorized repository owner 'Reyansh-Niranjan'.`
**Resolution:**
```powershell
gh auth switch --user Reyansh-Niranjan
```

## 3. Repairing Broken Installation
To re-install R2 cleanly:
```powershell
& ([scriptblock]::Create((gh api -H "Accept: application/vnd.github.raw+json" repos/Reyansh-Niranjan/r2/contents/install.ps1))) -Force
```

## 4. Re-running /r2:init
If project dependencies change (e.g. adding React or Python):
In Antigravity chat, run:
```text
/r2:init
```
It will re-inspect dependencies, install newly needed specialist skills, and fetch matching ECC rule packs.
