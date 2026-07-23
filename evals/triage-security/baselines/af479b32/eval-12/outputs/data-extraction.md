# Step 1 -- Data Extraction: TC-8030

## Extracted Fields

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Summary | CVE-2026-48901 h2 - HTTP/2 CONTINUATION flood [rhtpa-2.2] |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | "versions prior to the fix" (imprecise -- no explicit threshold in Jira description) |
| Fixed version | "see advisory" (imprecise -- no explicit version in Jira description) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Matched Version Stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue is **scoped** to the 2.2.x stream

## Ecosystem Detection

- Library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- Upstream branch: `release/0.4.z`

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: `upstream` (default -- no Deployment Context column in Source Repositories table)

## Notes

The Jira description provides only imprecise version information:
- Affected versions: "versions prior to the fix" -- no explicit version threshold
- Fixed version: "see advisory" -- no explicit version number

External CVE data enrichment (Step 1.5) is required to determine the precise fix threshold.
