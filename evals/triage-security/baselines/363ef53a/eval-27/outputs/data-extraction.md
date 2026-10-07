# Step 1 -- Data Extraction

## Extracted CVE Data for TC-8051

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99002 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Affected version range | versions before 0.23.5 |
| Fixed version | 0.23.5 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 |
| Advisory URL | -- |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 |
| Due date | 2026-08-01 |
| Existing comments | (none) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Triage is scoped to the 2.2.x stream only (rhtpa-release.0.4.z)

## Ecosystem Detection

- Ecosystem: **Cargo** (Rust crate -- rustls)
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: upstream (default -- no Deployment Context column in Source Repositories table)
