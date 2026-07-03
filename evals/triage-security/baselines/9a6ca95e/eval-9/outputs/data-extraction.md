# Step 1 -- Data Extraction: TC-8011

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **Jira Key** | TC-8011 |
| **CVE ID** | CVE-2026-45678 |
| **Summary** | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Severity / CVSS** | High / 7.8 |
| **Due Date** | 2026-08-15 |
| **Assignee** | Unassigned |

## Affected Component

| Field | Value |
|-------|-------|
| **Upstream Affected Component** (customfield_10632) | webpack |
| **PS Component** (customfield_10669) | pscomponent:org/rhtpa-ui |
| **Stream** (customfield_10832) | rhtpa-2.2 |
| **Affects Versions** | RHTPA 2.2.0 |

## Vulnerability Details

| Field | Value |
|-------|-------|
| **Affected package** | webpack |
| **Affected versions** | versions before 5.98.0 |
| **Fixed version (fix threshold)** | 5.98.0 |
| **Vulnerability type** | Arbitrary Code Execution via loader chain |
| **Attack vector** | Attacker with control over webpack configuration can execute arbitrary code during build via unsanitized loader paths (path traversal) |

## Ecosystem Detection

| Field | Value |
|-------|-------|
| **Ecosystem** | npm |
| **Lock file** | package-lock.json (or equivalent) |
| **Detection basis** | webpack is an npm package |

## Stream Scope Resolution

| Field | Value |
|-------|-------|
| **Stream suffix** | [rhtpa-2.2] |
| **Resolved stream** | 2.2.x |
| **Konflux Release Repo** | git.example.com/rhtpa/rhtpa-release.0.4.z |

## Remote Links / Advisories

| Source | URL |
|--------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-45678 |

## Labels

- CVE-2026-45678
- pscomponent:org/rhtpa-ui

## Issue Links

No existing issue links found on TC-8011.
