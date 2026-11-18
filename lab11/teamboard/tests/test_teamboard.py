import time
import unittest
from datetime import date

from teamboard import db, report, tasks


def make_db():
    conn = db.connect()
    db.add_task(conn, "Write report", "ann lee", "2026-11-20")
    db.add_task(conn, "Fix login bug", "ben chu", "2026-11-19")
    db.add_task(conn, "Prepare demo", "ann lee", "2026-11-25")
    return conn


class StorageTests(unittest.TestCase):
    def test_add_and_list_tasks(self):
        conn = make_db()
        titles = [t["title"] for t in db.all_tasks(conn)]
        self.assertEqual(titles, ["Fix login bug", "Write report", "Prepare demo"])

    def test_mark_done(self):
        conn = make_db()
        first = db.all_tasks(conn)[0]
        db.mark_done(conn, first["id"])
        self.assertEqual(db.all_tasks(conn)[0]["done"], 1)

    def test_find_by_assignee_returns_that_persons_tasks(self):
        conn = make_db()
        mine = db.find_by_assignee(conn, "ann lee")
        self.assertEqual([t["title"] for t in mine], ["Write report", "Prepare demo"])


class DueDateTests(unittest.TestCase):
    TODAY = date(2026, 11, 18)

    def test_due_within_includes_the_last_day(self):
        conn = make_db()
        db.add_task(conn, "Boundary task", "cara wu", "2026-11-21")  # exactly 3 days away
        soon = tasks.due_within(db.all_tasks(conn), self.TODAY, 3)
        self.assertIn("Boundary task", [t["title"] for t in soon])

    def test_due_within_skips_done_and_past(self):
        conn = make_db()
        db.add_task(conn, "Old task", "cara wu", "2026-11-10")
        done_id = db.add_task(conn, "Finished task", "cara wu", "2026-11-19")
        db.mark_done(conn, done_id)
        titles = [t["title"] for t in tasks.due_within(db.all_tasks(conn), self.TODAY, 3)]
        self.assertEqual(titles, ["Fix login bug", "Write report"])


class ReportTests(unittest.TestCase):
    def test_workload_counts_open_tasks(self):
        summary = report.workload_summary(db.all_tasks(make_db()))
        self.assertEqual(summary, {"Ann Lee": 2, "Ben Chu": 1})

    def test_workload_counts_unassigned_tasks(self):
        conn = make_db()
        db.add_task(conn, "Nobody owns this", None, "2026-11-22")
        summary = report.workload_summary(db.all_tasks(conn))
        self.assertEqual(summary["Unassigned"], 1)

    def test_timed_report_ends_with_timing_line(self):
        text = report.timed_report(db.all_tasks(make_db()))
        self.assertTrue(text.splitlines()[-1].startswith("(report built in"))


class DuplicateTests(unittest.TestCase):
    def test_duplicates_found_ignoring_case_and_spaces(self):
        items = [{"title": t} for t in ["Fix bug", " fix BUG ", "Write docs", "Fix bug"]]
        self.assertEqual(tasks.find_duplicate_titles(items), ["fix bug"])

    def test_duplicates_fast_on_large_input(self):
        items = [{"title": f"Task number {i}"} for i in range(20_000)]
        start = time.perf_counter()
        result = tasks.find_duplicate_titles(items)
        elapsed = time.perf_counter() - start
        self.assertEqual(result, [])
        self.assertLess(elapsed, 0.5, f"took {elapsed:.2f}s for 20,000 titles")


if __name__ == "__main__":
    unittest.main()
