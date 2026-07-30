# Step 0.7 -- Assign and Transition to Assigned

Before extracting CVE data, assign the issue and transition it to Assigned status:

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
   Select the transition whose target status name is `"Assigned"`.

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8005", <assigned-transition-id>)
   ```

---

# Step 1 -- Data Extraction

**Issue**: TC-8005
**Stream Scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| Upstream fix PR | _(none -- RPM system package)_ |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | _(none)_ |
| CVSS | 7.1 (High) |

## Ecosystem Detection

**Ecosystem: RPM** (not Cargo)

openssl-libs is a system-level RPM package, not a source dependency (Cargo/npm/Go). The ecosystem is determined by the package type: openssl-libs is an RPM distributed via Red Hat repositories, present in `rpms.lock.yaml`. The Ecosystem Mappings table in the 2.2.x stream's security-matrix.md confirms the RPM ecosystem with lock file `rpms.lock.yaml` and check command `git show <tag>:rpms.lock.yaml | grep '<library>'`.

Per the ecosystem classification table, RPM is a **system package** ecosystem. Remediation produces **1 task per stream** (Konflux release repo fix only), not the 2-task upstream backport + downstream propagation flow used for source dependency ecosystems.

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to the **2.2.x** stream in the Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Triage is scoped to the 2.2.x stream only. Versions from other streams (e.g., 2.1.x) are not included in Affects Versions correction or remediation for this issue.
