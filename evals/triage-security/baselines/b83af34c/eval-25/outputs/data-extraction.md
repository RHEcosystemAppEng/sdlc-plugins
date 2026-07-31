# Data Extraction — TC-8040

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |
| CVSS | 7.5 (High) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for stream 2.2.x)
- Issue stream scope: **scoped to 2.2.x**

## Ecosystem Detection

- Library: quinn-proto
- Detected ecosystem: **Go modules**
- Ecosystem Mappings in stream 2.2.x security-matrix.md: Cargo, RPM
- Ecosystem Mappings in stream 2.1.x security-matrix.md: Cargo, RPM
- **Result: Go modules is NOT listed in any stream's Ecosystem Mappings table**

The detected ecosystem "Go modules" does not appear in the Ecosystem Mappings table for any configured version stream. Per the skill's unsupported ecosystem handling rule (SKILL.md Step 1), automated triage must stop and the user must be notified.
