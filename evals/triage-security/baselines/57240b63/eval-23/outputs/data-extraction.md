# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | (none) |
| Ecosystem | Cargo (Rust crate) |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the configured version stream **2.2.x** (Konflux release repo `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will apply scoped behavior.

## Deployment Context Lookup

The affected component label is `pscomponent:org/rhtpa-server`. This maps to the source repository **rhtpa-backend** in the Source Repositories table from Security Configuration.

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | **customer-shipped** |

Deployment context for the affected repository: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions. The `customer-shipped` context requires coordination with Product Security for CVE assignment, advisory preparation, and formal disclosure.

## Version Impact Analysis

### Aggregated Supportability Matrix

**Stream 2.1.x** (rhtpa-release.0.3.z):

| Version | Build | Build Date | backend tag | Lock File | Check Command |
|---------|-------|------------|-------------|-----------|---------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | Cargo.lock | `git show <tag>:Cargo.lock` |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | Cargo.lock | `git show <tag>:Cargo.lock` |

**Stream 2.2.x** (rhtpa-release.0.4.z):

| Version | Build | Build Date | backend tag | Lock File | Check Command |
|---------|-------|------------|-------------|-----------|---------------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | Cargo.lock | `git show <tag>:Cargo.lock` |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | Cargo.lock | `git show <tag>:Cargo.lock` |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | Cargo.lock | retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | Cargo.lock | `git show <tag>:Cargo.lock` |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | Cargo.lock | `git show <tag>:Cargo.lock` |

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |

### Summary

- **Stream 2.2.x (scoped)**: Versions 2.2.0, 2.2.1, 2.2.2 are affected. Versions 2.2.3+ already ship the fixed version (0.11.14). The upstream branch release/0.4.z already has the fix.
- **Stream 2.1.x (out of scope)**: All versions (2.1.0, 2.1.1) are affected. The upstream branch release/0.3.z does NOT have the fix -- quinn-proto is still at 0.11.9.

### Affects Versions Correction (PROPOSAL)

Current Affects Versions on TC-8001: `RHTPA 2.0.0` (incorrect -- RHTPA 2.0 is not a configured stream)

Proposed Affects Versions (scoped to stream 2.2.x per issue suffix):
- RHTPA 2.2.0
- RHTPA 2.2.1
- RHTPA 2.2.2

Rationale: Lock file analysis at pinned commits from security-matrix.md confirms quinn-proto < 0.11.14 in versions 2.2.0 (v0.4.5: 0.11.9), 2.2.1 (v0.4.8: 0.11.12), and 2.2.2 (retag of 2.2.1). Versions 2.2.3+ ship quinn-proto 0.11.14 (the fixed version). RHTPA 2.0.0 does not correspond to any configured version stream.

### Cross-Stream Impact (Case B)

Stream 2.1.x is also affected (2.1.0: 0.11.9, 2.1.1: 0.11.9) but is outside the scope of TC-8001 (which is scoped to 2.2.x). The upstream branch release/0.3.z does not yet have the fix. Preemptive remediation tasks should be created for the 2.1.x stream under Case B.
