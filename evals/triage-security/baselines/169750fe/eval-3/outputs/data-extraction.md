# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| **Issue Key** | TC-8003 |
| **CVE ID** | CVE-2026-31812 |
| **Affected Component** | pscomponent:org/rhtpa-server |
| **Product Version (PSIRT-claimed)** | [rhtpa-2.2] |
| **Affects Versions (Jira field)** | RHTPA 2.2.0 |
| **Vulnerable Library** | quinn-proto |
| **Affected Version Range** | versions before 0.11.14 |
| **Fixed Version** | 0.11.14 |
| **CVSS** | 7.5 (High) |
| **Advisory URL** | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| **CVE Record URL** | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| **Due Date** | 2026-07-15 |
| **Status** | New |
| **Assignee** | Unassigned |
| **Existing Comments** | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry: stream 2.2.x at `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to the 2.2.x stream

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Classification: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
- Remediation pattern: 2 tasks per stream (upstream backport or dependency bump + downstream propagation)

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: upstream (default, no explicit Deployment Context column in Source Repositories)

## Remote Links

| Link | Type |
|------|------|
| https://github.com/advisories/GHSA-2026-qp73-x4mq | GitHub Advisory |
| https://www.cve.org/CVERecord?id=CVE-2026-31812 | CVE Record |

## Configuration Extracted (Step 0)

| Config Item | Value |
|-------------|-------|
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
