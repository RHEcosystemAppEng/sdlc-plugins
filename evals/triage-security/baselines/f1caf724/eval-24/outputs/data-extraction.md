# Step 1 — Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate) |
| Deployment context | upstream (default — Deployment Context column absent from Source Repositories) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- Issue is **scoped** to stream 2.2.x only

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Affects Versions Correction

- **Current (PSIRT-assigned):** RHTPA 2.0.0
- **Proposed (scoped to 2.2.x stream):** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale:** PSIRT assigned "RHTPA 2.0.0" but no 2.0.x stream exists. Lock file analysis at pinned commits shows quinn-proto < 0.11.14 in versions 2.2.0, 2.2.1, and 2.2.2. Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.
- The 2.1.x stream versions (2.1.0, 2.1.1) are also affected but belong to a different stream scope and are handled via cross-stream impact (Case A).

## Cross-Stream Impact

Stream 2.1.x is also affected (quinn-proto 0.11.9 in both 2.1.0 and 2.1.1). Since this issue is scoped to 2.2.x, stream 2.1.x impact is handled via Case A cross-stream proactive remediation.
