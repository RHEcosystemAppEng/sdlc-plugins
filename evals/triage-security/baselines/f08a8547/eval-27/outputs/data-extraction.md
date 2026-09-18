# Step 1 -- Data Extraction

## Extracted CVE Data for TC-8051

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99002 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Affected version range | versions before 0.23.5 |
| Fixed version | 0.23.5 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 |
| Advisory URL | -- |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 |
| Due date | 2026-08-01 |
| Existing comments | (no comments) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`

## Ecosystem Detection

- Ecosystem: **Cargo** (Rust crate)
- Category: Source dependency
- Remediation tasks per stream: 2 (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "rustls"'`
