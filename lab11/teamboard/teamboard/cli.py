"""Demo driver: python -m teamboard.cli"""
from datetime import date

from teamboard import db, report, tasks


def seed(conn):
    db.add_task(conn, "Write DECISIONS.md entry", "ann lee", "2026-11-18")
    db.add_task(conn, "Fix login bug", "ben chu", "2026-11-19")
    db.add_task(conn, "Prepare user test script", "ann lee", "2026-11-21")
    db.add_task(conn, "Draft design rationale", None, "2026-11-22")
    db.add_task(conn, "Merge day plan", "cara wu", "2026-11-20")


def main():
    conn = db.connect()
    seed(conn)
    today = date(2026, 11, 18)
    print("== Due in the next 3 days ==")
    print(report.due_soon_report(db.all_tasks(conn), today, 3))
    print("\n== Ann's tasks ==")
    for t in db.find_by_assignee(conn, "ann lee"):
        print(" ", t["title"])
    print("\n== Duplicates ==")
    print(tasks.find_duplicate_titles(db.all_tasks(conn)) or "none")
    print("\n== Workload ==")
    print(report.timed_report(db.all_tasks(conn)))


if __name__ == "__main__":
    main()
