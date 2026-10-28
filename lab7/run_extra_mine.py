"""Extra V0 queries for modes 3 and 4 (did-not-fail report). Does not modify TOOLS_V0."""
import sys
import week7_lab_starter as w

pass
n = 5
FILLER = ("I had a long day: my laptop updated, the cafeteria was out of rice, my team argued about "
          "naming a repository, and the bus was late. Anyway, unrelated to that, ")

SETS = {
  "Mode 3, own queries (starter condition)": [
    "What is 12 plus 30?",
    "How many days are in a week?",
    "Name the three primary colors.",
  ],
  "Mode 3, Step B: predicted to break": [
    "What is 7 times 8?",
    "What is 100 minus 1?",
  ],
  "Mode 3, changed conditions": [
    "法國的首都是哪裡？",                                   # Chinese
    FILLER + "what is 3 plus 4?",                          # irrelevant context
    "wat is the capitol of Frnace",                         # misspelled
  ],
  "Mode 4, own queries (starter condition)": [
    "What is the deadline for CP1?",
    "What does the code steward do in this course?",
    "What is 73 times 8191?",                               # true answer: 597943
  ],
  "Mode 4, Step B: predicted to break": [
    "How many deliverables does CP1 have?",
    "Is Assignment 1 due before or after the Week 7 lab?",
  ],
  "Mode 4, changed conditions": [
    "code steward 是做什麼的？",                            # Chinese
    "wk 6 stuff",                                           # vague
    "cp 1 deadlin",                                         # misspelled
    FILLER + "when is assignment 1 due?",                   # irrelevant context
  ],
}
for name, qs in SETS.items():
    print(f"\n===== {name} =====", flush=True)
    w.run_repeated(qs, n)
