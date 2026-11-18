# Week 11: Claude Code Setup (do this before start working on the lab)

In the lab you will debug the same codebase twice: first in an ordinary **chat window** (claude.ai in your browser), then with **Claude Code**, a tool that reads your files, runs commands and edits code on your computer. Install it and sign in **before class** if you can. The lab starts with 5 minutes for setup, which is enough to install and check when everything goes smoothly, but not to fix an installation problem.

For Part 1 you only need a browser signed in to **claude.ai** with the same account, plus Python and git. **No API key is needed for this lab.**

> **If you have an API key from earlier labs:** never write it in a file, a screenshot, an E3 post or a repository. Claude Code can see your folder.

---

## Step 1: Install Claude Code (5 minutes)

Open a terminal. Use the line for your system.

**macOS, Linux, or WSL**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows, PowerShell** (the prompt starts with `PS C:\`)

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows, Command Prompt** (the prompt starts with `C:\`, no `PS`)

```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

The installer shows no progress while it downloads. When it finishes, **open a new terminal window** and run:

```bash
claude --version
```

You should see a version number followed by `(Claude Code)`.

Other ways to install, if the line above fails: `brew install --cask claude-code` (macOS), `winget install Anthropic.ClaudeCode` (Windows), or `npm install -g @anthropic-ai/claude-code` (needs Node.js 22 or newer; do not use `sudo`). Requirements: macOS 13 or newer, Windows 10 (1809) or newer, or a recent Ubuntu/Debian; 4 GB of memory; an internet connection.

On Windows, installing **Git for Windows** (git-scm.com) is recommended. It is also what you will use for the version-control commands in the lab.

## Step 2: Sign in (3 minutes)

1. In your terminal, go to any folder and run `claude`.
2. A browser window opens. Sign in with **[instructor to fill in: the account or invitation students should use, for example "the claude.ai account that the course team invited you to"]**.
3. If the browser does not open, press `c` in the terminal to copy the sign-in link and paste it into a browser. If the browser shows a code instead of returning to the terminal, paste that code where Claude Code asks for it.
4. When you see `Login successful`, press Enter. Then type `/exit` to leave.

> **If Claude Code asks whether to use an API key** (this happens when `ANTHROPIC_API_KEY` is set in that terminal), **choose not to use it**, unless a TA tells you otherwise. Claude Code uses your key if you approve it, and that spends the class's API budget instead of your account's allowance. To be safe, do this step in a terminal where the key is **not** set.
> - macOS/Linux/WSL: `unset ANTHROPIC_API_KEY`
> - PowerShell: `Remove-Item Env:ANTHROPIC_API_KEY`

To check which account is in use at any time, start `claude` and type `/status`.

## Step 3: Try it on an empty folder (2 minutes)

```bash
mkdir claude_test
cd claude_test
claude
```

At the prompt, type: `what can you do in this folder?` Read the answer. Then type `/exit`. You do not need to create any files.

## Step 4: Check everything with one script (2 minutes)

In the lab folder (the one with `week11_setup_check.py`) run:

```bash
python week11_setup_check.py
```

It checks Python, git and Claude Code, and warns you if an API key is set in that terminal (it never prints the key). Fix anything it marks PROBLEM.

## Step 5: Check the chat for Part 1

Open **claude.ai** in your browser and make sure you are signed in with the same account. Start a chat and send "hello". That is all Part 1 needs.

---

## What Claude Code does 

- It reads files in the folder where you start it, and can run commands there (for example the tests).
- **It asks permission** before editing files or running commands. In the lab, **read each request before you approve it.** Do not turn on any option that skips these questions.
- Start it only inside the folder you are working in. Do not start it in your home folder.
- Useful commands inside Claude Code: `/help` (list of commands), `/clear` (start a fresh conversation), `/status` (account and model), `/exit` (leave).
- Press `Shift+Tab` to change the permission mode. Leave it on the default for the lab.

---

## If something goes wrong

| Problem | What to try |
|---|---|
| `claude: command not found` after installing | Close the terminal and open a new one. If it still fails, the install folder is not on your PATH: run `claude doctor` if it starts, or see the troubleshooting page linked below |
| The install line fails with an error like `syntax error near unexpected token '<'` or `403` | Use one of the other install methods listed in Step 1 |
| `'irm' is not recognized` | You are in Command Prompt. Use the Command Prompt line, or open PowerShell |
| `The token '&&' is not a valid statement separator` | You are in PowerShell. Use the PowerShell line |
| The browser does not open or does not return to the terminal | Press `c` to copy the link; paste the code if the browser shows one |
| Sign-in works but Claude Code says you do not have access | Your account may not have been invited or may not include Claude Code. Tell a TA before the lab |
| Login expired later (`Login expired`) | Run `/login` inside Claude Code |
| Nothing works and the lab is tomorrow | Tell a TA now. Do not wait until class. See the note at the end of the lab guide about what you can still do |

Official pages: Claude Code quickstart and advanced setup at code.claude.com/docs (look for "Quickstart", "Advanced setup" and "Troubleshoot installation and login").
