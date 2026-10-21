# Step 1 -- Data Extraction for TC-8021

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | [rhtpa-2.2] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS score | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | None | Comment history |
| Upstream Affected Component | quinn-proto | customfield_10632 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** version stream configured in the Version Streams table (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

**Issue stream scope: 2.2.x**

The issue is stream-scoped. Steps 3 and 4 will apply only to the 2.2.x stream. Cross-stream impact on 2.1.x will be handled via Case A in Step 8.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the security-matrix.md for stream 2.2.x, this maps to the **Cargo** ecosystem.

- Ecosystem: **Cargo**
- Category: **Source dependency**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch (2.2.x): `release/0.4.z`
- Upstream branch (2.1.x): `release/0.3.z`

Per the ecosystem classification table, Cargo (source dependency) produces **2 remediation tasks per stream**: upstream backport + downstream propagation (or dependency bump + downstream propagation if the upstream fix is already available).

## Deployment Context Lookup

The affected repository `rhtpa-backend` is found in the Source Repositories table. No Deployment Context column is present in the configuration, so the default deployment context is **upstream**.

## Step 1.5 -- External CVE Data Enrichment

### MITRE CVE API

Query: `https://cveawg.mitre.org/api/cve/CVE-2026-31812`

Expected result: Affected product quinn-proto, affected versions `lessThan: 0.11.14`, fixed version `0.11.14`.

### OSV.dev API

Query: `https://api.osv.dev/v1/vulns/CVE-2026-31812`

Expected result: Ecosystem Cargo (crates.io), introduced at 0 (all versions), fixed at 0.11.14.

### Cross-validation

All three sources agree on the fix threshold:

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | < 0.11.14 | 0.11.14 |
| MITRE CVE API | < 0.11.14 | 0.11.14 |
| OSV.dev | < 0.11.14 | 0.11.14 |

**Enriched fix threshold: 0.11.14** (all sources agree)

## Step 1.7 -- Embargo Check

- Embargo policy URL: Not configured in Security Configuration
- Step 1.7 is **skipped entirely** (no embargo policy URL configured)

## Version Impact Analysis (Step 2)

Using the enriched fix threshold of 0.11.14, the version impact analysis based on lock file data at pinned commits:

### Stream 2.2.x (issue scope)

| Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|---------|-----------|---------------------|-----------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | _(retag of v0.4.8)_ | **YES** | Same as 2.2.1 (backend retag) |
| 2.2.3 | v0.4.11 | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (at fix threshold) |
| 2.2.4 | v0.4.12 | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (at fix threshold) |

### Stream 2.1.x (cross-stream analysis)

| Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|---------|-----------|---------------------|-----------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |

### Summary

- **2.2.x stream**: 3 of 5 versions affected (2.2.0, 2.2.1, 2.2.2). Fixed in 2.2.3+.
- **2.1.x stream**: All versions affected (2.1.0, 2.1.1). Cross-stream impact.

## Step 0.3 -- Matrix Staleness Check

Matrix Last-Updated timestamp: 2026-06-28T10:00:00Z
Current date: 2026-10-21
Days since last update: approximately 115 days (exceeds 14-day threshold)

The matrix is **stale** -- it was last updated over 14 days ago. In a real triage, the engineer would be warned and offered options to refresh, proceed anyway, or stop. For this eval, proceeding with the current matrix data.

## Affects Versions Correction (Step 3)

### Current vs. Proposed

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Problem**: RHTPA 2.0.0 does not correspond to any configured version stream. There is no 2.0.x stream. The PSIRT assignment is incorrect.
- **Proposed (scoped to 2.2.x)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: These are the versions in the 2.2.x stream where quinn-proto < 0.11.14. Versions 2.2.3 and 2.2.4 ship 0.11.14 and are not affected.

Correction: `Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
