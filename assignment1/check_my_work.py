"""check_my_work.py -- a self-check for Assignment 1 (AI-Assisted Software Engineering).

HOW TO USE
    1. Put these files in the same folder:
           task_manager.py     (given to you; you edit it for Task 1 and Task 3)
           my_solutions.py     (you paste your code here for Task 2 and Part 2)
           CONVENTIONS.md      (given to you; read it when you rewrite Prompt 1)
           utils.py            (given to you; read it when you rewrite Prompt 2)
           check_my_work.py    (this file; do not edit it)
    2. Run:   python check_my_work.py
    3. Read the output. Fix what is marked FAIL, then run it again.

WHAT GOES WHERE
    Task 1  Fix get_overdue_tasks directly inside task_manager.py.
    Task 2  Put sort_tasks_by_priority in my_solutions.py (add `from datetime import date`
            at the top if your code needs it).
    Task 3  Paste your docstring into calculate_completion_rate inside task_manager.py.
    Part 2  Paste the code the model gave you into my_solutions.py, with these names:
                Prompt 1 -> add_subtask(tasks, parent_title, subtask_title)
                Prompt 2 -> format_task_line(task, today)
                Prompt 3 -> get_urgent_tasks(tasks, today)
            Do this twice for each prompt: first with the code from the ORIGINAL prompt,
            run this file and save the output; then replace it with the code from your
            REWRITTEN prompt, run this file again and save that output too. FAIL lines
            for the original code are expected: they are your evidence.
            If the model's code needs a class or helper it defined itself (for example
            TaskError), keep it in my_solutions.py too.

IMPORTANT
    * This file checks whether the CODE works. It does not give you marks. Your grade
      comes from your prompts, the model's responses, your reflections and your
      diagnoses, as described in the assignment.
    * Passing a check does not mean your prompt was good, and failing one does not
      mean your diagnosis is right. You still have to explain WHY.
    * Run only your own code. Do not edit the checks to make them pass.
"""
import copy
import importlib
import logging
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

PASS, FAIL, SKIP, WARN, INFO = "PASS", "FAIL", "SKIP", "WARN", "INFO"
SYMBOL = {PASS: "[ok]  ", FAIL: "[FAIL]", SKIP: "[skip]", WARN: "[warn]", INFO: "[info]"}
results = []


def report(status, label, detail=""):
    results.append(status)
    print(f"  {SYMBOL[status]} {label}")
    if detail:
        for line in str(detail).splitlines():
            print(f"         {line}")


def header(title):
    print(f"\n{title}\n" + "-" * len(title))


def load(name):
    """Import a module from this folder. Returns (module, error_message)."""
    try:
        if name in sys.modules:
            del sys.modules[name]
        return importlib.import_module(name), None
    except ModuleNotFoundError as e:
        if e.name == name:
            return None, f"Could not find {name}.py in this folder ({HERE})."
        return None, f"{name}.py imports something that is missing: {e}"
    except Exception as e:  # SyntaxError, NameError at import time, etc.
        return None, f"{name}.py has an error when loaded: {type(e).__name__}: {e}"


def t(title, due, priority="medium", done=False):
    return {"title": title, "due_date": due, "priority": priority, "completed": done}


def get_fn(mod, name):
    fn = getattr(mod, name, None) if mod else None
    return fn if callable(fn) else None


def missing(label, err, hint):
    """A function was not found: skip if nothing was pasted yet, FAIL if the file is broken."""
    if err and not err.startswith("Could not find"):
        return report(FAIL, label, err + "\nFix this first: nothing in the file can be checked until it loads.")
    return report(SKIP, label, hint)


