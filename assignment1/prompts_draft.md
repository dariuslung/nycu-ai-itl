# Draft prompts (edit freely; send each in a FRESH conversation)

For every run: paste the full `task_manager.py` first, then the prompt.
Save the full, unedited response.

---
## Part 1

### Task 1 — Chain-of-Thought

```
Here is `get_overdue_tasks`. It crashes with
`TypeError: '<' not supported between instances of 'NoneType' and 'datetime.date'`
when a task has no due date, which `add_task` allows by default.

Think step by step before writing any code:
1. Trace the function line by line for a task whose `due_date` is None and say exactly which expression raises.
2. Trace what happens for a completed task with no due date, and a task due today.
3. Decide what "overdue" should mean for a task with no due date and justify it.
Then give the corrected function.
```

Response:

````
### 1. Line-by-Line Trace with `due_date = None`

Assuming standard task structures and a typical implementation of `get_overdue_tasks`:

```python
def get_overdue_tasks(tasks, today=None):
    if today is None:
        today = datetime.date.today()
    overdue = []
    for task in tasks:
        # Check completion or due date
        if not task.get("completed") and task.get("due_date") < today:  # <--- CRASH
            overdue.append(task)
    return overdue

```

**Tracing a task where `task["due_date"] is None` and `task["completed"] is False`:**

1. The loop evaluates the condition: `if not task.get("completed") and task.get("due_date") < today:`.
2. `not task.get("completed")` evaluates to `True`.
3. Due to short-circuit evaluation, Python proceeds to evaluate the second operand: `task.get("due_date") < today`.
4. `task.get("due_date")` evaluates to `None`.
5. The comparison `None < today` executes.
6. **Exact Expression That Raises:** `task.get("due_date") < today` (specifically the `<` operator between `None` and an instance of `datetime.date`). Python 3 does not define an order comparison between `NoneType` and `datetime.date`, raising `TypeError: '<' not supported between instances of 'NoneType' and 'datetime.date'`.

---

### 2. Trace for Edge Cases

* **Completed task with no due date (`completed=True`, `due_date=None`):**
* The condition `not task.get("completed") and ...` evaluates `not task.get("completed")` first.
* Because `task.get("completed")` is `True`, `not True` evaluates to `False`.
* Python short-circuits and skips evaluating `task.get("due_date") < today` entirely.
* Therefore, it does **not** crash; the task is simply ignored. However, if the condition checks the date before completion (e.g., `if task.get("due_date") < today and not task.get("completed")`), it raises `TypeError` regardless of completion status.


* **Task due today (`due_date == today`):**
* Assuming `task.get("due_date")` is a `datetime.date` equal to `today`.
* The comparison evaluates `today < today`, which returns `False`.
* The task is not considered overdue on the day it is due (it remains valid until the day passes).



---

### 3. Semantics: What "Overdue" Means for Tasks Without Due Dates

A task without a due date **should never be considered overdue**.

**Justification:**

* **Definition of "Overdue":** By definition, an item is overdue only if a deadline was established and that deadline has elapsed.
* **Intent of Optional Deadlines:** In task tracking systems, allowing a task to exist without a `due_date` designates it as an open-ended backlog item or a general "to-do." Treating it as overdue would falsely trigger urgent alerts and clutter prioritized views.
* **Safety / Invariant:** Without a deadline, the elapsed-time condition cannot be satisfied. Therefore, a task must have a non-null `due_date` as a prerequisite before any date comparisons take place.

---

### Corrected Function

To fix the crash, ensure `task.get("due_date") is not None` is verified before evaluating whether the date precedes `today`:

```python
import datetime


def get_overdue_tasks(tasks, today=None):
    """Return all incomplete tasks whose due date has passed.

    Tasks without a due date are never considered overdue.
    """
    if today is None:
        today = datetime.date.today()

    overdue = []
    for task in tasks:
        # Task must be incomplete, have a due date set, and that date must precede today
        due_date = task.get("due_date")
        is_completed = task.get("completed", False)

        if not is_completed and due_date is not None and due_date < today:
            overdue.append(task)

    return overdue

```
````

### Task 1 — Step-back

```
Here is `get_overdue_tasks`, which crashes with
`TypeError: '<' not supported between instances of 'NoneType' and 'datetime.date'`
for tasks without a due date.

First, step back: in general, what is the principle for safely comparing or filtering on optional values (values that may be None) in a collection, and what design choices exist for what a missing value should mean? Answer this in general terms, without referring to this code.
Then apply that principle to `get_overdue_tasks` and give the corrected function.
```

Response:

````
### Safely Handling and Filtering Optional Values

