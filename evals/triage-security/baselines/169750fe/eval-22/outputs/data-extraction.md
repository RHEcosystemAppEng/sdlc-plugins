# Step 1 -- Data Extraction for TC-8021

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Upstream Affected Component | quinn-proto | customfield_10632 |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z` (for 2.2.x stream)
- Remediation task count per stream: 2 (upstream backport or dependency bump + downstream propagation)

## Deployment Context

- Affected repository: rhtpa-backend
- Deployment context: `upstream` (default, no Deployment Context column in Source Repositories)

## Affects Versions Discrepancy (noted for Step 3)

The PSIRT-assigned Affects Versions field contains **RHTPA 2.0.0**, but there is no 2.0.x version stream configured. This is incorrect and will need correction in Step 3 based on the version impact analysis.

## Version Impact Analysis (Step 2)

### Stream 2.2.x (in scope -- issue stream)

| Product Version | Build Tag | quinn-proto Version | Affected? | Notes |
|-----------------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of v0.4.8, same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed version) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed version) |

### Stream 2.1.x (out of scope -- cross-stream)

| Product Version | Build Tag | quinn-proto Version | Affected? | Notes |
|-----------------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Summary

- **In-scope stream (2.2.x)**: 3 versions affected (2.2.0, 2.2.1, 2.2.2), 2 versions already fixed (2.2.3, 2.2.4)
- **Out-of-scope stream (2.1.x)**: All 2 versions affected (2.1.0, 2.1.1)
- The fix (quinn-proto 0.11.14) is already present in the latest 2.2.x releases, confirming the upstream fix is available
