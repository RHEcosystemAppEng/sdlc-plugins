# Step 1 -- Data Extraction: TC-8010

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-44492 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-ui | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | [rhtpa-2.2] | Summary suffix |
| Stream scope | 2.2.x | Mapped from suffix `[rhtpa-2.2]` to Version Streams table |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | axios | Description text |
| Affected version range | versions before 1.8.2 | Description text |
| Fixed version (fix threshold) | 1.8.2 | Description text |
| CVSS score | 8.1 (High) | Description text |
| Upstream Affected Component | axios | customfield_10632 |
| PS Component | pscomponent:org/rhtpa-ui | customfield_10669 |
| Stream | rhtpa-2.2 | customfield_10832 |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 | Remote links |
| Upstream fix PR | (none found) | Remote links |
| Due date | 2026-08-01 | Issue `duedate` field |
| Status | New | Issue status |
| Assignee | Unassigned | Issue assignee |
| Existing comments | (none) | Issue comments |
| Existing issue links | (none) | Issue links |

## Stream Scope Resolution

The summary suffix `[rhtpa-2.2]` maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

This issue is **stream-scoped** to 2.2.x only. Steps 3-4 are scoped to this single stream.

## Ecosystem Detection

The vulnerable library **axios** is an **npm** package (JavaScript/TypeScript). This is a source dependency ecosystem, which under normal circumstances would produce **2 remediation tasks per stream** (dependency bump or upstream backport + downstream propagation).

## Vulnerability Description

A vulnerability was found in axios. The axios package before version 1.8.2 is vulnerable to Server-Side Request Forgery (SSRF) via a crafted URL that bypasses hostname validation. An attacker can exploit this to make requests to internal services. The vulnerability exists because axios does not properly validate the hostname in URLs when following redirects.
