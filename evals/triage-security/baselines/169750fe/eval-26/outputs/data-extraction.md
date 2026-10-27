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
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 |
| Upstream fix PR | (none found in remote links) |
| Advisory URL | (none found in remote links) |
| Due date | 2026-08-01 |
| Existing comments | (no comments) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local Path: `/home/dev/repos/rhtpa-release.0.4.z`

The issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

- Ecosystem: **Cargo**
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`
- Category: Source dependency
- Remediation task count per stream: 2 (upstream fix + downstream propagation)

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: upstream (default -- Deployment Context column absent)
