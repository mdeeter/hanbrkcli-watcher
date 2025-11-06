# Executable Files - Ready to Run Guide

## Summary: Will files be executable after cloning?

### ✅ **macOS/Linux Users - YES, Ready to Run**

When a user clones/pulls the repo on macOS or Linux:

- ✅ Git **preserves** the executable permission bit
- ✅ `.sh` files will be executable immediately
- ✅ `.py` files will be executable immediately
- ✅ Can run `./setup_mac.sh` right away

**Current permissions** (already set in repo):

```
-rwxr-xr-x  handbrake_watcher.py
-rwxr-xr-x  setup_mac.sh
-rwxr-xr-x  start_watcher_mac.sh
```

### ✅ **Windows Users - YES, but with notes**

#### Command Prompt (.bat files):

- ✅ **Work immediately** - No setup needed
- ✅ Can run `setup.bat` directly

#### PowerShell (.ps1 files):

- ⚠️ **May need one-time setup** for execution policy
- First-time users might see: "cannot be loaded because running scripts is disabled"
- **Solution** (one-time):
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- After that, can run `.\setup.ps1` normally

## What Git Tracks

Git **tracks and preserves**:

- ✅ Executable permissions on Unix-like systems (macOS, Linux)
- ✅ File contents
- ✅ File names

Git **does NOT track**:

- ❌ Windows file permissions (not applicable)
- ❌ Windows execution policy settings (system-level, not file-level)

## Platform-Specific Summary

### **macOS/Linux:**

```bash
git clone <repo>
cd handbrake
./setup_mac.sh          # ✅ Works immediately
./start_watcher_mac.sh  # ✅ Works immediately
```

### **Windows (Command Prompt):**

```cmd
git clone <repo>
cd handbrake
setup.bat               REM ✅ Works immediately
start_watcher.bat       REM ✅ Works immediately
```

### **Windows (PowerShell):**

```powershell
git clone <repo>
cd handbrake

# May need this first time only:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

.\setup.ps1             # ✅ Works after execution policy set
.\start_watcher.ps1     # ✅ Works after execution policy set
```

## Recommendations

The README now includes:

1. ✅ Instructions for Windows PowerShell execution policy (in Prerequisites)
2. ✅ Troubleshooting section for permission issues
3. ✅ Platform-specific setup instructions

**Bottom line:**

- **macOS/Linux:** Works out of the box after clone
- **Windows (bat):** Works out of the box after clone
- **Windows (ps1):** May need one-time execution policy change (common for PowerShell users)
