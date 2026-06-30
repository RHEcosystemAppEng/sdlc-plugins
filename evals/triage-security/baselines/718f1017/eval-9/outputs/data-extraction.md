# Step 1 -- Data Extraction for TC-8011

## Extracted Fields

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 |
| Fixed version | 5.98.0 |
| Upstream fix PR | (none found in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Existing comments | (none) |
| CVSS | 7.8 (High) |

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the configured Version Stream **2.2.x** in the Security Configuration (Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

**Issue stream scope**: 2.2.x (scoped to single stream)

Steps 3 and 4 will be scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **webpack**, which is an npm (JavaScript/TypeScript) package.

**Ecosystem**: npm

The ecosystem mappings in the 2.2.x stream's security-matrix.md list Cargo and RPM ecosystems but do not include an npm ecosystem mapping. This means there is no configured lock file path or check command for npm dependencies in this stream.

This would need to be flagged to the engineer: the npm ecosystem is not configured in the security-matrix.md Ecosystem Mappings table for the 2.2.x stream. The engineer would need to provide the lock file path (e.g., `package-lock.json`) and the check command for inspecting webpack's version in the npm lock file.

## Fix Threshold

From the Jira description and cross-validated with external CVE data enrichment (Step 1.5):

- **Fix threshold**: 5.98.0 (webpack versions before 5.98.0 are vulnerable)
- **Affected range**: < 5.98.0
- **Fixed version**: >= 5.98.0
