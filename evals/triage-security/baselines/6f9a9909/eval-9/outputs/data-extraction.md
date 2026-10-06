# Step 1 -- Data Extraction: TC-8011

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **Issue Key** | TC-8011 |
| **CVE ID** | CVE-2026-45678 |
| **Summary** | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Affected Component (label)** | pscomponent:org/rhtpa-ui |
| **Upstream Affected Component** (customfield_10632) | webpack |
| **PS Component** (customfield_10669) | pscomponent:org/rhtpa-ui |
| **Stream** (customfield_10832) | rhtpa-2.2 |
| **Vulnerable Library** | webpack |
| **Affected Version Range** | versions before 5.98.0 |
| **Fixed Version (fix threshold)** | 5.98.0 |
| **CVSS Score** | 7.8 (High) |
| **Affects Versions (Jira field)** | RHTPA 2.2.0 |
| **Due Date** | 2026-08-15 |
| **Assignee** | Unassigned |
| **Existing Comments** | None |
| **Existing Issue Links** | None |

## Remote Links

| Title | URL |
|-------|-----|
| GHSA-2026-wk55-m3rr | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE-2026-45678 | https://www.cve.org/CVERecord?id=CVE-2026-45678 |

## Stream Scope Resolution

- **Stream suffix**: `[rhtpa-2.2]`
- **Mapped stream**: 2.2.x
- **Konflux Release Repo**: git.example.com/rhtpa/rhtpa-release.0.4.z
- **Local Path**: /home/dev/repos/rhtpa-release.0.4.z

The issue is **stream-scoped** to the 2.2.x stream. Steps 3-4 will be scoped to this stream only.

## Ecosystem Detection

- **Ecosystem**: npm (webpack is a JavaScript/TypeScript build tool package)
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)
- **Lock file**: determined by the stream's security-matrix.md Ecosystem Mappings table

## Deployment Context

- **Repository**: rhtpa-backend (from Source Repositories in CLAUDE.md)
- **Deployment context**: upstream (default -- no Deployment Context column configured)

## Vulnerability Description

A vulnerability was found in webpack. The webpack package before version 5.98.0 allows arbitrary code execution through a specially crafted loader chain configuration. An attacker with control over a project's webpack configuration can execute arbitrary code during the build process. The vulnerability exists because webpack does not properly sanitize loader paths when resolving the loader chain, allowing path traversal to execute arbitrary modules.
