# Step 1 -- Data Extraction for TC-8001

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote links |
| Advisory URL | GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Assignee | engineer-a@example.com | Jira `assignee` field |
| Upstream Affected Component | quinn-proto | customfield_10632 |
| PS Component | pscomponent:org/rhtpa-server | customfield_10669 |
| Stream | rhtpa-2.2 | customfield_10832 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table row for `rhtpa-release.0.4.z`)
- Issue stream scope: **scoped to 2.2.x only**

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Remediation task structure: 2 tasks per stream (upstream backport/dependency bump + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

## Existing Issue Links (Pre-Existing)

| Link Type | Linked Issue | Summary | Status |
|-----------|-------------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

## Existing Comments (Pre-Existing)

1. **Description digest comment**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (posted 2026-07-01T10:00:00Z)
2. **Post-triage summary comment**: Documents version impact, Affects Versions correction, remediation tasks TC-8100 and TC-8101, transition to In Progress, and `ai-cve-triaged` label (posted 2026-07-01T10:01:00Z)

## Existing Labels

- `CVE-2026-31812` -- CVE identifier
- `pscomponent:org/rhtpa-server` -- component label
- `ai-cve-triaged` -- **triage completion marker from prior run**

## Version Impact Table (from security-matrix mock data)

Scoped to stream 2.2.x only (per issue suffix `[rhtpa-2.2]`):

| Version | quinn-proto | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | tag v0.4.5 |
| 2.2.1 | 0.11.12 | YES | tag v0.4.8 |
| 2.2.2 | 0.11.12 | YES | retag of v0.4.8 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | tag v0.4.11 -- at fix threshold |
| 2.2.4 | 0.11.14 | NO | tag v0.4.12 -- at fix threshold |

Affected versions within scope: RHTPA 2.2.0, RHTPA 2.2.1 (and 2.2.2 by retag).
The Jira Affects Versions field already lists RHTPA 2.2.0 and RHTPA 2.2.1.
