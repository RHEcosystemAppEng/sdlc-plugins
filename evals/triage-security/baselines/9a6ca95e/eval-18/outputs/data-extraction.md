# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | quinn-rs/quinn#2048 (https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | GHSA-2026-qp73-x4mq (https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | engineer-a@example.com |
| Status | In Progress |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Ecosystem: **Cargo** (quinn-proto is a Rust crate)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Upstream branch: `release/0.4.z`

## Custom Fields

| Field | ID | Value |
|-------|----|-------|
| Upstream Affected Component | customfield_10632 | quinn-proto |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-server |
| Stream | customfield_10832 | rhtpa-2.2 |

## Existing Issue Links

| Link Type | Issue | Summary | Status |
|-----------|-------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

TC-8101 also has a Blocks link to TC-8100 (downstream blocked by upstream).

## Existing Comments

1. **Description digest comment**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (posted 2026-07-01T10:00:00Z by sdlc-workflow/triage-security)
2. **Post-triage summary comment**: documents version impact, Affects Versions correction, remediation tasks TC-8100 and TC-8101, and transition to In Progress (posted 2026-07-01T10:01:00Z by sdlc-workflow/triage-security)

## Version Impact Table (from security-matrix.md mock data)

Scoped to stream 2.2.x only (per issue suffix `[rhtpa-2.2]`):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 0.11.12 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 0.11.14 | NO | >= 0.11.14 (fixed) |

Cross-stream reference (2.1.x, outside issue scope):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 0.11.9 | YES | < 0.11.14 |
