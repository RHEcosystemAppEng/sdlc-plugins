# Step 1 -- Data Extraction for TC-8021

## Extracted CVE Metadata

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
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. This issue is **scoped** to stream 2.2.x only.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. This maps to the **Cargo** ecosystem per the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md. Cargo is a source dependency ecosystem, meaning remediation produces **two tasks per stream**: upstream backport (or dependency bump) + downstream propagation.

## Deployment Context Lookup

The affected repository is **rhtpa-backend** (identified via the pscomponent:org/rhtpa-server label). The Source Repositories table in CLAUDE.md lists rhtpa-backend. The Deployment Context column is absent from the Source Repositories table, so the default deployment context is **upstream**.

## Version Impact Analysis (Step 2)

### Scoped stream: 2.2.x

Using lock file data from security-matrix.md for quinn-proto versions by tag:

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | = 0.11.14 (at fix threshold) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | = 0.11.14 (at fix threshold) |

### Cross-stream: 2.1.x (for Case A evaluation)

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

## Affects Versions Mismatch

PSIRT-assigned Affects Versions: `RHTPA 2.0.0`
This is incorrect -- RHTPA 2.0.0 does not exist in any configured version stream.

Correct Affects Versions (scoped to 2.2.x stream): `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2`
(Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 which is at or above the fix threshold.)
