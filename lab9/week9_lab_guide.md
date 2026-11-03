# Week 9 Lab: Measure and Improve a RAG Pipeline
## In-person lab | ~60 minutes | Individual

You are given a small question-answering system over a (fictional) company handbook. It finds the relevant passages and gives them to a model (RAG). Your job is to **measure** how well it finds the right passage, **find out why it sometimes does not**, and **improve** both the search and the prompt. Retrieval can be scored without calling a model at all, so you can run many experiments quickly and for free.

> Retrieval scores are deterministic: the same command gives the same result every time. If answer generation does not fail for you, that is a valid result; Part 3 says what to report.

---

## What you submit (read this first)

| | |
|---|---|
| **Who** | Individual. Each student submits their own file |
| **What** | **One PDF document** with the contents listed below |
| **Where** | E3, under "Week 9 Lab" |
| **When** | By the end of **Wednesday, November 4 (23:59)** |
| **File name** | `Week9_Lab_<your student ID>.pdf` |
| **Grading** | Graded on completion, like the earlier labs. Be specific |

**Your PDF should contain, in this order:**

1. **Header:** your name, student ID, team number, and the model you used
2. **Part 1:** the with/without retrieval comparison, with your predictions
3. **Part 2:** retrieval results: the chunking table, your two diagnosed misses, and your `chunk_by_heading` code
4. **Part 3:** your `build_prompt`, before/after answer scores, a faithfulness spot-check of three answers, and three classified failures (or the "did not fail" report)
5. **Part 4:** your written responses to Question 1 and Question 2

A fillable copy is in `week9_lab_submission_template.md`. Write in any tool and save as PDF before uploading. Please do **NOT** include your API key.

---

## Time plan

| Part | What |
|---|---|
| Setup | files, packages, smoke test |
| Part 1 | RAG vs. no RAG on four questions |
| Part 2 | measure and diagnose retrieval; write a second chunker |
| Part 3 | measure the answers; write a better prompt |
| Part 4 | written responses |

---

## Setup (5 minutes)

You need Python 3.9 or newer.

1. Put `week9_lab_starter.py`, `eval_questions.json` and the `corpus/` folder **in the same folder**. Download them from E3, under "Week 9 Lab Files"
2. Install the packages: `pip install chromadb anthropic`
3. Run `python week9_setup_check.py`. The first run downloads a small embedding model
4. **API key** (needed in Parts 1 and 3 only): Get your team's API key from the course website. Set it in your terminal and never in a file: `export ANTHROPIC_API_KEY=your-key-here` (macOS/Linux), or `setx ANTHROPIC_API_KEY your-key-here` and open a **new** terminal (Windows)
5. **Smoke test (free, no key needed):** `python week9_lab_starter.py eval`. You should see a list of questions with `ok` or `MISS`

> **Protect your key.** Never post it on E3, Discord, in email, in a screenshot, or in your team's repository. The class shares a budget: keep `--repeat` at 5 or below.

---

## What the starter file gives you

- **The corpus:** 20 short documents from the "Nimbus Notes" engineering handbook (architecture, policies, runbooks, postmortems, a changelog)
- **21 questions** in `eval_questions.json`, each with the evidence it needs and a type (factual, paraphrase, exact term, conflict, and so on)
- **Chunking:** `chunk_fixed(size, overlap)`, sized in words (roughly 1.3 tokens per word)
- **Two retrievers:** `bm25` (keyword search) and `dense` (semantic search with a local embedding model)
- **Scoring (no API calls):** `hit@k` (do the top-k chunks contain *all* the evidence?), `MRR` (how high is the first relevant chunk?), `precision@k`, and the number of context words the model must read
- **Generation:** `ask`, `run-all`, and an automatic answer check (a rough heuristic: read the answers yourself)

You write three things: `chunk_by_heading` (Part 2), `build_prompt` (Part 3), and optionally `HybridIndex.search` (Part 4).

**Commands you will use**

```
python week9_lab_starter.py eval --retriever bm25 --chunk fixed:200:0 --k 3
python week9_lab_starter.py grid --retrievers bm25,dense --k 3
python week9_lab_starter.py ask "question"            # add --no-rag, --retriever dense, --k 5
python week9_lab_starter.py run-all --prompt v0       # all 21 questions with the basic prompt
python week9_lab_starter.py run-all                   # all 21 questions with YOUR prompt
```

`--chunk fixed:200:0` means chunks of 200 words with 0 words of overlap. `fixed:200:50` means 50 words are shared between neighbouring chunks.

---

## Part 1: Does retrieval help? (10 minutes)

