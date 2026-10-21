# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | pscomponent:org/rhtpa-server | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS score | 7.5 (High) | Description text |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote link: https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | GHSA-2026-qp73-x4mq | Remote link: https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | CVE-2026-31812 | Remote link: https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 | Issue `duedate` field |
| Assignee | engineer-a@example.com | Issue `assignee` field |
| Upstream Affected Component | quinn-proto | customfield_10632 |
| PS Component | pscomponent:org/rhtpa-server | customfield_10669 |
| Stream | rhtpa-2.2 | customfield_10832 |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Classification: Source dependency -- 2 remediation tasks per stream (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

## Deployment Context

- Affected repository: rhtpa-backend
- Deployment context: upstream (default -- no explicit Deployment Context column in Source Repositories table)

## Existing Issue State (relevant to re-run)

- **Status**: In Progress (not New -- issue has already been triaged)
- **Labels**: CVE-2026-31812, pscomponent:org/rhtpa-server, **ai-cve-triaged** (triage marker already present)
- **Issue links**: Two Depend links to remediation tasks (TC-8100, TC-8101) already exist
- **Comments**: Description digest comment and post-triage summary comment already exist
