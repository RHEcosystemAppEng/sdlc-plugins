# Step 0.7 — Early Assignment

Before extracting CVE data, assign the issue and transition to Assigned status:

1. **Retrieve current user's Jira account ID**: `jira.user_info()` -> current user account ID
2. **Assign TC-8060 to current user**: `jira.edit_issue(TC-8060, assignee=<current-user-account-id>)`
3. **Discover target transition**: `jira.get_transitions(TC-8060)` -> select transition whose target status is "Assigned"
4. **Transition to Assigned**: `jira.transition_issue(TC-8060, <assigned-transition-id>)` (issue is currently in New status)

---

# Step 1 — Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99010 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | < 0.4.5 |
| Fixed version | 0.4.5 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | -- |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 |
| Due date | 2026-08-15 |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** stream in the Version Streams table (Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z). Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem (source dependency category). This means remediation will produce **two tasks** per stream: an upstream backport task and a downstream propagation subtask.

## Deployment Context Lookup

The Source Repositories table does not include a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. No Coordination Guidance subsection will be added to remediation task descriptions.
