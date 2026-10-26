# Data Extraction (Step 1) -- TC-8021

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
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** version stream in Security Configuration (Konflux release repo:
`git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will apply only to
versions within the 2.2.x stream, while the full version impact analysis
(Step 2) covers all configured streams for cross-stream visibility.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem
Mappings tables in security-matrix.md, the ecosystem is **Cargo**.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branches: `release/0.3.z` (2.1.x), `release/0.4.z` (2.2.x)

Ecosystem classification: **Source dependency** -- remediation produces 2 tasks
per affected stream (dependency bump + downstream propagation, since the upstream
fix is already available per Step 2.5 analysis).

## Version Impact Analysis (Step 2)

Using lock file data from the security matrix for quinn-proto versions:

### Version Impact Table

| Version | Stream | quinn-proto version | Affected? | Notes |
|---------|--------|---------------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as v0.4.8 = 0.11.12) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD (latest tag) | Fixed? |
|--------|-----------|-----------------|------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

For the 2.2.x stream, the upstream branch `release/0.4.z` already ships
quinn-proto 0.11.14 at its latest tag (v0.4.12). This means the remediation
path is a **dependency bump** (`cargo update`) rather than an upstream backport.

For the 2.1.x stream, the upstream branch `release/0.3.z` still ships
quinn-proto 0.11.9 at its latest tag (v0.3.12). If remediation is needed for
2.1.x, it would require an upstream backport.

## Affects Versions Correction (Step 3)

The issue is scoped to stream 2.2.x. Only 2.2.x versions are included in the
correction.

- **Current (PSIRT-assigned):** RHTPA 2.0.0
- **Proposed correction:** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Rationale: RHTPA 2.0.0 does not exist as a configured version stream. The
actual affected 2.2.x versions are 2.2.0, 2.2.1, and 2.2.2 based on lock file
evidence showing quinn-proto versions below the 0.11.14 fix threshold. Versions
2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 and are not affected.
