# Step 1 -- Data Extraction: TC-8021

## Extracted CVE Data

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
| Advisory URL | GHSA-2026-tk91-v5pp (https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (Konflux release repo: rhtpa-release.0.3.z)
- Issue is **stream-scoped** to rhtpa-2.1 only

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Source repository: rhtpa-backend

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: upstream (default -- no Deployment Context column in Source Repositories table)

## Custom Fields

| Custom Field | ID | Value |
|--------------|----|-------|
| Upstream Affected Component | customfield_10632 | tokio |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-server |
| Stream | customfield_10832 | rhtpa-2.1 |