When filtering or ordering collections containing optional values (`None`, `null`, `nil`), comparisons crash if the language's comparison operators require non-null operands. Safely operating on such data requires establishing explicit semantics for missing values before evaluation.

#### The Core Principle: Guard or Transform

To prevent runtime type errors, evaluate optional values using one of two strategies:

1. **Explicit Guarding (Short-circuiting):** Check whether the value exists before executing the comparison. If the value is `None`, branch immediately to a default classification without evaluating the relational operator.
2. **Value Normalization (Coalescing / Sentinel Values):** Map `None` to a concrete sentinel value that naturally sorts or compares according to the intended business logic (e.g., treating `None` as positive infinity $+\infty$ or negative infinity $-\infty$).

#### Design Choices for What "Missing" Means

A missing value carries no inherent mathematical or chronological meaning; its interpretation is a domain design decision:

* **Excluded by Default (Strict Match):** Missing values do not satisfy the condition. For example, in a filter checking for items satisfying `value < threshold`, an item with no value is disqualified immediately.
* **Included by Default (Permissive Match):** Missing values are assumed to meet the criteria (or are handled as "unbounded/always applicable").
* **Sort Semantics (`NULLS FIRST` vs. `NULLS LAST`):**
* **Missing as $+\infty$:** Placing missing values at the end of an ascending sort, meaning they are considered greater than any known value (e.g., an unscheduled task has no deadline and cannot expire).
* **Missing as $-\infty$:** Placing missing values at the beginning of an ascending sort, meaning they are treated as already past or having maximum priority.


* **Segregation (Partitioning):** Splitting the collection into two separate sets (e.g., items with values evaluated normally, and a separate bucket for items lacking values) to avoid forcing an arbitrary comparison.

---

### Application to `get_overdue_tasks`

In task management, a task lacking a `due_date` represents an unscheduled or open-ended task. It cannot be "overdue" because no deadline was ever set or missed. Therefore, the appropriate design choice is **Excluded by Default**: a task must possess a valid date **and** that date must precede the reference date.

#### Corrected Function

Assuming standard dictionary or object models, use short-circuit evaluation (`and`) to ensure the comparison executes only when `due_date is not None`.

```python
from datetime import date


def get_overdue_tasks(tasks, current_date=None):
    """Filter and return tasks whose due date is strictly before current_date.

    Tasks without a due date (None) are treated as not overdue.
    """
    if current_date is None:
        current_date = date.today()

    # Supports either dict-like objects (task.get('due_date'))
    # or attribute-based objects (task.due_date)
    return [
        task
        for task in tasks
        if (due := getattr(task, "due_date", None) or (task.get("due_date") if isinstance(task, dict) else None)) is not None
        and due < current_date
    ]

```

If your tasks are standard dictionaries structured as `{"due_date": ...}`:

```python
from datetime import date


def get_overdue_tasks(tasks, current_date=None):
    if current_date is None:
        current_date = date.today()

    return [
        task
        for task in tasks
        if task.get("due_date") is not None and task["due_date"] < current_date
    ]

```

Because Python evaluates logical `and` from left to right with short-circuiting, `task["due_date"] < current_date` is never evaluated when `task.get("due_date") is None`.
````

### Task 2 — Zero-shot

```
Write a function `sort_tasks_by_priority(tasks)` for this module. It returns a new list (the input list must not be modified) sorted so that higher-priority tasks come first ("high", then "medium", then "low"). Within the same priority, tasks with earlier due dates come first, and tasks with no due date (None) come last within their priority tier.
```

### Task 2 — Self-correction (one conversation, three turns)

Turn 1: send the Zero-shot prompt above (identical).

Response:
````
```python
from datetime import date, datetime
from typing import Any, Dict, List


def sort_tasks_by_priority(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sorts tasks by priority tier, then due date, without modifying the input list.

    Priority order:
        1. "high"
        2. "medium"
        3. "low"

    Within each priority:
        - Earlier due dates come first.
        - Tasks with due date `None` come last.
    """
    priority_order = {"high": 0, "medium": 1, "low": 2}

    def sort_key(task: Dict[str, Any]):
        # Tasks with unrecognized priority default to the lowest tier
        priority_rank = priority_order.get(task.get("priority", "").lower(), 3)
        due_date = task.get("due_date")

        # False sorts before True, placing tasks with due dates before None
        has_no_due_date = due_date is None

        return (priority_rank, has_no_due_date, due_date)

    return sorted(tasks, key=sort_key)

```

### Key Implementation Details

* **Input Immutability:** Uses Python's built-in `sorted()`, which constructs and returns a new list rather than calling `.sort()` in-place.
* **Tie-Breaking `None` Values:** Python cannot directly compare `datetime.date` objects with `None` via `<`. The tuple key handles this by using a boolean flag `has_no_due_date`:
* `False` (0) for tasks that have a date.
* `True` (1) for tasks where `due_date is None`.


