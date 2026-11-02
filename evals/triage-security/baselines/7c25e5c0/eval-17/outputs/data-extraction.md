# Step 0.7 — Early Assignment

Before data extraction, the following actions are performed:

1. **Assign the CVE issue to the current user**: `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`
2. **Transition to Assigned status**: Discover the Assigned transition via `jira.get_transitions(TC-8001)`, then `jira.transition_issue(TC-8001, <assigned-transition-id>)`. Since TC-8001 is currently in `New` status, the transition proceeds.

# Step 1 — Data Extraction

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] → scoped to 2.2.x stream |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate — quinn-proto) |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the `2.2.x` stream in the Version Streams table. Triage is scoped to the 2.2.x stream.

## Deployment Context Lookup

The Source Repositories table does not include a Deployment Context column. All repositories default to `upstream`.
