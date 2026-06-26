# Data Extraction — TC-8020

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Issue Key | TC-8020 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream Scope | 2.2.x (mapped from suffix `[rhtpa-2.2]` to Version Streams table) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable Library | tokio |
| Affected Version Range | versions before 1.42.0 |
| Fixed Version | 1.42.0 |
| CVSS | 8.1 (High) |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
| Upstream Affected Component (customfield_10632) | tokio |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server |
| Stream (customfield_10832) | rhtpa-2.2 |

## Labels

- CVE-2026-55123
- pscomponent:org/rhtpa-server

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Upstream Fix PR | https://github.com/tokio-rs/tokio/pull/7001 |

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0088.html

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate — tokio)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "tokio"'`
- **Remediation type**: Source dependency — requires 2 tasks (upstream backport + downstream propagation)

## Stream Scope Resolution

The issue summary suffix `[rhtpa-2.2]` maps to the **2.2.x** version stream in Security Configuration:
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z
- Upstream Branch: release/0.4.z
