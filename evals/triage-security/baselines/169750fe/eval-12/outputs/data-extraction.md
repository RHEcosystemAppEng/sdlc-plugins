# Step 1 -- Data Extraction

## Extracted CVE Data for TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions prior to the fix (imprecise -- no specific threshold provided) |
| Fixed version | see advisory (imprecise -- no specific version provided) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. Based on the Ecosystem Mappings table for the 2.2.x stream, this falls under the **Cargo** ecosystem.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
- Ecosystem category: Source dependency

## Data Quality Notes

The Jira description provides **imprecise** affected version information:
- Affected versions: "versions prior to the fix" -- no specific version threshold
- Fixed version: "see advisory" -- no specific version number

External CVE data enrichment (Step 1.5) is required to obtain a precise fix threshold for version impact analysis.
