# Step 1 — Data Extraction

## Step 0.7 — Early Assignment

Before data extraction, perform early assignment actions:

1. **Assign TC-8001 to current user**: `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`
2. **Transition to Assigned**: Retrieve available transitions via `jira.get_transitions(TC-8001)`, select the transition whose target status is "Assigned", and execute `jira.transition_issue(TC-8001, <assigned-transition-id>)`. Since the issue is currently in "New" status, the transition proceeds.

## Extracted CVE Data

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

## Stream Scope

Issue summary contains suffix `[rhtpa-2.2]` → mapped to stream **2.2.x** from Version Streams table.

## Ecosystem Detection

Library **quinn-proto** is a Rust crate → ecosystem is **Cargo** (read from Ecosystem Mappings in security-matrix.md for stream 2.2.x).

Cargo is a source dependency ecosystem → remediation produces **2 tasks** per stream (upstream backport + downstream propagation).
