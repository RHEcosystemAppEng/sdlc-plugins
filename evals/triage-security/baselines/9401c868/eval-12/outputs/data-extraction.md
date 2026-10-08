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
| Fixed version | see advisory (imprecise -- no specific version) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table row: `2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x only** (scoped issue)

## Ecosystem Detection

- Library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- Deployment Context column absent from Source Repositories table)

## Critical Field Assessment

The Jira description provides **imprecise** version information:
- Affected version range: "versions prior to the fix" -- no specific version threshold
- Fixed version: "see advisory" -- no specific version number

External CVE data enrichment (Step 1.5) is required to obtain precise fix thresholds for version impact analysis.
