# Step 1 -- Data Extraction: TC-8001

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
| Due date | 2026-07-15 |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Status | New |
| Assignee | Unassigned |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)
- Issue is **stream-scoped** -- Steps 3 and 8 are scoped to the 2.2.x stream. Cross-stream impact (Case A) applies to 2.1.x if also affected.

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Remediation tasks per stream: 2 (dependency bump or upstream backport + downstream propagation)

## Deployment Context Lookup

- Component label: `pscomponent:org/rhtpa-server`
- Mapped repository: **rhtpa-backend** (from Source Repositories table)
- Source Repository URL: https://github.com/rhtpa/rhtpa-backend
- **Deployment Context: customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination
guidance in each remediation task's Implementation Notes.

## Version Impact Analysis (Step 2)

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0   | 2.1.x  | v0.3.8      | 0.11.9      | YES       |       |
| 2.1.1   | 2.1.x  | v0.3.12     | 0.11.9      | YES       |       |
| 2.2.0   | 2.2.x  | v0.4.5      | 0.11.9      | YES       |       |
| 2.2.1   | 2.2.x  | v0.4.8      | 0.11.12     | YES       |       |
| 2.2.2   | 2.2.x  | v0.4.8      | 0.11.12     | YES       | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3   | 2.2.x  | v0.4.11     | 0.11.14     | NO        | ships fixed version |
| 2.2.4   | 2.2.x  | v0.4.12     | 0.11.14     | NO        | ships fixed version |

### Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (assumed from Cargo.lock presence)
  Profile: production (quinn-proto is a QUIC transport runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag | Version at Tag | Fixed? |
|--------|-----------|-----------------|------------|----------------|--------|
| 2.1.x  | Cargo     | release/0.3.z   | v0.3.12    | 0.11.9         | NO     |
| 2.2.x  | Cargo     | release/0.4.z   | v0.4.12    | 0.11.14        | YES    |

### Affects Versions Correction (Step 3)

- Current (PSIRT-assigned): `[RHTPA 2.0.0]`
- RHTPA 2.0.0 does not match any version in the supportability matrix -- PSIRT assignment is incorrect.
- Proposed correction (scoped to 2.2.x stream): `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
- Rationale: lock file analysis at pinned commits confirms quinn-proto < 0.11.14 in versions 2.2.0 through 2.2.2. Versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (fixed).

### Cross-Stream Impact Summary

- **2.2.x** (issue scope): versions 2.2.0, 2.2.1, 2.2.2 affected. Fix available upstream (release/0.4.z ships 0.11.14).
- **2.1.x** (cross-stream): versions 2.1.0, 2.1.1 affected. Fix NOT available upstream (release/0.3.z ships 0.11.9). Case A cross-stream impact applies -- preemptive remediation tasks will be created for 2.1.x.
