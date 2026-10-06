# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)
- Issue is **scoped** to the 2.2.x stream

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Remediation tasks per stream: **2** (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

## Deployment Context Lookup

- Affected component label: `pscomponent:org/rhtpa-server`
- Source Repository match: **rhtpa-backend**
- Deployment Context column value: **customer-shipped**
- Lookup result: The repository `rhtpa-backend` is configured with deployment context `customer-shipped` in the Source Repositories table of Security Configuration.

## Affects Versions Assessment

- PSIRT-assigned: `RHTPA 2.0.0`
- Problem: No 2.0.x stream exists in the Version Streams configuration. The PSIRT version is **wrong**.
- This will be corrected in Step 3 based on the version impact table.

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build | Backend Tag | quinn-proto | Affected? | Notes |
|--------|---------|-------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.8` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | 0.11.14 | NO | fixed at 0.11.14 |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | release/0.3.z | Latest tag v0.3.12 ships 0.11.9 -- NOT fixed |
| 2.2.x | Cargo | release/0.4.z | Tags v0.4.11+ ship 0.11.14 -- FIXED at v0.4.11 |

### Scoped Impact Summary

Since this issue is scoped to stream **2.2.x**:

- **In-scope affected versions**: 2.2.0, 2.2.1, 2.2.2
- **In-scope unaffected versions**: 2.2.3, 2.2.4 (already fixed)
- **Cross-stream affected versions**: 2.1.0, 2.1.1 (Case A -- cross-stream impact)

### Affects Versions Correction (Step 3)

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
- Rationale: RHTPA 2.0.0 does not exist as a configured stream. Based on lock file analysis at pinned commits from security-matrix.md, versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14. Versions 2.2.3 and 2.2.4 ship the fixed version and are not affected. Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.
