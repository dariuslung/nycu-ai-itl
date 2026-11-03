doc_id: D12
title: Postmortem: Search Latency Incident of 2026-06-22
date: 2026-06-25
status: final
---
Severity: SEV2. Duration: 2 hours 10 minutes. Author: Daniel Ho.

## Summary

On Monday 2026-06-22, search became slow for most users. The 95th percentile latency (p95) of search requests rose from its usual 180 ms to 2.4 seconds. Search results stayed correct, but many users stopped using search while it was slow.

## Impact

Roughly a third of active users ran at least one search during the incident. Support received 41 tickets.

## Root cause

The nightly reindex job and the index compaction job were both scheduled for 02:00. Normally the reindex finishes in 20 minutes, but after the index grew it took longer than expected. This time the compaction job started while the reindex was still running, and both jobs competed for disk and memory on the search nodes.

## Resolution

The on-call engineer stopped the compaction job and restarted the search nodes one by one. Latency returned to normal after the last restart.

## Action items

1. Add a lock so that only one maintenance job can run on a search node at a time (owner: Daniel Ho).
2. Alert when the p95 latency of search exceeds 500 ms for 10 minutes (owner: search team).
3. Move the compaction job to 04:00 (done).
