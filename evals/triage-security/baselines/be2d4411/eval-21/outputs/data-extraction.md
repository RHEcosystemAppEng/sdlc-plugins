# Step 1 -- Data Extraction for TC-8020

## Extracted CVE Data

| Field | Value |
|-------|-------|
| Issue Key | TC-8020 |
| CVE ID | CVE-2026-31812 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server |
| Affects Versions (PSIRT-assigned) | RHTPA 2.0.0 |
| Due Date | 2026-07-15 |
| Assignee | Unassigned |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream Fix PR | https://github.com/quinn-rs/quinn/pull/2048 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable package `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**, with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

## Component and Deployment Context

- Component label: `pscomponent:org/rhtpa-server`
- Affected repository: rhtpa-backend (matched from Source Repositories)
- Deployment context: upstream (default -- no Deployment Context column in Source Repositories)

## Version Impact Analysis (Step 2)

### Aggregated Version Impact Table

Using the mock lock file data from the security matrix, comparing quinn-proto versions against the fix threshold of 0.11.14:

| Version | Stream | Build Tag | quinn-proto version | Affected? | Notes |
|---------|--------|-----------|---------------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Stream-Scoped Summary (2.2.x only, per issue scope)

- **Affected**: 2.2.0, 2.2.1, 2.2.2
- **Not affected**: 2.2.3, 2.2.4

### Cross-Stream Impact

The 2.1.x stream (versions 2.1.0 and 2.1.1) is also affected -- both ship quinn-proto 0.11.9 which is below the fix threshold of 0.11.14. This triggers Case B (cross-stream impact) in Step 8.

### Affects Versions Correction (Step 3)

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed (stream-scoped to 2.2.x, based on lock file analysis)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: RHTPA 2.0.0 does not exist in any configured version stream. The affected 2.2.x versions are 2.2.0 (quinn-proto 0.11.9), 2.2.1 (quinn-proto 0.11.12), and 2.2.2 (retag of 2.2.1). Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 which is at or above the fix threshold.
