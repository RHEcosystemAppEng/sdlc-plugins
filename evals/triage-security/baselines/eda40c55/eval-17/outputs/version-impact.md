# Step 2 -- Version Impact Analysis

## Issue Stream Scope

This issue is scoped to stream **2.2.x** (from the `[rhtpa-2.2]` suffix in the summary). The version impact table below covers the scoped stream (2.2.x) and also checks the 2.1.x stream for cross-stream impact (Case B).

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

### Stream 2.2.x (issue scope)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0   | 0.11.9      | YES       |       |
| 2.2.1   | 0.11.12     | YES       |       |
| 2.2.2   | --          | YES       | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3   | 0.11.14     | NO        | ships fixed version |
| 2.2.4   | 0.11.14     | NO        | ships fixed version |

### Stream 2.1.x (cross-stream check)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0   | 0.11.9      | YES       |       |
| 2.1.1   | 0.11.9      | YES       |       |

## Evidence

All version determinations are based on the lock file data extracted via `git show <tag>:Cargo.lock` for each pinned backend tag in the supportability matrix:

- **v0.4.5** (2.2.0): quinn-proto 0.11.9 -- AFFECTED (0.11.9 < 0.11.14)
- **v0.4.8** (2.2.1): quinn-proto 0.11.12 -- AFFECTED (0.11.12 < 0.11.14)
- **v0.4.9** (2.2.2): retag of v0.4.8 -- same as 2.2.1, AFFECTED
- **v0.4.11** (2.2.3): quinn-proto 0.11.14 -- NOT AFFECTED (0.11.14 >= 0.11.14)
- **v0.4.12** (2.2.4): quinn-proto 0.11.14 -- NOT AFFECTED (0.11.14 >= 0.11.14)
- **v0.3.8** (2.1.0): quinn-proto 0.11.9 -- AFFECTED (0.11.9 < 0.11.14)
- **v0.3.12** (2.1.1): quinn-proto 0.11.9 -- AFFECTED (0.11.9 < 0.11.14)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x  | Cargo     | release/0.4.z   | 0.11.14         | YES    |
| 2.1.x  | Cargo     | release/0.3.z   | 0.11.9          | NO     |

- **2.2.x**: The upstream branch `release/0.4.z` already has quinn-proto 0.11.14 (fixed). Remediation is a downstream Konflux release repo change to bump the source tag/commit reference.
- **2.1.x**: The upstream branch `release/0.3.z` still has quinn-proto 0.11.9 (vulnerable). Remediation requires an upstream PR first to bump the dependency, then a downstream Konflux update.

## Summary

- **Scoped stream (2.2.x)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fix. The upstream branch is already fixed.
- **Cross-stream (2.1.x)**: All versions (2.1.0, 2.1.1) are affected. The upstream branch is NOT yet fixed.
- **Affects Versions correction needed**: The Jira issue currently has "RHTPA 2.0.0" which does not match any configured stream. The correct Affects Versions for the 2.2.x scope are RHTPA 2.2.0, RHTPA 2.2.1, and RHTPA 2.2.2.
