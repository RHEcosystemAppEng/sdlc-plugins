# Step 1 -- Data Extraction: TC-8011

## Extracted CVE Fields

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-45678 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-ui | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | webpack | Description text |
| Affected version range | versions before 5.98.0 | Description text |
| Fixed version | 5.98.0 | Description text |
| CVSS score | 7.8 (High) | Description text |
| Upstream fix PR | (none found) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 | Remote links |
| Due date | 2026-08-15 | Issue `duedate` field |
| Existing comments | (none) | Issue comments |
| Assignee | Unassigned | Issue `assignee` field |
| Status | New | Issue `status` field |

## Custom Fields

| Custom Field | Field ID | Value |
|--------------|----------|-------|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches configured Version Stream `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Vulnerable library: **webpack**
- Detected ecosystem: **npm** (JavaScript/TypeScript package)
- Ecosystem classification: **Source dependency** -- produces 2 remediation tasks per stream (dependency bump + downstream propagation, since fix version 5.98.0 is available)

**Note:** The security matrix Ecosystem Mappings tables for both the 2.1.x and 2.2.x streams list only **Cargo** and **RPM** ecosystems. The **npm** ecosystem is not present in the Ecosystem Mappings table. Per skill rules, this would normally trigger an unsupported ecosystem warning:

> "Unsupported ecosystem: npm is not yet supported for automated triage. Manual assessment is required."

However, the triage analysis continues for Step 4.3 overlap detection since that step operates on Jira metadata (Upstream Affected Component field and remediation task descriptions) rather than lock file evidence.

## Deployment Context Lookup

- Affected repository from component label: rhtpa-ui (from `pscomponent:org/rhtpa-ui`)
- Source Repositories table contains only `rhtpa-backend`
- rhtpa-ui is **not found** in the Source Repositories table
- Default deployment context: **upstream**

## Existing Issue Links

No existing issue links on TC-8011.
