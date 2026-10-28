# Step 1 -- Data Extraction

## Issue: TC-8050

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
| Upstream fix PR | (none) |
| Advisory URL | (none) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 |
| Due date | 2026-08-01 |
| Existing comments | (none) |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to the **2.2.x** stream (Konflux release repo: `rhtpa-release.0.4.z`). Triage is scoped to this stream only.

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "criterion"'`
- **Upstream branch**: `release/0.4.z`
- **Category**: Source dependency -- 2 tasks per stream (upstream + downstream)

## Deployment Context

- **Repository**: rhtpa-backend
- **Deployment context**: upstream (default -- no Deployment Context column in Source Repositories table)
