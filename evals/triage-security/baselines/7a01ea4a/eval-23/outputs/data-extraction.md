# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream
(Konflux release repo: `rhtpa-release.0.4.z`). This issue is **scoped** to stream 2.2.x only.

## Ecosystem Detection

Vulnerable library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**.

Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
Upstream branch (2.2.x stream): `release/0.4.z`
Upstream branch (2.1.x stream): `release/0.3.z`

## Deployment Context Lookup

Affected component label `pscomponent:org/rhtpa-server` maps to source repository **rhtpa-backend**.

Source Repositories table lookup:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | **customer-shipped** |

Deployment context for rhtpa-backend: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance
in remediation task descriptions. The `customer-shipped` context requires coordination with
Product Security for CVE assignment, advisory preparation, and formal disclosure.

## Version Impact Table

CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.8` | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | fixed at 0.11.14 |

### Summary

- **2.2.x stream (in scope):** Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Fixed from 2.2.3 onwards (quinn-proto bumped to 0.11.14).
- **2.1.x stream (out of scope):** All versions (2.1.0, 2.1.1) are affected. This is a cross-stream impact finding (Case B).

### Affects Versions Correction

Current Affects Versions on TC-8001: `RHTPA 2.0.0`

RHTPA 2.0.0 does not match any version in the supportability matrix -- this is incorrect.
Scoped to the 2.2.x stream, the correct Affects Versions are:

- RHTPA 2.2.0
- RHTPA 2.2.1
- RHTPA 2.2.2

Proposed correction: `[RHTPA 2.0.0]` --> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`
