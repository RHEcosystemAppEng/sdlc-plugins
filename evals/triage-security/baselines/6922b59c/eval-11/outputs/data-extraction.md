# Step 1 -- Data Extraction: TC-8021

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Upstream Affected Component (customfield_10632) | tokio |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server |
| Stream (customfield_10832) | rhtpa-2.1 |
| Stream Scope | 2.1.x (mapped from summary suffix [rhtpa-2.1]) |
| Vulnerable Library | tokio |
| Ecosystem | Cargo (Rust crate) |
| Affected Version Range | versions before 1.42.0 |
| Fixed Version | 1.42.0 |
| CVSS | 8.1 (High) |
| Affects Versions (PSIRT-claimed) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
| Existing Comments | None |
| Existing Issue Links | None |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE Record | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Upstream Fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |

## Stream Scope Resolution

The issue summary contains `[rhtpa-2.1]`, which maps to the **2.1.x** version stream
in the Security Configuration's Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |

This is a **stream-scoped** issue. Steps 3-8 will be scoped to the 2.1.x stream only.

## Ecosystem Detection

The vulnerable library `tokio` is a Rust crate. The 2.1.x stream's Ecosystem Mappings
table includes Cargo with lock file `Cargo.lock` and check command
`git show <tag>:Cargo.lock`. The ecosystem classification is **source dependency**,
which produces 2 remediation tasks per stream (upstream backport/dependency bump +
downstream propagation).

## Version Impact (stream 2.1.x)

From the security matrix mock data, the tokio versions are not directly listed,
but the issue description states versions before 1.42.0 are affected. The stream
2.1.x contains versions 2.1.0 (build v0.3.8) and 2.1.1 (build v0.3.12).

Based on PSIRT Affects Versions and the CVE data, both product versions in the
2.1.x stream are affected.

## Deployment Context

The source repository `rhtpa-backend` has deployment context `upstream` (default,
since the Deployment Context column is absent from the Source Repositories table
in the mock CLAUDE.md).
