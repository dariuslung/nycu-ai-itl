# Task Manager Team Conventions

Every function in the task manager project follows these rules. Code that breaks them is sent back in code review.

1. **Errors.** A function that cannot do what it was asked raises `TaskError`, a subclass of `Exception`. Define it in the same file if it does not exist yet. Never raise `ValueError` or `KeyError`, and never return `None` or `False` to signal a failure.
2. **Return value.** A function that changes the task list returns the updated task list, like `add_task` does.
3. **Finding tasks by title.** Titles are compared ignoring upper/lower case and ignoring spaces at the start and end. `"  write REPORT "` finds the task titled `"Write report"`.
4. **Subtasks.** A task's subtasks are stored in a list under the key `"subtasks"` on the parent task. Each subtask is a dict with the same four keys as any task: `"title"`, `"due_date"`, `"priority"`, `"completed"`. A new subtask has the parent's priority, `due_date` of `None`, and `completed` of `False`.
5. **Docstrings.** Every function has a Google-style docstring with an `Args:` section and a `Returns:` section.
