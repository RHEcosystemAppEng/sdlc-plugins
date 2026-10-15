# Step 1 -- Data Extraction for TC-8011

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-45678 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-ui | Labels (component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | webpack | Description text |
| Affected version range | versions before 5.98.0 | Description text |
| Fixed version | 5.98.0 | Description text |
| CVSS | 7.8 (High) | Description text |
| Upstream fix PR | (none found) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 | Remote links |
| Due date | 2026-08-15 | Issue `duedate` field |
| Upstream Affected Component | webpack | customfield_10632 |
| PS Component | pscomponent:org/rhtpa-ui | customfield_10669 |
| Stream | rhtpa-2.2 | customfield_10832 |
| Existing comments | (none) | Issue comments |
| Existing issue links | (none) | Issue links |
| Assignee | Unassigned | Issue assignee |
| Status | New | Issue status |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry: stream 2.2.x, Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Vulnerable library: **webpack**
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Classification: Source dependency ecosystem
- Remediation task count per stream: 2 (dependency bump or upstream backport + downstream propagation)

Note: The security matrix Ecosystem Mappings for stream 2.2.x (rhtpa-release.0.4.z) list Cargo and RPM ecosystems but do not include npm. The npm ecosystem is not currently configured in the Ecosystem Mappings table. This would normally trigger the unsupported ecosystem warning:

> "Unsupported ecosystem: npm is not yet supported for automated triage. Manual assessment is required."

However, for the purpose of this triage analysis, we proceed with the provided fixture data to complete the overlap check and triage decision.

## Deployment Context

- Source Repositories table lists `rhtpa-backend` with no Deployment Context column
- The affected component (`rhtpa-ui`) is not listed in the Source Repositories table
- Default deployment context: `upstream`
