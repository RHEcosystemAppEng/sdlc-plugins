# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data Table

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text ("A vulnerability was found in quinn-proto") |
| Affected version range | < 0.11.14 | Description text ("before version 0.11.14") |
| Fixed version | 0.11.14 | Description text ("Fixed version: 0.11.14") |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (CVE Record) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | (none) | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x** (scoped issue -- Steps 3-4 apply only to this stream; Case A checks other streams)

## Ecosystem Detection

- Vulnerable library: `quinn-proto` (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Remediation tasks per stream: 2 (upstream backport or dependency bump + downstream propagation)

## Deployment Context Lookup

- Affected repository: `rhtpa-backend` (resolved from component label `pscomponent:org/rhtpa-server`)
- Deployment context: **upstream** (default -- Deployment Context column absent from Source Repositories table)

## Configuration Extracted (Step 0)

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | (not configured -- Steps 4.3, 7 skipped) |
| PS Component field | (not configured) |
| Stream custom field | (not configured) |
| ProdSec contact email | (not configured) |
| ProdSec Jira account ID | (not configured -- @mentions skipped) |
| Embargo policy URL | (not configured -- Step 1.7 skipped) |
