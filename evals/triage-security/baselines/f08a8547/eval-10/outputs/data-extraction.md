# Step 1 -- Data Extraction: TC-8020

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Due date | 2026-08-15 |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)
- Issue is **scoped** to stream rhtpa-2.2

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Category: **Source dependency** -- 2 remediation tasks per stream (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

## Upstream Affected Component

- Custom field: customfield_10632
- Value: tokio

## Additional References

- [RUSTSEC-2026-0088](https://rustsec.org/advisories/RUSTSEC-2026-0088.html)

## Vulnerability Description

A use-after-free vulnerability was found in the tokio crate. Versions of tokio before 1.42.0 are vulnerable to a use-after-free when a spawned task is aborted while holding a borrowed reference. This can lead to memory corruption and potential code execution.
