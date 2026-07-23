# Step 0.7 -- Assign and Transition to Assigned

## Early Assignment Actions

1. **Retrieve current user's Jira account ID:**

   ```
   jira.user_info()
   ```

   Result: current user account ID retrieved (e.g., `5f1234abc567de0012345678`)

2. **Assign TC-8001 to the current user:**

   ```
   jira.edit_issue("TC-8001", assignee="<current-user-account-id>")
   ```

   TC-8001 was previously Unassigned. Assigning to the current user provides
   immediate visibility into who is actively triaging this issue.

3. **Discover the target transition dynamically:**

   ```
   jira.get_transitions("TC-8001")
   ```

   Select the transition whose target status name is `"Assigned"`. The transition
   ID is discovered dynamically -- not hardcoded -- because Vulnerability issues
   use a different Jira workflow than Task issues.

4. **Transition to Assigned:**

   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

   TC-8001 is currently in `New` status. Transitioning to `Assigned` to indicate
   active triage is underway. This enables Step 7 (Concurrent Triage Detection) to
   reliably identify active work.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **scoped** to the 2.2.x stream. Steps 3 and 8 will only include
versions belonging to the 2.2.x stream in Affects Versions and remediation task
scope. Cross-stream impact on other streams (e.g., 2.1.x) is handled via Case B
in Step 8.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**.

From the 2.2.x stream's Ecosystem Mappings:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Deployment Context

The affected repository `rhtpa-backend` is listed in the Source Repositories table.
No Deployment Context column is present in the table, so the default deployment
context is `upstream`.
