# Step 1 -- Data Extraction for TC-8001

## Parsed CVE Data Table

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field (current value) |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Status | New | Jira `status` field |
| Assignee | Unassigned | Jira `assignee` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue is **scoped** to stream 2.2.x only
- Other streams (2.1.x) will be analyzed for cross-stream impact (Case A) but remediation tasks within this issue's scope are limited to 2.2.x

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Detected ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Remediation tasks per stream: 2 (dependency bump or upstream backport + downstream propagation)

## Deployment Context

- Repository: rhtpa-backend
- Deployment Context column: absent from Source Repositories table
- Result: default to `upstream`, but per remediation-templates.md, coordination guidance subsection is omitted when the column is absent entirely

## Affects Versions Mismatch (Flagged)

The current Affects Versions field contains **RHTPA 2.0.0**, but no 2.0.x version stream is configured. This is incorrect and will be corrected in Step 3 based on lock file evidence from the version impact analysis.

## Embargo Check (Step 1.7)

- CVSS: 7.5 (High) -- meets the threshold (>= 7.0) for embargo check
- Embargo policy URL: not configured in Security Configuration
- Result: Step 1.7 is **skipped** (no embargo policy URL configured)
