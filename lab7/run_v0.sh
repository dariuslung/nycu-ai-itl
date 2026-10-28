#!/usr/bin/env bash
# Run from lab7/ in YOUR terminal, after exporting ANTHROPIC_API_KEY.
# Saves outputs to results/ so they can be pasted into the report.
set -e
PY=${PY:-python}
mkdir -p results
[ -n "$ANTHROPIC_API_KEY" ] || { echo "ANTHROPIC_API_KEY not set"; exit 1; }
$PY week7_lab_starter.py --v0 "Hello" 2>&1 | tee results/smoke.txt
$PY week7_lab_starter.py --v0 --tests 2>&1 | tee results/v0_tests.txt
$PY week7_lab_starter.py --v0 --modes --repeat 5 2>&1 | tee results/v0_modes.txt
echo "Done. Outputs in results/"
