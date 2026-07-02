# Step 1 -- Data Extraction for TC-8021

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Issue Key | TC-8021 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x only. Affects Versions corrections (Step 3) and remediation task creation (Step 8) are scoped to this stream, while cross-stream impact on 2.1.x is handled via Case B.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. The ecosystem is **Cargo**. Both streams (2.1.x and 2.2.x) have Cargo configured in their Ecosystem Mappings tables with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.3.z` (2.1.x) / `release/0.4.z` (2.2.x)

## Version Impact Analysis (Step 2)

Using the lock file data from security-matrix.md:

### quinn-proto versions by pinned tag

| Tag | quinn-proto version |
|-----|---------------------|
| v0.3.8 | 0.11.9 |
| v0.3.12 | 0.11.9 |
| v0.4.5 | 0.11.9 |
| v0.4.8 | 0.11.12 |
| v0.4.9 | (retag of v0.4.8) |
| v0.4.11 | 0.11.14 |
| v0.4.12 | 0.11.14 |

### Version Impact Table

Fix threshold: 0.11.14 (versions before 0.11.14 are affected)

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Affects Versions Correction (Step 3)

- **Current (PSIRT-assigned):** RHTPA 2.0.0
- **Proposed (scoped to 2.2.x stream):** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- RHTPA 2.0.0 is incorrect -- no 2.0.x stream exists in the Version Streams configuration. The issue is scoped to 2.2.x, and versions 2.2.0, 2.2.1, and 2.2.2 are affected based on lock file analysis.
- Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fix), so they are NOT affected.
