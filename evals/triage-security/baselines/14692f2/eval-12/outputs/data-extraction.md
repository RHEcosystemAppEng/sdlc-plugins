# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | **versions prior to the fix** (imprecise -- no specific version threshold in Jira description) |
| Fixed version | **see advisory** (imprecise -- Jira description defers to external advisory) |
| CVSS | 7.5 (High) |
| Upstream fix PR | [hyperium/h2#800](https://github.com/hyperium/h2/pull/800) |
| Advisory URL | [GHSA-2026-r7f2-kk9p](https://github.com/advisories/GHSA-2026-r7f2-kk9p) |
| CVE record URL | [CVE-2026-48901](https://www.cve.org/CVERecord?id=CVE-2026-48901) |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for stream 2.2.x)
- Issue stream scope: **2.2.x only**

## Ecosystem Detection

- Vulnerable library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

## Notes on Imprecise Version Data

The Jira description provides **imprecise** affected version information:

- "Affected versions: versions prior to the fix" -- no specific version number
- "Fixed version: see advisory" -- defers to external source

This imprecision triggers Step 1.5 (External CVE Data Enrichment) to obtain
a precise fix threshold from authoritative external sources (MITRE CVE API
and OSV.dev).
