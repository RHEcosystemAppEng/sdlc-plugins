# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| Jira Issue Key | TC-8001 |
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | None |

## Remote Links

| Link | Type | URL |
|------|------|-----|
| GHSA-2026-qp73-x4mq | GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE-2026-31812 | CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| quinn-rs/quinn#2048 | Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Matched Version Stream: 2.2.x at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue is **scoped** to the 2.2.x stream

## Ecosystem Detection

- Library: quinn-proto
- Detected ecosystem: **Go modules**
- Ecosystem Mappings table (2.2.x stream) lists: Cargo, RPM
- **Go modules is NOT listed** in the Ecosystem Mappings table for any configured stream

### Result: Unsupported Ecosystem

The detected ecosystem "Go modules" does not appear in the Ecosystem Mappings table of any configured version stream's security-matrix.md. Automated triage cannot proceed for this ecosystem because there is no configured lock file, check command, or upstream branch mapping. Manual assessment is required.
