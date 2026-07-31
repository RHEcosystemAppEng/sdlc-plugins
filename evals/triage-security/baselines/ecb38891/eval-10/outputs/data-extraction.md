# Step 0.7 — Assign and Transition to Assigned

Before extracting CVE data, assign the issue and transition its status:

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```
   Result: current user account ID (e.g., `557058:current-user-id`)

2. **Assign TC-8020 to current user:**
   ```
   jira.edit_issue("TC-8020", assignee=<current-user-account-id>)
   ```
   Proposed action: Assign TC-8020 to the current user.

3. **Discover transitions:**
   ```
   jira.get_transitions("TC-8020")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8020", <assigned-transition-id>)
   ```
   Proposed action: Transition TC-8020 from New to Assigned.

---

# Step 1 — Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | < 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Issue links | None |
| Reporter | (from Jira issue reporter field) |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`. Mapping to configured Version Streams:

- `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)

The issue is **scoped** to stream 2.2.x. Steps 3-4 apply to this stream scope.

## Ecosystem Detection

The vulnerable library is **tokio**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**.

Cargo is classified as a **source dependency** ecosystem per the ecosystem classification table. This means remediation produces **2 tasks per stream**: upstream backport + downstream propagation (with the downstream subtask blocked by the upstream task).

## Deployment Context Lookup

The affected repository identified from the component label `pscomponent:org/rhtpa-server` is **rhtpa-backend**. The Source Repositories table in the CLAUDE.md does not include a Deployment Context column. Per backward compatibility, the deployment context defaults to **upstream**. No Coordination Guidance subsection will be included in remediation task descriptions.
