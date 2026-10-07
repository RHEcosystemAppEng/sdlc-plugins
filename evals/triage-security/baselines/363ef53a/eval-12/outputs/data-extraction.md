# Step 1 -- Data Extraction for TC-8030

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-48901 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | h2 | Description text |
| Affected version range | "versions prior to the fix" (imprecise -- no explicit threshold) | Description text |
| Fixed version | "see advisory" (imprecise -- no explicit version) | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 | Jira `duedate` field |
| Existing comments | None | Issue comment history |
| Status | New | Jira `status` field |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table row: 2.2.x / rhtpa-release.0.4.z)
- Issue stream scope: **2.2.x only**

## Ecosystem Detection

- Library: h2
- Ecosystem: **Cargo** (Rust crate, identified from Ecosystem Mappings in 2.2.x stream's security-matrix.md)
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

## Deployment Context

- Affected repository: rhtpa-backend (matched from Source Repositories table)
- Deployment context: not explicitly configured (Deployment Context column absent) -- defaults to `upstream`

## Critical Field Assessment

The Jira description provides **imprecise** version data:
- Affected range: "versions prior to the fix" -- no numeric threshold
- Fixed version: "see advisory" -- no explicit version number

External CVE data enrichment (Step 1.5) is required to obtain a precise fix threshold for version impact analysis.
