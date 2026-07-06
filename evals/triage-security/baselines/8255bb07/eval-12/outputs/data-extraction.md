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
| Affected version range | "versions prior to the fix" (imprecise -- no specific version threshold provided) |
| Fixed version | "see advisory" (imprecise -- no specific version provided) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |
| Ecosystem | Cargo (h2 is a Rust crate) |
| Deployment context | upstream (default -- no explicit deployment context configured) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table. This issue is scoped to the 2.2.x stream only.

Matching stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. The Ecosystem Mappings table for stream 2.2.x lists **Cargo** with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

## Data Quality Flag

The Jira description provides **imprecise version data**:
- Affected range: "versions prior to the fix" -- lacks a specific version threshold
- Fixed version: "see advisory" -- defers to external sources

External CVE data enrichment (Step 1.5) is required to obtain a precise fix threshold for version impact analysis.
