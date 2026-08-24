# Step 1 -- Data Extraction: TC-8006

## Extracted CVE Data

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

## Remote Links

- [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) -- GitHub Advisory
- [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) -- CVE Record

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.1]`, which maps to
the **2.1.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |

This issue is **scoped** to the 2.1.x stream only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Per the Ecosystem Mappings
table in the 2.1.x stream's security-matrix.md, the ecosystem is **Cargo**.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`

Cargo is a **source dependency** ecosystem, which means remediation produces
2 tasks per stream: upstream backport + downstream propagation.

## Existing Issue Links

The following links already exist on TC-8006:

- **Related** (outward): TC-8001 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
  - Link ID: 1990401

## Version Impact (from mock lock file data)

Using the mock lock file data from security-matrix-mock.md:

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

Both versions in the 2.1.x stream ship quinn-proto 0.11.9, which is below
the fix threshold of 0.11.14. All versions in this stream are affected.
