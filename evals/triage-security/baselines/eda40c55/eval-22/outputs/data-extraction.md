# Step 1 -- Data Extraction for TC-8021

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | quinn-rs/quinn#2048 (https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | GHSA-2026-qp73-x4mq (https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration's Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

The issue is **scoped** to the 2.2.x stream. Steps 3 and 4 will only operate on versions within this stream.

## Ecosystem Detection

quinn-proto is a Rust crate. The Ecosystem Mappings table for the 2.2.x stream lists:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.4.z |

Ecosystem: **Cargo** (source dependency). This means remediation will produce two tasks: an upstream backport task and a downstream propagation subtask.

## Deployment Context Lookup

The affected repository (rhtpa-backend) is listed in Source Repositories:

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

No Deployment Context column is present, so the default context of `upstream` applies.

## Version Impact Analysis (Step 2)

Using the mock lock file data from security-matrix-mock.md, the quinn-proto versions at each tag are:

### 2.2.x stream (in scope)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8: 0.11.12) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | = 0.11.14 (fixed version) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | = 0.11.14 (fixed version) |

### 2.1.x stream (out of scope -- cross-stream analysis)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

## Affects Versions Assessment

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**. There is no 2.0.x stream configured in the Version Streams table. The correct Affects Versions for the 2.2.x scope are **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2** (the affected versions within the scoped stream). Versions 2.2.3 and 2.2.4 are NOT affected (they ship quinn-proto 0.11.14, the fixed version).

This requires an Affects Versions correction in Step 3:
- Current: [RHTPA 2.0.0]
- Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
