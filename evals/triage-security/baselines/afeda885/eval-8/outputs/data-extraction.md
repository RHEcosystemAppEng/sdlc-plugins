# Step 1 -- Data Extraction: TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Issue Key | TC-8010 |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component (label) | pscomponent:org/rhtpa-ui |
| Upstream Affected Component (customfield_10632) | axios |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |
| Vulnerable Library | axios |
| Affected Version Range | versions before 1.8.2 |
| Fixed Version (fix threshold) | 1.8.2 |
| CVSS | 8.1 (High) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Existing Issue Links | None |
| Existing Comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration's Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

This issue is **scoped** to the 2.2.x stream only. Steps 3-4 will only apply Affects Versions within this stream.

## Ecosystem Detection

The vulnerable library is **axios**, which is an npm (JavaScript/TypeScript) package. The ecosystem is **npm**. Lock file inspection would use `package-lock.json` with the npm check command pattern.

Note: The security-matrix-mock.md provided for this eval does not include npm ecosystem mappings -- it contains Cargo and RPM ecosystems for the backend repository. The axios library is a frontend dependency (rhtpa-ui component), so in a real triage the npm ecosystem mapping would be read from the rhtpa-ui component's security matrix. For this eval, we proceed with the data as given.
