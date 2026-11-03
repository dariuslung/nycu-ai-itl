# Week 9 Lab: Submission

**Name:**
**Student ID:**
**Team number:**
**Model used:** (for example, claude-haiku-5-5)
**Date:**

> How to use this template: copy this file, fill in every section, and save or export it as **one PDF** named `Week9_Lab_<your student ID>.pdf`. Upload it to E3 under "Week 9 Lab" by **Wednesday, November 4, 23:59**.
> You may delete the instruction lines (the ones starting with ">") before you export.
> **Do not include your API key anywhere in this document or in screenshots.**

---

## Part 1: Does retrieval help?

> Write your prediction first. Then run each question with `--no-rag` and with retrieval (`--prompt v0`).

| # | Question | My prediction: will the model know without retrieval? Why? | Answer without retrieval (correct?) | Chunk ids retrieved | Answer with retrieval (correct?) |
|---|---|---|---|---|---|
| a | Which port does the search service listen on? | | | | |
| b | How many approvals does a change to the billing code need? | | | | |
| c | What uptime SLA do Team plan customers get? | | | | |
| d | What is the maximum size of a pull request? | | | | |

**What did the model do when it did not know (say so, or invent)? Which question has no answer in the documents, and what did RAG do with it? Were b and d answered correctly?**

>

---

## Part 2: Measure and diagnose retrieval

### 2.1 Prediction

Which two question types do I expect keyword search (BM25) to find hardest, and why? Which do I expect semantic search (dense) to handle better, and which worse?

>

### 2.2 Results with `fixed:200:0`, k = 3

| Retriever | hit@3 | MRR | Questions marked MISS |
|---|---|---|---|
| bm25 | | | |
| dense | | | |

How do these compare with my prediction?

>

### 2.3 Chunking table

> Copy at least four rows from `grid --retrievers bm25,dense --k 3`. Each cell: hit@k / MRR / average context words.

| Chunking | Chunks | bm25 | dense |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |

- **The setting I would choose for each retriever, and why** (consider the score and the context words):
- **Did overlap help? My explanation:**
- **What did k = 1 and k = 5 do for my chosen setting?**

### 2.4 My `chunk_by_heading` code

```python
# paste your function here
```

- **`heading:250` compared with my best fixed setting** (better / worse / same, and one reason):
- **Would the difference survive on a bigger corpus?**

### 2.5 Two diagnosed misses

**Miss 1**
- **Question and retriever:**
- **What was retrieved** (chunk ids, and what they contain):
- **Most likely reason** (vocabulary mismatch, evidence split across chunks, same words in another chunk, chunk too small, k too small, other):
- **One change that might fix it:**

**Miss 2**
- **Question and retriever:**
- **What was retrieved:**
- **Most likely reason:**
- **One change that might fix it:**

---

## Part 3: Measure the answers and improve the prompt

### 3.1 My retrieval setting

`--retriever ____  --chunk ______  --k __`

### 3.2 Basic prompt (v0) result

- **Questions passed (automatic check):** ___ of 21
- **What I found when I read the answers myself, especially conflict, unanswerable and injection questions:**

>

### 3.3 My `build_prompt`

```python
# paste your function here
```

### 3.4 Before and after

| | Questions passed (of 21) | Notes from reading the answers |
|---|---|---|
| Basic prompt (v0) | | |
| My prompt | | |

### 3.5 Three classified failures

> Failure types: retrieval miss; context ignored or misread; conflicting sources; invented answer; injection followed; other.

| Question | Failure type | Evidence (what the answer said, what was retrieved) | First fix |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

### "Did not fail" report (only if generation did not fail)

> Skip this section if some questions failed. A complete report counts the same as a record of failures.

**Evidence.** `run-all --prompt v0 --repeat 3`: how many of 3 runs passed for the conflict, unanswerable and injection questions?

| Question (type) | Passes out of 3 |
|---|---|
| | |
| | |
| | |

**My own attempts to break it** (prediction written *before* running):

| My question | My prediction and reasoning | What happened |
|---|---|---|
| | | |
| | | |

**Reflection (4–5 sentences):** why it held up; what would make it fail in a real project; what I would log or test; why "it passed today" is not enough.

>

---

## Part 4: Written responses

### Question 1 (3–5 sentences)

What would my team's knowledge base contain, and would we use RAG (consider size, how often it changes, and what I learned about retriever and chunk size)? If not RAG, why not?

>

### Question 2 (2–4 sentences)

Who can write to our project's knowledge base, and what could go wrong if a document there were malicious or wrong? Two controls I would use:

>

---

## Optional: hybrid search

> Skip unless you did the extension. `grid --retrievers bm25,dense,hybrid`: does combining help? Which questions does each retriever get right that the other gets wrong?

>

---

## Final checklist

- [ ] Name, student ID, team number and model are filled in
- [ ] Part 1 table with predictions
- [ ] Part 2: predictions, results for both retrievers, a chunking table with at least four rows, `chunk_by_heading`, two diagnosed misses
- [ ] Part 3: retrieval setting, v0 result, `build_prompt`, before/after, three classified failures (or the "did not fail" report)
- [ ] Question 1 and Question 2 answered
- [ ] No API key appears anywhere
- [ ] Saved as one PDF named `Week9_Lab_<student ID>.pdf`
