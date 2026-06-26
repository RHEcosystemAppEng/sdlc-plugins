# Step 1 -- Data Extraction

## Parsed CVE Data for TC-8006

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Issue Key | TC-8006 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.1] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Product Version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable Library | quinn-proto |
| Affected Version Range | versions before 0.11.14 (< 0.11.14) |
| Fixed Version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due Date | 2026-07-15 |
| Assignee | Unassigned |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Existing Comments | None |

## Stream Scope Resolution

- Stream suffix parsed from summary: `[rhtpa-2.1]`
- Mapped to configured Version Stream: **2.1.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`, local path: `/home/dev/repos/rhtpa-release.0.3.z`)
- Issue stream scope: **2.1.x only**

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: rhtpa-backend (`release/0.3.z` branch for 2.1.x stream)

## Existing Issue Links

The following links already exist on TC-8006:

| Link ID | Type | Direction | Linked Issue |
|---------|------|-----------|--------------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) |

## Remote Links

| Title | URL |
|-------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
