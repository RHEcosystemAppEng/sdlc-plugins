# Step 0.7 -- Early Assignment

Before extracting CVE data, assign the issue and transition to Assigned status.

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info() -> { accountId: "557058:current-user-id" }
   ```

2. **Assign TC-8006 to the current user:**
   ```
   jira.edit_issue("TC-8006", assignee="557058:current-user-id")
   ```

3. **Discover the target transition dynamically:**
   ```
   jira.get_transitions("TC-8006")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8006", <assigned-transition-id>)
   ```

TC-8006 is now assigned to the current user and in Assigned status.

---

# Step 1 -- Data Extraction

**Issue:** TC-8006

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.1] |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

### Stream scope resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`. Mapping to the Version Streams table:

- `[rhtpa-2.1]` maps to stream **2.1.x** (Konflux release repo: rhtpa-release.0.3.z)
- **Issue stream scope**: 2.1.x

This is a **scoped** issue -- triage Steps 3-8 are scoped to the 2.1.x stream only.

### Ecosystem detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the 2.1.x stream's security-matrix.md, the ecosystem is **Cargo**.

Cargo is a **source dependency** ecosystem per the classification table:
- Remediation tasks per stream: 2 (upstream backport + downstream propagation)

### Existing issue links

The following links already exist on TC-8006:

| Link Type | Direction | Linked Issue |
|-----------|-----------|--------------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) |

### Deployment context lookup

The affected repository (rhtpa-backend, identified from component label pscomponent:org/rhtpa-server) is looked up in the Source Repositories table. The Source Repositories table does not have a Deployment Context column, so the deployment context defaults to `upstream`.
