# Week 2 Lab — API Exploration: Tokens, System Prompts, and Context

**Goal:** Build concrete intuition for the three invisible constraints governing every API call — tokenization, system prompt grounding, and context window limits.

**Working style:** Individual | **Total time:** ~60 minutes

> **Provider note:** All three tasks below now default to a path that needs no API key, no account setup, and no billing risk of any kind. If you already have working, funded Anthropic or Google API access and want to see each task done exactly the way it's described in lecture, an optional appendix follows every task with that version. Neither path affects your grade.

### Setup — do this once, before you start

**If you're using the primary path (recommended, no account needed):**

```bash
pip install tiktoken
```

That's it — no key, no signup, no config file. Skip straight to Task 1 below.

**If you're using the optional API appendices instead (only if you already have working, funded access):**

```bash
pip install anthropic google-genai python-dotenv
```

Create a file named `.env` in the same folder as your script, and add whichever key(s) you're using:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
GOOGLE_API_KEY=your-gemini-key-here
```

You don't need to write any client setup code — `claude_client.py` and `gemini_client.py` are already provided in this folder and read your key(s) from `.env` for you:

```python
# claude_client.py
from dotenv import load_dotenv
import anthropic

load_dotenv()  # loads ANTHROPIC_API_KEY from a .env file in your project root
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
```

```python
# gemini_client.py
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()  # loads GOOGLE_API_KEY from a .env file in your project root
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
```

Just add `from claude_client import client` or `from gemini_client import client` to the top of your script — the appendix scripts referenced below already do this.

**Never commit your `.env` file or paste your key directly into code you share** — if you're using version control, add `.env` to your `.gitignore` before your first commit.

---

## Task 1 — Token Counting and Cost Estimation (15 min)

Use the fixed inputs below (the same for every student, so results are comparable across the class) — **except** the Mandarin translation, which you will produce yourself.

### The inputs

**Sentence:**
> "Our team deployed the new authentication service to production this morning."

**Paragraph (~200 words):**
> "The team spent the last three weeks redesigning the onboarding flow for new users joining the platform. The original flow required seven separate steps before a user could reach the main dashboard, and internal data showed that nearly forty percent of new signups abandoned the process before completing it. After reviewing session recordings and interviewing a sample of recent users, the team identified that the account verification step and the initial preference-setting step were the two biggest sources of drop-off. The redesigned flow reduces the process to three steps: account creation, email verification, and a single optional preferences screen that users can skip entirely and configure later from their settings page. Engineers also added a progress indicator at the top of each screen so users always know how many steps remain. Early testing with a small group of beta users showed a noticeable improvement in completion rates, though the team is still waiting on a full week of production data before drawing firm conclusions. The next phase of this work will focus on localizing the onboarding flow for non-English-speaking users, starting with Mandarin and Japanese."

**Mandarin translation:** Translate the paragraph above yourself. It doesn't need to be professional quality — a reasonable good-faith translation of the same content is fine.

**Python function (~20 lines):**
```python
def find_duplicate_orders(orders):
    """Return order IDs that appear more than once in the list."""
    seen = {}
    duplicates = []

    for order in orders:
        order_id = order["id"]
        if order_id in seen:
            seen[order_id] += 1
        else:
            seen[order_id] = 1

    for order_id, count in seen.items():
        if count > 1:
            duplicates.append(order_id)

    return duplicates


def summarize_duplicates(orders):
    dupes = find_duplicate_orders(orders)
    if not dupes:
        return "No duplicate orders found."
    return f"Found {len(dupes)} duplicate order ID(s): {dupes}"
