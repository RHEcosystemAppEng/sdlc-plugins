# Step 1 -- Data Extraction: TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Issue Key | TC-8010 |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x (mapped from suffix `[rhtpa-2.2]` to Version Streams table) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Ecosystem | npm |
| Affected version range | versions before 1.8.2 |
| Fixed version (fix threshold) | 1.8.2 |
| CVSS | 8.1 (High) |
| Due date | 2026-08-01 |
| Assignee | Unassigned |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Upstream fix PR | Not available (no PR link in remote links) |
| Existing comments | None |
| Existing issue links | None |

## Custom Fields

| Custom Field | Field ID | Value |
|--------------|----------|-------|
| Upstream Affected Component | customfield_10632 | axios |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Labels

- CVE-2026-44492
- pscomponent:org/rhtpa-ui

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** stream in the Version Streams table (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`). The triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **axios**, which is an npm package. The ecosystem is **npm**. The lock file and check command will be determined from the 2.2.x stream's `security-matrix.md` Ecosystem Mappings table.
