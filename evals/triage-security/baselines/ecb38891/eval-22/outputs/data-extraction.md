# Step 0.7 -- Early Assignment

Before extracting CVE data, assign the issue and transition to Assigned status:

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info() -> account ID: 557058:current-user-mock-id
   ```

2. **Assign the issue to the current user:**
   ```
   jira.edit_issue(TC-8021, assignee=557058:current-user-mock-id)
   ```

3. **Discover the target transition dynamically:**
   ```
   jira.get_transitions(TC-8021)
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned (issue is currently in New status):**
   ```
   jira.transition_issue(TC-8021, <assigned-transition-id>)
   ```

# Step 1 -- Data Extraction

**Source**: Vulnerability issue TC-8021

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |
| CVSS | 7.5 (High) |
| Upstream Affected Component (customfield_10632) | quinn-proto |

### Stream scope resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to this stream.

### Ecosystem detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem.

Cargo is a **source dependency** ecosystem per the classification table, which means remediation produces **two tasks** per stream: upstream backport + downstream propagation.

### Deployment context lookup

The affected component `pscomponent:org/rhtpa-server` maps to the `rhtpa-backend` repository. The Source Repositories table does not include a Deployment Context column, so the deployment context defaults to `upstream`.
