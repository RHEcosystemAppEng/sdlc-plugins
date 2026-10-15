# Step 1 -- Data Extraction: TC-8003

## Extracted CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This is a **scoped** issue -- Steps 3 and 4 apply only to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table for the 2.2.x stream lists **Cargo** as a configured ecosystem with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Ecosystem classification: **Source dependency (Cargo)**. This would normally produce 2 remediation tasks per affected stream (upstream backport or dependency bump + downstream propagation).

## Deployment Context

The affected repository `rhtpa-backend` has deployment context: **upstream** (default, since the Deployment Context column is absent from the Source Repositories table in the mock CLAUDE.md).

## Step 0 -- Configuration Validation

All required Security Configuration sections are present:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Jira version prefix: RHTPA
- Vulnerability issue type ID: 10024
- Product pages URL: https://access.example.com/product-life-cycle/rhtpa
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Version Streams: 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z)
- Source Repositories: rhtpa-backend

## Step 2 -- Version Impact Analysis

Using the mock lock file data from the security matrix, the quinn-proto versions at each pinned tag are:

### Full Version Impact Table (all streams)

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Stream-scoped impact (2.2.x only, per issue scope)

Affected versions within stream 2.2.x: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**
Not affected within stream 2.2.x: RHTPA 2.2.3, RHTPA 2.2.4

### Cross-stream impact

Stream 2.1.x is also affected (2.1.0, 2.1.1), but this is outside TC-8003's scope. Cross-stream impact would normally be noted in a Case A comment.

### Upstream fix status

The mock lock file data shows that tag `v0.4.11` (used in 2.2.3) and `v0.4.12` (used in 2.2.4) both ship quinn-proto 0.11.14, which is the fix version. The upstream branch `release/0.4.z` appears to carry the fixed version.
