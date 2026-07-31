# Step 0.7 — Assign and Transition to Assigned

Before extracting CVE data, assign the issue and transition it to Assigned status:

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```
   Result: current user account ID (e.g., `557058:current-user-id`)

2. **Assign the issue to the current user:**
   ```
   jira.edit_issue("TC-8050", assignee="557058:current-user-id")
   ```

3. **Discover the target transition dynamically:**
   ```
   jira.get_transitions("TC-8050")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8050", <assigned-transition-id>)
   ```

---

# Step 1 — Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99001 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | **2.2.x** (scoped — matches Version Streams table) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | criterion |
| Affected version range | versions before 0.5.2 (< 0.5.2) |
| Fixed version | 0.5.2 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | _(none in remote links)_ |
| Advisory URL | _(none)_ |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99001 |
| Due date | 2026-08-01 |
| Existing comments | _(none)_ |
| Reporter | _(from Jira issue reporter field)_ |

### Ecosystem Detection

The vulnerable library is **criterion**, a Rust crate. Based on the component context (pscomponent:org/rhtpa-server, a Rust backend service) and the library name, the ecosystem is **Cargo**.

Cargo is listed in the 2.2.x stream's Ecosystem Mappings table:
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Cargo is a **source dependency** ecosystem per the classification table, which means remediation produces **two tasks** per stream (upstream backport + downstream propagation).

### Deployment Context Lookup

The Source Repositories table does not have a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. No Coordination Guidance subsection will be included in remediation task descriptions.

### Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to this stream only.
