"""utils.py -- shared helpers for the task manager project."""


def due_label(due, today):
    """Describe a due date in words, relative to today.

    Every screen in the app uses this function so that due dates are worded the
    same way everywhere.

    Args:
        due (date or None): The task's due date, or None if it has none.
        today (date): The date to compare against.

    Returns:
        str: One of "no due date", "due today", "due in N day(s)" or
            "overdue by N day(s)". "day" is singular only when N is 1.
    """
    if due is None:
        return "no due date"
    delta = (due - today).days
    if delta == 0:
        return "due today"
    if delta > 0:
        return f"due in {delta} day" + ("" if delta == 1 else "s")
    return f"overdue by {-delta} day" + ("" if delta == -1 else "s")
