# Step 1 — Data Extraction

## Step 0.7 — Early Assignment (proposed actions)

Before proceeding with data extraction, the following early assignment actions are proposed:

1. **Assign TC-8001 to the current user**: The issue is currently Unassigned. Propose assigning it to the current triager via `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`.
2. **Transition TC-8001 to Assigned status**: The issue is currently in New status. Propose transitioning to Assigned via `jira.transition_issue(TC-8001, <assigned-transition-id>)` after dynamically discovering the transition ID from `jira.get_transitions(TC-8001)`.

These actions provide immediate visibility into who is triaging the issue and enable Step 7 (Concurrent Triage Detection) to reliably identify active work.

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, Summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (Component label pattern: `pscomponent:`) |
| Product version (PSIRT-claimed) | [rhtpa-2.2] → 2.2.x stream | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 | Description ("versions before 0.11.14") |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote links |
| Advisory URL | GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Version Streams configuration. Triage is scoped to this stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**.

Cargo is a source dependency ecosystem, so remediation will follow the two-task pattern: upstream backport task + downstream propagation subtask (with Blocks dependency).
