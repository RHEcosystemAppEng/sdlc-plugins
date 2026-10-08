# Step 1 -- Data Extraction for TC-8021

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
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table. This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings table in the security-matrix.md for both streams, the matching ecosystem is **Cargo**.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch (2.2.x / 0.4.z stream): `release/0.4.z`
- Upstream branch (2.1.x / 0.3.z stream): `release/0.3.z`
- Ecosystem classification: **Source dependency** -- produces 2 remediation tasks per affected stream (dependency bump + downstream propagation when fix is available upstream, or upstream backport + downstream propagation when fix is not available)

## Version Impact Analysis (Step 2)

Using the mock lock file data from security-matrix-mock.md, the quinn-proto versions at each pinned tag are:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of v0.4.8, same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | = 0.11.14 (fixed version) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | = 0.11.14 (fixed version) |

### Combined Version Impact Table

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

## Upstream Fix Status (Step 2.5)

Based on the lock file data, the latest tags on each upstream branch already ship the fix:

| Stream | Ecosystem | Upstream Branch | Latest Tag | Version at Latest Tag | Fixed? |
|--------|-----------|-----------------|------------|----------------------|--------|
| 2.1.x | Cargo | release/0.3.z | v0.3.12 | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | v0.4.12 | 0.11.14 | YES |

For stream 2.2.x, the upstream branch (release/0.4.z) already ships quinn-proto 0.11.14 as of v0.4.11. The fix is available upstream for 2.2.x.

For stream 2.1.x, the upstream branch (release/0.3.z) still ships quinn-proto 0.11.9. The fix is NOT available upstream for 2.1.x.

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is `RHTPA 2.0.0`. However, no 2.0.x stream is configured in the Version Streams table. The issue is scoped to stream 2.2.x.

Within the 2.2.x stream, the affected versions are: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.
Versions RHTPA 2.2.3 and RHTPA 2.2.4 are NOT affected (they ship quinn-proto 0.11.14).

Proposed correction: `Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

The PSIRT-assigned version "RHTPA 2.0.0" is incorrect -- there is no 2.0.x stream, and the issue's stream suffix indicates 2.2.x. The correction scopes Affects Versions to only the actually-affected 2.2.x versions based on lock file evidence.
