# Step 0.7 -- Assign and Transition to Assigned

## Early Assignment Actions

1. **Retrieve the current user's Jira account ID:**

   ```
   jira.user_info()
   ```

   Result: current user account ID retrieved (e.g., `5f1234567890abcdef012345`).

2. **Assign TC-8001 to the current user:**

   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```

   TC-8001 was previously Unassigned. Now assigned to the current user to provide immediate visibility into who is actively triaging this issue.

3. **Discover the target transition dynamically:**

   ```
   jira.get_transitions("TC-8001")
   ```

   Select the transition whose target status name is `"Assigned"`. The transition ID is discovered dynamically -- not hardcoded -- because Vulnerability issues use a different Jira workflow than Task issues.

4. **Transition to Assigned:**

   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

   TC-8001 is currently in **New** status. Transitioning to **Assigned** status. This enables Step 7 (Concurrent Triage Detection) to reliably identify active work on this issue.

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
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate) |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will apply only to versions within the 2.2.x stream. However, the full version impact analysis (Step 2) checks all streams to detect cross-stream impact.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings tables in the security matrix confirm that **Cargo** is a configured ecosystem for both the 2.1.x and 2.2.x streams, with:

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branches: `release/0.3.z` (2.1.x stream), `release/0.4.z` (2.2.x stream)

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories. The Deployment Context column is absent from the configuration (backward compatibility), so the default deployment context is `upstream`.
