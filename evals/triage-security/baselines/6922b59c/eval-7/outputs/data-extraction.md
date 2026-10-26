# Step 1 -- Data Extraction for TC-8006

## Extracted CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`, which maps to the **2.1.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |

This issue is **scoped** to the 2.1.x stream only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.1.x stream's Ecosystem Mappings table includes:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |

Ecosystem: **Cargo** (source dependency). Per the ecosystem classification table, this produces **2 remediation tasks per stream**: upstream backport (or dependency bump if fix available) + downstream propagation.

## Existing Issue Links

The issue already has the following links:

- **Related** (outward): TC-8001 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
  - Link ID: 1990401

## Remote Links

- [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) -- GitHub Advisory
- [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) -- CVE Record

## Version Impact (2.1.x stream only, scoped)

From the security-matrix.md mock lock file data for quinn-proto:

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 fix threshold |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 fix threshold |

Both versions in the 2.1.x stream ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14. All versions in this stream are affected.

## Cross-stream Impact (informational)

The 2.2.x stream is also affected (versions 2.2.0 and 2.2.1 ship quinn-proto 0.11.9 and 0.11.12 respectively, both below 0.11.14). However, this issue is scoped to 2.1.x only. The 2.2.x stream has its own CVE Jira: TC-8001.
