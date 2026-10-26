# Step 1 -- Data Extraction

## Issue: TC-8001

### Parsed CVE Metadata

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels: `CVE-2026-31812`; Summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 (stream 2.2.x) | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description: "A vulnerability was found in quinn-proto" |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description: "before version 0.11.14" |
| Fixed version | 0.11.14 | Description: "Fixed version: 0.11.14" |
| CVSS | 7.5 (High) | Description: "CVSS: 7.5 (High)" |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comments |
| Issue status | New | Issue status field |
| Assignee | Unassigned | Issue assignee field |

### Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This is a **scoped** issue -- triage is scoped to the 2.2.x stream, with cross-stream impact analysis for other streams (2.1.x) in Case A.

### Ecosystem Detection

- **Ecosystem:** Cargo (Rust crate)
- **Library:** quinn-proto
- **Lock file:** `Cargo.lock`
- **Check command:** `git show <tag>:Cargo.lock`
- **Upstream branch:** `release/0.4.z` (for 2.2.x stream)
- **Remediation task count per stream:** 2 (source dependency ecosystem -- upstream backport or dependency bump + downstream propagation)

### Affects Versions Discrepancy

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, but no 2.0.x stream is configured in the Version Streams table. The configured streams are 2.1.x and 2.2.x. This suggests the Affects Versions field needs correction in Step 3 based on lock file evidence from the version impact analysis.

### quinn-proto Version Impact Data (from mock lock files)

| Stream | Version | Build Tag | quinn-proto Version | Vulnerable? (< 0.11.14) |
|--------|---------|-----------|---------------------|------------------------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.x | 2.2.2 | v0.4.9 | _(retag of v0.4.8)_ = 0.11.12 | YES (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO (fixed version) |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO (fixed version) |

### Version Impact Summary

- **Stream 2.1.x:** ALL versions affected (2.1.0, 2.1.1 both ship quinn-proto 0.11.9)
- **Stream 2.2.x:** Versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3 and 2.2.4 are NOT affected (ship fixed quinn-proto 0.11.14)
- **Latest released version in scoped stream (2.2.x):** 2.2.4 ships quinn-proto 0.11.14 -- NOT vulnerable
- **Earliest fixed version in 2.2.x:** 2.2.3 (build tag v0.4.11)

### Notes

- Version 2.2.2 is a retag of 2.2.1 (same build tag v0.4.8 for backend), so it inherits the same quinn-proto version 0.11.12.
- The fix was introduced in build tag v0.4.11, which corresponds to product version 2.2.3.
- The 2.1.x stream has no version shipping the fixed quinn-proto (all versions use 0.11.9), making it a cross-stream impact candidate under Case A.
