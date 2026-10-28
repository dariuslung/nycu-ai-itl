# Week 7 Lab — Diagnose and Fix a Three-Tool Agent
## Online lab | ~60 minutes | Individual

You are given a small agent with three tools whose descriptions are **deliberately weak**. First you make it work. Then you find out how it fails. Then you write better descriptions and show, with evidence, that they help. The goal is **not** a perfect agent. It is to see how tool use goes wrong, and to learn how to tell whether a fix really worked.

> **Models are good, and sometimes nothing fails.** Newer models often handle tools well even with weak descriptions. If a failure mode does not appear for you, that is a legitimate finding. This lab tells you exactly what to try next and what to report. Read "If a failure mode did not fail" in Part 2.

---

## What you submit (read this first)

| | |
|---|---|
| **Who** | Individual. Each student submits their own file |
| **What** | **One PDF document** with the contents listed below |
| **Where** | E3, under "Week 7 Lab" |
| **When** | By the end of **Wednesday, October 21 (23:59)** |
| **File name** | `Week7_Lab_<your student ID>.pdf` |
| **Grading** | 1% of your grade, graded on completion. We encourage you to be specific and detailed, because the detail is what makes the lab useful to you |

**Your PDF should contain, in this order:**

1. **Header:** your name, student ID, and the model you used
2. **Part 1:** your `handle_tool_call` code, your answer to the design question, and the baseline results
3. **Part 2:** a prediction and a record for **each of the four failure modes**, with run counts. For any mode that did **not** fail, the **"did not fail" report**
4. **Part 3:** your final schemas, a before/after comparison, and a list of the queries you re-tested
5. **Part 4:** your written responses to Question 1 and Question 2

A fillable copy is in `week7_lab_submission_template.md`. Write in any tool you like (Word, Google Docs, Notion, a Markdown editor) and save as PDF before uploading. Do **not** include your API key anywhere.

---

## Time plan

| Part | What | Minutes |
|---|---|---|
| Setup | key, install, smoke test | 5 |
| Part 1 | wire up the tools (`handle_tool_call`) and run the baseline | 8 |
| Part 2 | diagnose the provided descriptions: find the failures | 20 |
| Part 3 | write your own descriptions and show they help | 17 |
| Part 4 | written responses | 10 |

---

## Setup (5 minutes)

You need Python 3.9 or newer and an API key.

1. **Download the starter file** `week7_lab_starter.py` from [the course website / E3: instructor to fill in]
2. **Install the SDK:** `pip install anthropic`
3. **Get your API key** from [instructor to fill in how keys are distributed]. Set it in your terminal (do not paste it into the file):
   - macOS / Linux: `export ANTHROPIC_API_KEY=your-key-here`
   - Windows: `setx ANTHROPIC_API_KEY your-key-here`, then open a **new** terminal
4. **Smoke test:** run `python week7_lab_starter.py --v0 "Hello"`. If you see `ANSWER: ...`, your key works

> **Protect your key.** Never post it on E3, the course website, in email, in a screenshot, or in your team's GitHub repository. A key in a public repo is usually found and misused within minutes. If you think yours leaked, tell a TA right away so it can be replaced.

The lab uses a small, inexpensive model. The class shares a budget, so please keep `--repeat` at 10 or lower and do not run long loops.

If you do not have a working key yet, tell a TA in the session. You may watch a partner while yours is being fixed, but **write your own answers**.

---

## What the starter file gives you

- **Three tools that already work:** `calculator` (a safe parser, no `eval`), `search_knowledge_base` (course **content**: what is covered, what is in a deliverable, what a role does) and `get_course_calendar` (course **dates**: when something is due)
- **`TOOLS_V0`:** a set of provided tool descriptions that are **deliberately flawed**. Do not edit them. You will diagnose them in Part 2
- **`TOOLS`:** where you write **your own** descriptions in Part 3 (placeholders marked `TODO`)
- **`run_agent`:** the message loop from the lecture. It prints every tool call and result
- **Test lists and flags:** `--tests`, `--modes`, `--stress`, `--repeat N`, and `--v0` (use the provided flawed descriptions)

You write only two things: `handle_tool_call` (Part 1) and your own descriptions (Part 3).

---

## Part 1 — Wire up the tools (8 minutes)

In `handle_tool_call(tool_name, tool_input)`, write the code that:

- runs the right function for each of the three tools
- returns an **error message the model can understand** for an unknown tool name
- returns `(result_text, is_error)`

**Design question (one sentence):** `run_calculator` reports bad input as a string beginning with `Error:`. Should that count as `is_error=True`? Decide, and say why.

**Baseline check.** Run `python week7_lab_starter.py --v0 --tests`:

