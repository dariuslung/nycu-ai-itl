"""SQLite storage for TeamBoard tasks."""
import sqlite3


def connect(path=":memory:"):
    """Open a database and make sure the tasks table exists."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
               id       INTEGER PRIMARY KEY AUTOINCREMENT,
               title    TEXT NOT NULL,
               assignee TEXT,
               due      TEXT NOT NULL,
               done     INTEGER NOT NULL DEFAULT 0
           )"""
    )
    return conn


def add_task(conn, title, assignee, due):
    """Insert a task. `due` is an ISO date string such as '2026-11-23'. Returns the new id."""
    cur = conn.execute(
        "INSERT INTO tasks (title, assignee, due) VALUES (?, ?, ?)",
        (title, assignee, due),
    )
    conn.commit()
    return cur.lastrowid


def mark_done(conn, task_id):
    """Mark one task as done."""
    conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()


def all_tasks(conn):
    """Return every task as a dict, soonest due date first."""
    rows = conn.execute("SELECT * FROM tasks ORDER BY due, id")
    return [dict(r) for r in rows]


def find_by_assignee(conn, name):
    """Return all tasks assigned to `name`, soonest due date first."""
    query = f"SELECT * FROM tasks WHERE assignee = '{name}' ORDER BY due, id"
    return [dict(r) for r in conn.execute(query)]
