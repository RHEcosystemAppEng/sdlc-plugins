# Step 0 -- Validate Project Configuration

## Configuration Extracted

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories (with Deployment Context)

The Source Repositories table includes a **Deployment Context** column. Each repository is parsed into a mapping of repository name to deployment context:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | **customer-shipped** |

Parsed deployment context mapping:
- `rhtpa-backend` -> `customer-shipped`

## Step 0.8 -- Assign and Transition to Assigned

**Proposed actions (not executed -- eval mode):**

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-8001 to the current user via `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`
3. Discover available transitions via `jira.get_transitions(TC-8001)` and select the transition whose target status name is "Assigned"
4. Transition TC-8001 from New to Assigned via `jira.transition_issue(TC-8001, <assigned-transition-id>)`

These actions provide immediate visibility into who is actively triaging the issue and enable Step 7 (Concurrent Triage Detection) to reliably identify active work.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-31812 |
| **Affected component** | pscomponent:org/rhtpa-server |
| **Product version (PSIRT-claimed)** | [rhtpa-2.2] |
| **Affects Versions (Jira field)** | RHTPA 2.0.0 |
| **Vulnerable library** | quinn-proto |
| **Affected version range** | < 0.11.14 |
| **Fixed version** | 0.11.14 |
| **CVSS** | 7.5 (High) |
| **Upstream fix PR** | https://github.com/quinn-rs/quinn/pull/2048 |
| **Advisory URL** | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| **CVE record URL** | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| **Due date** | 2026-07-15 |
| **Existing comments** | None |

### Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` which maps to the **2.2.x** version stream in the configured Version Streams table. Triage is scoped to this stream for Affects Versions correction and remediation task creation.

### Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**.

Cargo is a **source dependency** ecosystem, which means remediation produces **2 tasks** per affected stream: upstream backport (or dependency bump) + downstream propagation.

### Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to repository **rhtpa-backend** in the Repository Registry. Looking up the deployment context from the Source Repositories mapping extracted in Step 0:

- **Repository**: rhtpa-backend
- **Deployment Context**: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to include coordination guidance in remediation task descriptions. The `customer-shipped` context means the component is shipped to customers and requires coordination with Product Security for CVE assignment, advisory preparation, and formal disclosure.
