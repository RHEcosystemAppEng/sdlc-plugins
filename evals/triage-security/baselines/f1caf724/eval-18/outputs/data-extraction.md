# Step 1 -- Data Extraction

## Issue Metadata

| Field | Value |
|-------|-------|
| Issue Key | TC-8001 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | In Progress |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged |
| Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1 |
| Due Date | 2026-07-15 |
| Assignee | engineer-a@example.com |

## Extracted CVE Data

| Field | Source | Value |
|-------|--------|-------|
| CVE ID | Labels + summary | CVE-2026-31812 |
| Affected component | Label (pscomponent:) | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | Summary suffix | [rhtpa-2.2] |
| Affects Versions (Jira field) | Jira `versions` field | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | Description text | quinn-proto |
| Affected version range | Description text | versions before 0.11.14 |
| Fixed version | Description text | 0.11.14 |
| CVSS | Description text | 7.5 (High) |
| Upstream fix PR | Remote links | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | Remote links | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | Remote links | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | Issue field | 2026-07-15 |

## Custom Fields

| Custom Field | ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | quinn-proto |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-server |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- Issue is **stream-scoped** to the 2.2.x stream only

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Remediation task count per stream: **2** (upstream backport + downstream propagation)

## Existing Issue Links

| Link Type | Issue Key | Summary | Status |
|-----------|-----------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

TC-8101 also has a Blocks relationship to TC-8100 (downstream blocked by upstream).

## Existing Comments

1. **Description digest comment**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (posted 2026-07-01T10:00:00Z by sdlc-workflow/triage-security)
2. **Post-triage summary comment**: Documents version impact, actions taken, remediation tasks created (posted 2026-07-01T10:01:00Z by sdlc-workflow/triage-security)

## Version Impact Table (from mock lock file data, scoped to 2.2.x stream)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | v0.4.5 pin |
| 2.2.1 | 0.11.12 | YES | v0.4.8 pin |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | v0.4.11 pin (at fix threshold) |
| 2.2.4 | 0.11.14 | NO | v0.4.12 pin (at fix threshold) |

Fix threshold: quinn-proto >= 0.11.14

Affected versions within scope: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Not affected: RHTPA 2.2.3, RHTPA 2.2.4

## Cross-stream impact (out of scope for this issue)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | v0.3.8 pin (stream 2.1.x -- outside issue scope) |
| 2.1.1 | 0.11.9 | YES | v0.3.12 pin (stream 2.1.x -- outside issue scope) |

Stream 2.1.x is also affected but tracked separately per PSIRT stream scoping.
