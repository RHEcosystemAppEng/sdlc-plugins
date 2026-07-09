# Step 0.7 -- Early Assignment Actions

**PROPOSED ACTIONS** (not executed -- eval prohibits Jira calls):

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```

2. **Assign TC-8001 to the current user:**
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```

3. **Discover available transitions:**
   ```
   jira.get_transitions("TC-8001")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

These actions are proposed before data extraction to provide immediate visibility into who is actively triaging the issue and to enable Step 7 (Concurrent Triage Detection).

---

# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream for Steps 3-8.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in security-matrix.md, the ecosystem is **Cargo**. The lock file is `Cargo.lock` and the check command is `git show <tag>:Cargo.lock`.

## Deployment Context Lookup

The affected repository (rhtpa-backend, matched via component label pscomponent:org/rhtpa-server) is found in the Source Repositories table. The Source Repositories table does NOT have a Deployment Context column, so the deployment context defaults to `upstream`.