* **Date Formats:** The tuple comparison handles standard `datetime.date`, `datetime.datetime`, or ISO 8601 string dates (`"YYYY-MM-DD"`).
````

Turn 2 (critique; tailor to what the model actually wrote — keep it specific):

```
Review your code critically against the spec. Check specifically: (1) does it crash or misorder when due_date is None, since None cannot be compared with a date? (2) does it mutate the input list or its tasks? (3) how does it handle a priority value outside high/medium/low? (4) is the order stable for tasks with equal priority and equal due date? List each problem you find, or state explicitly that the check passed and why.
```

Response:
````
### 1. Does it crash or misorder when `due_date` is `None`?

**Verdict: Passed.**

Python compares tuples lexicographically element-by-element and short-circuits as soon as a mismatch is found.

The sort key produces `(priority_rank, has_no_due_date, due_date)`:

* **Between a dated task and a `None` task:** The second element is compared first (`False` vs `True`). Because `False < True` evaluates to `True`, Python determines the relative order immediately. It never advances to comparing the third tuple elements (`date` vs `None`), preventing a `TypeError`.
* **Between two `None` tasks:** The second element ties (`True == True`), and Python proceeds to compare `None == None`, which succeeds without raising an exception.
* **Between two dated tasks:** The second element ties (`False == False`), and Python compares the two valid date values directly.

---

### 2. Does it mutate the input list or its tasks?

**Verdict: Passed.**

* **List mutation:** `sorted(tasks, ...)` allocates and returns a completely new list object; the original container is untouched.
* **Task mutation:** The key function uses read-only lookups (`task.get(...)`) and does not reassign, pop, or modify any dictionary keys or nested values.

---

### 3. How does it handle a priority value outside "high" / "medium" / "low"?

**Verdict: Potential Spec Mismatch (Problem identified).**

* **Current behavior:** Unrecognized or missing priority values default to rank `3` via `.get(..., 3)`. They are grouped together after `"low"` priority tasks. Additionally, `.lower()` is called on the string, making inputs like `"HIGH"` or `"Medium"` match valid tiers.
* **Potential issues:**
1. The specification defines priority tiers strictly as `"high"`, then `"medium"`, then `"low"`, without specifying whether case-folding or an implicit fourth fallback tier is acceptable.
2. If tasks with non-standard priorities (or non-string priorities like `None` or integers) are passed, `.lower()` can raise an `AttributeError` (e.g., if `task.get("priority")` is `None`, `"".lower()` works, but if `priority` is `123`, `123.lower()` fails).
3. Depending on the desired system contract, unexpected values should either raise a `ValueError` / `KeyError` or explicitly map to a defined fallback behavior.



---

### 4. Is the order stable for tasks with equal priority and equal due date?

**Verdict: Passed.**

Python's built-in sorting algorithm (Timsort) is guaranteed to be stable. When two tasks produce identical sort keys—same priority rank, same `has_no_due_date` boolean, and equal `due_date` values (including two `None` values)—their relative order from the original input list is preserved.
````

Turn 3:

```
Now revise the function to fix every problem you listed, and show the final complete code.
```

Response:
````
Here is the revised, robust implementation. It explicitly enforces the specified priority values (`"high"`, `"medium"`, `"low"`), rejects invalid or missing priorities with a clear `ValueError`, and maintains all tie-breaking and immutability guarantees.

```python
from typing import Any, Dict, List, Mapping


def sort_tasks_by_priority(tasks: List[Mapping[str, Any]]) -> List[Mapping[str, Any]]:
    """Sorts tasks by priority tier, then due date, without modifying the input list.

    Priority order:
        1. "high"
        2. "medium"
        3. "low"

    Within each priority:
        - Earlier due dates come first.
        - Tasks with due date `None` come last.
        - Tasks with identical priority and due date preserve their original order (stable sort).

    Raises:
        ValueError: If a task is missing the 'priority' key or contains an
                    unrecognized priority value outside {'high', 'medium', 'low'}.
    """
    priority_order = {"high": 0, "medium": 1, "low": 2}

    def sort_key(task: Mapping[str, Any]):
        priority = task.get("priority")
        if priority not in priority_order:
            raise ValueError(
                f"Invalid or missing task priority: {priority!r}. "
                f"Expected one of: {list(priority_order.keys())}"
            )

        due_date = task.get("due_date")
        # False (0) sorts before True (1).
        # Short-circuits comparison to avoid `date < None` TypeError.
        has_no_due_date = due_date is None

        return (priority_order[priority], has_no_due_date, due_date)

    return sorted(tasks, key=sort_key)

```

### Changes Made

