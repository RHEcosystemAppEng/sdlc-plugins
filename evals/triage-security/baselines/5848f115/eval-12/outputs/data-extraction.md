# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | "versions prior to the fix" (imprecise -- no concrete threshold in Jira description) |
| Fixed version | "see advisory" (imprecise -- no concrete version in Jira description) |
| CVSS | 7.5 (High) |
| Upstream fix PR | [hyperium/h2#800](https://github.com/hyperium/h2/pull/800) |
| Advisory URL | [GHSA-2026-r7f2-kk9p](https://github.com/advisories/GHSA-2026-r7f2-kk9p) |
| CVE record URL | [CVE-2026-48901](https://www.cve.org/CVERecord?id=CVE-2026-48901) |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
configured Version Stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3--8 apply to the 2.2.x stream,
with cross-stream impact analysis covering 2.1.x.

## Ecosystem Detection

- **Library**: h2 (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`

## Deployment Context

- **Repository**: rhtpa-backend
- **Deployment context**: upstream (default -- no Deployment Context column configured)

## Critical Data Gap

The Jira description provides **imprecise** version range information:
- Affected versions: "versions prior to the fix" -- no specific version threshold
- Fixed version: "see advisory" -- no specific version number

External CVE data enrichment (Step 1.5) is required to determine the precise
fix threshold before version impact analysis can proceed.
