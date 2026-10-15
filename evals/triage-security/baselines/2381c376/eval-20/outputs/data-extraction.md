# Step 1 -- Data Extraction

## Issue: TC-8001

### Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | pscomponent:org/rhtpa-server | Label matching component label pattern `pscomponent:` |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (CVE Record) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | (none) | Issue comment history |
| Issue status | New | Jira status field |
| Assignee | Unassigned | Jira assignee field |

### Stream Scope Resolution

- **Summary suffix**: `[rhtpa-2.2]`
- **Mapped stream**: 2.2.x
- **Match**: The suffix `rhtpa-2.2` maps to the `2.2.x` entry in the Version Streams table (Konflux release repo `rhtpa-release.0.4.z`)
- **Scope**: This issue is **stream-scoped** to 2.2.x only. Steps 3-4 will apply only to versions within the 2.2.x stream. Cross-stream impact on 2.1.x will be evaluated in Case A.

### Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Category**: Source dependency
- **Remediation task count per stream**: 2 (upstream backport or dependency bump + downstream propagation)

### Deployment Context

- **Affected repository**: rhtpa-backend
- **URL**: https://github.com/rhtpa/rhtpa-backend
- **Deployment context**: upstream (default -- no Deployment Context column in Source Repositories table)

### Affects Versions Discrepancy (noted for Step 3)

The PSIRT-assigned Affects Version is `RHTPA 2.0.0`, but no 2.0.x stream exists in the Version Streams configuration. This is a wrong version assignment that will need correction in Step 3 based on the version impact analysis from Step 2.

### Version Impact Preview (from mock lock file data)

Using the quinn-proto versions from the security matrix mock data:

| Version | Stream | Build Tag | quinn-proto version | Affected? (< 0.11.14) | Notes |
|---------|--------|-----------|---------------------|----------------------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |
