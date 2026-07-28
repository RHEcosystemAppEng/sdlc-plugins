# Step 0.7 -- Early Assignment

**Proposed actions** (require confirmation before execution):

1. **Assign TC-8020 to current user**: Retrieve current user's Jira account ID via `jira.user_info()`, then assign the issue via `jira.edit_issue(TC-8020, assignee=<current-user-account-id>)`.
2. **Transition TC-8020 to Assigned status**: Discover the target transition dynamically via `jira.get_transitions(TC-8020)`, select the transition whose target status name is "Assigned", then execute `jira.transition_issue(TC-8020, <assigned-transition-id>)`. The issue is currently in New status, so the transition applies.

These actions provide immediate visibility into who is actively triaging the issue and enable Step 7 (Concurrent Triage Detection) to reliably identify active work.

---

# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| Reporter | psirt-analyst (557058:psirt-analyst-mock-id) |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is **scoped to the 2.2.x stream**.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, which is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem.

- Ecosystem: **Cargo** (source dependency)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
- Remediation task structure: **2 tasks** per stream (upstream backport + downstream propagation)

## Deployment Context Lookup

The affected repository is `rhtpa-backend` (from the component label `pscomponent:org/rhtpa-server`). Looking up the Source Repositories table in the Security Configuration, the Deployment Context column is **absent** -- defaulting all repositories to `upstream`.
