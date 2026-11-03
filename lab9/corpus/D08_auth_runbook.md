doc_id: D08
title: Authentication Runbook
date: 2026-03-03
status: current
---
This runbook is for engineers operating the auth service.

## Token lifetimes

An access token is valid for 15 minutes. A refresh token is valid for 30 days and can be used once; each refresh issues a new refresh token. Clients that stay offline longer than 30 days must sign in again.

## Signing keys

Signing keys are rotated every 90 days. Rotation is automatic, but an engineer should confirm after each rotation that both the old and the new public key are published for the overlap period, so that tokens issued just before rotation still verify.

## Emergency revocation

If an account is compromised, run nimbusctl auth revoke --user followed by the user id. Revocation propagates to all gateway instances within 60 seconds. After revoking, tell the security contact, and ask the user to reset the password and re-enroll multi-factor authentication.

## Troubleshooting

If many users report sudden sign-outs, check whether a rotation just happened, then check whether the Redis instance that stores revocation entries is healthy. A full Redis instance can cause revocation lookups to fail closed, which signs everyone out.
