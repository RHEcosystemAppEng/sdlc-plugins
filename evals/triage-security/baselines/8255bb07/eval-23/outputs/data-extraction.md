# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component (label) | pscomponent:org/rhtpa-server |
| Mapped repository | rhtpa-backend |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo (Rust crate) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Deployment context | **customer-shipped** |

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to the `rhtpa-backend` repository. Looking up `rhtpa-backend` in the Source Repositories table from Security Configuration:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | customer-shipped |

Result: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions. The `customer-shipped` context requires coordination with Product Security for CVE assignment, advisory preparation, and formal disclosure.

## Stream Scope Resolution

The issue summary contains `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo `rhtpa-release.0.4.z`). This issue is stream-scoped to 2.2.x only.

## Ecosystem Detection

`quinn-proto` is a Rust crate -- ecosystem is **Cargo**. From the 2.2.x stream's Ecosystem Mappings:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Version Impact Analysis

### Stream 2.2.x (scoped -- primary analysis)

| Version | Build | Build Date | Backend Tag | quinn-proto Version | Affected? | Evidence |
|---------|-------|------------|-------------|---------------------|-----------|----------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | 0.11.12 (retag of v0.4.8) | YES | same as 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

The latest 2.2.x releases (2.2.3, 2.2.4) already ship the fixed version of quinn-proto. The fix was incorporated starting with build 0.4.11. Versions 2.2.0 through 2.2.2 shipped vulnerable versions.

### Stream 2.1.x (cross-stream impact)

| Version | Build | Build Date | Backend Tag | quinn-proto Version | Affected? | Evidence |
|---------|-------|------------|-------------|---------------------|-----------|----------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

All 2.1.x versions are affected. The fix has not been backported to the release/0.3.z branch.

## Affects Versions Correction

The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) is incorrect:
- There is no configured 2.0.x version stream
- The correct Affects Versions based on lock file evidence: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**
- Versions 2.2.3 and 2.2.4 are NOT affected (already ship the fix)
