# Step 1 -- Data Extraction: TC-8040 (CVE-2026-31812)

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | _(none)_ | Issue comment history |
| Issue status | New | Issue `status` field |
| Assignee | Unassigned | Issue `assignee` field |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to the 2.2.x stream

## Ecosystem Detection

- Vulnerable library: quinn-proto
- Detected ecosystem: **Go modules**

### Ecosystem Mappings (from 2.2.x stream security-matrix.md)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Result**: The detected ecosystem "Go modules" is **not listed** in the Ecosystem Mappings table for the 2.2.x stream (nor in the 2.1.x stream). The supported ecosystems are limited to Cargo and RPM.

## Deployment Context Lookup

- Affected repository (from component label `pscomponent:org/rhtpa-server`): rhtpa-backend
- Deployment context: `upstream` (default -- no Deployment Context column present in Source Repositories table)

## Configuration Extracted (Step 0)

| Config Item | Value |
|-------------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | _(not configured)_ |
| PS Component field | _(not configured)_ |
| Stream field | _(not configured)_ |
| ProdSec contact email | _(not configured)_ |
| ProdSec Jira account ID | _(not configured)_ |
| Embargo policy URL | _(not configured)_ |
