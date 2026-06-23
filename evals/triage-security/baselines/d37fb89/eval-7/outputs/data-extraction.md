# Step 1 -- Data Extraction for TC-8006

## Extracted Fields

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

## Existing Issue Links

| Link Type | Direction | Target Issue | Target Summary |
|-----------|-----------|--------------|----------------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |

Link ID: 1990401

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.1]`
- Mapped to stream: **2.1.x**
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.3.z
- Local Path: /home/dev/repos/rhtpa-release.0.3.z

The issue is **stream-scoped** to 2.1.x. Steps 2-7 will analyze only the 2.1.x stream versions for this issue, though cross-stream impact on 2.2.x will be noted.

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Source repository: backend
- Upstream branch: `release/0.3.z` (for 2.1.x stream)

## Version Impact Analysis (Step 2)

Based on the security-matrix.md mock data, the following quinn-proto versions are pinned per release:

### Stream 2.1.x (issue scope)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

### Stream 2.2.x (sibling scope -- for cross-stream awareness)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES | same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

All versions in the 2.1.x stream ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14. Both 2.1.0 and 2.1.1 are affected.
