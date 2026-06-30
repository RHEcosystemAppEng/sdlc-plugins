# Data Extraction — TC-8003

## Step 0 — Configuration Validation

Project configuration validated from CLAUDE.md:

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend) |

All required sections present: Repository Registry, Jira Configuration, Code Intelligence, Security Configuration (with Product Lifecycle, Version Streams, Source Repositories).

No Embargo policy URL configured — Step 1.7 will be skipped.
No ProdSec Jira account ID configured — @mentions will be omitted.
No Upstream Affected Component / PS Component / Stream custom fields configured — Step 4.3 (cross-CVE overlap detection) will be skipped.

## Step 1 — Parsed CVE Data

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
| Upstream fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

Summary suffix: `[rhtpa-2.2]`
Mapped to configured Version Stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
Issue stream scope: **2.2.x only**

Steps 3-4 will be scoped to the 2.2.x stream. Cross-stream impact on 2.1.x will be noted separately (Case B).

## Ecosystem Detection

Library: quinn-proto (Rust crate)
Ecosystem: **Cargo**
Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock`
Upstream branch: `release/0.4.z` (for stream 2.2.x)

## Step 1.5 — External CVE Data Enrichment

(Simulated — external APIs not called per eval instructions)

Fix threshold from Jira description: **0.11.14**
This fix threshold is used for version impact comparisons in Step 2.3.

## Step 1.7 — Embargo Check

No Embargo policy URL is configured in Security Configuration. Step 1.7 is skipped.
