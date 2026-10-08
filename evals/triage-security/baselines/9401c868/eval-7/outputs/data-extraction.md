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
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.1]`
- Mapped to Version Stream: **2.1.x** (Konflux release repo: `rhtpa-release.0.3.z`)
- This issue is **scoped** to the 2.1.x stream only

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`

## Existing Issue Links

The following links already exist on TC-8006:

- **Related** (outward): TC-8001 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] (Link ID: 1990401)

## Remote Links

- [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) -- GitHub Advisory
- [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) -- CVE Record

## Version Impact Table (from security-matrix.md mock data)

Scoped to stream 2.1.x per issue suffix `[rhtpa-2.1]`:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0   | 0.11.9      | YES       | < 0.11.14, affected |
| 2.1.1   | 0.11.9      | YES       | < 0.11.14, affected |

Cross-stream reference (2.2.x stream, tracked by sibling TC-8001):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0   | 0.11.9      | YES       | < 0.11.14, affected |
| 2.2.1   | 0.11.12     | YES       | < 0.11.14, affected |
| 2.2.2   | --          | YES       | retag of 2.2.1 |
| 2.2.3   | 0.11.14     | NO        | >= 0.11.14, fixed |
| 2.2.4   | 0.11.14     | NO        | >= 0.11.14, fixed |
