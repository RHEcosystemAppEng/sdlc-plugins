# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99010 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.5 |
| Fixed version | 0.4.5 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 |
| Advisory URL | -- |
| Due date | 2026-08-15 |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Existing comments | None |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Matched Version Streams entry: 2.2.x at git.example.com/rhtpa/rhtpa-release.0.4.z
- Issue is **scoped** to the 2.2.x stream only

## Ecosystem Detection

- Library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Remediation tasks per stream: 2 (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

## Deployment Context

- Source repository: rhtpa-backend
- Deployment context: upstream (default -- Deployment Context column absent from Source Repositories table)
