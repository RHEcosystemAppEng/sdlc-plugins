# Step 1 -- Data Extraction

## Issue: TC-8021

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Upstream fix PR | tokio-rs/tokio#7001 (https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | GHSA-2026-tk91-v5pp (https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Existing comments | None |
| Existing issue links | None |

## Custom Fields

| Field | ID | Value |
|-------|----|-------|
| Upstream Affected Component | customfield_10632 | tokio |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-server |
| Stream | customfield_10832 | rhtpa-2.1 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Parsed stream: `2.1.x`
- Matched Version Stream: `2.1.x` at `git.example.com/rhtpa/rhtpa-release.0.3.z` (local path: `/home/dev/repos/rhtpa-release.0.3.z`)
- Issue is **stream-scoped** to `2.1.x` only

## Ecosystem Detection

- Vulnerable library: `tokio` (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Source repository: `backend`

## Remote Links

| URL | Type |
|-----|------|
| https://github.com/advisories/GHSA-2026-tk91-v5pp | GitHub Advisory |
| https://www.cve.org/CVERecord?id=CVE-2026-55123 | CVE Record |
| https://github.com/tokio-rs/tokio/pull/7001 | Upstream fix PR |

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0088.html
