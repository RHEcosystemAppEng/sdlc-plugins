# Data Extraction — TC-8003

## Step 1: Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Issue Key | TC-8003 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server |
| Affected Component | pscomponent:org/rhtpa-server |
| Product Version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable Library | quinn-proto |
| Affected Version Range | versions before 0.11.14 |
| Fixed Version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due Date | 2026-07-15 |
| Assignee | Unassigned |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Existing Comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (from Version Streams table in Security Configuration)
- Issue is **stream-scoped** to 2.2.x

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Classification: Source dependency ecosystem -> 2 tasks per stream (upstream backport + downstream propagation)
