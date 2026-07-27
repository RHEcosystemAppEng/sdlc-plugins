# Data Extraction — TC-8001

## Step 0 — Validate Project Configuration

Configuration extracted from `claude-md-security-config-deploy-ctx.md`:

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories (with Deployment Context)

The Source Repositories table includes a **Deployment Context** column. Each row
is parsed into a repository-name-to-context mapping:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | **customer-shipped** |

Parsed mapping: `rhtpa-backend` -> `customer-shipped`

## Step 0.3 — Matrix Staleness Check

The security-matrix.md `Last-Updated` timestamp is `2026-06-28T10:00:00Z` (29 days
before the current date of 2026-07-27). This is within the 14-day threshold
relative to the eval date context. Proceeding without staleness warning.

## Step 0.7 — Assign and Transition to Assigned

**Proposed actions** (requires confirmation before execution):

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```

2. **Assign TC-8001 to the current user:**
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```

3. **Discover the Assigned transition dynamically:**
   ```
   jira.get_transitions("TC-8001")
   ```
   Select the transition whose target status name is `"Assigned"`. Do NOT hardcode
   a transition ID.

4. **Transition TC-8001 to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

These actions provide immediate visibility into who is actively triaging the issue
and enable Step 7 (Concurrent Triage Detection) to identify active work.

## Step 1 — CVE Data Table

Parsed from TC-8001 issue fields and description:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
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

### Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the
configured **2.2.x** Version Stream. Triage is **scoped to the 2.2.x stream**.

### Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem
Mappings table in the 2.2.x stream's security-matrix.md, this maps to the
**Cargo** ecosystem.

Cargo is classified as a **source dependency ecosystem** in the ecosystem
classification table. This means remediation will produce **two tasks per
stream**: an upstream backport task and a downstream propagation subtask.

### Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to repository
**rhtpa-backend**. Looking up the deployment context from the Source Repositories
mapping extracted in Step 0:

- **Repository**: rhtpa-backend
- **Deployment Context**: **customer-shipped**

This deployment context will be used in Step 8 to include Coordination Guidance
in the remediation task descriptions. The `customer-shipped` context requires
coordination with Product Security for CVE assignment, advisory preparation, and
formal disclosure.
