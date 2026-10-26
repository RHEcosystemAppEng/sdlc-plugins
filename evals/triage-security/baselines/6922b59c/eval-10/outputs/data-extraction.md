# Data Extraction -- Step 1

## Issue: TC-8020

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Labels | CVE-2026-55123, pscomponent:org/rhtpa-server |
| Affects Versions (PSIRT-claimed) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
| Upstream Affected Component | tokio (customfield_10632) |
| PS Component | pscomponent:org/rhtpa-server (customfield_10669) |
| Stream | rhtpa-2.2 (customfield_10832) |

## CVE Details

| Field | Value |
|-------|-------|
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Ecosystem | Cargo |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- Issue is **stream-scoped** to rhtpa-2.2

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |

## References

- https://github.com/advisories/GHSA-2026-tk91-v5pp
- https://rustsec.org/advisories/RUSTSEC-2026-0088.html

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "tokio"'`
- Remediation task count per stream: **2** (upstream backport/bump + downstream propagation)

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default, no explicit Deployment Context column in Source Repositories)
