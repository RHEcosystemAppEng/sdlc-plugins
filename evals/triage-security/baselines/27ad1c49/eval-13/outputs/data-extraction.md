# Step 1 -- Data Extraction for TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Version Streams table.

- Issue stream scope: **2.2.x**
- Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local Path: `/home/dev/repos/rhtpa-release.0.4.z`

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate -- quinn-proto is a Rust package)
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream fix + downstream propagation) when fix is not available upstream; or 2 (dependency bump + downstream propagation) when fix is already available upstream

## Deployment Context

The Source Repositories table does not include a Deployment Context column. All repositories default to `upstream`.

- rhtpa-backend: deployment context = `upstream`

## Affects Versions Analysis

PSIRT assigned `RHTPA 2.0.0` as the Affects Version, but there is no 2.0.x stream configured in the Version Streams table. The PSIRT-assigned Affects Version is **incorrect** and must be corrected based on lock file analysis in Step 2.

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