| Query                            | Expected                   |
| -------------------------------- | -------------------------- |
| "What is 247 times 38?"          | calculator, answer 9386    |
| "What is covered in Week 6?"     | knowledge base             |
| "When is the Week 7 lab due?"    | calendar, Wed Oct 21 23:59 |
| "What is the capital of France?" | answers directly, no tool  |

Record what happened for each. If one did not behave as expected, that is already a finding. Note it and carry on.

---

## Part 2 — Diagnose the provided descriptions (20 minutes)

### Step 1: read and predict (4 minutes)

Read the descriptions in `TOOLS_V0` carefully. For **each of the four failure modes below**, write down, **before you run anything**:

- which query you expect to trigger it
- which part of the V0 description you think would cause it

Predictions can be wrong. Writing them first is what makes the experiment meaningful.

### Step 2: run (6 minutes)

```
python week7_lab_starter.py --v0 --modes --repeat 5
```

This runs the starter queries for each mode five times and counts what the model did. Results vary from run to run, so counts are more reliable than a single run. Look at the printed tool sequences, errors and first answer.

### Step 3: judge and record (10 minutes)

For each mode, decide whether it **failed**, using these definitions, then fill in one record (template at the end of this section).

| Mode | It failed if... | Try (starter queries) |
|---|---|---|
| **1. Wrong tool** | the model used a tool that cannot answer the question, or the wrong one of two overlapping tools, or a tool where none was needed | "How many techniques are covered in Week 5?", "What are the deliverables for CP1?", "When is the Week 7 lab due?" |
| **2. Wrong parameters** | the right tool, but arguments that are malformed or not what you meant, so the tool errored or answered the wrong question | "twenty-four divided by eight, then multiplied by three", "square root of 144 plus 15 percent of 240", "What is covered in Week6?" |
| **3. Unnecessary call** | a tool was called when the model could easily have answered directly | "What does the term 'hallucination' mean...", "What is the capital of France?", "What is chain-of-thought prompting?" |
| **4. Missed call** | the model answered from memory when a tool would give the accurate, course-specific answer, or a number that is wrong | "What does the code steward do?", "When is Assignment 1 due?", "What is 48273 times 9167?" |

For mode 4, check the answer against the truth: the correct product is 442518591, and the code steward answer should match the knowledge base text. Plausible but wrong is exactly the problem.

**Three possible outcomes for each mode:**

- **A. It failed on the starter queries.** Record it (template below)
- **B. It failed only under stress.** Run `python week7_lab_starter.py --v0 --stress --repeat 5` and record the failure from there
- **C. It did not fail.** Complete the **"did not fail" report** below

Notice the tension. Mode 3 and mode 4 pull in opposite directions: fixing unnecessary calls pushes toward calling less, and fixing missed calls pushes toward calling more. Keep this in mind for Part 3.

### Record for each mode

```
Failure mode N: ______________________
My prediction (query, and the V0 words I expected to cause it):
Query used:
Runs: 5.  What the model did (tool sequences and counts, e.g. "calculator x3, no tool x2"):
Tool errors (n of 5), and an example argument if any:
Correct answer, and was the final answer correct?
Outcome:  A failed on starter queries / B failed only under stress / C did not fail
Which words in the V0 description made this plausible:
```

### If a failure mode did not fail

Not failing is a real result. It is **not** a mistake and you do **not** lose credit for it. But "it worked once" is weak evidence. If a mode did not fail, complete **all four steps** and report them.

**Step A. Show it with numbers.** For that mode, run **at least three different queries**, each with `--repeat 5`: the starter queries, plus at least **one you wrote yourself**. Put the counts in a table.

**Step B. Try to break it deliberately.** Run `--v0 --stress --repeat 5`. Then write **two queries of your own** that you predict could trigger the failure. Write your prediction (and why) **before** you run them.

**Step C. Change a condition.** Try **at least two** of these and re-run with `--repeat 5`:

- ask the same question in **Chinese**, or mix Chinese and English
- add **a lot of irrelevant context** before the question
- use a **vague or misspelled** version ("wk 6 stuff", "cp 1 deadlin")
- ask a question that needs **two tools** or **two steps**
- in **your own copy** of the file, add a fourth tool whose description **overlaps** one of the existing tools
- in your own copy, delete one sentence from a V0 description and see if it matters (do not edit `TOOLS_V0` itself; copy it)

**Step D. Report and reflect (4–6 sentences).** Say:

1. **What you tried:** a short table of query, condition, and counts
2. **Your verdict:** "no failure in N queries across K conditions", or "it did fail once, under X"
3. **Why you think it held up.** Which of these protected it? Pick and justify: self-explanatory tool names, a clear parameter, an easy question, a strong model, a small number of tools, or something else
4. **What would make it fail in a real project.** For example: many tools, similar tool names, long conversations, vague user phrasing, a different model, or a model update
5. **What you would monitor.** One thing you would log or test regularly so you would notice if it started failing, and why "it didn't fail today" is not enough to ship

