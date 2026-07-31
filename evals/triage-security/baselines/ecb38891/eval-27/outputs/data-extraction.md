# Step 0.7 -- Early Assignment

Before extracting CVE data, assign the issue and transition to Assigned status:

1. **Retrieve current user's Jira account ID:** `jira.user_info()` to get the current user.
2. **Assign TC-8051 to current user:** `jira.edit_issue(TC-8051, assignee=<current-user-account-id>)`
3. **Discover Assigned transition:** `jira.get_transitions(TC-8051)` -- select the transition whose target status name is "Assigned".
4. **Transition to Assigned:** `jira.transition_issue(TC-8051, <assigned-transition-id>)` -- the issue is currently in New status, so the transition proceeds.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99002 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Affected version range | < 0.23.5 |
| Fixed version | 0.23.5 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 |
| Advisory URL | -- |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `rustls` is a Rust crate. Checking the 2.2.x stream's Ecosystem Mappings table, the **Cargo** ecosystem is configured with:

- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Ecosystem classification: **Cargo** is a **source dependency** ecosystem, which normally produces 2 remediation tasks per stream (upstream backport + downstream propagation).

## Deployment Context Lookup

The affected repository is identified from the component label `pscomponent:org/rhtpa-server` as `rhtpa-backend`. Looking up the Source Repositories table in the CLAUDE.md, `rhtpa-backend` is present but the table has no Deployment Context column. Per Step 0, all repositories default to `upstream`.
