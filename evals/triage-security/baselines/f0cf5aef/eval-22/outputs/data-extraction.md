# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| Issue Key | TC-8021 |
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
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

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 8 will apply only to versions within the 2.2.x stream. Cross-stream impact on other streams (2.1.x) is handled via Case A.

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Classification**: Source dependency
- **Remediation task count per stream**: 2 (upstream backport + downstream propagation)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch (2.2.x stream)**: `release/0.4.z`

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories. No explicit Deployment Context column is present, so the default context is `upstream`.

## Version Impact Analysis (Step 2)

Using lock file data from the security matrix, the quinn-proto dependency versions at each pinned commit are:

### Stream 2.2.x (rhtpa-release.0.4.z) -- in scope

| Version | Build Tag | quinn-proto Version | Affected? | Reason |
|---------|-----------|---------------------|-----------|--------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 (fix threshold) |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | Retag of v0.4.8, same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (at or above fix threshold) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (at or above fix threshold) |

### Stream 2.1.x (rhtpa-release.0.3.z) -- out of scope, for Case A analysis

| Version | Build Tag | quinn-proto Version | Affected? | Reason |
|---------|-----------|---------------------|-----------|--------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which is incorrect -- there is no 2.0.x version stream configured.

Scoped to the 2.2.x stream, the affected versions are RHTPA 2.2.0, RHTPA 2.2.1, and RHTPA 2.2.2. Versions 2.2.3 and 2.2.4 are not affected (quinn-proto was already updated to 0.11.14).

Proposed correction:
- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
