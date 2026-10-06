# Step 1 -- Data Extraction: TC-8021

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Stream scope | 2.1.x (Konflux release repo: rhtpa-release.0.3.z) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Due date | 2026-08-15 |
| Existing comments | None |
| Existing issue links | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.1]`. This maps to the **2.1.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |

The issue is **scoped** to stream 2.1.x only. Steps 3--8 operate within this stream scope.

## Ecosystem Detection

The vulnerable library is **tokio**, a Rust crate. The 2.1.x stream's security-matrix.md Ecosystem Mappings table includes:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |

Ecosystem: **Cargo** (source dependency). Per the ecosystem classification table, this produces **2 remediation tasks per stream** (upstream backport + downstream propagation).

## Deployment Context

The affected repository (rhtpa-backend) is listed in Source Repositories with no Deployment Context column, so it defaults to `upstream`.

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |

## Notes

- The issue description notes: "A proactive remediation task (TC-8022) already exists for this stream, created by a prior cross-stream triage of TC-8020 (stream [rhtpa-2.2])."
- This will be handled in Step 4.4 (Preemptive Task Reconciliation).
