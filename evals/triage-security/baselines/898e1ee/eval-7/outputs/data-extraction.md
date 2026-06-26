# Step 1 -- Data Extraction

## Parsed CVE Data for TC-8006

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Stream scope | 2.1.x |
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

## Labels

- CVE-2026-31812
- pscomponent:org/rhtpa-server

## Remote Links

- [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) -- GitHub Advisory
- [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) -- CVE Record

## Existing Issue Links

- **Related**: TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2])
  - Link ID: 1990401
  - Type: Related
  - Direction: outward (TC-8006 -> TC-8001)

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`, which maps to the **2.1.x** version stream.

From Security Configuration Version Streams table:
- Stream 2.1.x -> Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.3.z, Local Path: /home/dev/repos/rhtpa-release.0.3.z

This issue is **stream-scoped** to 2.1.x. Steps 3-4 will only apply to versions within the 2.1.x stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. From the security-matrix.md Ecosystem Mappings table for the 2.1.x stream:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | `release/0.3.z` |

Ecosystem: **Cargo** (Rust crate)
Lock file: `Cargo.lock`
Source repository: backend (rhtpa-backend)

This means remediation will require **two tasks**: an upstream backport task (fix in rhtpa-backend) and a downstream propagation subtask (update the reference in the Konflux release repo).
