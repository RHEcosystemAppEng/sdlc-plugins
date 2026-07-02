# Data Extraction (Step 1) -- TC-8003

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
- Source repository: backend

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: upstream (default -- no Deployment Context column in Source Repositories)

## Version Impact Analysis (Step 2)

Using the security matrix data for the 2.2.x stream (rhtpa-release.0.4.z):

### Version Impact Table

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES | same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

Also checking the 2.1.x stream (rhtpa-release.0.3.z) for cross-stream awareness:

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Affects Versions Assessment (Step 3)

Issue is scoped to stream 2.2.x. Within that stream, affected versions are:
- RHTPA 2.2.0 (quinn-proto 0.11.9 -- vulnerable)
- RHTPA 2.2.1 (quinn-proto 0.11.12 -- vulnerable)
- RHTPA 2.2.2 (retag of 2.2.1 -- vulnerable)

PSIRT-assigned Affects Versions: `[RHTPA 2.2.0]`
Correct Affects Versions (based on lock file analysis): `[RHTPA 2.2.0, RHTPA 2.2.1]`
(Note: RHTPA 2.2.2 may not have a registered Jira version since it is a retag.)

However, this correction is moot because the issue will be closed as a duplicate (see duplicate-check.md).
