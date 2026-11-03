doc_id: D13
title: Release Process
date: 2026-05-05
status: current
---
We ship the web, mobile, and backend releases together on a fixed schedule.

## Schedule

A release goes out every second Tuesday. The code freeze starts on the Monday before at 17:00 Asia/Taipei. After the freeze only fixes that the release owner approves may be merged to the release branch.

## Canary

The release first goes to 10 percent of traffic for 30 minutes. The release owner watches error rates, latency, and the crash-free session rate. If anything looks wrong, stop the rollout. If everything is healthy, continue to 100 percent.

## Rollback

To roll back, run nimbusctl rollback --to followed by the version you want to return to. A rollback takes about 3 minutes for backend services. Mobile clients cannot be rolled back, so mobile releases use a staged rollout in the app stores.

## Hotfixes

A hotfix outside the schedule needs approval from the on-call lead. Hotfixes still go through code review and the canary stage.

## Release owner

The release owner rotates every release. The owner writes the release notes in the changelog and announces the release in #eng-announce.
