# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| Issue Key | TC-8021 |
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE Record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
configured **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This is a **scoped** issue -- triage Steps 3 and 4 are scoped to the 2.2.x stream.
Other streams (2.1.x) are checked for cross-stream impact (Case A) but Affects
Versions corrections apply only to 2.2.x.

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

## Version Impact Analysis (Step 2)

Using the security matrix data and lock file contents for quinn-proto:

### Version Impact Table

| Version | Stream | Build Tag | quinn-proto version | Affected? | Notes |
|---------|--------|-----------|---------------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8, quinn-proto 0.11.12) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Status |
|--------|-----------|-----------------|------------|
| 2.1.x | Cargo | release/0.3.z | Unknown (not checked -- out of issue scope) |
| 2.2.x | Cargo | release/0.4.z | Fixed at v0.4.11+ (quinn-proto 0.11.14) |

### Affects Versions Correction (Step 3)

- **Current Affects Versions**: RHTPA 2.0.0 (incorrect -- no 2.0.x stream exists)
- **Issue scope**: 2.2.x stream only
- **Affected versions in 2.2.x**: 2.2.0, 2.2.1, 2.2.2
- **Proposed Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Action**: Remove RHTPA 2.0.0, add RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