A complete report on a mode that did not fail counts exactly as much as a record of a mode that did.

---

## Part 3 — Fix it with your own descriptions (17 minutes)

### Write your schemas (8 minutes)

Open `week7_lab_starter.py` and replace each `TODO` in `TOOLS` with your description and parameter description, for all **three** tools.

Use the six-question checklist from the lecture. A good description says:

1. **What** the tool does
2. **When** to use it
3. **When NOT** to use it (and what to use instead)
4. What each **parameter** means and its format
5. What it **returns**
6. Its **limits**

Aim for at least three to four sentences per tool. Pay particular attention to where two tools could be confused, and to what the calculator can and cannot accept.

> You must fix the failures you found. If a mode did **not** fail, still write the description that you would use to **prevent** it, and test that it holds up.

### Rerun and compare (9 minutes)

Run your version on exactly the same queries:

```
python week7_lab_starter.py --modes --repeat 5
python week7_lab_starter.py --stress --repeat 5
```

Then:

1. **Compare before and after** in a table: for each mode's main query, the V0 counts and your counts
2. **Check for new problems.** Did a fix for one mode break another? Re-test **all** the queries you used
3. **Explain one fix** in terms of the exact words you changed

If something still fails, say so. A partial fix with an honest explanation is a good result.

### Before/after table

```
Query | V0 result (5 runs) | My result (5 runs) | Better / same / worse
```

---

## Part 4 — Written responses (10 minutes)

**Question 1 (3–5 sentences).** Which failure mode was hardest to fix or to provoke, and why? What does this tell you about designing tool descriptions, and about how much evidence you need before you trust an AI component, in your project?

**Question 2 (2–3 sentences).** Imagine your team's AI component could use a tool that **changes something** (sends a message, creates an issue, edits a file, deletes data). Name that tool. Who or what should approve it before it runs, and what would happen if the model called it wrongly?

---

## Submission checklist

Before you upload, check that your PDF:

- [ ] Has your name, student ID and the model you used at the top
- [ ] Shows your `handle_tool_call` code, your `is_error` reasoning and the baseline results
- [ ] Has a **prediction and a record** for all four failure modes, with run counts
- [ ] For any mode that did not fail, has the **"did not fail" report** (numbers, stress, changed conditions, reflection)
- [ ] Shows your final schemas for all three tools, a before/after table and the queries you re-tested
- [ ] Answers Question 1 and Question 2
- [ ] Is specific to what you saw. A reader should be able to tell that you ran the queries yourself
- [ ] Does **not** contain your API key
- [ ] Is saved as a single PDF named `Week7_Lab_<your student ID>.pdf`

Then upload it on E3 under "Week 7 Lab" by **Wednesday, October 21 (23:59)**. A fillable template is in `week7_lab_submission_template.md`.

---

## If things go wrong

| Problem | What to do |
|---|---|
| `ModuleNotFoundError: anthropic` | Run `pip install anthropic`. Make sure the terminal uses the same Python you installed it for |
| An authentication error | The key is missing or wrong. Reset it in the terminal, open a **new** terminal if you used `setx`, and rerun. Ask a TA if it persists |
| "Your credit balance is too low" | The class credit has run out or is not set up for your key. Tell a TA. Do not keep retrying |
| Rate limit or "overloaded" error | Wait 30 seconds and retry. Use a smaller `--repeat`, and do not run many queries in a loop |
| `NotImplementedError: TODO: implement handle_tool_call` | You have not written Part 1 yet |
| "Your schemas in TOOLS still contain TODO text" | Normal until Part 3. Use `--v0` for Parts 1–2 |
| The model never calls a tool | Check that the tool names in your code match the schemas |
| An error about `tool_use` ids without `tool_result` | The loop in the starter handles this. If you edited the loop, check that every tool call gets a result in the very next message |
| "(stopped after 5 model calls)" | The loop's safety limit. This is a finding. Note which query caused it |
| Different results from a classmate | Expected. Models vary between runs. Compare counts, and discuss |
| A mode never fails for you | See "If a failure mode did not fail" in Part 2 |

---

## Optional extensions (not submitted)

If you finish early:

- Add a fourth tool of your own and see whether your fixes still hold
- Look up `tool_choice` in Anthropic's "Define tools" documentation and see what it changes. Note that some options are restricted on the newest models
- Wrap your tools as a small MCP server (see lecture slide 32) and compare the schemas

---

## Connection to the course

- **Week 5:** "specify before you generate." A tool description is a specification, written for the model
- **Week 6:** failure modes and triage. The four tool-use failures use the same method: symptom, likely cause, first fix, retest
- **Week 10:** prompt testing. The counts and the list of re-tested queries are the start of a test suite, and "it worked once" is not a test
- **Your project:** if your team's AI component calls tools, record important description or approval decisions in `DECISIONS.md`
