# Step 0.7 — Early Assignment

Before data extraction, the following early assignment actions are performed:

1. **Assign issue TC-8020 to current user** — `jira.edit_issue(TC-8020, assignee=<current-user-account-id>)`
2. **Transition to Assigned** — Discover the "Assigned" transition via `jira.get_transitions(TC-8020)`, then execute `jira.transition_issue(TC-8020, <assigned-transition-id>)`. If the issue is already in Assigned or later status, skip the transition silently.

# Step 1 — Data Extraction

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] → stream 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo |
| Upstream Affected Component | quinn-proto (from customfield_10632) |

### Stream scope resolution

Issue summary contains `[rhtpa-2.2]` → mapped to stream **2.2.x** in Version Streams table. Triage is scoped to the 2.2.x stream.

### Ecosystem detection

Library `quinn-proto` is a Rust crate → Ecosystem: **Cargo** (from Ecosystem Mappings table in security-matrix.md). Cargo is a source dependency ecosystem → remediation produces 2 tasks per stream (upstream backport + downstream propagation).
