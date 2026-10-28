# Step 1 -- Data Extraction for TC-8001

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 | Description text ("versions before 0.11.14") |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote links |
| Advisory URL | GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Assignee | engineer-a@example.com | Issue `assignee` field |
| Upstream Affected Component | quinn-proto | customfield_10632 |
| PS Component | pscomponent:org/rhtpa-server | customfield_10669 |
| Stream | rhtpa-2.2 | customfield_10832 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x** (rhtpa-release.0.4.z)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Expected remediation tasks per stream: 2 (upstream backport + downstream propagation)

## Existing Issue Links

| Link Type | Target | Summary | Status |
|-----------|--------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

## Existing Comments

1. Description digest comment: `sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (posted by sdlc-workflow/triage-security)
2. Post-triage summary comment documenting version impact, actions taken, and remediation tasks (posted by sdlc-workflow/triage-security)

## Version Impact Table (from security-matrix-mock.md)

Stream 2.2.x (rhtpa-release.0.4.z):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 0.11.14 | NO | >= 0.11.14 (fixed) |
