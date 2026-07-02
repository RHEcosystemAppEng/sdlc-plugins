# Step 1 -- Data Extraction: TC-8011

## Extracted CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 |
| Fixed version | 5.98.0 |
| CVSS | 7.8 (High) |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Custom Fields

| Field | Value |
|-------|-------|
| customfield_10632 (Upstream Affected Component) | webpack |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (from Version Streams table: 2.2.x -> rhtpa-release.0.4.z)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Library: webpack
- Detected ecosystem: **npm** (webpack is a JavaScript/TypeScript build tool)
- Ecosystem Mappings check: the 2.2.x stream's security-matrix.md lists Cargo and RPM ecosystems only; **npm is not configured** in the Ecosystem Mappings table
- Per skill rules: "If the detected ecosystem is not listed in the stream's Ecosystem Mappings table, inform the user and stop automated triage for that ecosystem"

**Note**: Automated lock file inspection (Step 2.3) cannot proceed for npm because the ecosystem is not mapped in the security matrix. However, Jira-level triage operations (Steps 3-8) can still proceed based on the description-provided fix threshold (5.98.0) and cross-CVE overlap analysis.

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-45678 |

## Issue Links

No existing issue links on TC-8011.

## Vulnerability Description Summary

webpack before version 5.98.0 allows arbitrary code execution through a specially crafted loader chain configuration. An attacker with control over a project's webpack configuration can execute arbitrary code during the build process. The vulnerability exists because webpack does not properly sanitize loader paths when resolving the loader chain, allowing path traversal to execute arbitrary modules.
