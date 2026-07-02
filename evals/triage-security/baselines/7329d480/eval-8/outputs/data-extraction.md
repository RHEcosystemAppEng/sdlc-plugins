# Step 1 -- Data Extraction: TC-8010

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Jira Issue Key | TC-8010 |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 |
| Fixed version | 1.8.2 |
| CVSS | 8.1 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| Assignee | Unassigned |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | axios |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** version stream from the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

The issue is **stream-scoped** to the 2.2.x stream. Steps 3-4 will apply only to versions within this stream.

## Ecosystem Detection

The vulnerable library is **axios**, which is a JavaScript/TypeScript npm package. The ecosystem is **npm**.

Note: The security-matrix.md Ecosystem Mappings table for the 2.2.x stream lists Cargo and RPM ecosystems but does not list npm. In a live triage, this would require either:
1. Confirming that npm ecosystem mappings exist elsewhere in the configuration, or
2. Flagging that npm is an unsupported ecosystem for automated lock file inspection in this stream.

However, this does not affect the cross-CVE overlap analysis in Step 4.3, which operates on Jira issue data and remediation task descriptions rather than lock file inspection.

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-44492 |

## Vulnerability Description Summary

axios before version 1.8.2 is vulnerable to Server-Side Request Forgery (SSRF) via a crafted URL that bypasses hostname validation. An attacker can craft a URL that initially resolves to an external host but redirects to an internal service. The vulnerability exists because axios does not properly validate the hostname in URLs when following redirects.
