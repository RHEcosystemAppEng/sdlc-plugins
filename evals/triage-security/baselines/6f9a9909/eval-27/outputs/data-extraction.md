# Step 1 -- Data Extraction: TC-8051

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99002 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Affected version range | versions before 0.23.5 (< 0.23.5) |
| Fixed version | 0.23.5 |
| CVSS | 8.1 (High) |
| Upstream fix PR | [rustls/rustls#2100](https://github.com/rustls/rustls/pull/2100) |
| CVE record URL | [CVE-2026-99002](https://www.cve.org/CVERecord?id=CVE-2026-99002) |
| Advisory URL | -- |
| Due date | 2026-08-01 |
| Existing comments | None |
| Issue status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue is **stream-scoped** to the 2.2.x stream only

## Ecosystem Detection

- Library: rustls (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Remediation tasks per stream: 2 (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "rustls"'`
- Upstream branch: `release/0.4.z`

## Vulnerability Description

A vulnerability was found in rustls. The rustls crate before version 0.23.5 improperly validates server certificates when using custom certificate verifiers, allowing a man-in-the-middle attacker to present an invalid certificate chain.
