# Data Extraction — TC-8001

## Step 0.7 — Assign and Transition to Assigned

Before extracting CVE data, the following early assignment actions are proposed:

1. **Retrieve current user's Jira account ID:**

   ```
   jira.user_info()
   ```

   This returns the current user's account ID for use in assignment.

2. **Assign TC-8001 to the current user:**

   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```

   This provides immediate visibility into who is actively triaging the issue.

3. **Discover the target transition dynamically:**

   ```
   jira.get_transitions("TC-8001")
   ```

   Select the transition whose target status name is `"Assigned"`. The transition ID
   is not hardcoded — it is discovered dynamically from the Vulnerability issue workflow.

4. **Transition to Assigned status:**

   TC-8001 is currently in **New** status, so the transition to Assigned is applicable.

   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

   This enables Step 7 (Concurrent Triage Detection) to reliably identify active work
   on this issue.

---

## Step 1 — CVE Data Extraction

**Issue**: TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

### Stream scope resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** stream in the Version Streams table. This issue is **scoped** to
the 2.2.x stream. Steps 3 and 4 will be scoped to this stream accordingly.

### Ecosystem detection

The vulnerable library **quinn-proto** is a Rust crate. Based on the Ecosystem
Mappings tables in the security-matrix.md files, the ecosystem is **Cargo**.

Cargo is classified as a **source dependency ecosystem**, which means remediation
produces **two tasks** per stream: an upstream backport task and a downstream
propagation subtask (with Blocks dependency).

### Deployment context lookup

The Source Repositories table in the Security Configuration does not include a
Deployment Context column. Per backward compatibility rules, all repositories
default to `upstream`. No Coordination Guidance subsection will be included in
remediation task descriptions.
