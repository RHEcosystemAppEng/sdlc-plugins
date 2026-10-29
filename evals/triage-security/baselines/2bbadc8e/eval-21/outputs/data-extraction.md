# Step 1 -- Data Extraction for TC-8020

## Extracted CVE Metadata

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote links (GitHub PR) |
| Advisory URL | GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (CVE Record) |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | None | Issue comment history |
| Upstream Affected Component | quinn-proto | customfield_10632 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to stream **2.2.x** in the Version Streams table from Security Configuration:

- Stream 2.2.x -> Konflux Release Repo: rhtpa-release.0.4.z

The issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will be scoped to this single stream, and Case A cross-stream analysis will check the other configured stream (2.1.x).

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. The Ecosystem Mappings table in the security-matrix.md for the 2.2.x stream lists:

| Ecosystem | Repository | Lock File | Check Command |
|-----------|------------|-----------|---------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` |

quinn-proto is a **Cargo** (Rust) ecosystem dependency. Per the ecosystem classification table, source dependency ecosystems produce **2 tasks per stream**: upstream backport + downstream propagation (or dependency bump + downstream propagation if the fix is already available upstream).

## Deployment Context Lookup

The affected repository rhtpa-backend is found in the Source Repositories table. Since no Deployment Context column is present, the default is `upstream`.

## Step 2 -- Version Impact Analysis

Using the mock lock file data from security-matrix-mock.md, the quinn-proto versions at each pinned commit are:

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue scope

| Product Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|-----------------|-----------|---------------------|-----------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 (fix threshold) |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES | Same as 2.2.1 -- retag, carries forward 0.11.12 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (at or above fix threshold) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (at or above fix threshold) |

### Stream 2.1.x (rhtpa-release.0.3.z) -- cross-stream check

| Product Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|-----------------|-----------|---------------------|-----------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |

## Summary

- **In-scope stream (2.2.x)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 are NOT affected (they ship the fixed version 0.11.14).
- **Cross-stream (2.1.x)**: ALL versions (2.1.0, 2.1.1) are affected -- this triggers Case A cross-stream impact analysis.
- **PSIRT Affects Versions mismatch**: PSIRT assigned "RHTPA 2.0.0" but no 2.0.x stream exists in the Version Streams configuration. The correct Affects Versions for the 2.2.x scope are RHTPA 2.2.0, RHTPA 2.2.1, and RHTPA 2.2.2 (affected versions within the issue's stream scope).
- **Fix was introduced in build v0.4.11** (product version 2.2.3), where quinn-proto was bumped to 0.11.14.
