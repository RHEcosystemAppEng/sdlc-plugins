# Step 1 -- Data Extraction for TC-8006

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x**
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.3.z
- Local Path: /home/dev/repos/rhtpa-release.0.3.z

The issue is **stream-scoped** to the 2.1.x stream. Steps 3 and 4 will be scoped to this stream only.

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend
- Upstream branch: `release/0.3.z`

## Existing Issue Links

The issue already has the following links:

- **Related**: TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2])
  - Link ID: 1990401
  - Type: Related
  - Direction: outward (TC-8006 -> TC-8001)

## Remote Links

- [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) -- GitHub Advisory
- [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) -- CVE Record

## Version Impact (from security-matrix mock data)

Using the 2.1.x stream (rhtpa-release.0.3.z) supportability matrix:

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

Both versions in the 2.1.x stream ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14. All versions in this stream are affected.

## Cross-stream reference (from sibling TC-8001's stream 2.2.x)

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES | same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
