# Step 1 -- Data Extraction: TC-8011

## Extracted CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Issue Key | TC-8011 |
| Issue Type | Vulnerability |
| Status | New |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| Affected Component | pscomponent:org/rhtpa-ui |
| Vulnerable Library | webpack |
| Affected Version Range | versions before 5.98.0 |
| Fixed Version (fix threshold) | 5.98.0 |
| CVSS Score | 7.8 (High) |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Upstream Fix PR | Not provided in remote links |
| Existing Comments | None |

## Custom Fields

| Custom Field | Value |
|---|---|
| customfield_10632 (Upstream Affected Component) | webpack |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. Mapping to the
configured Version Streams:

- Suffix: `[rhtpa-2.2]` maps to stream **2.2.x**
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z

This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **webpack**, which is a JavaScript/TypeScript
package distributed via npm. This classifies as:

- **Ecosystem**: npm
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)

## Vulnerability Description

A vulnerability was found in webpack. The webpack package before version 5.98.0
allows arbitrary code execution through a specially crafted loader chain
configuration. An attacker with control over a project's webpack configuration
can execute arbitrary code during the build process.

The vulnerability exists because webpack does not properly sanitize loader paths
when resolving the loader chain, allowing path traversal to execute arbitrary
modules.

## Deployment Context Lookup

The affected repository is identified from the component label
`pscomponent:org/rhtpa-ui`. Looking up in Source Repositories:

- Repository: rhtpa-backend (the only configured source repo)
- The component `rhtpa-ui` does not directly match `rhtpa-backend`
- Defaulting deployment context to: **upstream** (per Step 0 fallback rule)
