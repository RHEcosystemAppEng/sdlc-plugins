# Step 1 -- Data Extraction

## Vulnerability Issue: TC-8060

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99010 |
| Summary | CVE-2026-99010 h2 - Memory exhaustion via CONTINUATION frames [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.5 (< 0.4.5) |
| Fixed version | 0.4.5 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 (hyperium/h2#800) |
| Advisory URL | -- |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table row for 2.2.x)
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Issue stream scope: **2.2.x only** (scoped issue)

## Ecosystem Detection

- Ecosystem: **Cargo** (Rust crate -- h2 is a Rust HTTP/2 implementation)
- Category: Source dependency
- Remediation tasks per stream: 2 (upstream fix + downstream propagation)
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

## Deployment Context Lookup

- Repository: rhtpa-backend
- Deployment Context column: absent from Source Repositories table (no Deployment Context column configured)
- Result: default to `upstream`
