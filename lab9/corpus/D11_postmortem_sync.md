doc_id: D11
title: Postmortem: Sync Outage of 2026-03-14
date: 2026-03-20
status: final
---
Severity: SEV1. Duration: 47 minutes. Author: Mei-Ling Chen.

## Summary

On Saturday 2026-03-14, mobile and desktop clients could not sync notes for 47 minutes. Reading and editing offline continued to work, and no data was lost.

## Timeline (Asia/Taipei)

At 02:13 the first customer report arrived through support. At 02:20 the on-call engineer acknowledged the escalation from support, because no automated alert had fired. At 02:31 the incident commander was named and the team confirmed that the api-gateway was healthy while all requests to the sync path failed. At 02:44 the team noticed TLS handshake errors in the gateway logs when it connected to the sync-service. At 02:52 a new certificate was installed and traffic recovered. At 03:00 the incident was closed.

## What went well

Offline mode kept clients usable. The incident commander kept the channel focused, and the rollback of the certificate was rehearsed.

## What went poorly

No alert fired, so detection depended on a customer. The renewal job had been disabled during an earlier migration and nobody noticed.

## Root cause

The root cause was an expired TLS certificate on the sync-service. The certificate renewal job was switched off during the NATS migration and was not turned on again.

## Action items

1. Automate certificate renewal and add a test that fails if the job is disabled (owner: Mei-Ling Chen, due 2026-04-10).
2. Alert 14 days before any certificate expires (owner: platform team, due 2026-04-03).
3. Add a synthetic check that performs a full sync every 5 minutes (owner: sync team, due 2026-04-24).
