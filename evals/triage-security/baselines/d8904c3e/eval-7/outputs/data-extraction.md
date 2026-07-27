# Step 1 -- Data Extraction

## Issue Metadata

| Field | Value |
|-------|-------|
| Issue Key | TC-8006 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.1] |
| Issue Type | Vulnerability |
| Status | New |
| Assignee | Unassigned |
| Due Date | 2026-07-15 |

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
| Upstream fix PR | (none found in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Existing comments | (none) |

## Stream Scope Resolution

- Summary stream suffix: `[rhtpa-2.1]`
- Mapped to configured Version Stream: **2.1.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`, local path: `/home/dev/repos/rhtpa-release.0.3.z`)
- Issue is **stream-scoped** to 2.1.x only

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Remediation task count per stream: **2** (upstream backport + downstream propagation)

## Existing Issue Links

| Link Type | Direction | Linked Issue | Link ID |
|-----------|-----------|--------------|---------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) | 1990401 |

## Remote Links

| Title | URL |
|-------|-----|
| GHSA-2026-qp73-x4mq | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE-2026-31812 | https://www.cve.org/CVERecord?id=CVE-2026-31812 |

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: upstream (default -- no Deployment Context column in Source Repositories table)
