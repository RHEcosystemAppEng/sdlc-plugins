# Step 1 -- Data Extraction: TC-8001

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
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo `rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. From the 2.2.x stream's Ecosystem Mappings table:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

Detected ecosystem: **Cargo** (source dependency)

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to source repository `rhtpa-backend`.

From the Source Repositories table in Security Configuration:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | **customer-shipped** |

Deployment context for rhtpa-backend: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance requiring coordination with Product Security for CVE assignment, advisory preparation, and formal disclosure.

## Version Impact Analysis

### Scoped stream: 2.2.x

| Version | Build | Backend Tag | quinn-proto Version | Affected? | Notes |
|---------|-------|-------------|---------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.11.9 | **YES** | < 0.11.14 |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.11.12 | **YES** | < 0.11.14 |
| 2.2.2 | 0.4.9 | `v0.4.8` | 0.11.12 | **YES** | same as 2.2.1 (retag) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.11.14 | NO | >= 0.11.14 (fixed) |

The fix was incorporated starting with version 2.2.3 (build 0.4.11, backend tag `v0.4.11`).

### Cross-stream: 2.1.x

| Version | Build | Backend Tag | quinn-proto Version | Affected? | Notes |
|---------|-------|-------------|---------------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 0.11.9 | **YES** | < 0.11.14 |
| 2.1.1 | 0.3.12 | `v0.3.12` | 0.11.9 | **YES** | < 0.11.14 |

All 2.1.x versions ship a vulnerable version of quinn-proto. No fix has been incorporated in this stream.

## Affects Versions Correction

PSIRT set Affects Versions to `RHTPA 2.0.0`, but there is no 2.0.x version stream configured. Based on lock file evidence, the correct Affects Versions for the scoped 2.2.x stream are:

- **RHTPA 2.2.0** (ships quinn-proto 0.11.9)
- **RHTPA 2.2.1** (ships quinn-proto 0.11.12)
- **RHTPA 2.2.2** (ships quinn-proto 0.11.12, retag of 2.2.1)

Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, the fixed version).

Remove: `RHTPA 2.0.0`
Add: `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`
