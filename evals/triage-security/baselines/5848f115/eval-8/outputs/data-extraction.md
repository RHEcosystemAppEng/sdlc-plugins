# Step 1 -- Data Extraction: TC-8010

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Jira Issue Key | TC-8010 |
| Issue Type | Vulnerability |
| Status | New |
| Affected component (label) | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 |
| Fixed version (fix threshold) | 1.8.2 |
| CVSS | 8.1 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| Assignee | Unassigned |
| Existing comments | None |
| Existing issue links | None |
| Upstream Affected Component (customfield_10632) | axios |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **axios**, which is a JavaScript/TypeScript npm package. The ecosystem is **npm**, which is a **source dependency** ecosystem per the classification table. This means remediation would normally require 2 tasks per stream (upstream backport + downstream propagation).

## Vulnerability Summary

CVE-2026-44492 is a Server-Side Request Forgery (SSRF) vulnerability in the axios HTTP client library. Versions before 1.8.2 do not properly validate hostnames in URLs when following redirects, allowing an attacker to craft a URL that initially resolves to an external host but redirects to an internal service. The fix threshold is axios >= 1.8.2.