# --------------------------------------------------------------------------
# Part 1, Task 1: get_overdue_tasks  (in task_manager.py)
# --------------------------------------------------------------------------
def check_task1(tm, tm_err):
    header("Part 1, Task 1: get_overdue_tasks (task_manager.py)")
    fn = get_fn(tm, "get_overdue_tasks")
    if fn is None:
        return report(FAIL, "get_overdue_tasks not available", tm_err or "Function not found.")
    today = date(2026, 10, 12)
    tasks = [
        t("late", date(2026, 10, 3), "high"),
        t("no date yet", None, "low"),
        t("later", date(2026, 10, 20)),
        t("late but finished", date(2026, 10, 1), done=True),
        t("due today", today),
        t("finished, no date", None, done=True),
    ]
    try:
        out = fn(copy.deepcopy(tasks), today)
    except Exception as e:
        return report(FAIL, "runs on a list that includes tasks without a due date",
                      f"It crashed: {type(e).__name__}: {e}\n"
                      "Hint: which line runs first for a task whose due_date is None?")
    report(PASS, "runs on a list that includes tasks without a due date")
    got = [x["title"] for x in out]
    if got == ["late"]:
        report(PASS, "returns exactly the unfinished tasks whose due date is before today")
    else:
        report(FAIL, "returns exactly the unfinished tasks whose due date is before today",
               f"Expected ['late'], got {got}.\n"
               "Remember: due today is not overdue, finished tasks are not overdue, "
               "and decide what a task with no due date should mean.")
    try:
        ok = fn([], today) == []
    except Exception as e:
        ok = False
        report(FAIL, "returns [] for an empty list", f"{type(e).__name__}: {e}")
    else:
        report(PASS if ok else FAIL, "returns [] for an empty list")
    # a second, different mix: undated task that is NOT finished comes first in the list
    try:
        out2 = fn([t("undated", None), t("old", date(2026, 9, 1))], today)
        report(PASS if [x["title"] for x in out2] == ["old"] else FAIL,
               "an unfinished undated task does not hide or break a later overdue task",
               "" if [x["title"] for x in out2] == ["old"] else
               f"Expected ['old'], got {[x['title'] for x in out2]}.")
    except Exception as e:
        report(FAIL, "an unfinished undated task does not hide or break a later overdue task",
               f"{type(e).__name__}: {e}")


# --------------------------------------------------------------------------
# Part 1, Task 2: sort_tasks_by_priority  (in my_solutions.py)
# --------------------------------------------------------------------------
def check_task2(ms, ms_err):
    header("Part 1, Task 2: sort_tasks_by_priority (my_solutions.py)")
    fn = get_fn(ms, "sort_tasks_by_priority")
    if fn is None:
        return missing("sort_tasks_by_priority not found yet", ms_err,
                       "Paste your function into my_solutions.py to check it.")
    tasks = [
        t("low, dated", date(2026, 10, 4), "low"),
        t("high, no date", None, "high"),
        t("high, early", date(2026, 10, 6), "high"),
        t("medium", date(2026, 10, 5), "medium"),
        t("high, late", date(2026, 10, 14), "high"),
        t("medium, no date", None, "medium"),
        t("high, early (second)", date(2026, 10, 6), "high"),
    ]
    original = copy.deepcopy(tasks)
    try:
        out = fn(tasks)
    except Exception as e:
        return report(FAIL, "runs on a list that mixes priorities and missing due dates",
                      f"It crashed: {type(e).__name__}: {e}")
    report(PASS, "runs on a list that mixes priorities and missing due dates")
    expected = ["high, early", "high, early (second)", "high, late", "high, no date",
                "medium", "medium, no date", "low, dated"]
    got = [x["title"] for x in out] if isinstance(out, list) else out
    report(PASS if got == expected else FAIL, "order is correct (priority, then due date, undated last in each tier)",
           "" if got == expected else f"Expected: {expected}\nGot:      {got}")
    report(PASS if tasks == original else FAIL, "does not modify the list you passed in",
           "" if tasks == original else "The original list changed. The spec says to return a NEW list.")
    report(PASS if out is not tasks else FAIL, "returns a new list object")
    try:
        report(PASS if fn([]) == [] else FAIL, "returns [] for an empty list")
    except Exception as e:
        report(FAIL, "returns [] for an empty list", f"{type(e).__name__}: {e}")


# --------------------------------------------------------------------------
# Part 1, Task 3: docstring of calculate_completion_rate  (in task_manager.py)
# --------------------------------------------------------------------------
def check_task3(tm, tm_err):
    header("Part 1, Task 3: calculate_completion_rate docstring (task_manager.py)")
    fn = get_fn(tm, "calculate_completion_rate")
    if fn is None:
        return report(FAIL, "calculate_completion_rate not available", tm_err or "Function not found.")
    # the function itself must still work
    try:
        four = [t("a", None, done=True), t("b", None), t("c", None), t("d", None)]
        ok = fn([]) == 0.0 and fn(four) == 0.25
    except Exception:
        ok = False
    report(PASS if ok else FAIL, "the function still behaves the same (you only add a docstring)")
    doc = fn.__doc__
    if not doc or not doc.strip():
        return report(SKIP, "docstring not added yet", "Paste your docstring inside the function.")
    first = doc.strip().splitlines()[0].strip()
    report(PASS if first else FAIL, "starts with a one-line summary", f"First line: {first!r}")
    report(PASS if "Args:" in doc else FAIL, "has an Args: section, like add_task and mark_complete")
    report(PASS if "Returns:" in doc else FAIL, "has a Returns: section, like add_task and mark_complete")
    low = doc.lower()
    report(PASS if "tasks" in low else WARN, "documents the tasks parameter")
    if "percent" in low and "fraction" not in low:
        report(WARN, "check what the function really returns",
               "Your docstring says 'percent' but never says 'fraction'. "
               "Call the function on a list with 1 of 4 tasks done and read the number.")
    if "empty" not in low and "0.0" not in doc:
        report(WARN, "what does it return for an empty list?",
               "Run it on [] and consider whether your docstring says what happens.")


