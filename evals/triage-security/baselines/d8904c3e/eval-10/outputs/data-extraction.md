# Data Extraction — TC-8020

## Step 1: Parsed CVE Data

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
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Due date | 2026-08-15 |
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
- Category: **Source dependency**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "tokio"'`
- Remediation tasks per stream: **2** (upstream backport + downstream propagation)

## Remote Links

- [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) — GitHub Advisory
- [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) — CVE Record
- [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) — Upstream fix PR

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0088.html
