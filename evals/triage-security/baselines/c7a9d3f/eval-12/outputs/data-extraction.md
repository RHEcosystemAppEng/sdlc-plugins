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
| Affected version range | "versions prior to the fix" (IMPRECISE -- no specific version threshold provided) |
| Fixed version | "see advisory" (IMPRECISE -- no specific version provided) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

Issue stream scope: **2.2.x only**

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. Based on the Ecosystem Mappings in the 2.2.x stream's security-matrix.md:

- **Ecosystem**: Cargo
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- **Upstream Branch**: `release/0.4.z`

## Data Quality Flag

The Jira description provides IMPRECISE version data:
- Affected range: "versions prior to the fix" -- this is not a machine-parseable version constraint
- Fixed version: "see advisory" -- defers to external sources without stating a version

External CVE data enrichment (Step 1.5) is required to obtain precise fix thresholds for version impact analysis.
