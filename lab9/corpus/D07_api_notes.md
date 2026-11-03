doc_id: D07
title: Public API Notes
date: 2026-05-12
status: current
---
These notes describe behaviors of the public REST API that are easy to miss in the generated reference.

## Authentication

Send the access token in the Authorization header as Bearer followed by the token. Tokens are issued by the auth service; see the auth runbook for their lifetime.

## Rate limits

Each API key may make 600 requests per minute. When the limit is exceeded the api-gateway answers with HTTP status 429 and a Retry-After header that says how many seconds to wait. Clients should back off and retry after that delay and should not retry immediately in a loop.

## Pagination

List endpoints use cursor-based pagination. The default page size is 25 and the maximum is 100. The response contains a next_cursor value; pass it back as the cursor parameter to get the next page. When next_cursor is null there are no more results.

## Idempotency

POST requests may carry an Idempotency-Key header. The server remembers the key for 24 hours, and a repeated request with the same key returns the original response instead of creating a second note.

## Deprecations

The endpoint /v1/notes/export is deprecated. Use /v2/export instead. See the changelog for the removal plan.
