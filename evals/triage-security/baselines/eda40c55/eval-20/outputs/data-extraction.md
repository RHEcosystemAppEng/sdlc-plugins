# Step 1 -- Data Extraction

## Issue: TC-8001

### Parsed CVE Data Table

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`), summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS score | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | None | Issue comment history |

### Stream Scope Resolution

- **Summary suffix**: `[rhtpa-2.2]`
- **Mapped stream**: 2.2.x
- **Konflux release repo**: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- **Scope**: Scoped -- analyze only the 2.2.x stream (Steps 3-4 scoped to single stream)

The suffix `rhtpa-2.2` maps to the configured Version Stream `2.2.x` in the
Security Configuration. This issue is stream-scoped to 2.2.x only.

### Ecosystem Detection

- **Library**: quinn-proto
- **Ecosystem**: Cargo (Rust crate)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch**: `release/0.4.z` (for the 2.2.x stream)
- **Remediation pattern**: 2 tasks (upstream backport + downstream propagation)

### Deployment Context

- **Affected repository**: rhtpa-backend (matched from component label `pscomponent:org/rhtpa-server`)
- **Deployment context**: `upstream` (default -- no Deployment Context column in Source Repositories table)

### Affects Versions Discrepancy (noted for Step 3)

The Jira `Affects Versions` field is set to **RHTPA 2.0.0**, but the issue summary
indicates stream **2.2.x** (`[rhtpa-2.2]`). There is no `2.0.x` stream configured
in the Version Streams table. This discrepancy will be corrected in Step 3 based on
lock file evidence from the version impact analysis.

### quinn-proto Versions in 2.2.x Stream (from mock lock file data)

| Product Version | Build Tag | quinn-proto Version | Affected? |
|-----------------|-----------|---------------------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES (< 0.11.14) |
| 2.2.1 | v0.4.8 | 0.11.12 | YES (< 0.11.14) |
| 2.2.2 | v0.4.9 | _(retag of v0.4.8)_ | YES (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO (>= 0.11.14, fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO (>= 0.11.14, fixed) |

### quinn-proto Versions in 2.1.x Stream (cross-stream reference)

| Product Version | Build Tag | quinn-proto Version | Affected? |
|-----------------|-----------|---------------------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES (< 0.11.14) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES (< 0.11.14) |
