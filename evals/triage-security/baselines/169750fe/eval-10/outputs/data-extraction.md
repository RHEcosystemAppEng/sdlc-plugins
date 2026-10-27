# Data Extraction — TC-8020

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Jira Issue Key | TC-8020 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Upstream Affected Component | tokio |
| PS Component | pscomponent:org/rhtpa-server |
| Stream (custom field) | rhtpa-2.2 |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable Library | tokio |
| Affected Version Range | versions before 1.42.0 |
| Fixed Version | 1.42.0 |
| CVSS | 8.1 (High) |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
| Labels | CVE-2026-55123, pscomponent:org/rhtpa-server |
| Existing Comments | (none) |
| Existing Links | (none) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (rhtpa-release.0.4.z)
- Issue is **scoped** to stream rhtpa-2.2
- Cross-stream analysis required for other configured streams

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Remediation tasks per stream: **2** (upstream backport/dependency bump + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Upstream Fix PR | https://github.com/tokio-rs/tokio/pull/7001 |

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0088.html
