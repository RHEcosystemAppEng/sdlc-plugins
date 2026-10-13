# Step 1 -- Data Extraction for TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Affected component | pscomponent:org/rhtpa-ui (from label matching `pscomponent:` pattern) |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (mapped from suffix `[rhtpa-2.2]` to Version Streams table) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 |
| Fixed version (fix threshold) | 1.8.2 |
| Upstream fix PR | (none found in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| CVSS | 8.1 (High) |
| Existing comments | (none) |
| Existing issue links | (none) |

## Custom Fields

| Field | ID | Value |
|-------|----|-------|
| Upstream Affected Component | customfield_10632 | axios |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the `2.2.x` stream in the Version Streams table from Security Configuration. The issue is therefore **scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **axios**, which is a JavaScript/TypeScript npm package. The ecosystem is **npm**.

This is a **source dependency** ecosystem per the classification table. Source dependency ecosystems produce 2 remediation tasks per stream: dependency bump (or upstream backport) + downstream propagation.

## Deployment Context Lookup

The affected repository identified from the component label `pscomponent:org/rhtpa-ui` does not appear in the Source Repositories table (which only lists `rhtpa-backend`). Per skill rules, the deployment context defaults to `upstream`.
