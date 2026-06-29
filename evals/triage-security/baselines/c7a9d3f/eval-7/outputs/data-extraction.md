# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| Issue Key | TC-8006 |
| CVE ID | CVE-2026-31812 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.1] |
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
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Existing Comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`
- Local path: `/home/dev/repos/rhtpa-release.0.3.z`

This issue is **stream-scoped** to the 2.1.x stream. Steps 3-4 will apply only to versions within the 2.1.x stream.

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: rhtpa-backend
- Upstream branch: `release/0.3.z`

## Existing Issue Links

The issue has the following pre-existing links (from `issuelinks` array in the Jira response):

| Link ID | Type | Direction | Linked Issue |
|---------|------|-----------|--------------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) |

## Remote Links

| Title | URL |
|-------|-----|
| GHSA-2026-qp73-x4mq | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE-2026-31812 | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
