# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-48901 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | [rhtpa-2.2] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | h2 | Description ("A vulnerability was found in h2") |
| Affected version range | "versions prior to the fix" (imprecise -- no specific threshold) | Description |
| Fixed version | "see advisory" (imprecise -- no specific version) | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links (hyperium/h2#800) |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links (CVE Record) |
| Due date | 2026-08-01 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for 2.2.x stream)
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue stream scope: **2.2.x only** (scoped issue)

## Ecosystem Detection

- Library: h2 (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Classification: Source dependency ecosystem -- 2 remediation tasks per stream (upstream backport/bump + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- Deployment Context column absent from Source Repositories table)

## Critical Field Assessment

- CVE ID: parsed successfully
- Library: parsed successfully
- Affected version range: **IMPRECISE** -- Jira description says "versions prior to the fix" with no specific version threshold. External CVE data enrichment (Step 1.5) is required to determine the precise fix threshold.
- Fixed version: **IMPRECISE** -- Jira description says "see advisory" with no specific version. External CVE data enrichment (Step 1.5) is required.
