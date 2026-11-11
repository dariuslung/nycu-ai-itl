#!/usr/bin/env python3
"""
Week 10 setup check. Run this BEFORE the lab, or at the start of it, from the lab folder.

    python week10_setup_check.py

It checks that:
  1. Node.js is installed and is version 22.22 or newer (PromptFoo needs it),
  2. npx is available,
  3. the lab files are in this folder,
  4. an API key is set (it only says yes or no; it NEVER prints the key),
  5. PromptFoo can be downloaded and started (the first run downloads it; be patient).
It makes NO model calls and costs nothing.
"""
import os
import re
import shutil
import subprocess
import sys

problems = []


def run(cmd, timeout=120):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=(os.name == "nt"))


print("1. Node.js")
node = shutil.which("node")
if not node:
    print("   Node.js was not found. Install the current LTS from https://nodejs.org, open a NEW terminal, and rerun.")
    problems.append("node")
else:
    out = run(["node", "--version"]).stdout.strip()
    m = re.match(r"v(\d+)\.(\d+)", out)
    ok = bool(m) and (int(m.group(1)), int(m.group(2))) >= (22, 22)
    print(f"   {out}  ->  {'OK' if ok else 'TOO OLD: PromptFoo needs 22.22 or newer. Install the current LTS and open a new terminal.'}")
    if not ok:
        problems.append("node version")

print("2. npx")
if shutil.which("npx"):
    print("   OK")
else:
    print("   npx was not found. It comes with Node.js: reinstall Node.js and open a new terminal.")
    problems.append("npx")

print("3. Lab files in this folder")
needed = ["promptfooconfig.yaml", "promptfooconfig.practice.yaml", "practice_provider.js", "checks.js", "tests.yaml",
          "prompts/triage_v0.txt", "prompts/triage_mine.txt", "prompts/triage_v0_reworded.txt", "tickets/long_ticket.txt"]
missing = [f for f in needed if not os.path.exists(f)]
if missing:
    print("   Missing:", ", ".join(missing))
    print("   Run this script from the folder that holds the lab files (keep the folder structure).")
    problems.append("files")
else:
    print("   OK: all files found")

print("4. API key")
if os.environ.get("ANTHROPIC_API_KEY"):
    print("   ANTHROPIC_API_KEY is set (its value is not shown).")
else:
    print("   ANTHROPIC_API_KEY is not set in this terminal. That is fine for now:")
    print("   you can use the practice stand-in (promptfooconfig.practice.yaml) until your key arrives.")

print("5. PromptFoo (the first run downloads it: this can take a minute)")
if "node" not in problems and "npx" not in problems:
    try:
        r = run(["npx", "--yes", "promptfoo@latest", "--version"], timeout=240)
        if r.returncode == 0 and r.stdout.strip():
            print(f"   OK: PromptFoo {r.stdout.strip().splitlines()[-1]}")
        else:
            print("   PromptFoo did not start. Message:", (r.stderr or r.stdout).strip()[-300:])
            print("   Check your network (a VPN or proxy can block it), or try: npm install -g promptfoo")
            problems.append("promptfoo")
    except subprocess.TimeoutExpired:
        print("   Timed out. Check your network (a VPN or proxy can block it), then try again or tell a TA.")
        problems.append("promptfoo")
else:
    print("   Skipped (fix Node.js first).")

if problems:
    print("\nNot ready yet:", ", ".join(problems), "\nFix the lines above, or tell a TA before the lab and include this output.")
    sys.exit(1)
print("\nAll set. You are ready for the Week 10 lab.")
