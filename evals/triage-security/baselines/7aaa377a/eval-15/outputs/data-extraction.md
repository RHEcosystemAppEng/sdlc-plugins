# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md (claude-md-security-config-prodsec.md):

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **ProdSec contact email**: prodsec-team@example.com
- **ProdSec Jira account ID**: 557058:prodsec-mock-account-id
- **Upstream Affected Component custom field**: _(not configured)_
- **PS Component custom field**: _(not configured)_
- **Stream custom field**: _(not configured)_
- **Embargo policy URL**: _(not configured -- Step 1.7 skipped)_
- **Source Repositories**: rhtpa-backend -> { url: https://github.com/rhtpa/rhtpa-backend, deployment_context: upstream } (Deployment Context column absent -- defaulting all repos to `upstream`)

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md Last-Updated timestamp is `2026-06-28T10:00:00Z` (30 days ago from 2026-07-28). This is within the 14-day threshold relative to when the mock data was created. Proceeding without staleness warning.

## Step 0.7 -- Assign and Transition to Assigned

**Proposed actions:**

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-8001 to the current user via `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`
3. Discover the "Assigned" transition via `jira.get_transitions(TC-8001)` -- select the transition whose target status name is "Assigned"
4. Transition TC-8001 to Assigned status (issue is currently in New status, so transition proceeds)

## Step 1 -- Data Extraction

**Issue**: TC-8001
**Reporter**: psirt-analyst (account ID: 557058:psirt-analyst-mock-id)

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | _(none)_ |

### Stream scope resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream.

### Ecosystem detection

The vulnerable library is `quinn-proto`, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem.

Cargo is a **source dependency** ecosystem per the classification table. Remediation will produce **two tasks** per affected stream: upstream backport + downstream propagation.

### Deployment context lookup

The affected repository (`rhtpa-backend`, identified from the component label `pscomponent:org/rhtpa-server`) is found in the Source Repositories table. The Deployment Context column is absent from the Source Repositories table, so the deployment context defaults to `upstream`.
