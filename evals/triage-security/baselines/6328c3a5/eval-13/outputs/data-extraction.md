# Step 1 -- Data Extraction for TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary `CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]` contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`, local path: `/home/dev/repos/rhtpa-release.0.4.z`).

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Category**: Source dependency
- **Remediation pattern**: 2 tasks per stream (upstream backport or dependency bump + downstream propagation)

## Deployment Context

- **Repository**: rhtpa-backend
- **URL**: https://github.com/rhtpa/rhtpa-backend
- **Deployment context**: upstream (default -- no explicit Deployment Context column in Source Repositories table)

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |

## Vulnerability Description

quinn-proto crate before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. Classified as denial of service (DoS). The vulnerability exists because quinn-proto does not properly validate the number of streams requested in a STREAMS frame.
