# Step 1 -- Data Extraction

## Issue: TC-8010

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component (label) | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 |
| Fixed version (fix threshold) | 1.8.2 |
| CVSS | 8.1 (High) |
| Due date | 2026-08-01 |
| Assignee | Unassigned |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Upstream fix PR | Not provided |
| Existing comments | None |
| Existing issue links | None |

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | axios |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`). This issue is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **axios**, which is a JavaScript/TypeScript npm package. The ecosystem is **npm**.

Note: The security-matrix.md Ecosystem Mappings for the 2.2.x stream list Cargo and RPM ecosystems but do not include npm. In a real triage, this would trigger an unsupported ecosystem warning. However, for the purposes of this eval, the cross-CVE overlap analysis in Step 4.3 proceeds based on the Upstream Affected Component field regardless of ecosystem support.
