# Step 0.7 -- Early Assignment

Before extracting CVE data, assign the issue and transition to Assigned status:

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```

2. **Assign the issue to the current user:**
   ```
   jira.edit_issue("TC-8004", assignee=<current-user-account-id>)
   ```

3. **Discover the target transition dynamically:**
   ```
   jira.get_transitions("TC-8004")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8004", <assigned-transition-id>)
   ```

These actions provide immediate visibility into who is actively triaging TC-8004
and enable Step 7 (Concurrent Triage Detection) to reliably identify active work.

---

# Step 1 -- Data Extraction

**Issue**: TC-8004
**Summary**: CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(no stream suffix -- unscoped)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | < 0.4.8 (versions before 0.4.8) |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Due date | 2026-08-01 |
| Existing comments | None |
| Reporter | _(from Jira issue reporter field)_ |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames"
contains **no stream suffix** in brackets. Therefore this issue is treated as
**unscoped** -- it covers all streams. The version impact analysis will check
ALL versions across ALL configured streams (2.1.x and 2.2.x).

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. Based on the Ecosystem Mappings
tables in both streams' security-matrix.md files, the ecosystem is **Cargo**.

Cargo is a **source dependency** ecosystem per the classification table:

| Category | Ecosystems | Remediation tasks per stream |
|----------|-----------|------------------------------|
| Source dependency | Cargo, npm | 2 -- upstream backport + downstream propagation |
| System package | RPM | 1 -- Konflux release repo fix only |

This means remediation for affected streams will produce **two tasks per stream**:
an upstream backport task and a downstream propagation subtask (blocked by the
upstream task).

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to repository
`rhtpa-backend`. The Source Repositories table in Security Configuration does not
include a Deployment Context column, so the deployment context defaults to
`upstream` for all repositories.
