# Step 1 -- Data Extraction: TC-8021

## Parsed CVE Data

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
| Upstream fix PR | tokio-rs/tokio#7001 (https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Existing issue links | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (matches Version Streams table entry: stream 2.1.x at rhtpa-release.0.3.z)
- Scope: This issue is **stream-scoped** to 2.1.x only

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend
- Upstream branch: `release/0.3.z`

## Custom Fields

- Upstream Affected Component (customfield_10632): tokio
- PS Component (customfield_10669): pscomponent:org/rhtpa-server
- Stream (customfield_10832): rhtpa-2.1

## Remote Links

1. GitHub Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp
2. CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-55123
3. Upstream fix PR: https://github.com/tokio-rs/tokio/pull/7001
4. RustSec Advisory: https://rustsec.org/advisories/RUSTSEC-2026-0088.html
