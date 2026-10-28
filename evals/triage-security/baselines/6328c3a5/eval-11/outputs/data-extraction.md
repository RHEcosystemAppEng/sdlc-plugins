# Step 1 -- Data Extraction: TC-8021

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Issue Key | TC-8021 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Upstream Affected Component | tokio (customfield_10632) |
| PS Component | pscomponent:org/rhtpa-server (customfield_10669) |
| Stream (custom field) | rhtpa-2.1 (customfield_10832) |
| Product version (PSIRT-claimed) | rhtpa-2.1 (from summary suffix [rhtpa-2.1]) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Existing issue links | (none) |
| Existing comments | (none) |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE Record | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0088.html

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (matches Version Streams table entry: stream 2.1.x at Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.3.z`)
- Issue is **scoped** to stream 2.1.x only

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Remediation task count per stream: 2 (dependency bump + downstream propagation, since upstream fix is available at version 1.42.0)

## Deployment Context

- Repository: rhtpa-backend
- Default deployment context: upstream (from Source Repositories table)
