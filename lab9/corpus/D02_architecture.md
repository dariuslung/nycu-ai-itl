doc_id: D02
title: Architecture Overview
date: 2026-02-20
status: current
---
Nimbus Notes is built from a small number of services behind a single public gateway. This document lists the services, the ports they use, and the data stores behind them.

## Services

The api-gateway is the only service exposed to the internet. It terminates HTTPS on port 8443, checks authentication tokens, applies rate limits, and forwards requests to the internal services.

The notes-service stores and retrieves notes, folders, and sharing permissions. It listens on port 8100 inside the private network.

The sync-service keeps clients in step with the server. It receives changes from the mobile and desktop apps and publishes them to other devices. It listens on port 9100. Internally and in the glossary it is often called NSS.

The search-service maintains the full-text index and answers search requests. It listens on port 7700.

## Data stores

PostgreSQL 15 is the primary data store for notes, users, and permissions (see ADR-001 for the reasons). Redis 7 is used for caching and for the counters behind rate limiting. Background work and events travel over NATS, which replaced RabbitMQ in 2025 (see ADR-007).

## Clients

The web client is written in React. The mobile clients are written in Swift for iOS and Kotlin for Android. All clients talk only to the api-gateway and never to an internal service directly.
