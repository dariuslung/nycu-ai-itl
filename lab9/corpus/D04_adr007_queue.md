doc_id: D04
title: ADR-007: Replace RabbitMQ with NATS
date: 2025-06-02
status: accepted
---
## Status

Accepted on 2025-06-02. This decision, ADR-007, supersedes ADR-003, which introduced RabbitMQ.

## Context

RabbitMQ served the first two years of the product. As the number of devices grew, fan-out of sync events to many subscribers became the main load on the broker. The cluster needed frequent manual attention, and upgrades required planned downtime.

## Decision

We will replace RabbitMQ with NATS for background jobs and for event fan-out. NATS is simpler to operate, and in our benchmark it showed about 40 percent lower p99 latency for fan-out to 10,000 subscribers.

## Migration

The migration was done service by service, starting with the search-service. The last service moved on 2025-09-30, and the RabbitMQ cluster was shut down in October 2025.

## Consequences

Engineers must learn NATS subjects and consumer groups. Messages that need guaranteed delivery use JetStream. The old RabbitMQ runbooks are archived and must not be used.
