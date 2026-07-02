# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Jira Issue Key | TC-8011 |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Ecosystem | npm |
| Affected version range | versions before 5.98.0 |
| Fixed version (fix threshold) | 5.98.0 |
| CVSS | 7.8 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Existing comments | None |
| Existing issue links | None |

## Custom Fields

| Custom Field | Field ID | Value |
|--------------|----------|-------|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** version stream in the Security Configuration's Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

The issue is **stream-scoped** to 2.2.x. Steps 3-4 apply only to this stream.

## Ecosystem Detection

The vulnerable library is **webpack**, which is an npm (JavaScript/TypeScript) package.

Checking the 2.2.x stream's Ecosystem Mappings table from security-matrix.md:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | git show <tag>:Cargo.lock | release/0.4.z |
| RPM | -- | rpms.lock.yaml | git show <tag>:rpms.lock.yaml | -- |

The **npm** ecosystem is not listed in the Ecosystem Mappings table. Per the skill rules, this means automated version impact analysis (Step 2) via lock file inspection cannot be performed for this ecosystem. Manual assessment would be required for version impact analysis.

However, the cross-CVE overlap check (Step 4.3) can still proceed because it operates on Jira issue data and remediation task descriptions, not on lock files.

## Deployment Context

The affected repository (rhtpa-ui, from the component label pscomponent:org/rhtpa-ui) is not found in the Source Repositories table, which only lists rhtpa-backend. Defaulting deployment context to `upstream`.
