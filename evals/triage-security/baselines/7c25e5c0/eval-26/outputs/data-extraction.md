# Step 0.7 — Early Assignment

Before data extraction, the following early assignment actions are performed:

1. **Assign TC-8050** to the current user via `jira.edit_issue(TC-8050, assignee=<current-user-account-id>)`
2. **Transition TC-8050 to Assigned** — discover the "Assigned" transition via `jira.get_transitions(TC-8050)`, then execute `jira.transition_issue(TC-8050, <assigned-transition-id>)`. The issue is currently in New status, so the transition proceeds.

# Step 1 — Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99001 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] → scoped to 2.2.x stream |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | criterion |
| Affected version range | versions before 0.5.2 (< 0.5.2) |
| Fixed version | 0.5.2 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | _(none in remote links)_ |
| Advisory URL | _(none)_ |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 |
| Due date | 2026-08-01 |
| Existing comments | _(no comments)_ |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in Security Configuration. Triage is scoped to this stream only.

## Ecosystem Detection

The vulnerable library **criterion** is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**.

Cargo is a **source dependency** ecosystem → remediation produces 2 tasks per stream (upstream backport + downstream propagation).
