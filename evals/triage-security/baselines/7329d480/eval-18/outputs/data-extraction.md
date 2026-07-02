# Step 1 -- Data Extraction: TC-8001

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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Assignee | engineer-a@example.com |
| Issue status | In Progress |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Scope: **Single stream** -- only the 2.2.x stream is in scope for this issue

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
- Source repository: rhtpa-backend

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: upstream (default -- no explicit Deployment Context column in Source Repositories)

## Existing Comments

1. **Description digest comment**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (posted 2026-07-01T10:00:00Z by sdlc-workflow/triage-security)
2. **Post-triage summary comment**: Documents triage completion for CVE-2026-31812 including version impact, Affects Versions correction, remediation tasks TC-8100 and TC-8101, and transition to In Progress (posted 2026-07-01T10:01:00Z by sdlc-workflow/triage-security)

## Existing Issue Links

- **Depend**: TC-8100 -- Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] (Status: In Progress, Labels: ai-generated-jira, Security, CVE-2026-31812)
- **Depend**: TC-8101 -- Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] (Status: Open, Labels: ai-generated-jira, Security, CVE-2026-31812, Blocks: TC-8100)

## Remote Links

- [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) -- GitHub Advisory
- [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) -- CVE Record
- [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) -- Upstream fix PR
