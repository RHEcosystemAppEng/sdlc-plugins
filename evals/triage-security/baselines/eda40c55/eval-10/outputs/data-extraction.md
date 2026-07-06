# Data Extraction — TC-8020

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Due date | 2026-08-15 |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Additional reference | https://rustsec.org/advisories/RUSTSEC-2026-0088.html |
| Existing comments | None |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

- Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local Path: `/home/dev/repos/rhtpa-release.0.4.z`

This issue is **stream-scoped** to 2.2.x. Steps 3-4 apply to the single stream, but cross-stream version impact analysis (Step 2) covers all configured streams.

## Ecosystem Detection

- **Ecosystem**: Cargo (tokio is a Rust crate)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Repository**: backend
- **Upstream Branch (2.1.x)**: `release/0.3.z`
- **Upstream Branch (2.2.x)**: `release/0.4.z`

## Deployment Context

The affected repository `rhtpa-backend` has deployment context: **upstream** (default, as no Deployment Context column is present in the Source Repositories table).
