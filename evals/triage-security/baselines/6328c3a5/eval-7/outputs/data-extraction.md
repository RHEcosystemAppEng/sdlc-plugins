# Step 1 -- Data Extraction for TC-8006

## Parsed CVE Data

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
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`, which maps to the
**2.1.x** version stream (Konflux release repo: `rhtpa-release.0.3.z`).

This is a **scoped** issue -- Steps 3 and 4 apply only to the 2.1.x stream.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem
Mappings in the security matrix, this maps to the **Cargo** ecosystem.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z` (for 2.1.x stream)
- Ecosystem category: Source dependency

Per the ecosystem classification table, source dependency ecosystems produce
**2 remediation tasks per stream**: upstream backport (or dependency bump if fix
is available) + downstream propagation.

## Existing Issue Links

The following links already exist on TC-8006:

- **Related** to TC-8001 (link ID: 1990401, direction: outward)
  - TC-8001 summary: CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]

## Remote Links

- [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) -- GitHub Advisory
- [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) -- CVE Record

## Version Impact Analysis (Step 2)

Based on the security matrix lock file data for the 2.1.x stream:

| Version | Build Tag | quinn-proto Version | Affected? |
|---------|-----------|---------------------|-----------|
| RHTPA 2.1.0 | v0.3.8 | 0.11.9 | YES (< 0.11.14) |
| RHTPA 2.1.1 | v0.3.12 | 0.11.9 | YES (< 0.11.14) |

Cross-stream analysis (2.2.x stream, for Case A assessment):

| Version | Build Tag | quinn-proto Version | Affected? |
|---------|-----------|---------------------|-----------|
| RHTPA 2.2.0 | v0.4.5 | 0.11.9 | YES (< 0.11.14) |
| RHTPA 2.2.1 | v0.4.8 | 0.11.12 | YES (< 0.11.14) |
| RHTPA 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES (same as 2.2.1) |
| RHTPA 2.2.3 | v0.4.11 | 0.11.14 | NO (>= 0.11.14, fixed) |
| RHTPA 2.2.4 | v0.4.12 | 0.11.14 | NO (>= 0.11.14, fixed) |

**Conclusion**: Both versions in the 2.1.x stream ship quinn-proto 0.11.9,
which is below the fix threshold of 0.11.14. TC-8006 is confirmed affected.
