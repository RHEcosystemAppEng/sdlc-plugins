# Step 1 -- Data Extraction for TC-8001

## Parsed CVE Data Table

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary text |
| Affected component | pscomponent:org/rhtpa-server | Label matching pattern `pscomponent:` |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 | Description text |
| Fixed version | 0.11.14 | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GHSA) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (cve.org) |
| Due date | 2026-07-15 | Issue `duedate` field |
| CVSS | 7.5 (High) | Description text |
| Assignee | engineer-a@example.com | Issue `assignee` field |
| Status | In Progress | Issue `status` field |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for stream 2.2.x)
- Issue stream scope: **2.2.x only** (scoped issue)

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Classification: Source dependency -- produces 2 remediation tasks per stream (upstream backport + downstream propagation)

## Custom Fields

- Upstream Affected Component (customfield_10632): quinn-proto
- PS Component (customfield_10669): pscomponent:org/rhtpa-server
- Stream (customfield_10832): rhtpa-2.2

## Existing Comments (from prior triage run)

1. Description digest comment: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (posted 2026-07-01T10:00:00Z)
2. Post-triage summary comment documenting version impact, actions taken, and remediation tasks TC-8100/TC-8101 (posted 2026-07-01T10:01:00Z)

## Existing Issue Links (from prior triage run)

- Depend: TC-8100 (upstream backport task, status: In Progress)
- Depend: TC-8101 (downstream propagation task, status: Open, blocked by TC-8100)
