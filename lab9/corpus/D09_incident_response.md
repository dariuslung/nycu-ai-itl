doc_id: D09
title: Incident Response Policy
date: 2026-01-28
status: current
---
This policy defines how we classify and handle incidents. The on-call engineer decides the initial severity and may raise it at any time.

## Severity levels

SEV1 is a complete outage or any loss of customer data. The on-call engineer must acknowledge a SEV1 page within 5 minutes. Status updates go to the channel #inc-live every 30 minutes until resolution, and a written postmortem is due within 5 business days.

SEV2 means a major feature is degraded for many users, for example search or sync being very slow. The on-call engineer must acknowledge within 15 minutes, post updates every 60 minutes, and deliver a postmortem within 10 business days.

SEV3 is a minor problem with a workaround. It is handled on the next business day, and a postmortem is optional.

## Roles

For SEV1 and SEV2 the on-call engineer names an incident commander, who coordinates the response and speaks for the team. Everyone else follows the commander's requests. One person writes the timeline as the incident unfolds.

## After the incident

Postmortems are blameless. They describe what happened, why the system allowed it, and what we will change. Every postmortem ends with action items that have an owner and a due date.
