# Step 1 -- Data Extraction for TC-8021

## Parsed CVE Data

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
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`. This maps to the
configured Version Stream **2.1.x** (Konflux Release Repo:
`git.example.com/rhtpa/rhtpa-release.0.3.z`, Local Path:
`/home/dev/repos/rhtpa-release.0.3.z`).

**Issue stream scope**: 2.1.x (scoped issue -- Steps 3-4 apply only to this stream)

## Ecosystem Detection

The vulnerable library is **tokio**, a Rust crate. This maps to the **Cargo**
ecosystem. Per the Ecosystem Mappings table in the security matrix for stream
2.1.x:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |

Ecosystem classification: **Source dependency** (Cargo) -- remediation produces
2 tasks per stream (upstream backport + downstream propagation).

## Remote Links

- [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) -- GitHub Advisory
- [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) -- CVE Record
- [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) -- Upstream fix PR

## Vulnerability Description

A use-after-free vulnerability in the tokio crate. Versions of tokio before
1.42.0 are vulnerable to a use-after-free when a spawned task is aborted while
holding a borrowed reference. This can lead to memory corruption and potential
code execution.

## Deployment Context

The affected repository (rhtpa-backend) is listed in Source Repositories. No
explicit Deployment Context column is present, so the default is `upstream`.
