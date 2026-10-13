# Data Extraction — TC-8020

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-55123 |
| **Jira Issue Key** | TC-8020 |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Affected component** | pscomponent:org/rhtpa-server |
| **Product version (PSIRT-claimed)** | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| **Affects Versions (Jira field)** | RHTPA 2.2.0, RHTPA 2.2.1 |
| **Vulnerable library** | tokio |
| **Affected version range** | versions before 1.42.0 |
| **Fixed version** | 1.42.0 |
| **CVSS** | 8.1 (High) |
| **Due date** | 2026-08-15 |
| **Assignee** | Unassigned |
| **Upstream Affected Component** | tokio (customfield_10632) |
| **PS Component** | pscomponent:org/rhtpa-server (customfield_10669) |
| **Stream** | rhtpa-2.2 (customfield_10832) |

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

No existing issue links.

## Existing Comments

No existing comments.

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Issue is **scoped** to the rhtpa-2.2 stream
- Matching Version Stream: rhtpa-release.0.4.z (Konflux release repo)

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate)
- **Library**: tokio
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream fix + downstream propagation)
- **Lock file**: Cargo.lock
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch (2.2.x)**: release/0.4.z
- **Upstream branch (2.1.x)**: release/0.3.z

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: upstream (default, no Deployment Context column in Source Repositories table)

## Vulnerability Description

A vulnerability was found in the tokio crate. Versions of tokio before 1.42.0 are vulnerable to a use-after-free when a spawned task is aborted while holding a borrowed reference. This can lead to memory corruption and potential code execution.
