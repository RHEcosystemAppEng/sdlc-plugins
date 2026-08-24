# Data Extraction -- CVE-2026-28940

## Source Issue

| Field | Value |
|-------|-------|
| Issue Key | TC-8002 |
| Summary | CVE-2026-28940 serde_json - Stack overflow on deeply nested input [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Assignee | Unassigned |
| Due Date | 2026-07-30 |

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected Component | pscomponent:org/rhtpa-server |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable Library | serde_json |
| Affected Version Range | versions before 1.0.135 |
| Fixed Version | 1.0.135 |
| CVSS Score | 5.3 (Medium) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Upstream Fix PR | None found in remote links |
| Existing Comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (from Version Streams table in Security Configuration)
- Issue is **stream-scoped** to 2.2.x

## Ecosystem Detection

- Library: serde_json (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`
- Remediation tasks per stream (if affected): 2 (upstream backport + downstream propagation)

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: upstream (default, no explicit Deployment Context column in Source Repositories table)
