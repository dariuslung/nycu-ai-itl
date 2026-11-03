doc_id: D03
title: ADR-001: Use PostgreSQL as the primary database
date: 2024-03-12
status: accepted
---
## Status

Accepted on 2024-03-12.

## Context

Nimbus Notes needs to store notes, folders, and sharing permissions. Sharing a folder changes permissions on many notes at once, so we need reliable multi-row transactions. The team also wanted a store that every engineer already knew and that a managed cloud service could run for us.

## Decision

We will use PostgreSQL as the primary database. Note bodies are stored in JSONB columns so that the editor format can evolve without a migration for every change.

## Alternatives considered

MongoDB was rejected because, at the time of this decision, its multi-document transactions were less mature and the team had little experience operating it. DynamoDB was rejected because it would tie us closely to a single cloud provider and make local development harder.

## Consequences

Schema migrations are reviewed by the Change Review Board before they reach production. We accept that vertical scaling has limits and that we may need read replicas later.
