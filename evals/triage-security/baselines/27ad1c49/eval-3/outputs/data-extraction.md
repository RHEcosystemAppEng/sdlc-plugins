# Data Extraction — TC-8003

## Step 0 — Configuration Validation

Project configuration validated successfully. All required sections present.

| Configuration Field | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | Not configured |
| PS Component field | Not configured |
| Stream custom field | Not configured |
| ProdSec contact email | Not configured |
| ProdSec Jira account ID | Not configured |
| Embargo policy URL | Not configured |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default — no Deployment Context column) |

## Step 0.3 — Matrix Staleness Check

Security matrix `Last-Updated` timestamp: `2026-06-28T10:00:00Z`
Current date: 2026-10-13
Days since last update: 107 days (exceeds 14-day threshold)

Staleness warning would be raised. For this eval, proceeding with current matrix data.

## Step 1 — Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`.
Mapped to configured Version Stream: **2.2.x**
Issue stream scope: **2.2.x** (scoped issue — Steps 3-4 apply to this stream only)

## Ecosystem Detection

Library: quinn-proto (Rust crate)
Ecosystem: **Cargo**
Category: Source dependency
Remediation tasks per stream (if needed): 2 (upstream backport/dependency bump + downstream propagation)

## Deployment Context

Repository: rhtpa-backend
Deployment context: **upstream** (default, Deployment Context column absent from Source Repositories table)

## Step 1.5 — External CVE Data Enrichment

(Not performed — no external API calls in this eval. Would query MITRE CVE API and OSV.dev for CVE-2026-31812 to cross-validate the fix threshold of 0.11.14.)

## Step 1.7 — Embargo Check

Embargo policy URL is not configured in Security Configuration. Step 1.7 skipped entirely.

## Step 2 — Version Impact Analysis (Partial)

Using mock lock file data from the security matrix, the version impact for quinn-proto across the issue's scoped stream (2.2.x) would be:

### Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

Cross-stream impact (2.1.x, outside issue scope):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |

Note: Full version impact analysis is documented here for context, but because TC-8003 is identified as a duplicate in Step 4, remediation task creation does not proceed.
