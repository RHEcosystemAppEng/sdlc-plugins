# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions prior to the fix (imprecise -- no exact threshold in Jira description) |
| Fixed version | see advisory (not specified precisely in Jira description) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (from Version Streams table: stream 2.2.x at `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue stream scope: **scoped to 2.2.x only**

## Ecosystem Detection

- Library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Remediation tasks per stream: 2 (upstream fix + downstream propagation), or dependency bump + downstream propagation if upstream already ships the fix

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- Deployment Context column absent from Source Repositories table)

## Data Quality Note

The Jira description provides only an imprecise affected range ("versions prior to the fix") and no concrete fixed version ("see advisory"). External CVE data enrichment (Step 1.5) is required to determine the precise fix threshold for version impact analysis.
