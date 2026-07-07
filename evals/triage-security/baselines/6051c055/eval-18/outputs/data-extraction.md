# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`), summary text |
| Affected component | pscomponent:org/rhtpa-server | Labels (`pscomponent:org/rhtpa-server`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote links (https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | GHSA-2026-qp73-x4mq | Remote links (https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | CVE-2026-31812 | Remote links (https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 | Jira `duedate` field |
| Assignee | engineer-a@example.com | Jira `assignee` field |
| Current status | In Progress | Jira `status` field |
| Existing comments | 2 (description digest + post-triage summary) | Jira comments |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue is **scoped** to stream 2.2.x only

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

## Existing Issue Links

| Link Type | Target | Summary | Status |
|-----------|--------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

## Existing Comments

| # | Type | Content (truncated) | Author | Created |
|---|------|---------------------|--------|---------|
| 1 | Description digest | sha256-md:a1b2c3d4e5f6... | sdlc-workflow/triage-security | 2026-07-01T10:00:00Z |
| 2 | Post-triage summary | Triage complete for CVE-2026-31812... | sdlc-workflow/triage-security | 2026-07-01T10:01:00Z |

## Existing Labels

- `CVE-2026-31812` -- CVE identifier
- `pscomponent:org/rhtpa-server` -- component label
- `ai-cve-triaged` -- triage completion marker
