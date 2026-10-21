# Step 1 -- Data Extraction: TC-8021

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-55123 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.1 | Summary suffix `[rhtpa-2.1]` |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 | Jira `versions` field |
| Vulnerable library | tokio | Description text |
| Affected version range | versions before 1.42.0 | Description text |
| Fixed version | 1.42.0 | Description text |
| CVSS | 8.1 (High) | Description text |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) | Remote links |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) | Remote links |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) | Remote links |
| Due date | 2026-08-15 | Jira `duedate` field |
| Existing comments | None | Issue comment history |

## Custom Fields

| Custom Field | Value |
|---|---|
| Upstream Affected Component (customfield_10632) | tokio |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server |
| Stream (customfield_10832) | rhtpa-2.1 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (from Version Streams table: 2.1.x -> Konflux release repo `rhtpa-release.0.3.z`)
- Issue is **stream-scoped** to 2.1.x only

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Classification: Source dependency ecosystem
- Expected remediation per stream: 2 tasks (upstream backport or dependency bump + downstream propagation)

## Deployment Context

- Repository: rhtpa-backend
- URL: https://github.com/rhtpa/rhtpa-backend
- Deployment context: upstream (default -- Deployment Context column absent in Source Repositories table)

## Configuration (Step 0)

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
