# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Summary | CVE-2026-48901 h2 - HTTP/2 CONTINUATION flood [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | "versions prior to the fix" (IMPRECISE -- no specific version threshold) |
| Fixed version | "see advisory" (IMPRECISE -- no specific version provided) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to the 2.2.x stream

## Ecosystem Detection

- Library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- Upstream branch: `release/0.4.z`

## Data Quality Assessment

The Jira description provides **imprecise** affected version information:
- "Affected versions: versions prior to the fix" -- no specific version threshold
- "Fixed version: see advisory" -- defers to external advisory

This imprecision triggers Step 1.5 (External CVE Data Enrichment) to obtain structured, machine-readable version constraints from authoritative external sources.
