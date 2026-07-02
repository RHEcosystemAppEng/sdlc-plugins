# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions prior to the fix (imprecise -- no specific threshold) |
| Fixed version | see advisory (imprecise -- no specific version stated) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local path: /home/dev/repos/rhtpa-release.0.4.z

The issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will be scoped to this stream only. Cross-stream impact (2.1.x) is reported via Case B.

## Ecosystem Detection

- Library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- Upstream branch (2.2.x stream): `release/0.4.z`
- Source repository: backend

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)

## Notes

The Jira description provides only imprecise version information:
- "Affected versions: versions prior to the fix" -- no specific version threshold
- "Fixed version: see advisory" -- no specific fixed version number

External CVE data enrichment (Step 1.5) is required to obtain a precise fix threshold for version impact analysis.
