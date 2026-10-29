# Step 1 -- Data Extraction: TC-8030

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-48901 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | [rhtpa-2.2] | Summary suffix |
| Stream scope | 2.2.x | Mapped from suffix `[rhtpa-2.2]` to Version Streams table |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | h2 | Description text |
| Affected version range | "versions prior to the fix" (IMPRECISE) | Description text |
| Fixed version | "see advisory" (IMPRECISE) | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 | Jira `duedate` field |
| Existing comments | (none) | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo `rhtpa-release.0.4.z`)
- This issue is **scoped** to the 2.2.x stream only

## Ecosystem Detection

- Library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Remediation tasks per stream: 2 (upstream fix + downstream propagation)

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- Deployment Context column absent from Source Repositories table)

## Critical Data Quality Issue

The Jira description provides **imprecise** affected version and fix version data:
- Affected versions: "versions prior to the fix" -- no explicit version threshold
- Fixed version: "see advisory" -- no explicit version number

**External CVE data enrichment (Step 1.5) is required** to establish a precise fix threshold before version impact analysis can proceed.
