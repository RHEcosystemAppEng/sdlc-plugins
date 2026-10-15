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
- Mapped to configured Version Stream: **2.2.x**
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Issue is **stream-scoped** to the 2.2.x stream only

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
- Expected remediation tasks per stream: 2 (upstream backport + downstream propagation)

## Custom Fields

| Field | Field ID | Value |
|-------|----------|-------|
| Upstream Affected Component | customfield_10632 | quinn-proto |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-server |
| Stream | customfield_10832 | rhtpa-2.2 |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |

## Existing Comments

1. **Description digest comment**: `sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` -- posted by sdlc-workflow/triage-security on 2026-07-01T10:00:00Z
2. **Post-triage summary comment**: Documents version impact, actions taken (Affects Versions corrected, label added, remediation tasks created, transitioned to In Progress) -- posted by sdlc-workflow/triage-security on 2026-07-01T10:01:00Z

## Existing Issue Links

| Link Type | Linked Issue | Summary | Status |
|-----------|-------------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

TC-8101 also has a Blocks link to TC-8100 (downstream is blocked by upstream).

## Version Impact Table (from prior triage, confirmed by mock lock file data)

Scoped to stream 2.2.x only:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 0.11.14 | NO | >= 0.11.14 (fixed) |

Cross-stream reference (stream 2.1.x, outside this issue's scope):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 0.11.9 | YES | < 0.11.14 |

The 2.1.x versions are outside the scope of this stream-scoped issue and would be handled by a separate CVE Jira for that stream.
