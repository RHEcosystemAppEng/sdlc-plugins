# Step 0.7 -- Assign and Transition to Assigned

Before extracting CVE data, perform early assignment to provide visibility into
active triage and enable Step 7 (Concurrent Triage Detection).

**Proposed actions:**

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```

2. **Assign TC-8005 to the current user:**
   ```
   jira.edit_issue("TC-8005", assignee=<current-user-account-id>)
   ```

3. **Discover the target transition dynamically:**
   ```
   jira.get_transitions("TC-8005")
   ```
   Select the transition whose target status name is "Assigned". Do NOT hardcode
   a transition ID -- Vulnerability issues use a different Jira workflow.

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8005", <assigned-transition-id>)
   ```

These actions are proposed for engineer confirmation before execution.

---

# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (mapped from suffix [rhtpa-2.2] to Version Streams table) |
| Affects Versions (current) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | (none) |
| Issue status | New |
| Assignee | Unassigned |

### Ecosystem Detection

The vulnerable library **openssl-libs** is a system-level RPM package, not a
source dependency. The Ecosystem Mappings table in the 2.2.x stream's
security-matrix.md lists RPM as a configured ecosystem with lock file
`rpms.lock.yaml` and check command `git show <tag>:rpms.lock.yaml`.

**Detected ecosystem: RPM** (system package)

Per the ecosystem classification table:

| Category | Ecosystems | Remediation tasks per stream |
|---|---|---|
| Source dependency | Cargo, npm | 2 -- upstream backport + downstream propagation |
| System package | RPM | 1 -- Konflux release repo fix only |

RPM is a system package ecosystem, so remediation will produce **one task**
per affected stream (Konflux release repo fix only -- no upstream backport step).

### Stream Scope

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** stream in the Version Streams table. Triage is scoped to this stream
only. The 2.2.x stream uses the Konflux release repo at
`git.example.com/rhtpa/rhtpa-release.0.4.z`.

### Deployment Context

The Source Repositories table does not include a Deployment Context column.
Per backward compatibility rules, all repositories default to `upstream`.
