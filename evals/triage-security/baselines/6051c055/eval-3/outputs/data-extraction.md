# Step 1 -- Data Extraction: TC-8003

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

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`.

- Parsed suffix: `rhtpa-2.2` maps to stream **2.2.x**
- Matched Version Stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z` (local path: `/home/dev/repos/rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x only** (scoped issue)

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend
- Upstream branch: `release/0.4.z`

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: `upstream` (default -- no Deployment Context column configured)

## Version Impact Analysis (from security-matrix.md mock data)

Stream 2.2.x (rhtpa-release.0.4.z) -- quinn-proto versions by pinned tag:

| Version | Build Tag | quinn-proto version | Affected? (< 0.11.14) |
|---------|-----------|---------------------|------------------------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) = 0.11.12 | YES (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO (fixed) |

Stream 2.1.x (rhtpa-release.0.3.z) -- quinn-proto versions by pinned tag (for cross-stream context):

| Version | Build Tag | quinn-proto version | Affected? (< 0.11.14) |
|---------|-----------|---------------------|------------------------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.1 | v0.3.12 | 0.11.9 | YES |

**Summary**: Within the scoped stream (2.2.x), versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are not affected. The other stream (2.1.x) is also affected but is outside this issue's scope.
