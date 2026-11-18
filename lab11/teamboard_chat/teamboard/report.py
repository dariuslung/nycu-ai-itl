"""Plain-text reports for the team."""
import time

from teamboard.tasks import due_within


def workload_summary(tasks):
    """Count open tasks per person. Tasks with no assignee are counted under 'Unassigned'."""
    counts = {}
    for task in tasks:
        if task["done"]:
            continue
        name = (task["assignee"] or "").strip().title() or "Unassigned"
        counts[name] = counts.get(name, 0) + 1
    return counts


def timed_report(tasks):
    """Return the workload report followed by a line saying how long it took to build."""
    start = time.perf_counter()
    summary = workload_summary(tasks)
    elapsed = time.perf_counter() - start
    lines = [f"{name}: {count} open" for name, count in sorted(summary.items())]
    lines.append(f"(report built in {elapsed * 1000:.2f} ms)")
    return "\n".join(lines)


def due_soon_report(tasks, today, days=3):
    """List the open tasks due within `days` days."""
    soon = due_within(tasks, today, days)
    if not soon:
        return "Nothing due soon."
    return "\n".join(f"{t['due']}  {t['title']} ({t['assignee'] or 'unassigned'})" for t in soon)