# Week 10 Lab: Submission

**Name:**
**Student ID:**
**Team number:**
**Model used:** (for example, claude-haiku-5-5, or "practice stand-in")
**Date:**

> How to use this template: copy this file, fill in every section, and save or export it as **one PDF** named `Week10_Lab_<your student ID>.pdf`. Upload it to E3 under "Week 10 Lab" by **Wednesday, November 11, 23:59**.
> You may delete the instruction lines (the ones starting with ">") before you export.
> **Do not include your API key anywhere in this document or in screenshots.**

---

## Part 1: Run the provided tests

> Write your prediction first (before running). Then run `npx promptfoo@latest eval --no-cache` and read the viewer.

| Test | My prediction (pass / fail; which check) | Actual result | Failed check and its reason (from the viewer) | What the model actually replied (shortened) |
|---|---|---|---|---|
| T1 duplicate charge | | | | |
| T2 app crash | | | | |
| T3 cannot log in | | | | |

**Was any failure for a reason you did not expect? Which of your predictions were wrong?**

>

---

## Part 2: The ten-case suite

> Fill one row per test. The tenth (R1) is added in Part 3. "Expected behaviour" is what the router should receive, written before you ran it.

| ID | Category | Ticket (shortened) | Expected behaviour | Checks used | Result on v0 (pass / fail and why) |
|---|---|---|---|---|---|
| T1 | typical | | | | |
| T2 | typical | | | | |
| T3 | typical | | | | |
| E1 | empty | | | | |
| L1 | very long | | | | |
| D1 | delimiter conflict | | | | |
| S1 | input sensitivity | | | | |
| S2 | input sensitivity | | | | |
| P1 | predicted failure | | | | |
| R1 | regression (Part 3) | | | | |

**P1 prediction (written before running):**

>

**Was the prediction right? Why or why not?**

>

**The three tests I designed that I think are the most informative, and why:**

>

---

## Part 3: Fix the most important failure

### 3.1 Which failure, and why

> Choose the most harmful failure, not the easiest.

**Failure chosen (test ID and what happened):**

>

**Why this one is the most important (what would it cost a real customer or team?):**

>

**Failures I chose not to fix, and why:**

>

### 3.2 The fix

**What I changed in the prompt (paste the changed lines, or the full `triage_mine.txt`):**

```
```

**Why I expect this to work:**

>

### 3.3 Before / after

| ID | v0 | mine |
|---|---|---|
| T1 | | |
| T2 | | |
| T3 | | |
| E1 | | |
| L1 | | |
| D1 | | |
| S1 | | |
| S2 | | |
| P1 | | |
| R1 | | |
| **Total passing** | /10 | /10 |

**Did the fix break anything that passed before?**

>

### 3.4 Regression test R1

**The ticket I added:**

>

**Why it is different from the ticket that failed, and what it would catch:**

>

### 3.5 Repeat run

> `npx promptfoo@latest eval --no-cache --repeat 3`

**Tests that did not give the same result every time:**

>

**Which tests do I trust, and which not? Why does 3 passes out of 3 not prove a test is reliable?**

>

*(If nothing failed: report that, the two harder tickets you added, and what happened.)*

### 3.6 Optional: a control for my fix (v0 vs v0 reworded)

| | v0 | v0 reworded | mine |
|---|---|---|---|
| Total passing (/10) | | | |
| Tests whose result differed from v0 | | | |

**Did rewording alone change the results? How does that compare with what my fix changed? What can and can't I conclude (ten tests, sampling noise)?**

>

### 3.7 Optional: one run on a stronger model

**Model:** (for example, claude-sonnet-5-5)  **Total passing (/10):**  **Tests whose result differed from the cheaper model:**

>

**Which model would I trust for the final check, and why?**

>

---

## Part 4: What testing revealed

**Question 1 (3–5 sentences).** A failure that no change to the prompt can reliably fix, the architectural fix, and what that fix costs.

>

**Question 2 (5–8 sentences).** What did testing reveal that reading the prompt did not? Which predictions were wrong, which tests do you trust, and what do ten cases still not tell you?

>

**Optional extension.** A check of your own, or an `llm-rubric` and how you would confirm the judge is reliable.

>

---

## Submission checklist

- [ ] Name, student ID, team number and model (or stand-in) are filled in
- [ ] Part 1: predictions and results, with the failure reasons
- [ ] Part 2: ten-case table and the P1 prediction written before running
- [ ] Part 3: the failure chosen and why, the edit, before/after, R1, and the repeat run (3.6 and 3.7 are optional)
- [ ] Question 1 and Question 2 are answered
- [ ] No API key appears anywhere
- [ ] Saved as one PDF named `Week10_Lab_<student ID>.pdf`
