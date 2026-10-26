# Step 1 -- Data Extraction for TC-8020

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Vulnerability type | Denial of Service (DoS) -- panic on large stream counts | Description |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| RustSec advisory | RUSTSEC-2026-0042 | Description references |
| Due date | 2026-07-15 | Jira `duedate` field |
| Assignee | Unassigned | Jira `assignee` field |
| Status | New | Jira `status` field |
| Upstream Affected Component (customfield_10632) | quinn-proto | Custom field |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- This is a **scoped** issue -- triage is scoped to the 2.2.x stream for Affects Versions and remediation. Cross-stream impact on other streams (2.1.x) is handled via Case A.

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z` (for 2.2.x stream)
- Remediation task structure: 2 tasks per affected stream (upstream backport or dependency bump + downstream propagation)

## Affects Versions Discrepancy

The PSIRT-assigned Affects Version **RHTPA 2.0.0** is incorrect. There is no 2.0.x stream configured in Security Configuration. The version impact analysis (Step 2) determines the correct Affects Versions based on lock file evidence.

## Version Impact Analysis (Step 2)

Using mock lock file data from security-matrix-mock.md:

### Stream 2.1.x (rhtpa-release.0.3.z) -- outside issue scope, for cross-stream reference

| Version | Build Tag | quinn-proto version | Affected? |
|---------|-----------|---------------------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES (< 0.11.14) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES (< 0.11.14) |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue scope

| Version | Build Tag | quinn-proto version | Affected? |
|---------|-----------|---------------------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES (< 0.11.14) |
| 2.2.1 | v0.4.8 | 0.11.12 | YES (< 0.11.14) |
| 2.2.2 | v0.4.9 | 0.11.12 (retag of v0.4.8) | YES (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO (>= 0.11.14, fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO (>= 0.11.14, fixed) |

### Summary

- **Affected versions in scoped stream (2.2.x):** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Not affected versions in scoped stream:** RHTPA 2.2.3, RHTPA 2.2.4 (ship quinn-proto 0.11.14, the fixed version)
- **Cross-stream impact:** Stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9) -- tracked via Case A cross-stream notice

### Affects Versions Correction (Step 3)

- Current (PSIRT-assigned): `[RHTPA 2.0.0]`
- Proposed (scoped to 2.2.x, based on lock file evidence): `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
- RHTPA 2.0.0 does not correspond to any configured version stream and must be removed
- RHTPA 2.2.3 and 2.2.4 are NOT affected and must NOT be included
