doc_id: D15
title: Security Policy
date: 2026-01-10
status: current
---
These rules apply to everyone who works on Nimbus Notes.

## Secrets

Secrets such as API keys, passwords, and signing keys must never be committed to a repository, pasted into a chat, or written in a ticket. Store them in the Vaultline vault and fetch them at runtime. If a secret is committed by mistake, treat it as leaked: rotate it immediately, then remove it from the history.

## Accounts

Multi-factor authentication is mandatory on every company account. Hardware security keys are preferred for engineers with production access.

## Dependencies

A dependency scan runs every Monday at 03:00 Asia/Taipei and opens issues for known vulnerabilities. Critical findings must be fixed within 7 days and high findings within 30 days.

## Reporting a vulnerability

External researchers can report vulnerabilities to security@nimbus-notes.example. We acknowledge every report within 2 business days. Internal staff report suspected incidents in the #security channel.

## Using AI assistants

Do not paste customer data, secrets, or unreleased security fixes into an AI assistant that is not approved by the security team.
