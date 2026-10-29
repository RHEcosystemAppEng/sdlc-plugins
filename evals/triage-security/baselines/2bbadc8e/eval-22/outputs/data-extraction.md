# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote links (GitHub PR) |
| Advisory URL | GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (CVE Record) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Upstream Affected Component | quinn-proto | customfield_10632 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to the 2.2.x stream

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

Per the ecosystem classification table, Cargo is a source dependency ecosystem. This produces **2 remediation tasks per stream**: either upstream backport + downstream propagation (if fix not available upstream), or dependency bump + downstream propagation (if fix already available upstream).

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: upstream (default, no Deployment Context column in Source Repositories)

## Vulnerability Details

The quinn-proto crate before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. This is classified as a denial of service (DoS) vulnerability.

The vulnerability exists because quinn-proto does not properly validate the number of streams requested in a STREAMS frame. An attacker can send a specially crafted frame that causes the server to allocate an unbounded number of stream state objects, leading to a panic when the allocation exceeds internal limits.

## Version Impact Analysis (Step 2)

### 2.1.x stream (rhtpa-release.0.3.z) -- cross-stream reference

| Version | Build Tag | quinn-proto Version | Affected? | Evidence |
|---------|-----------|---------------------|-----------|----------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

### 2.2.x stream (rhtpa-release.0.4.z) -- issue-scoped stream

| Version | Build Tag | quinn-proto Version | Affected? | Evidence |
|---------|-----------|---------------------|-----------|----------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of v0.4.8 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed version) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed version) |

### Summary

- **2.2.x stream (scoped)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14) and are NOT affected.
- **2.1.x stream (cross-stream)**: Both versions (2.1.0, 2.1.1) are affected. All ship quinn-proto 0.11.9.
- The fix was introduced in the 2.2.x stream starting with build v0.4.11 (version 2.2.3).
- Since later builds in the 2.2.x stream already ship quinn-proto 0.11.14, the upstream branch (`release/0.4.z`) already has the fix available. This means remediation uses the "dependency bump" variant rather than "upstream backport."

## Affects Versions Correction (Step 3)

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed (based on lock file evidence, scoped to 2.2.x stream)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: RHTPA 2.0.0 does not match any configured version stream. The issue is scoped to stream 2.2.x per its summary suffix `[rhtpa-2.2]`. Lock file analysis confirms versions 2.2.0 through 2.2.2 ship quinn-proto < 0.11.14. Versions 2.2.3 and 2.2.4 already ship the fixed version and should not be included.
