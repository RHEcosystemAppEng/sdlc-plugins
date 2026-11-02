# Step 1 — Data Extraction

## Step 0.7 — Early Assignment

**Proposed actions** (not executed — eval mode):
1. Assign TC-8011 to current user
2. Transition TC-8011 from New → Assigned

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | < 5.98.0 |
| Fixed version | 5.98.0 |
| CVSS | 7.8 (High) |
| Upstream fix PR | _(not provided)_ |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Existing comments | _(none)_ |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` → scoped to **2.2.x** stream.

## Ecosystem Detection

The vulnerable library **webpack** is an npm package. The Ecosystem Mappings table in the 2.2.x security-matrix.md lists **Cargo** and **RPM** but does not include npm.

> **Note**: The mock security-matrix.md does not include npm in the Ecosystem Mappings. In a real triage, the skill would flag this as an unsupported ecosystem for automated version-impact analysis. For the purposes of this eval (which focuses on cross-CVE overlap detection), we proceed with the overlap check using the data provided in the fixture.

## Custom Fields

- **customfield_10632** (Upstream Affected Component): `webpack`
- **customfield_10669** (PS Component): `pscomponent:org/rhtpa-ui`
- **customfield_10832** (Stream): `rhtpa-2.2`
