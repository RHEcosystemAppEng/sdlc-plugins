# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions prior to the fix (imprecise -- no exact threshold in Jira description) |
| Fixed version | see advisory (imprecise -- no exact version in Jira description) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Vulnerable library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- Category: Source dependency -- produces 2 remediation tasks per affected stream (upstream backport/bump + downstream propagation)

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)

## Remote Links

| Title | URL | Type |
|-------|-----|------|
| GHSA-2026-r7f2-kk9p | https://github.com/advisories/GHSA-2026-r7f2-kk9p | GitHub Advisory |
| CVE-2026-48901 | https://www.cve.org/CVERecord?id=CVE-2026-48901 | CVE Record |
| hyperium/h2#800 | https://github.com/hyperium/h2/pull/800 | Upstream fix PR |

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0089.html

## Critical Field Assessment

- CVE ID: parsed successfully from labels and summary
- Library: parsed successfully ("h2")
- Affected range: **IMPRECISE** -- Jira description says "versions prior to the fix" with no version threshold. External CVE data enrichment (Step 1.5) is required to obtain a precise fix threshold.
