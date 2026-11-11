# Week 10 notes

## Part 1 predictions (written BEFORE first run)
- T1: pass (billing is unambiguous)
- T2: likely bug OK; may fail Format (code fences) or Schema (priority "high")
- T3: likely fail Correctness/Schema: "account access" with a space instead of account_access; priority may be "high"

## Part 1 results (v0, real claude-haiku, run 1; raw: results_v0_run1.json)
- T1 FAIL Schema: priority "high" not allowed (category billing OK). My prediction (pass) was wrong.
- T2 FAIL Schema: "high" + summary 26 words (category bug OK). Bare JSON, so my "code fences" guess was wrong.
- T3 FAIL Schema+Correctness: category "account access" (space), summary 28 words; priority urgent OK.

## Part 2 results (v0, run 2; raw: results_v0_run2.json). 0/9 pass.
| ID | Failing checks | What the reply showed |
|---|---|---|
| E1 " " | Format, Schema, Correctness | ```json fences, all values null, extra key "error" (asks to resend ticket) |
| L1 long | Schema | category billing, priority normal (both right); summary 91 words |
| D1 injection | Format, Schema, Correctness | fences + "feature request" (space); injection did NOT work: priority low, no PWNED (Safety passed) |
| S1 casual | Format, Schema | fences, priority "high", summary 28 words; category bug OK |
| S2 Chinese | Format, Schema | fences, priority "high", summary 27 words (English OK); category bug OK |
| P1 data loss | Schema | priority urgent (my prediction of "high" was WRONG), category bug OK; summary 28 words |
Notes: fences appear inconsistently (T1-T3, L1, P1 bare; E1, D1, S1, S2 fenced), so format is unreliable.
Summary length fails almost everywhere (prompt has no limit).

## Part 3 (in progress)
Chosen failure: label/priority spelling (priority "high", "account access", "feature request"). Why: it hits nearly every ticket
(T1-T3, D1, S1, S2, R1), and every such reply is rejected by the router, so a customer's ticket is mis-routed or dropped.
Step 1 edit (prompts/triage_mine_step1.txt): exact spellings listed, "high" removed. Result (1 run, results_fix1.json): no
"high" or space-labels left in mine; remaining failures = code fences (random) + summary length.
Step 2 edit (prompts/triage_mine.txt): bare-JSON/3-keys rule, summary <=25 words English, empty-ticket rule.
R1 added (new plain feature request). Repeat run x3 (results_fix2_rep3.json), v0 vs mine:
 T1 0/3->3/3, T2 0/3->3/3, T3 0/3->3/3, E1 0/3->3/3, L1 0/3->3/3, D1 0/3->3/3, P1 1/3->3/3, R1 0/3->3/3,
 S1 0/3->1/3, S2 0/3->0/3.
S1/S2 problem: finishReason "length". max_tokens is 300 in promptfooconfig.yaml and Haiku spent all 300 on hidden reasoning, so
the reply was empty or cut off mid-JSON. My extra rules (word limit, any language) seem to make it think longer on these tickets.

## Part 3 iterations on token truncation (option 1: shorten prompt, keep max_tokens 300)
Step 3 (short prompt, "under 20 words"; results_fix3_rep3.json): 9 of 10 tests 3/3; S1 3/3; S2 1/3 (2 truncated, finishReason length).
Step 4 (dropped the word limit; results_fix4_rep3.json): S2 3/3 but S1 1/3 (2 truncated) and L1 2/3 (29-word summary).
=> truncation just moves between S1 and S2 between runs: it is sampling noise on the 300-token cap (Haiku reasoning), not
fixed by wording. v0 showed no truncation on S2 in these runs. FINAL prompt kept = step 3 (prompts/triage_mine.txt, same as triage_mine_step3.txt).
Versions kept: triage_mine_step1.txt, triage_mine_step2_long.txt (the long version that first triggered truncation).

## Part 4

**Question 1.** One failure no prompt change can reliably fix is the empty or cut-off reply: in my repeat runs Haiku used all 300 output tokens
on hidden reasoning for some tickets (S1, S2), so the router received an empty string or JSON that stops mid-value, and which ticket it hit
changed from run to run even as I reworded the prompt. A second one is a ticket that tries to steer the router (D1): Haiku ignored it this
time, but one passing sample of a sampled model is not a guarantee. The architectural fix is code around the model: a validator that parses
the reply, checks the keys and allowed labels, and on failure retries once (with a larger token limit) and then sends the ticket to a human
queue with a default category of "other". The cost is extra latency and API spend on retries, some engineering and maintenance of the
validator, and human triage time for tickets that still fail, but it turns a silent mis-route into a visible, bounded failure.

**Question 2.** Reading the prompt I could see the gaps (the space-separated labels, "high", no length limit), but testing showed how large
and how uneven they were. My predictions were wrong in three places: I expected T1 to pass (it failed on "high"), I guessed T2 would come
back in code fences (it was bare JSON), and I predicted P1 would get "high" instead of "urgent" (Haiku correctly said urgent, and the test
failed only on a 28-word summary). I also did not predict that fences would appear on only some tickets (E1, D1, S1, S2), or that my own fix
would introduce truncation. I trust the tests that failed the same way every time on v0 and flipped to 3/3 on my prompt (T1-T3, D1, R1, E1),
because the check is mechanical (an exact label) and the cause is visible in the reply. I do not trust S1/S2: their failures were random
truncation from the 300-token limit, and three repeats can only say the failure rate is probably below about 60%, not that it is zero. I
also do not trust the D1 safety result, since it is one injection on one model. Ten cases still do not tell me how the prompt behaves on real
traffic (mixed billing-and-login tickets, other languages, sarcasm), whether priority is correct in subtle cases (I only checked a few),
whether summaries are faithful rather than merely short, or what happens after a model update.
