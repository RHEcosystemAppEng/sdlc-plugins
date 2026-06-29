# Data Extraction — TC-8020

## Extracted Fields

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Issue Key | TC-8020 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable Library | tokio |
| Affected Version Range | versions before 1.42.0 |
| Fixed Version | 1.42.0 |
| CVSS | 8.1 (High) |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
| Labels | CVE-2026-55123, pscomponent:org/rhtpa-server |
| Stream (custom field) | rhtpa-2.2 (customfield_10832) |
| Upstream Affected Component | tokio (customfield_10632) |
| PS Component | pscomponent:org/rhtpa-server (customfield_10669) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: 2.2.x
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z
- Issue is **stream-scoped** to rhtpa-2.2

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: Cargo
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend
- Upstream branch: `release/0.4.z` (for 2.2.x stream)

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Upstream Fix PR | https://github.com/tokio-rs/tokio/pull/7001 |

## References

- https://github.com/advisories/GHSA-2026-tk91-v5pp
- https://rustsec.org/advisories/RUSTSEC-2026-0088.html
