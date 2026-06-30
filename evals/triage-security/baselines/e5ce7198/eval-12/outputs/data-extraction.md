# Step 1 -- Data Extraction for TC-8030

## Extracted Fields

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions prior to the fix (imprecise -- no explicit threshold in Jira description) |
| Fixed version | see advisory (imprecise -- no explicit version in Jira description) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for 2.2.x)
- Issue stream scope: **2.2.x only** (scoped issue -- Steps 3-4 apply only to the 2.2.x stream)

## Ecosystem Detection

- Library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z` (from 2.2.x stream Ecosystem Mappings)

## Critical Data Quality Issue

The Jira description provides **imprecise version data**:
- Affected versions: "versions prior to the fix" -- no explicit version threshold
- Fixed version: "see advisory" -- no explicit version number

This means the Jira description alone is **insufficient** for version impact analysis. Step 1.5 (External CVE Data Enrichment) is critical for this issue to establish a machine-readable fix threshold.
