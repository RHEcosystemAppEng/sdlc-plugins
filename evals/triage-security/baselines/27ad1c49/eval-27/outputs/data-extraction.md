# Step 1 -- Data Extraction for TC-8051

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99002 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Affected version range | versions before 0.23.5 (< 0.23.5) |
| Fixed version | 0.23.5 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 |
| Advisory URL | -- (none in remote links) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches configured Version Stream `2.2.x` at `rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x** (scoped -- Steps 3-4 apply only to this stream)

## Ecosystem Detection

- Ecosystem: **Cargo** (Rust crate -- rustls)
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z` (from 2.2.x stream Ecosystem Mappings)

## Deployment Context Lookup

- Affected repository: rhtpa-backend (matched from pscomponent:org/rhtpa-server)
- Deployment context: **upstream** (default -- Deployment Context column is absent from Source Repositories table)
