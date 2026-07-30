# Step 1 -- Data Extraction

## Vulnerability Issue: TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Status | New |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream from the Version Streams table in Security Configuration.

Issue stream scope: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. This maps to the **Cargo** ecosystem from the Ecosystem Mappings table in the stream's security-matrix.md.

- Ecosystem: Cargo
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Repository: backend

Ecosystem mappings per stream:

| Stream | Upstream Branch | Lock File | Check Command |
|--------|-----------------|-----------|---------------|
| 2.1.x | `release/0.3.z` | `Cargo.lock` | `git show <tag>:Cargo.lock` |
| 2.2.x | `release/0.4.z` | `Cargo.lock` | `git show <tag>:Cargo.lock` |

Since Cargo is a **source dependency** ecosystem (per the classification table), remediation will require **two tasks per affected stream**: an upstream backport task and a downstream propagation subtask (with a Blocks dependency).

## Deployment Context

The Source Repositories table in the project CLAUDE.md does not have a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. However, since the column is absent, coordination guidance is omitted from remediation task descriptions.

## Version Impact Analysis

Using the mock lock file data (simulating `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8: 0.11.12) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | fixed (>= 0.11.14) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | fixed (>= 0.11.14) |

### Summary

- **Stream 2.1.x**: All versions (2.1.0, 2.1.1) are affected -- both ship quinn-proto 0.11.9
- **Stream 2.2.x**: Versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, the fixed version)
- Version 2.2.2 is a retag of 2.2.1 (tag v0.4.9 = retag of v0.4.8), so the affected status is carried forward

### Affects Versions Correction

The PSIRT-assigned Affects Versions field contains **RHTPA 2.0.0**, which does not match any version in the supportability matrix. Based on lock file evidence, the corrected Affects Versions for the scoped stream (2.2.x) should be:

- Current: [RHTPA 2.0.0]
- Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Rationale:
- RHTPA 2.0.0 is not a version in the supportability matrix (no 2.0.x stream exists)
- RHTPA 2.2.0 ships quinn-proto 0.11.9 (< 0.11.14) -- affected
- RHTPA 2.2.1 ships quinn-proto 0.11.12 (< 0.11.14) -- affected
- RHTPA 2.2.2 is a retag of 2.2.1 (same quinn-proto 0.11.12) -- affected
- RHTPA 2.2.3 ships quinn-proto 0.11.14 (>= 0.11.14) -- NOT affected
- RHTPA 2.2.4 ships quinn-proto 0.11.14 (>= 0.11.14) -- NOT affected

PROPOSAL: Jira Mutation

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Note: Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3). These are placeholder references -- the actual IDs are resolved at execution time.
