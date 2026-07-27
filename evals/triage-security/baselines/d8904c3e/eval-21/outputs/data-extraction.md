# Step 1 -- Data Extraction

## Issue Metadata

| Field | Value |
|-------|-------|
| Issue Key | TC-8020 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Assignee | Unassigned |
| Due Date | 2026-07-15 |

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary text |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern from Security Configuration) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

**Issue stream scope**: 2.2.x (scoped issue -- Steps 3 and 4 apply only to this stream; Case A cross-stream check applies to other streams).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Per the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the matching ecosystem is **Cargo**.

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

Cargo is a **source dependency** ecosystem per the ecosystem classification table. This means remediation produces **2 tasks per affected stream**: upstream backport + downstream propagation.

## Deployment Context Lookup

The affected repository `rhtpa-backend` is found in Source Repositories. No Deployment Context column is present, so the default is `upstream`.

## Upstream Affected Component

The issue has `customfield_10632` (Upstream Affected Component) set to **quinn-proto**. This field is used in Step 4.3 (cross-CVE overlap detection) and Step 7 (concurrent triage detection).

## Affects Versions Discrepancy (Preliminary)

PSIRT assigned Affects Versions: **RHTPA 2.0.0**. There is no 2.0.x version stream configured in Security Configuration. This version is incorrect and will be corrected in Step 3 after the version impact analysis in Step 2.

## Version Impact Analysis (Step 2)

Using the lock file data from the security matrix, the quinn-proto versions at each pinned tag are:

### Stream 2.1.x (rhtpa-release.0.3.z) -- out of scope but checked for Case A

| Version | Build Tag | quinn-proto Version | Affected? (< 0.11.14) |
|---------|-----------|---------------------|------------------------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.1 | v0.3.12 | 0.11.9 | YES |

### Stream 2.2.x (rhtpa-release.0.4.z) -- in scope

| Version | Build Tag | quinn-proto Version | Affected? (< 0.11.14) |
|---------|-----------|---------------------|------------------------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.2 | v0.4.9 | _(retag of v0.4.8)_ -- same as 2.2.1 | YES |
| 2.2.3 | v0.4.11 | 0.11.14 | NO (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO (fixed) |

### Summary

- **Stream 2.2.x (in scope)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are NOT affected.
- **Stream 2.1.x (out of scope)**: Both versions 2.1.0 and 2.1.1 are affected. This triggers Case A (cross-stream impact).

## Affects Versions Correction (Step 3)

PSIRT assigned: `RHTPA 2.0.0` (incorrect -- no 2.0.x stream exists).

Proposed correction (scoped to stream 2.2.x): `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2`

Versions 2.2.3 and 2.2.4 are NOT included because they ship quinn-proto 0.11.14 (the fixed version).