**Predict first.** For each question below, write whether you expect the model to answer **correctly without retrieval**, and why. The company is fictional, so think about what a model could possibly know.

| # | Question |
|---|---|
| a | Which port does the search service listen on? |
| b | How many approvals does a change to the billing code need? |
| c | What uptime SLA do Team plan customers get? |
| d | What is the maximum size of a pull request? |

**Run each question twice:**

```
python week9_lab_starter.py ask "Which port does the search service listen on?" --no-rag
python week9_lab_starter.py ask "Which port does the search service listen on?" --prompt v0
```

Record, for each: the answer, the chunk ids retrieved (RAG only), and whether it is correct. Look at the **ideal answers** by reading the retrieved chunks yourself.

**Look for:** what did the model do when it did **not** know? Did it say so, or invent something? Which question is unanswerable from the documents, and what did RAG do with it? Were b and d answered correctly with the basic prompt? Check the retrieved chunks: is there more than one version of the relevant policy?

---

## Part 2: Measure and diagnose retrieval (20 minutes)

All commands in this part are free: no API calls.

### Step 1: predict (3 minutes)

The questions have these types: **factual**, **paraphrase** (the question uses different words from the document), **exact term** (an acronym or command), **conflict**, **multi chunk** (the evidence is in two places far apart), **multi hop** (needs two documents), **number confusion**. Write down which two types you expect keyword search (BM25) to find hardest, and why. Then which types you expect semantic search (dense) to handle better, and which worse.

### Step 2: run (4 minutes)

```
python week9_lab_starter.py eval --retriever bm25 --chunk fixed:200:0 --k 3
python week9_lab_starter.py eval --retriever dense --chunk fixed:200:0 --k 3
```

Record `hit@3`, `MRR`, and the **list of questions marked MISS** for each retriever. Compare with your prediction.

### Step 3: the chunking table (6 minutes)

```
python week9_lab_starter.py grid --retrievers bm25,dense --k 3
```

Each cell shows `hit@k / MRR / average context words`. Copy at least **four rows** into your PDF. Then answer:

- Which chunk setting would you choose for each retriever, and why? Consider both the score and the number of context words the model has to read (cost and noise)
- Did overlap help? Look at `fixed:200:0` against `fixed:200:50`. Can you explain what you see? (Hint: how long are the documents?)
- Try `--k 1` and `--k 5` for your chosen setting. What does a larger k buy you, and what does it cost?

### Step 4: write a second chunker (5 minutes)

Implement `chunk_by_heading(doc, max_words)` in the starter. Documents are split into sections that begin with `## `. Pack consecutive sections into one chunk until adding the next section would make the chunk longer than `max_words`; cut any single section that is longer than `max_words`. Then compare:

```
python week9_lab_starter.py grid --retrievers bm25,dense --k 3 --heading
```

Is `heading:250` better, worse, or the same as your best `fixed` setting? Offer one reason, and say whether you think the difference would survive on a bigger corpus.

### Step 5: diagnose two misses (2 minutes)

Choose **two** questions that missed with your best setting (different retrievers or different types if possible). For each, run `eval` and look at the chunk ids it retrieved. Use the printed `top:` list and open the files if you need to. Write: the question; what was retrieved; the **most likely reason** it missed (vocabulary mismatch, evidence split across two chunks, a different chunk with the same words, a chunk too small, k too small, or something else); and **one change** that might fix it.

---

## Part 3: Measure the answers and improve the prompt (15 minutes)

Use the best retrieval setting you found. These commands call the model: about 21 calls per run.

### Step 1: baseline with the basic prompt (3 minutes)

```
python week9_lab_starter.py run-all --prompt v0 --retriever dense --chunk fixed:200:0 --k 3
```

(Use your own best retriever and chunk setting.) It prints a pass/fail line for each question and saves all answers to a `results_*.json` file. The automatic check is a rough heuristic, so **open the results file and read the answers**, especially the failures and these three types: **conflict**, **unanswerable** and **injection**.

### Step 2: write a better prompt (6 minutes)

Edit `build_prompt` in the starter. Think about:

- telling the model to answer **only** from the documents, and exactly what to say if the answer is not there
- showing each chunk's source (`doc_id`, title, date, status) so the model can cite and compare
- what to do when two documents disagree
- what to do with an **instruction found inside a document**

Run `python week9_lab_starter.py run-all --retriever ... --chunk ... --k ...` again (without `--prompt v0`). Compare the number of questions passed with the basic prompt and with yours.

### Step 3: faithfulness spot-check (3 minutes)

