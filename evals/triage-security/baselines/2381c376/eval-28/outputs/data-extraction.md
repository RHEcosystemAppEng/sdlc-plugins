# Step 1 -- Data Extraction

## Issue: TC-8060

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99010 |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.5 |
| Fixed version | 0.4.5 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [hyperium/h2#800](https://github.com/hyperium/h2/pull/800) |
| Advisory URL | -- |
| CVE record URL | [CVE-2026-99010](https://www.cve.org/CVERecord?id=CVE-2026-99010) |
| Due date | 2026-08-15 |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local path: `/home/dev/repos/rhtpa-release.0.4.z`

This issue is **stream-scoped** to 2.2.x. Steps 3 and 8 apply only to 2.2.x versions. Case A cross-stream impact check will verify whether other streams (2.1.x) are also affected.

## Ecosystem Detection

- Library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- Upstream branch: `release/0.4.z`
- Remediation tasks per stream: **2** (dependency bump + downstream propagation)

## Deployment Context Lookup

- Affected repository: rhtpa-backend
- URL: https://github.com/rhtpa/rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)
