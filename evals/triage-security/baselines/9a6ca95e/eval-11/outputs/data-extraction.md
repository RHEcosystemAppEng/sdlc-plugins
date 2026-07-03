# Step 1 -- Data Extraction: TC-8021

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1] |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
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
- Mapped stream: **2.1.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`
- Local path: `/home/dev/repos/rhtpa-release.0.3.z`

The suffix `[rhtpa-2.1]` matches the configured Version Stream `2.1.x` in Security Configuration.

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend
- Upstream branch: `release/0.3.z`

## Deployment Context

- Source repository: rhtpa-backend
- Deployment context: upstream (default -- no explicit Deployment Context column in Source Repositories table)

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | tokio |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-server |
| Stream | customfield_10832 | rhtpa-2.1 |

## Remote Links

| Title | URL | Type |
|---|---|---|
| GHSA-2026-tk91-v5pp | https://github.com/advisories/GHSA-2026-tk91-v5pp | GitHub Advisory |
| CVE-2026-55123 | https://www.cve.org/CVERecord?id=CVE-2026-55123 | CVE Record |
| tokio-rs/tokio#7001 | https://github.com/tokio-rs/tokio/pull/7001 | Upstream fix PR |

## Issue Links

No existing issue links on TC-8021.

## Labels

- CVE-2026-55123
- pscomponent:org/rhtpa-server

## Security Configuration (from project CLAUDE.md)

| Setting | Value |
|---|---|
| Project key | TC |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |

## Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Note on Existing Preemptive Task

The issue description notes that a proactive remediation task TC-8022 already exists for this stream, created by a prior cross-stream triage of TC-8020 (stream [rhtpa-2.2]). This is handled in Step 4.4 reconciliation.
