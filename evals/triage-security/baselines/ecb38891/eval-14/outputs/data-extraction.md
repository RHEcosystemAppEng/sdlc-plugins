# Step 0.7 -- Early Assignment

Before extracting CVE data, assign the issue and transition to Assigned status:

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```

2. **Assign TC-8005 to the current user:**
   ```
   jira.edit_issue("TC-8005", assignee=<current-user-account-id>)
   ```

3. **Discover the Assigned transition:**
   ```
   jira.get_transitions("TC-8005")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8005", <assigned-transition-id>)
   ```

# Step 1 -- Data Extraction

**Issue**: TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | < 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| Upstream fix PR | (none) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| CVSS | 7.1 (High) |
| Existing comments | (none) |

### Stream scope resolution

The issue summary contains stream suffix `[rhtpa-2.2]`. Mapping to configured Version Streams:
- `[rhtpa-2.2]` matches stream **2.2.x** (Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- **Issue stream scope**: 2.2.x only

### Ecosystem detection

The vulnerable library is **openssl-libs**, which is a system RPM package (not a Cargo crate or npm package). Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the **RPM** ecosystem is configured with:
- Lock File: `rpms.lock.yaml`
- Check Command: `git show <tag>:rpms.lock.yaml`
- Upstream Branch: (none)

**Ecosystem**: RPM (system package category)

Per the ecosystem classification table:
- System package ecosystems (RPM) produce **1 remediation task** per stream (Konflux release repo fix only -- no upstream backport needed).

### Deployment context lookup

The affected component `pscomponent:org/rhtpa-server` maps to repository `rhtpa-backend`. Looking up in Source Repositories table: the Deployment Context column is **absent** from the Source Repositories table (backward compatibility). All repositories default to `upstream`.
