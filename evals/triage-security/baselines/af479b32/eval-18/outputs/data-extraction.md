# Step 1 -- Data Extraction for TC-8001

## Extracted CVE Data

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
- Mapped stream: **2.2.x** (matches Version Streams row: `2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Library: quinn-proto
- Ecosystem: **Cargo** (Rust crate)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Upstream branch: `release/0.4.z`

## Existing Issue Links (from prior triage)

| Link Type | Issue | Summary | Status |
|-----------|-------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

## Existing Comments (from prior triage)

1. **Description digest comment**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (posted 2026-07-01T10:00:00Z by sdlc-workflow/triage-security)
2. **Post-triage summary comment**: Documents version impact (RHTPA 2.2.0 and 2.2.1 affected, 2.2.2+ not affected), Affects Versions correction, ai-cve-triaged label, remediation tasks TC-8100 and TC-8101, transition to In Progress (posted 2026-07-01T10:01:00Z by sdlc-workflow/triage-security)

## Remote Links

| Title | URL |
|-------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |

## Version Impact Table (from security-matrix mock data)

Based on the security matrix mock data, the quinn-proto versions by tag for the 2.2.x stream are:

| Version | Tag | quinn-proto version | Affected? (< 0.11.14) | Notes |
|---------|-----|---------------------|-----------------------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | v0.4.9 | -- | YES | retag of v0.4.8 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

Cross-stream data (2.1.x, for Case B analysis):

| Version | Tag | quinn-proto version | Affected? (< 0.11.14) | Notes |
|---------|-----|---------------------|-----------------------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | |
