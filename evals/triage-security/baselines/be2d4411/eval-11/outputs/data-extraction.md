# Step 1 -- Data Extraction

## Vulnerability Issue: TC-8021

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | None |
| Existing issue links | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (from Version Streams table: stream 2.1.x at rhtpa-release.0.3.z)
- Issue is **stream-scoped** to 2.1.x only

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend (from Ecosystem Mappings in security-matrix.md)
- Upstream branch: `release/0.3.z`

## Custom Fields

| Custom Field | Value |
|---|---|
| customfield_10632 (Upstream Affected Component) | tokio |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-server |
| customfield_10832 (Stream) | rhtpa-2.1 |

## Remote Links

| Title | URL |
|---|---|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| RustSec Advisory | https://rustsec.org/advisories/RUSTSEC-2026-0088.html |

## Security Configuration (from CLAUDE.md)

| Setting | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
