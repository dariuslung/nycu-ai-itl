doc_id: D05
title: Code Review Policy
date: 2026-04-01
status: current
---
This policy describes how changes reach the main branch. It replaces the policy dated 2024-02-10.

## Approvals

Every change needs at least one approval from a teammate who did not write it. Changes under /billing or /auth are more sensitive and require two approvals, one of which must come from a member of the code steward rotation. Nobody may merge their own pull request.

## Size

A pull request should change no more than 400 lines. Generated files and lockfiles do not count. If a change must be larger, split it into several pull requests or ask a steward to agree on a plan in advance.

## Timing

Reviewers should respond within 1 business day. If you cannot review in time, say so in the pull request and suggest someone else.

## AI-assisted changes

Code written or substantially edited with an AI assistant is welcome, but it must be labelled. Add the tag AI-assisted to the pull request description and state which parts the assistant produced. The reviewer reads AI-assisted code with the same care as any other code and runs the tests locally when the change is not trivial.

## Checks

The continuous integration pipeline must pass before merge. A failing check is never merged with a note to fix it later.
