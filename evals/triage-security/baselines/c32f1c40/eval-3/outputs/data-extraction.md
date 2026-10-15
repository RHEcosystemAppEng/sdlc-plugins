# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Deployment Context column**: absent -- defaulting all repositories to `upstream`
- **ProdSec contact**: not configured -- skipping @mentions silently
- **Embargo policy URL**: not configured -- skipping Step 1.7

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Deployment Context |
|------------|-----|-------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default) |

---

# Step 0.8 -- Assign and Transition to Assigned

**Proposed actions** (not executed -- eval prohibits external tool calls):

1. **Assign TC-8003 to the current user**: Retrieve current user's Jira account ID via `jira.user_info()`, then assign:
   ```
   jira.edit_issue("TC-8003", assignee=<current-user-account-id>)
   ```

2. **Discover the target transition dynamically**:
   ```
   jira.get_transitions("TC-8003")
   ```
   Select the transition whose target status name is "Assigned".

3. **Transition to Assigned**: The issue is currently in New status, so the transition would be executed:
   ```
   jira.transition_issue("TC-8003", <assigned-transition-id>)
   ```

These actions provide immediate visibility into who is actively triaging the issue and enable Step 7 (Concurrent Triage Detection) to identify active work.

---

# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | (not available from remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

### Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream only.

### Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**.

Cargo is a source dependency ecosystem, which means remediation would normally produce two tasks per stream: upstream backport + downstream propagation (or dependency bump + downstream propagation if the fix is already available upstream).

However, since this issue will be identified as a duplicate in Step 4, remediation task creation will not be reached.