The automatic check does not tell you whether an answer is **grounded**. Pick **three** answers from your improved prompt (include one conflict or unanswerable question). For each, list the claims the answer makes and mark whether a retrieved chunk supports each claim (**faithful**: yes or no), and whether the answer addresses the question that was asked (**relevant**: yes or no). Note any claim you cannot point to a passage for.

### Step 4: classify three failures (3 minutes)

Pick **three** questions that failed with either prompt (or that you consider wrong after reading). For each, say which of these it is, and what the first fix would be:

| Failure | What it looks like | First fix to try |
|---|---|---|
| **Retrieval miss** | the needed chunk was not retrieved | change the chunk size, k, or retriever (Part 2) |
| **Context ignored or misread** | the chunk was retrieved but the answer is wrong | prompt: ask for quotes or citations, reduce noise |
| **Conflicting sources** | an outdated document was used | show status and date; tell the model which to prefer |
| **Invented answer** | the answer is not in the documents, but the model gave one | prompt: allow "I could not find this" |
| **Injection followed** | the model obeyed an instruction inside a document | prompt: treat documents as data; filter or review the corpus |
| **Other** | | |

### If generation did not fail

Because the model is strong, some generation problems may not show up for you. That is a valid result and earns the same credit. If the basic prompt already passes the **conflict**, **unanswerable** and **injection** questions, do all of these:

1. **Evidence.** Run `run-all --prompt v0 --repeat 3` and report, for those questions, how many of 3 runs passed
2. **Try to break it.** Write **two questions of your own** that you predict could trip the basic prompt (for example, ask about a topic the documents only touch on, ask in Chinese, or ask something an outdated document would answer differently). Write your prediction first, then report the result
3. **Reflect (4–5 sentences):** why do you think it held up? What would make it fail in a real project (a bigger corpus, more conflicting versions, a user-editable corpus, a different model)? What would you log or test to notice? Why is "it passed today" not enough?

---

## Part 4: Written responses (10 minutes)

**Question 1 (3–5 sentences).** Think of your team's project. What would a knowledge base for it contain, and would you use RAG? Consider the size of the knowledge base (could it simply be placed in the prompt?), how often it changes, and what you learned about which retriever and chunk size worked. If you would **not** use RAG, say why.

**Question 2 (2–4 sentences).** One document in the corpus contains an instruction aimed at AI assistants. Who can write to your project's knowledge base, and what could go wrong if a document there were malicious or simply wrong? Name **two** controls you would use (for example: restrict who can add documents, review additions, show sources to the user, tell the model that retrieved text is data and not instructions, test with known-bad documents).

**Optional extension (not required).** Implement `HybridIndex.search` (reciprocal rank fusion of BM25 and dense) and run `grid --retrievers bm25,dense,hybrid`. Does combining the two help? Which questions does each retriever get right that the other gets wrong?

---

## Submission checklist

- [ ] Name, student ID, team number and model are filled in
- [ ] Part 1: predictions and the with/without retrieval table
- [ ] Part 2: predictions, the retrieval results for both retrievers, a chunking table (at least four rows), your `chunk_by_heading` code, and two diagnosed misses
- [ ] Part 3: the basic-prompt result, your `build_prompt`, the before/after pass counts, the faithfulness spot-check, and three classified failures (or the "did not fail" report)
- [ ] Question 1 and Question 2 are answered
- [ ] Your answers are specific to what you saw
- [ ] No API key appears anywhere
- [ ] Saved as one PDF named `Week9_Lab_<student ID>.pdf`

Upload it on E3 under "Week 9 Lab" by **Wednesday, November 4 (23:59)**.

---

## If things go wrong

| Problem | What to do |
|---|---|
| `Semantic search needs chromadb` | Run `pip install chromadb` |
| The embedding model will not download | Check your network and free disk space; a VPN or proxy can block it. Use `--retriever bm25` meanwhile and tell a TA |
| `ModuleNotFoundError: anthropic` | Run `pip install anthropic` (only needed for Parts 1 and 3) |
| An authentication error | The key is missing or wrong. Reset it, open a **new** terminal if you used `setx`, and rerun |
| "Your credit balance is too low" | Tell a TA. Do not keep retrying |
| Rate limit or "overloaded" | Wait 30 seconds, then retry with a smaller `--repeat` |
| `NotImplementedError: TODO` | That function is yours to write: `chunk_by_heading` in Part 2, `HybridIndex.search` in Part 4 |
| `FileNotFoundError` for corpus or questions | Keep the script, `corpus/` and `eval_questions.json` in one folder, and run from that folder |
| The first dense run is slow | It embeds every chunk once. Results are cached while the program runs |
| Scores differ slightly from a neighbour's | Different chunk or `k` settings. Compare your commands |
