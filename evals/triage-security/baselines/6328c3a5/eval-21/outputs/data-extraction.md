# Step 1 -- Data Extraction for TC-8020

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching component label pattern `pscomponent:` |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field (PSIRT-assigned) |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote link |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote link |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote link |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Upstream Affected Component | quinn-proto | customfield_10632 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Remediation task structure: 2 tasks per stream (upstream backport or dependency bump + downstream propagation)

## Version Impact Analysis (Step 2)

Using mock lock file data from security-matrix-mock.md:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES | same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14, fixed |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14, fixed |

### Combined Version Impact Table

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed |

## Affects Versions Correction (Step 3)

Since TC-8020 is scoped to stream 2.2.x, only 2.2.x versions are in scope for
Affects Versions on this issue:

- **Current (PSIRT-assigned):** RHTPA 2.0.0
- **Proposed (lock-file evidence):** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

RHTPA 2.0.0 is incorrect -- there is no 2.0.x stream configured. The PSIRT-assigned
version does not match any configured version stream. Correction is required.

Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, which is the
fix version) and are excluded from Affects Versions.

## Cross-Stream Impact (Case A consideration)

The issue is scoped to 2.2.x, but version impact analysis shows stream 2.1.x is
also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). This
triggers Case A -- cross-stream impact, which would post a cross-stream impact
comment and check for existing sibling CVE Jiras for stream 2.1.x.
