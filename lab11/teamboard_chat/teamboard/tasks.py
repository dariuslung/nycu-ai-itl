"""Pure functions that work on lists of task dicts (as returned by db.all_tasks)."""
from datetime import date


def parse_due(text):
    """Turn '2026-11-23' into a date."""
    return date.fromisoformat(text)


def due_within(tasks, today, days):
    """Return the open tasks due from `today` up to and including `days` days from today.

    Example: with days=3, a task due exactly 3 days from today IS included.
    Finished tasks and tasks already overdue are not included.
    """
    result = []
    for task in tasks:
        if task["done"]:
            continue
        delta = (parse_due(task["due"]) - today).days
        if 0 <= delta <= days:
            result.append(task)
    return result


def find_duplicate_titles(tasks):
    """Return the titles that appear more than once, ignoring case and spaces.

    Each duplicated title is returned once, in lower case, in the order it first repeats.
    """
    seen = set()
    already_reported = set()
    duplicates = []
    for task in tasks:
        title = task["title"].strip().lower()
        if title in seen:
            if title not in already_reported:
                already_reported.add(title)
                duplicates.append(title)
        else:
            seen.add(title)
    return duplicates