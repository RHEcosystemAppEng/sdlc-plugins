# Step 1 -- Data Extraction: TC-8040

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x.

## Ecosystem Detection

| Attribute | Value |
|-----------|-------|
| Detected ecosystem | Go modules |
| Detection basis | Library name and component context analysis |
| Supported ecosystems (2.1.x stream) | Cargo, RPM |
| Supported ecosystems (2.2.x stream) | Cargo, RPM |
| Ecosystem supported? | **No** -- Go modules is not listed in the Ecosystem Mappings table of any configured stream |

The detected ecosystem "Go modules" does not appear in the Ecosystem Mappings table of either the 2.1.x or 2.2.x version stream. Both streams only define mappings for Cargo and RPM ecosystems.

**Result**: Automated triage cannot proceed. The skill does not have a configured lock file path, check command, or repository mapping for the Go modules ecosystem. Manual assessment is required.
