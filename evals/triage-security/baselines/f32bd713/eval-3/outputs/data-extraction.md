# Step 1 -- Data Extraction: TC-8003

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (Component label pattern: `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | (none extracted) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links -- GitHub Advisory |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links -- CVE Record |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | (none) | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for stream `2.2.x` at Konflux release repo `rhtpa-release.0.4.z`)
- Issue stream scope: **scoped to 2.2.x only**

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo** (listed in stream 2.2.x Ecosystem Mappings table)
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

## Deployment Context Lookup

- Affected repository (from component label `pscomponent:org/rhtpa-server`): rhtpa-backend
- Deployment context: `upstream` (from Source Repositories table; no Deployment Context column present, so default applies)

## Version Impact Analysis (from mock lock file data)

Scoped to stream 2.2.x only (per issue stream scope):

| Version | Build Tag | quinn-proto Version | Affected? (< 0.11.14) | Notes |
|---------|-----------|---------------------|----------------------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | Ships vulnerable version |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | Ships vulnerable version |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES | Same as 2.2.1 (retag) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | Ships fixed version (>= 0.11.14) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | Ships fixed version (>= 0.11.14) |

Cross-stream reference (stream 2.1.x, outside issue scope):

| Version | Build Tag | quinn-proto Version | Affected? (< 0.11.14) |
|---------|-----------|---------------------|----------------------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.1 | v0.3.12 | 0.11.9 | YES |

## Configuration Extracted (Step 0)

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Jira version prefix: RHTPA
- Vulnerability issue type ID: 10024
- Product pages URL: https://access.example.com/product-life-cycle/rhtpa
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- Security matrix last updated: 2026-06-28T10:00:00Z (within 14-day staleness threshold relative to a triage date shortly after)
