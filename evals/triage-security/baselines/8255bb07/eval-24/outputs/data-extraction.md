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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x**, which matches a configured Version Stream in Security Configuration. This issue is **stream-scoped** to 2.2.x.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**, which is listed in both streams' Ecosystem Mappings tables with:
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z` (2.2.x stream), `release/0.3.z` (2.1.x stream)

## Deployment Context Lookup

The Source Repositories table in CLAUDE.md does **not** have a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. However, since the column is absent entirely, the Coordination Guidance subsection is omitted from remediation task descriptions.

## Step 0 -- Configuration Validation

All required Security Configuration sections are present:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Jira version prefix: RHTPA
- Vulnerability issue type ID: 10024
- Product pages URL: https://access.example.com/product-life-cycle/rhtpa
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Embargo policy URL: not configured (Step 1.7 skipped)
- Upstream Affected Component custom field: not configured (Step 4.3 and Step 7 skipped)

No Deployment Context column detected in Source Repositories table -- defaulting all repos to `upstream`.

## Version Impact Analysis

### 2.2.x Stream (scoped)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed version |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed version |

### 2.1.x Stream (cross-stream analysis)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | |

### Summary

- **2.2.x stream**: versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14).
- **2.1.x stream**: all versions (2.1.0, 2.1.1) are affected -- this triggers Case B cross-stream impact.

### Affects Versions Correction

The PSIRT-assigned Affects Versions field contains `RHTPA 2.0.0`, which does not match any supported version stream. The correct Affects Versions based on lock file analysis should be `RHTPA 2.2.0`, `RHTPA 2.2.1`, and `RHTPA 2.2.2` (the affected versions within the scoped 2.2.x stream).
