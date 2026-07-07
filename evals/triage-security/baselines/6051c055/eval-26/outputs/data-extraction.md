# Step 1 -- Data Extraction: TC-8050

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99001 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | criterion |
| Affected version range | versions before 0.5.2 |
| Fixed version | 0.5.2 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | -- (none in remote links) |
| Advisory URL | -- (none in remote links) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 |
| Due date | 2026-08-01 |
| Existing comments | (none) |

## Stream Scope

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Ecosystem: **Cargo** (Rust crate -- criterion is a Rust benchmarking library)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "criterion"'`
- Upstream branch: `release/0.4.z`

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: `upstream` (default -- no Deployment Context column present)
