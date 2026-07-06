# Data Extraction -- Step 1

## Issue: TC-8020

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | quinn-rs/quinn#2048 (https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | GHSA-2026-qp73-x4mq (https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Status | New |
| Assignee | Unassigned |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x only. Steps 3 and 4 will be scoped accordingly -- only 2.2.x versions will be included in the Affects Versions correction. Impact on the 2.1.x stream is handled via cross-stream notification (Case B).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**, which is listed in the Ecosystem Mappings table for both streams.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch (2.2.x stream): `release/0.4.z`

Since this is a source dependency (Cargo ecosystem), remediation requires **two tasks**: an upstream backport task (fix in the source repo) and a downstream propagation subtask (update the reference in the Konflux release repo).

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories with no explicit Deployment Context column, so it defaults to `upstream`.

## Affects Versions Discrepancy

The PSIRT-assigned Affects Version is **RHTPA 2.0.0**, but there is no 2.0.x stream configured in the Version Streams table. The configured streams are 2.1.x and 2.2.x. This will require correction in Step 3.

## Version Impact Analysis (Step 2)

Using mock lock file data for quinn-proto versions at each pinned tag:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Product Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|----------------|-----------|---------------------|-----------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Product Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|----------------|-----------|---------------------|-----------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 (fix threshold) |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | Retag of v0.4.8 -- same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (at or above fix threshold) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (at or above fix threshold) |

## Summary

- **Scoped stream (2.2.x)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 are NOT affected (already ship the fix).
- **Cross-stream (2.1.x)**: Both 2.1.0 and 2.1.1 are affected. This will trigger Case B cross-stream notification.
- The fix was introduced in build v0.4.11 (product version 2.2.3), which ships quinn-proto 0.11.14.
