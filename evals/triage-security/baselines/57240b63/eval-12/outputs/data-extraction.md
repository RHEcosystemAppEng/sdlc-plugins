# Step 1 -- Data Extraction: TC-8030

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-48901 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels |
| Product version (PSIRT-claimed) | [rhtpa-2.2] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | h2 | Description |
| Affected version range | "versions prior to the fix" (imprecise -- no explicit threshold) | Description |
| Fixed version | "see advisory" (imprecise -- no explicit version) | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 | Issue `duedate` field |
| Existing comments | None | Issue comments |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local path: /home/dev/repos/rhtpa-release.0.4.z

## Ecosystem Detection

- Vulnerable library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- Repository: backend
- Upstream branch: `release/0.4.z`

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)

## Critical Data Gap

The Jira description provides **imprecise version data**:
- Affected range: "versions prior to the fix" -- no explicit version threshold
- Fixed version: "see advisory" -- no explicit version number

Step 1.5 (External CVE Data Enrichment) is required to obtain precise, machine-readable version constraints from MITRE CVE API and OSV.dev before proceeding to version impact analysis.
