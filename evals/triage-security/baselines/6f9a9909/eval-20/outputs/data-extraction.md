# Step 1 -- Data Extraction

## Issue: TC-8001

### Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

### Stream Scope Resolution

- **Summary suffix**: `[rhtpa-2.2]`
- **Mapped stream**: 2.2.x (matches Version Streams table entry for `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- **Issue stream scope**: Scoped to stream **2.2.x**

This issue is stream-scoped. Steps 3 and 4 will apply only to the 2.2.x stream for Affects Versions correction, while the version impact analysis (Step 2) will still check all streams for cross-stream impact detection (Case A).

### Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)

### Affects Versions Discrepancy (Preliminary)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, but no 2.0.x stream is configured in the Version Streams table. The issue summary suffix `[rhtpa-2.2]` indicates this issue should be scoped to the **2.2.x** stream. The Affects Versions field will need correction in Step 3 after version impact analysis confirms which 2.2.x versions are actually affected.

### Version Impact Table (from mock lock file data)

Using the mock lock file data from the security matrix as simulated `git show` output:

**Stream 2.1.x (rhtpa-release.0.3.z):**

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | `v0.3.12` | 0.11.9 | YES | < 0.11.14 |

**Stream 2.2.x (rhtpa-release.0.4.z):**

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | `v0.4.8` | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | `v0.4.11` | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | `v0.4.12` | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Summary

- **Affected versions in scoped stream (2.2.x)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected in scoped stream (2.2.x)**: 2.2.3, 2.2.4 (ship fixed quinn-proto 0.11.14)
- **Cross-stream impact (2.1.x)**: Both 2.1.0 and 2.1.1 are affected (quinn-proto 0.11.9) -- Case A applies
- **PSIRT Affects Versions mismatch**: Current `RHTPA 2.0.0` is incorrect; should be corrected to affected 2.2.x versions per Step 3
- **Ecosystem**: Cargo (source dependency) -- remediation requires 2 tasks per affected stream (upstream backport + downstream propagation)
