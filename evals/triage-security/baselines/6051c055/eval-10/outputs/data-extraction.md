# Data Extraction — TC-8020

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Issue Key | TC-8020 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 |
| Stream scope | 2.2.x (mapped from summary suffix [rhtpa-2.2]) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Due date | 2026-08-15 |
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
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |

## Issue Links

No existing links.

## Comments

No existing comments.

## Ecosystem Detection

- **Ecosystem**: Cargo (tokio is a Rust crate)
- **Lock file**: Cargo.lock
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "tokio"'`

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped to Version Stream: 2.2.x
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z
- Issue is **scoped** to stream rhtpa-2.2 -- cross-stream analysis required for other streams
