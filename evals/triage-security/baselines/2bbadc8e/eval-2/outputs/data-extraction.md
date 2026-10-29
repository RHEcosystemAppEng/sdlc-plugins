# Data Extraction -- Step 1

## Issue Metadata

| Field | Value |
|-------|-------|
| Issue Key | TC-8002 |
| Issue Type | Vulnerability |
| Status | New |
| Assignee | Unassigned |
| Due Date | 2026-07-30 |

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-28940 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | serde_json | Description |
| Affected version range | versions before 1.0.135 (< 1.0.135) | Description |
| Fixed version | 1.0.135 | Description |
| CVSS | 5.3 (Medium) | Description |
| Upstream fix PR | N/A (not provided in remote links) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 | Remote links |
| Additional references | https://rustsec.org/advisories/RUSTSEC-2026-0019.html | Description |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- This issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Vulnerable library: serde_json (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z` (for 2.2.x stream)

## Deployment Context

- Affected repository: rhtpa-backend
- Deployment context: **upstream** (default, from Source Repositories table)

## Security Configuration Extracted (Step 0)

| Config Item | Value |
|-------------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Embargo policy URL | Not configured |
| ProdSec contact email | Not configured |
| ProdSec Jira account ID | Not configured |
| Upstream Affected Component field | Not configured |
| PS Component field | Not configured |
| Stream custom field | Not configured |

## Embargo Check (Step 1.7)

- Embargo policy URL: Not configured -- Step 1.7 skipped entirely.

## Cross-CVE Overlap (Step 4.3)

- Upstream Affected Component field: Not configured -- Step 4.3 skipped entirely.

## Concurrent Triage Detection (Step 7)

- Upstream Affected Component field: Not configured -- Step 7 skipped entirely.
