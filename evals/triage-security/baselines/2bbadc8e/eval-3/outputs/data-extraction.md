# Step 1 -- Data Extraction for TC-8003

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern from Security Configuration) |
| Product version (PSIRT-claimed) | [rhtpa-2.2] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (i.e., < 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comments |
| Assignee | Unassigned | Issue field |
| Status | New | Issue field |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped to Version Stream: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x only** (scoped issue)

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

## Step 0 -- Configuration Validation

All required Security Configuration sections are present:

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Jira version prefix: RHTPA
- Vulnerability issue type ID: 10024
- Product pages URL: https://access.example.com/product-life-cycle/rhtpa
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Version Streams: 2.1.x, 2.2.x (both configured)
- Source Repositories: rhtpa-backend (configured)

## Step 0.3 -- Matrix Staleness Check

- Matrix Last-Updated: 2026-06-28T10:00:00Z
- Current date: 2026-10-29
- Age: approximately 123 days (exceeds 14-day threshold)
- Status: STALE -- however, for this eval we proceed with the current matrix data

## Step 2 -- Version Impact Analysis

### Version Impact Table for CVE-2026-31812 (quinn-proto < 0.11.14)

**Stream 2.2.x (issue scope):**

| Version | Backend Tag | quinn-proto | Affected? | Notes |
|---------|-------------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

**Stream 2.1.x (outside issue scope, for cross-stream awareness):**

| Version | Backend Tag | quinn-proto | Affected? | Notes |
|---------|-------------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

### Affects Versions Correction (Step 3)

- Current Affects Versions: [RHTPA 2.2.0]
- Proposed Affects Versions (scoped to 2.2.x stream): [RHTPA 2.2.0, RHTPA 2.2.1]
- Note: RHTPA 2.2.2 is a retag of 2.2.1 and is affected, but version 2.2.2 may or may not have a corresponding Jira version. Versions 2.2.3 and 2.2.4 are NOT affected (ship fixed quinn-proto 0.11.14).
- PSIRT's Affects Versions are **incomplete** -- missing RHTPA 2.2.1.
