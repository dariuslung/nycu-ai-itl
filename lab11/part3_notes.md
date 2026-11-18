# Part 3 notes (teamboard_cc)

Problem: workload_summary counted an assignee made only of spaces under the key "" instead of "Unassigned".
The docstring says "Tasks with no assignee are counted under 'Unassigned'". No test covers a blank name.
Bug or decision: decision. The docstring says "no assignee" and does not say whether "   " is one. I chose that a blank or
whitespace-only name counts as no assignee, so it goes under "Unassigned". (The chat version's code already did this; the Claude Code
version's did not.)

Red (test added in tests/test_teamboard.py, ReportTests; commit 5e5f87c "Add failing test"):
    def test_workload_treats_blank_assignee_as_unassigned(self):
        conn = make_db()
        db.add_task(conn, "Blank owner", "   ", "2026-11-22")
        summary = report.workload_summary(db.all_tasks(conn))
        self.assertEqual(summary.get("Unassigned"), 1)
        self.assertNotIn("", summary)
Output before the fix:
    AssertionError: None != 1
    Ran 1 test ... FAILED (failures=1)      (whole suite: Ran 12 tests, FAILED (failures=1))

Fix (teamboard/report.py):
-        name = (task["assignee"] or "Unassigned").strip().title()
+        name = (task["assignee"] or "").strip().title() or "Unassigned"

Green: Ran 1 test, OK.
Suite: Ran 12 tests, OK (11 from Part 2 plus my test). Nothing else broke.
Undo check: git stash -> my test FAILED (failures=1); git stash pop -> OK. So the test catches a bad fix.
