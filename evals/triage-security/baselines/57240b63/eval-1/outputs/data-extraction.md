# Step 0.7 -- Assign and Transition to Assigned

## PROPOSAL: Assign TC-8001 to current user

1. **Retrieve current user's Jira account ID:**

   ```
   jira.user_info()
   ```

   Result: (current user account ID retrieved)

2. **Assign TC-8001 to the current user:**

   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```

   Rationale: TC-8001 is currently Unassigned. Assigning immediately provides
   visibility into who is actively triaging and enables Step 7 (Concurrent
   Triage Detection) to reliably identify active work.

3. **Discover the target transition dynamically:**

   ```
   jira.get_transitions("TC-8001")
   ```

   Select the transition whose target status name is "Assigned". Do not
   hardcode a transition ID -- Vulnerability issues use a different Jira
   workflow than Task issues.

4. **Transition TC-8001 from New to Assigned:**

   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

   The issue is currently in New status, so the transition proceeds.

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
| Existing comments | (none) |
| Ecosystem | Cargo (Rust crate) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
configured Version Stream **2.2.x** (Konflux release repo: rhtpa-release.0.4.z).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 8 will apply only to
versions within the 2.2.x stream. However, all streams are still analyzed in
Step 2 for cross-stream impact detection (Case B).

## Ecosystem Detection

quinn-proto is a Rust crate, matching the **Cargo** ecosystem in the Ecosystem
Mappings tables. Lock file: `Cargo.lock`. Check command:
`git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`.

## Deployment Context

The affected repository (rhtpa-backend) is listed in Source Repositories without
a Deployment Context column. Default deployment context: **upstream**.
