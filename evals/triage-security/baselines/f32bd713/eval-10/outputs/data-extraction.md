# Step 1 -- Data Extraction: TC-8020

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** version stream from the Version Streams table in Security Configuration.

- Issue stream scope: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- The issue is **scoped** -- Steps 3 and 4 apply only to versions within the 2.2.x stream. Cross-stream impact is handled via Case A.

## Ecosystem Detection

- Vulnerable library: **tokio** (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Lock file: `Cargo.lock`
- Remediation task structure: **2 tasks per stream** (upstream backport/dependency bump + downstream propagation)

## Deployment Context Lookup

- Affected repository: rhtpa-backend (from component label pscomponent:org/rhtpa-server)
- Source Repositories table does not include a Deployment Context column
- Deployment context: not configured (coordination guidance omitted)

## Custom Fields

| Field | Field ID | Value |
|-------|----------|-------|
| Upstream Affected Component | customfield_10632 | tokio |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-server |
| Stream | customfield_10832 | rhtpa-2.2 |

## Configuration Extracted (Step 0)

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