```

**JSON object (5 nested keys):**
```json
{
  "project": {
    "name": "onboarding-redesign",
    "status": "in_review",
    "owner": {
      "name": "Priya N.",
      "team": "Growth Engineering"
    },
    "metrics": {
      "completion_rate": 0.72,
      "drop_off_step": "email_verification"
    }
  }
}
```

### Primary path — offline tokenizer, no account or API needed

(Uses the `tiktoken` install from Setup above — no key, no signup, no internet call at runtime.)

Open `task1_file/mandarin.txt` and replace its placeholder with your own translation of the paragraph above — that's the one input you produce yourself. Everything else in `task1_file/` (sentence, paragraph, function, JSON) is already filled in and fixed across the class.

Then run the provided script, which reads all five inputs from `task1_file/` and prints the char/token table:

```bash
python task1.py
```

**Important — read before you run this:** `tiktoken` is not an approximation or a simulator. It is OpenAI's real, exact production tokenizer. The "estimate" only enters because we're borrowing it to stand in for Claude's or Gemini's tokenizer, which aren't public — Anthropic and Google don't release their tokenizer vocabularies the way OpenAI does. So the count you get is a real, exact count — just for a different provider than the one you'd actually be billed by. The reason this is still a valid exercise: every major provider's tokenizer is some form of byte-pair encoding, and BPE tokenizers share the same general behavior regardless of vendor — English prose compresses efficiently, code and structured data compress less efficiently than prose, and CJK-script languages compress markedly less efficiently than English almost universally, because every major vocabulary is trained on corpora dominated by English and Latin-script text. The *relative pattern* across your five inputs is valid and transferable; the *exact numbers* would differ somewhat if run against Claude's or Gemini's real tokenizer.

Then calculate the cost of each input using a real provider's published per-token rate (e.g., Claude Sonnet 4.6 or Gemini Flash's rate card) applied to your tiktoken-estimated count — you're calculating what it would plausibly cost, using a stand-in count, not measuring an exact bill.

### Expected outcome

Plain English should land close to 1 token per word (a high chars/token ratio). Code and JSON should show a noticeably lower chars/token ratio than prose. Your Mandarin translation should show the lowest ratio of all — significantly more tokens for the same meaning as the English paragraph.

**Answer in your log:** which result surprised you most, and what does it imply for Mandarin-language users? Also note: given that tiktoken is a stand-in for a different provider's tokenizer, do you expect the actual Claude/Gemini numbers to be higher, lower, or about the same as what you found — and why?

### Appendix (optional) — real API token counting

If you have working, funded Anthropic or Google API access and want Claude's or Gemini's actual token count rather than a stand-in (see Setup above for installing the SDKs and configuring your `.env` file first), run the provided scripts — they read the same five inputs from `task1_file/`:

```bash
python task1_claude.py   # uses claude-sonnet-4-6
python task1_gemini.py   # uses gemini-3.5-flash
```

If you run this version, compare your real Claude/Gemini numbers against your tiktoken estimate from the primary path and note how close the pattern actually was. Not required, not the primary path.

---

## Task 2 — System Prompt Sensitivity: Standard-Library-Only Constraint (15–20 min)

**Setup:** Open **three separate new chats** in claude.ai or gemini.google.com (either is fine — no API key needed). Each chat tests one phrasing. Don't reuse the same chat for more than one phrasing, since you want each one tested clean, without the model having seen the other two.

### The three phrasings

In **Chat 1**, as your first message, send:

> "You may only use Python's standard library. Never import third-party packages such as `requests`, `numpy`, or `pandas`. Now, write a Python function that fetches the contents of a URL and returns the response as a string."

In **Chat 2**, as your first message, send:

> "You should generally try to stick to Python's standard library where possible. Now, write a Python function that fetches the contents of a URL and returns the response as a string."

In **Chat 3**, as your first message, send:

> "You are a Python assistant operating in a locked-down environment where only the standard library is installed. Third-party packages are not available to you. Now, write a Python function that fetches the contents of a URL and returns the response as a string."

### What to check

Look at the `import` statement in each of the three responses. Did it reach for `urllib.request` (standard library, compliant) or `requests` (third-party, non-compliant)? No special Python-version knowledge needed — just check whether the import belongs to the standard library.

### Expected outcome

All three phrasings express the same underlying rule, but you should notice a real compliance gap: the direct phrasing (Chat 1) typically produces strict standard-library-only code, while the softened phrasing (Chat 2 — "generally," "where possible") is more likely to reach for `requests` anyway, treating the constraint as a suggestion rather than a rule.

**Answer in your log:** where does information that must govern every response belong, and what does the gap between these three outputs tell you about writing system prompts for your own project?

### A note on what's different here vs. the API

Bundling the instruction into your first chat message isn't quite the same mechanism as the API's separate `system` field described in lecture — it's a user turn, not an architecturally distinct instruction channel. In practice it still tests the same underlying sensitivity phenomenon well, since the instruction is still the first, most prominent thing in the conversation. Worth naming this distinction in your log answer if you want to connect it back to the lecture's message-structure content.

### Appendix (optional) — API/code version

If you have working, funded API access already (see Setup at the top for installing the SDK and configuring your `.env` file), you can run the same test with a literal `system`/`system_instruction` parameter instead of a first chat message — both providers are provided:

```bash
python task2_claude.py
python task2_gemini.py
```

Both scripts loop over the same three phrasings and print each response so you can check the import statement, same as the chat version above.

Not required, not the primary path.

---

## Task 3 — Instruction Dilution: Push Until It Breaks (20–25 min)

**Working style:** Open-ended conversation, not a fixed script. You're trying to find the point where the model stops following an instruction it was given at the very start.

### Setup

Open a **new chat** in either claude.ai or gemini.google.com. As your **very first message**, set a strict rule:

> "For the rest of this conversation, you must respond only in bullet points. Never write full sentences or paragraphs, under any circumstances, no matter what I ask — even if I ask you to explain something or tell a story."

Confirm the first response actually follows the rule before continuing. If it doesn't comply immediately, that's already a finding worth logging — note it and move on.

### The exercise

Now just talk to it. Ask real questions, one at a time, and keep going. Don't ask it to break the rule directly — the point is to see whether it *drifts* away from the rule on its own over an ordinary conversation, not whether you can trick it.

A few kinds of questions tend to apply more pressure than others:

- **Neutral chat** (low pressure): "What's a good weekend activity?" "What's your favorite season?"
- **Narrative/explanatory** (higher pressure — these naturally pull toward prose): "Tell me a short story about two old friends reuniting." "Walk me through how a caterpillar becomes a butterfly." "Describe a bustling night market scene in detail."

Mix both kinds as you go. If you get stuck for what to ask next, here's a list to pull from — you don't need to use all of them, or use them in this order:

> Tell me about your favorite season · What makes a good movie · Tell me a short story about a lighthouse keeper · What's a good book for a rainy day · Walk me through how bread rises when baked · What's an underrated programming language · Explain, like a story, how a seed becomes a tree · What's a nice way to spend a day off · Describe a perfect morning in vivid detail · What's your take on morning routines · Walk me through the history of the printing press · Tell me a story about two old friends reuniting after years apart · What's an interesting fact about how bees communicate · Describe what it might feel like to summit a mountain at sunrise · Tell me the story of how coffee was first discovered · Walk me through how a caterpillar becomes a butterfly · Describe a bustling night market scene in detail · Can you explain how photosynthesis works

### What to log

- **How many messages in did compliance first slip?** (a full sentence sneaking in, a paragraph instead of bullets, etc.) Note the approximate turn number and paste the message where it happened.
- **What kind of question triggered it?** Was it a neutral question or a narrative/explanatory one?
- **Did it recover on its own**, or once it broke the rule once, did it stay broken for the rest of the conversation?
- If you reach the end of the provided question list and it *still* hasn't broken, keep going with your own questions — note how many total turns it took, or if it never broke at all.

### Expected outcome

This is open-ended by design — there isn't one correct place where it should break, and "it never broke" is itself a valid, useful result to report. The interesting thing to notice is *what kind of pressure* it was that eventually got through, if anything did — is it accumulated length alone, or does it specifically take a narrative/explanatory question to crack it?

**Answer in your log:** what would this mean for a long-running agent given a strict instruction at the very start of its task? What would you do about it as an engineer?

### Appendix (optional) — API/code version

If you already have working, funded API access and want to see the mechanism exactly as described in lecture (a literal `system`/`system_instruction` parameter rather than a first chat message), the provided scripts send the rule as the system prompt and loop through the same 18-question list from the exercise above, printing the final response so you can check whether it's still holding to bullet points:

```bash
python task3_claude.py
python task3_gemini.py
```

Want to push harder? Extend the `turns` list in either script with more questions of your own — the narrative/explanatory kind described above tend to apply the most pressure. A longer conversation is a more thorough pressure test, and there's no fixed length you're required to stop at.

This is not required and is not the primary path for this task.

---

## Grading Checklist (1%, binary completion)

- [ ] Token/char count table for all five inputs (including your own Mandarin translation), with chars/token ratio noted, and your prediction of how a real Claude/Gemini count would compare
- [ ] Three system-prompt-phrasing outputs for Task 2, with a written observation on which import statement each one used
- [ ] Task 3 log: approximate turn where compliance first slipped (or a clear note that it never did), plus what kind of question triggered it
- [ ] Written answers to all three log questions
- [ ] Wrap up the all the above in **a single text file (.txt)** or **markdown (.md) file**

*Reminder: which tool or provider you used for each task does not affect your grade. Note what you used at the top of your submission.*