1. **Strict Priority Validation:** Replaced silent fallback ranking (`3`) and `.lower()` with an explicit `priority in priority_order` membership check. Unrecognized strings, non-string types (e.g., `int`, `None`), or missing priority keys fail fast with a `ValueError`.
2. **Crash-Free Due Date Handling:** Retained the `(rank, has_no_due_date, due_date)` tuple structure. Because Python's tuple comparison is lexicographical, `False < True` resolves dated tasks vs. `None` tasks immediately without evaluating `due_date < None`.
3. **Immutability & Stability:** Uses `sorted()`, preserving the input list while relying on Python's stable Timsort for equal keys. Type annotations use `Mapping[str, Any]` to cleanly accept dictionaries or immutable mapping equivalents.
````

### Task 3 — Few-shot

Use both docstrings from the module as examples.

```
Here are two docstrings from this module, written in the team's style:

Example 1 (`add_task`):
"""Add a new task to the task list.

Args:
    tasks (list): The list of existing task dictionaries.
    title (str): The task's title.
    due_date (date, optional): The task's due date. Defaults to None.
    priority (str): One of "high", "medium", "low". Defaults to "medium".

Returns:
    list: The updated list of tasks.
"""

Example 2 (`mark_complete`):
"""Mark a task as completed by title.

Args:
    tasks (list): The list of task dictionaries.
    title (str): The title of the task to mark complete.

Returns:
    bool: True if a matching task was found and updated, False otherwise.
"""

Following the same style and sections, write the docstring for `calculate_completion_rate`.
```

Response:
````
"""Calculate the percentage of completed tasks in the task list.

Args:
    tasks (list): The list of task dictionaries.

Returns:
    float: The completion rate as a percentage (0.0 to 100.0), or 0.0 if the list is empty.
"""
````

#### Task 3 — Few-shot, RERUN (fresh conversation; original attempt above said "percentage", but the function returns a fraction)

Paste the full `task_manager.py` first, then:

```
Here are two docstrings from this module, written in the team's style:

Example 1 (`add_task`):
"""Add a new task to the task list.

Args:
    tasks (list): The list of existing task dictionaries.
    title (str): The task's title.
    due_date (date, optional): The task's due date. Defaults to None.
    priority (str): One of "high", "medium", "low". Defaults to "medium".

Returns:
    list: The updated list of tasks.
"""

Example 2 (`mark_complete`):
"""Mark a task as completed by title.

Args:
    tasks (list): The list of task dictionaries.
    title (str): The title of the task to mark complete.

Returns:
    bool: True if a matching task was found and updated, False otherwise.
"""

Following the same style and sections, write the docstring for this function. Read the code and describe what it actually returns, including the empty-list case.

def calculate_completion_rate(tasks):
    if not tasks:
        return 0.0
    completed = sum(1 for t in tasks if t["completed"])
    return completed / len(tasks)
```

Response:

````
"""Calculate the completion rate of the tasks.

Args:
    tasks (list): The list of task dictionaries.

Returns:
    float: The proportion of completed tasks from 0.0 to 1.0, or 0.0 if tasks is empty.
"""
````

If you submit the rerun, keep the first attempt too and say in the reflection that the first prompt gave only the docstrings, and the docstring it produced said "percentage" when the function returns a fraction.

---

## Part 2 — originals (verbatim, send exactly as given)

1. `Write a function `add_subtask(tasks, parent_title, subtask_title)` that adds a subtask to an existing task.`
2. `Write a function `format_task_line(task, today)` that returns a one-line display string for a task, showing its title, priority and due date. Use our existing date-formatting helper in `utils.py` for the due date.`
3. `Write a function `get_urgent_tasks(tasks, today)` that returns the urgent tasks, most urgent first.`

Do NOT paste CONVENTIONS.md or utils.py in the original runs.

## Part 2 — rewrite skeletons (finish AFTER you see the original outputs)

**P1:** paste the full CONVENTIONS.md, then: "Write `add_subtask(tasks, parent_title, subtask_title)` following every rule in the conventions above." (Adjust to the specific rules your original violated.)

**P2:** paste the full `utils.py`, then: "Write `format_task_line(task, today)` returning a one-line string with the title, priority and due date. Build the due-date text by calling `due_label(task["due_date"], today)` imported from `utils`; do not reimplement it." (Adjust to what your original did.)

**P3:** "Write `get_urgent_tasks(tasks, today)`. A task is urgent if it is not completed and at least one holds: it is overdue (due before today); it is due within the next 3 days counting today (today through today+3); or its priority is "high" (even with no due date). Return them earliest due date first, undated high-priority tasks last. Do not modify the input list." (Adjust to what your original got wrong; check the 3-day boundary against your output.)
