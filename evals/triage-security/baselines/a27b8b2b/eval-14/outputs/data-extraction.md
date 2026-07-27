# Step 0.7 -- Assign and Transition to Assigned

Before extracting CVE data, the issue is assigned to the current user and transitioned to Assigned status for triage visibility.

**Proposed actions:**

1. **Retrieve current user account ID:**
   ```
   jira.user_info()
   ```

2. **Assign TC-8005 to current user:**
   ```
   jira.edit_issue("TC-8005", assignee=<current-user-account-id>)
   ```

3. **Discover available transitions:**
   ```
   jira.get_transitions("TC-8005")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8005", <assigned-transition-id>)
   ```

---

# Step 1 -- Data Extraction

**Issue:** TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| CVSS | 7.1 (High) |
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **openssl-libs**, an RPM system package. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **RPM** (not Cargo).

RPM is classified as a **system package** ecosystem in the ecosystem classification table. This means remediation creates a **single task** (Konflux release repo fix only) -- not the two-task upstream backport + downstream propagation flow used for source dependency ecosystems like Cargo.

## Deployment Context Lookup

The affected component `pscomponent:org/rhtpa-server` maps to the `rhtpa-backend` repository. The Source Repositories table in the CLAUDE.md does not include a Deployment Context column, so the deployment context defaults to `upstream`.
