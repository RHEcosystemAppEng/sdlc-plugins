# Step 1 -- Data Extraction: TC-8010

## Extracted CVE Data

| Field | Value |
|-------|-------|
| Issue Key | TC-8010 |
| CVE ID | CVE-2026-44492 |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component (label) | pscomponent:org/rhtpa-ui |
| Stream Suffix | [rhtpa-2.2] |
| Stream Scope | 2.2.x (maps to Konflux release repo rhtpa-release.0.4.z) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable Library | axios |
| Affected Version Range | versions before 1.8.2 |
| Fixed Version (fix threshold) | 1.8.2 |
| CVSS | 8.1 (High) |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Upstream Affected Component (customfield_10632) | axios |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |

## Labels

- CVE-2026-44492
- pscomponent:org/rhtpa-ui

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-44492 |

## Issue Links

No existing issue links.

## Comments

No existing comments.

## Ecosystem Detection

The vulnerable library is **axios**, which is an npm (JavaScript/TypeScript) package. The ecosystem is **npm**.

## Stream Scope Resolution

The summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

This issue is **scoped** to stream 2.2.x only. Steps 3-7 apply only to versions within this stream.
