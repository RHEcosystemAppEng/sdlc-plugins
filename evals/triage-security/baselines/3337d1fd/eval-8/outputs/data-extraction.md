# Step 1 -- Data Extraction: TC-8010

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 |
| Fixed version | 1.8.2 |
| CVSS | 8.1 (High) |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| Existing comments | (none) |
| Issue status | New |
| Assignee | Unassigned |

## Custom Fields

| Custom Field | Value |
|--------------|-------|
| customfield_10632 (Upstream Affected Component) | axios |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to
the **2.2.x** version stream in the Security Configuration Version Streams
table. This issue is **scoped** to the 2.2.x stream only.

- Stream suffix: `[rhtpa-2.2]` -> stream `2.2.x`
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local path: `/home/dev/repos/rhtpa-release.0.4.z`

## Ecosystem Detection

The vulnerable library is **axios**, which is a JavaScript/TypeScript npm
package. The ecosystem is **npm**.

The Ecosystem Mappings table in the security-matrix.md for the 2.2.x stream
does not list npm as a configured ecosystem -- only Cargo and RPM are
configured. This means automated lock file inspection for axios is not
available via the standard matrix-based approach.

However, the component label `pscomponent:org/rhtpa-ui` identifies
this as a UI component (likely a frontend JavaScript application), which
would use npm/package-lock.json for dependency management.

## Vulnerability Description

axios before version 1.8.2 is vulnerable to Server-Side Request Forgery
(SSRF) via a crafted URL that bypasses hostname validation. An attacker can
exploit this to make requests to internal services. The vulnerability exists
because axios does not properly validate the hostname in URLs when following
redirects.

## Issue Links

No existing issue links on TC-8010.

## Remote Links

- GHSA-2026-ax91-r7pp (GitHub Advisory)
- CVE-2026-44492 (CVE Record)