# --------------------------------------------------------------------------
# Part 2: the code from your ORIGINAL prompts and from your REWRITES (my_solutions.py)
# --------------------------------------------------------------------------
def check_p1(ms, ms_err):
    header("Part 2, Prompt 1: add_subtask (my_solutions.py)")
    fn = get_fn(ms, "add_subtask")
    if fn is None:
        return missing("add_subtask not found yet", ms_err,
                       "Paste the code for Prompt 1 into my_solutions.py.")

    def fresh():
        return [t("Write report", date(2026, 10, 20), "high"), t("Buy milk", None, "low")]

    tasks = fresh()
    result, ran = None, False
    try:
        result = fn(tasks, "Write report", "Draft intro")
        ran = True
        report(PASS, "runs when the parent task exists")
    except Exception as e:
        report(FAIL, "runs when the parent task exists", f"It crashed: {type(e).__name__}: {e}")

    try:
        fn(fresh(), "No such task", "x")
        report(FAIL, "Convention 1: a missing parent task raises TaskError",
               "Nothing was raised for a task that does not exist.")
    except Exception as e:
        ok = type(e).__name__ == "TaskError" and isinstance(e, Exception)
        report(PASS if ok else FAIL, "Convention 1: a missing parent task raises TaskError",
               "" if ok else f"It raised {type(e).__name__}; see CONVENTIONS.md item 1.")

    if ran:
        report(PASS if result is tasks else FAIL, "Convention 2: returns the updated task list",
               "" if result is tasks else f"It returned {type(result).__name__}, not the task list you passed in.")
    else:
        report(SKIP, "Convention 2: returns the updated task list", "The function did not run.")

    try:
        t3 = fresh()
        fn(t3, "  write REPORT ", "x")
        report(PASS, "Convention 3: title matching ignores case and surrounding spaces")
    except Exception as e:
        report(FAIL, "Convention 3: title matching ignores case and surrounding spaces",
               f"'  write REPORT ' did not find 'Write report' ({type(e).__name__}).")

    if ran:
        parent = tasks[0]
        subs = parent.get("subtasks") if isinstance(parent, dict) else None
        problems = []
        if not isinstance(subs, list) or len(subs) != 1:
            problems.append("expected a list under the key \"subtasks\" with exactly one subtask")
        elif not isinstance(subs[0], dict):
            problems.append("the subtask should be a dict like any other task")
        else:
            s = subs[0]
            want = {"title": "Draft intro", "due_date": None, "priority": "high", "completed": False}
            for k, v in want.items():
                if k not in s:
                    problems.append(f"subtask is missing the key {k!r}")
                elif s[k] != v:
                    problems.append(f"subtask[{k!r}] is {s[k]!r}, expected {v!r}")
        report(PASS if not problems else FAIL, "Convention 4: the subtask is stored the way the team expects",
               "\n".join(problems))
    else:
        report(SKIP, "Convention 4: the subtask is stored the way the team expects", "The function did not run.")

    doc = fn.__doc__ or ""
    report(PASS if ("Args:" in doc and "Returns:" in doc) else FAIL,
           "Convention 5: Google-style docstring with Args: and Returns:")


def check_p2(ms, ms_err, ut, ut_err):
    header("Part 2, Prompt 2: format_task_line (my_solutions.py)")
    fn = get_fn(ms, "format_task_line")
    if fn is None:
        return missing("format_task_line not found yet", ms_err,
                       "Paste the code for Prompt 2 into my_solutions.py.")
    if get_fn(ut, "due_label") is None:
        return report(FAIL, "utils.py with due_label is needed for this check", ut_err or "due_label not found.")
    today = date(2026, 10, 23)
    cases = [t("Submit A1", date(2026, 10, 26), "high"),
             t("Old report", date(2026, 10, 20), "low"),
             t("Someday", None, "medium")]
    lines = []
    for task in cases:
        try:
            lines.append(fn(copy.deepcopy(task), today))
        except Exception as e:
            return report(FAIL, "runs on tasks with and without a due date",
                          f"It crashed on {task['title']!r}: {type(e).__name__}: {e}")
    report(PASS, "runs on tasks with and without a due date")
    ok = all(isinstance(s, str) and "\n" not in s for s in lines)
    report(PASS if ok else FAIL, "returns a single line of text", "" if ok else f"Got: {lines!r}")
    missing_bits = [f"{task['title']!r}: no {w!r} in {s!r}"
                    for task, s in zip(cases, lines) if isinstance(s, str)
                    for w in (task["title"], task["priority"]) if w not in s]
    report(PASS if not missing_bits else FAIL, "each line shows the task's title and priority",
           "\n".join(missing_bits))
    bad = []
    for task, s in zip(cases, lines):
        want = ut.due_label(task["due_date"], today)
        if not isinstance(s, str) or want not in s:
            bad.append(f"{task['title']!r}: expected the text {want!r} in {s!r}")
    report(PASS if not bad else FAIL, "the due-date wording is exactly what the team's helper in utils.py produces",
           "\n".join(bad))


