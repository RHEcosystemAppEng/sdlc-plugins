# Step 1 -- Data Extraction: TC-8003

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | Not available |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to
the **2.2.x** version stream, which is covered by the Konflux release repo
at `git.example.com/rhtpa/rhtpa-release.0.4.z` (local path:
`/home/dev/repos/rhtpa-release.0.4.z`).

**Issue stream scope**: 2.2.x only

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem
Mappings in the 2.2.x stream's security-matrix.md, this falls under the **Cargo**
ecosystem:

- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`
- **Upstream Branch**: `release/0.4.z`
- **Source Repository**: backend

## Version Impact Analysis (Step 2)

Since the issue is scoped to stream 2.2.x, the primary analysis focuses on
versions in that stream. However, following forward pointers and examining the
full matrix for completeness:

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | Outside issue scope |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | Outside issue scope |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | In scope |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | In scope |
| 2.2.x | 2.2.2 | v0.4.9 | (retag) | YES | Same as 2.2.1 |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | Fixed version shipped |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | Fixed version shipped |

### Affects Versions Correction (Step 3)

- **Current**: RHTPA 2.2.0
- **Proposed** (scoped to 2.2.x affected versions): RHTPA 2.2.0, RHTPA 2.2.1
- RHTPA 2.2.2 is a retag of 2.2.1 and is also affected, but since it shares
  the same source content it should be included if it exists as a Jira version.
- RHTPA 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are
  NOT affected.

The PSIRT-assigned Affects Versions is incomplete -- it is missing RHTPA 2.2.1
(which ships quinn-proto 0.11.12, still within the vulnerable range).
