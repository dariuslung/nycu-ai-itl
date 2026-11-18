#!/usr/bin/env python3
"""week11_setup_check.py: run this BEFORE the lab. It prints OK / PROBLEM lines and never shows your key."""
import os
import shutil
import subprocess
import sys

problems = 0


def report(ok, text, fix=""):
    global problems
    print(("OK       " if ok else "PROBLEM  ") + text)
    if not ok:
        problems += 1
        if fix:
            print("         -> " + fix)


report(sys.version_info >= (3, 9), f"Python {sys.version.split()[0]}", "Use Python 3.9 or newer.")
if os.environ.get("ANTHROPIC_API_KEY"):
    print("NOTE     ANTHROPIC_API_KEY is set in this terminal. This lab does not need it. Unset it before")
    print("         starting Claude Code, or Claude Code may offer to bill the class API budget (see the setup guide).")
else:
    report(True, "no API key set in this terminal (good: this lab does not need one)")
git = shutil.which("git")
report(git is not None, "git is installed", "Install git from git-scm.com.")
claude = shutil.which("claude")
if claude:
    try:
        out = subprocess.run([claude, "--version"], capture_output=True, text=True, timeout=30)
        report(out.returncode == 0, "Claude Code installed: " + out.stdout.strip(), "Run: claude doctor")
    except Exception as error:
        report(False, f"claude found but did not run ({error})", "Run: claude doctor")
else:
    report(False, "Claude Code is not installed (command 'claude' not found)",
           "Follow week11_claude_code_setup.md. If it will not install, tell a TA before the lab.")
print("\nNote: this script cannot check that you are signed in to Claude Code or claude.ai. Run 'claude', complete the sign-in, then type /exit.")
print("All checks passed." if not problems else f"{problems} problem(s) found. Fix them before the lab, or ask a TA.")
