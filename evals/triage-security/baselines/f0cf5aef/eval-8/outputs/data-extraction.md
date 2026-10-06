# Step 1 -- Data Extraction: TC-8010

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Issue Key | TC-8010 |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-ui |
| Vulnerable Library | axios |
| Affected Version Range | versions before 1.8.2 |
| Fixed Version | 1.8.2 |
| CVSS | 8.1 (High) |
| Affects Versions (PSIRT-claimed) | RHTPA 2.2.0 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Upstream Affected Component (customfield_10632) | axios |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |

## Remote Links

| Title | URL |
|-------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-44492 |

## Labels

- CVE-2026-44492
- pscomponent:org/rhtpa-ui

## Existing Issue Links

None.

## Existing Comments

None.

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **axios**, a JavaScript/TypeScript npm package. The ecosystem is **npm**, which is a **source dependency** ecosystem. Per the ecosystem classification table, source dependency ecosystems produce 2 remediation tasks per stream (upstream backport + downstream propagation).

Note: The security-matrix.md Ecosystem Mappings table for the 2.2.x stream lists Cargo and RPM ecosystems but does not explicitly list npm. However, based on the component label (`pscomponent:org/rhtpa-ui`) and the library name (`axios`), the ecosystem is npm. In a real triage, this would require confirming with the engineer that npm is a supported ecosystem for this stream.

## Deployment Context

The affected repository (`rhtpa-ui` from the component label `pscomponent:org/rhtpa-ui`) is not listed in the Source Repositories table in Security Configuration. Defaulting deployment context to `upstream`.
