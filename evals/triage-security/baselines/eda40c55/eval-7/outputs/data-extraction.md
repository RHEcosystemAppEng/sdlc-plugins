# Step 1 -- Data Extraction for TC-8006

## Parsed CVE Metadata

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

The issue summary contains the stream suffix `[rhtpa-2.1]`, which maps to the
configured Version Stream **2.1.x** (Konflux release repo:
`git.example.com/rhtpa/rhtpa-release.0.3.z`, local path:
`/home/dev/repos/rhtpa-release.0.3.z`).

This issue is **stream-scoped** to 2.1.x. Steps 3 and 4 will operate within
this stream scope only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.1.x stream's
`security-matrix.md` Ecosystem Mappings table lists **Cargo** as a supported
ecosystem, with:

- Repository: backend
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`

Ecosystem: **Cargo** (source dependency).

## Remote Links

- GitHub Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
- CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-31812

## Existing Issue Links

- **Related** to TC-8001 (link ID: 1990401, direction: outward, this issue -> TC-8001)
  - TC-8001 summary: CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]

## Version Impact (from security-matrix.md mock data)

For the issue-scoped stream 2.1.x:

| Version | Build Tag | quinn-proto version | Vulnerable? |
|---------|-----------|---------------------|-------------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES (< 0.11.14) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES (< 0.11.14) |

Both versions in the 2.1.x stream ship quinn-proto 0.11.9, which is below the
fix threshold of 0.11.14. Both are affected.
