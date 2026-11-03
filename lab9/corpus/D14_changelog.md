doc_id: D14
title: Changelog
date: 2026-09-20
status: current
---
Release notes for recent versions, newest first.

## v4.4.0 (2026-09-15)

The endpoint /v1/notes/export is now deprecated in favor of /v2/export. The old endpoint will be removed in v5.0. Improved the speed of opening large folders.

## v4.3.1 (2026-09-01)

Fixed a bug where attachment uploads failed for files larger than 25 MB on slow connections.

## v4.3.0 (2026-08-25)

Changed the sync batch size from 50 to 200 changes per request, which lowers battery use on mobile devices. Added a setting to pause sync on cellular data.

## v4.2.0 (2026-08-11)

Added offline mode for the web client. Notes opened in the last 7 days are available without a connection. Search is not available offline.

## v4.1.0 (2026-07-28)

Added the Team plan billing portal and per-user usage reports.
