# Step 1 -- Data Extraction for TC-8011

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-45678 | Labels: `CVE-2026-45678`; summary text |
| Affected component | pscomponent:org/rhtpa-ui | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | webpack | Description: "A vulnerability was found in webpack" |
| Affected version range | versions before 5.98.0 (i.e., < 5.98.0) | Description text |
| Fixed version | 5.98.0 | Description: "Fixed version: 5.98.0" |
| CVSS | 7.8 (High) | Description text |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 | Remote links |
| Upstream fix PR | Not provided | No PR URL in remote links |
| Due date | 2026-08-15 | Issue `duedate` field |
| Existing comments | None | No comments on issue |
| Existing issue links | None | No existing links |

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.2]`
- Parsed stream: `2.2.x`
- Matched to configured Version Stream: **2.2.x** (Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x only** (scoped issue -- Steps 3-4 apply to this stream only)

## Ecosystem Detection

- Vulnerable library: **webpack**
- Ecosystem: **npm** (webpack is a JavaScript/TypeScript build tool distributed via npm)
- The security-matrix.md for stream 2.2.x defines Cargo and RPM ecosystem mappings but does **not** include an npm ecosystem mapping
- This means there is no configured lock file path or check command for npm dependencies in this stream
- Impact: Lock file inspection for webpack would require an npm ecosystem entry in the Ecosystem Mappings table. Without it, the version of webpack shipped in each product version cannot be determined from the existing matrix configuration alone. The engineer would need to be informed of this gap.

## Vulnerability Summary

CVE-2026-45678 is a **High severity (CVSS 7.8)** arbitrary code execution vulnerability in the webpack package. Versions before 5.98.0 are vulnerable due to improper sanitization of loader paths during loader chain resolution, allowing path traversal to execute arbitrary modules. An attacker with control over a project's webpack configuration can execute arbitrary code during the build process. The fix is available in webpack 5.98.0.
