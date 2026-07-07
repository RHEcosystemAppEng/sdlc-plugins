# Step 1 -- Data Extraction

## Parsed CVE Data for TC-8011

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Jira Issue Key | TC-8011 |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-ui |
| Vulnerable Library | webpack |
| Affected Version Range | versions before 5.98.0 |
| Fixed Version (Fix Threshold) | 5.98.0 |
| CVSS Score | 7.8 (High) |
| Affects Versions (PSIRT-claimed) | RHTPA 2.2.0 |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
| Labels | CVE-2026-45678, pscomponent:org/rhtpa-ui |
| Existing Comments | None |
| Upstream Affected Component (customfield_10632) | webpack |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-45678 |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

**Issue stream scope**: 2.2.x (scoped to single stream)

## Ecosystem Detection

The vulnerable library is **webpack**, which is a JavaScript/TypeScript package. The detected ecosystem is **npm**.

## Vulnerability Description

The webpack package before version 5.98.0 allows arbitrary code execution through a specially crafted loader chain configuration. An attacker with control over a project's webpack configuration can execute arbitrary code during the build process. The vulnerability exists because webpack does not properly sanitize loader paths when resolving the loader chain, allowing path traversal to execute arbitrary modules.
