# Week 11 Lab — Submission Template
*Copy this into any tool, fill it in, save as PDF named `Week11_Lab_<student ID>.pdf`, and upload it to E3 under "Week 11 Lab" by Wednesday, November 18 (23:59). Do not include passwords or keys.*

## Header

| | |
|---|---|
| Name | |
| Student ID | |
| Team number | |
| Chat tool and model used in Part 1 (for example claude.ai, and the model it shows) | |
| Claude Code model (from `/status`) | |

## Before you started (one line each)
Your first guess at what the five bugs might be:

1. 
2. 
3. 
4. 
5. 

## Bug report

Fill one row per bug. "Attempted" is enough for completion; fixed and verified is better. Name the bugs in your own words (a one-line description), not by copying what the AI said.

| # | What is wrong (your words) | File and function | Failing test that shows it (or "none") | Found in the chat? How? | Found by Claude Code? How? | Fix (one line) | How I checked the fix was right |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |

**Totals**

| | Part 1 (chat window) | Part 2 (Claude Code) |
|---|---|---|
| Bugs attempted | | |
| Bugs fixed | | |
| Tests passing (of 10, plus any you added) | | |
| Changes I declined or edited | n/a | |

## Loop tables
One row per fix. "Whole suite after" means you ran **all** the tests after that fix.

**Part 1 (chat window)**

| Bug | Test that shows it (given, or mine) | Red before the fix? | Fix (one line) | Whole suite after (passing / total) | Anything else break? |
|---|---|---|---|---|---|
| | | | | | |

**Part 2 (Claude Code)**

| Bug | Test that shows it (given, mine, or Claude Code's) | Red before the fix? | Fix (one line) | Whole suite after (passing / total) | Anything else break? |
|---|---|---|---|---|---|
| | | | | | |

Did Claude Code write a failing test for the bug that had none, **before** fixing it? Did it run the whole suite after each fix? 

## Chat log, Part 1
At least three exchanges that mattered, copied from your `chat_log.md`: your prompt (or a summary of what you pasted), the key part of the answer, and **Your note**: what did you ask, was the answer right, how did you check?

> Entry 1:
>
> Your note:

**CHECKED DIAGNOSIS (required, at least one):**

| | |
|---|---|
| The model's diagnosis (one or two lines) | |
| The check (the command or test, as run) | |
| Output it predicted | |
| Output I got | |
| Would this check have failed if the diagnosis were wrong? Why? | |
| Did the diagnosis hold up? | |
| The fix I then applied | |

## Claude Code notes
In order, in short bullets: what you asked, what it did, what you approved, declined or edited.

- 

Answer these three in a line each:
- Did it change a test? 
- Did it change anything outside the five bugs? 
- Did it find a problem you did not?

## Part 3: one problem of my own, through the whole loop

| | |
|---|---|
| The problem (one line) | |
| Bug (breaks its own docstring) or decision (docstring does not say)? If a decision, what I chose | |

**Red: my test, and the output showing it fails**
```python
# my test
```
```text
# red output
```

**Fix (the diff, or the changed lines)**
```diff
```

**Green: my test passes**
```text
```

**Suite: all tests after the fix** (passing / total, and anything that broke)

**Would my test catch a bad fix?** After `git stash` (fix undone), my test was: red / green. After `git stash pop`: red / green.

## Part 4: comparison questions (4–8 sentences each; refer to specific moments)

**1. What did Claude Code do that the chat window could not?**

**2. Where did Claude Code make a decision you should have made yourself?**

**3. What context did Claude Code have automatically that you had to provide by hand? And what context did you have that it did not?**

## Optional extensions
The bug I am least sure the AI fixed correctly is bug # ____. A test that would catch a wrong fix:

```python
```

Tools check (on the original code):

| Tool and command | Bugs it found (by number) | What it reported |
|---|---|---|
| `ruff check --select S teamboard` | | |
| `mypy --check-untyped-defs teamboard` | | |
| `mypy teamboard` (default settings) | | |
