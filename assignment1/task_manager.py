from datetime import date

def add_task(tasks, title, due_date=None, priority="medium"):
    """Add a new task to the task list.

    Args:
        tasks (list): The list of existing task dictionaries.
        title (str): The task's title.
        due_date (date, optional): The task's due date. Defaults to None.
        priority (str): One of "high", "medium", "low". Defaults to "medium".

    Returns:
        list: The updated list of tasks.
    """
    tasks.append({
        "title": title,
        "due_date": due_date,
        "priority": priority,
        "completed": False,
    })
    return tasks


def mark_complete(tasks, title):
    """Mark a task as completed by title.

    Args:
        tasks (list): The list of task dictionaries.
        title (str): The title of the task to mark complete.

    Returns:
        bool: True if a matching task was found and updated, False otherwise.
    """
    for task in tasks:
        if task["title"] == title:
            task["completed"] = True
            return True
    return False


def get_overdue_tasks(tasks, current_date):
    overdue = []
    for task in tasks:
        if task["due_date"] < current_date and not task["completed"]:
            overdue.append(task)
    return overdue


def calculate_completion_rate(tasks):
    if not tasks:
        return 0.0
    completed = sum(1 for t in tasks if t["completed"])
    return completed / len(tasks)