def check_p3(ms, ms_err):
    header("Part 2, Prompt 3: get_urgent_tasks (my_solutions.py)")
    fn = get_fn(ms, "get_urgent_tasks")
    if fn is None:
        return missing("get_urgent_tasks not found yet", ms_err,
                       "Paste the code for Prompt 3 into my_solutions.py.")
    today = date(2026, 10, 23)
    tasks = [
        t("overdue, medium", date(2026, 10, 20), "medium"),
        t("overdue but finished", date(2026, 10, 19), "medium", True),
        t("due today, low", date(2026, 10, 23), "low"),
        t("due in 2 days, medium", date(2026, 10, 25), "medium"),
        t("due in 3 days, low", date(2026, 10, 26), "low"),
        t("due in 4 days, medium", date(2026, 10, 27), "medium"),
        t("due in 10 days, high", date(2026, 11, 2), "high"),
        t("no date, high", None, "high"),
        t("no date, medium", None, "medium"),
        t("no date, high, finished", None, "high", True),
    ]
    original = copy.deepcopy(tasks)
    try:
        out = fn(tasks, today)
    except Exception as e:
        return report(FAIL, "runs on a mixed list of tasks", f"It crashed: {type(e).__name__}: {e}")
    report(PASS, "runs on a mixed list of tasks")
    if not isinstance(out, list):
        return report(FAIL, "returns a list", f"Got {type(out).__name__}.")
    got = [x["title"] for x in out]
    rules = [
        ("includes unfinished overdue tasks", ["overdue, medium"], True),
        ("leaves out finished tasks", ["overdue but finished", "no date, high, finished"], False),
        ("includes a task due today and one due in exactly 3 days", ["due today, low", "due in 3 days, low"], True),
        ("leaves out a task due in 4 days (not high priority)", ["due in 4 days, medium"], False),
        ("includes a high-priority task even when it is due later or has no date",
         ["due in 10 days, high", "no date, high"], True),
        ("leaves out an unfinished medium task with no date", ["no date, medium"], False),
    ]
    for label, titles, should_be_in in rules:
        wrong = [x for x in titles if (x in got) != should_be_in]
        report(PASS if not wrong else FAIL, label,
               "" if not wrong else ("Missing: " if should_be_in else "Should not be there: ") + ", ".join(wrong))
    expected = ["overdue, medium", "due today, low", "due in 2 days, medium", "due in 3 days, low",
                "due in 10 days, high", "no date, high"]
    if set(got) == set(expected):
        report(PASS if got == expected else FAIL, "ordered earliest due date first, undated tasks last",
               "" if got == expected else f"Expected: {expected}\nGot:      {got}")
    else:
        report(SKIP, "ordered earliest due date first, undated tasks last",
               "Fix which tasks are included first; the order check needs the right set.")
    report(PASS if tasks == original else FAIL, "does not modify the list you passed in")


# --------------------------------------------------------------------------
def main():
    print("Assignment 1 self-check")
    print("This checks your code. It does not give you a grade.")
    tm, tm_err = load("task_manager")
    ms, ms_err = load("my_solutions")
    ut, ut_err = load("utils")
    check_task1(tm, tm_err)
    check_task2(ms, ms_err)
    check_task3(tm, tm_err)
    check_p1(ms, ms_err)
    check_p2(ms, ms_err, ut, ut_err)
    check_p3(ms, ms_err)
    header("Summary")
    print(f"  {results.count(PASS)} passed, {results.count(FAIL)} failed, "
          f"{results.count(WARN)} warnings, {results.count(SKIP)} not started yet")
    if results.count(FAIL):
        print("  Read the FAIL lines above. They say what the check saw, not why it happened.")
        print("  For Part 2, FAIL lines on the ORIGINAL code are your evidence; keep this output.")
    print("  Reminder: a passing check is not the same as a well-diagnosed prompt.\n")


if __name__ == "__main__":
    main()
