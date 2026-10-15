# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md (claude-md-security-config-embargo.md):

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Embargo policy URL**: https://example.com/security/embargo-policy (optional field -- extracted without error)
- **Upstream Affected Component custom field**: not configured (Step 4.3 and Step 7 will be skipped)
- **PS Component custom field**: not configured
- **Stream custom field**: not configured
- **ProdSec contact email**: not configured
- **ProdSec Jira account ID**: not configured
- **Version Streams**:
  - 2.1.x: git.example.com/rhtpa/rhtpa-release.0.3.z (local: /home/dev/repos/rhtpa-release.0.3.z)
  - 2.2.x: git.example.com/rhtpa/rhtpa-release.0.4.z (local: /home/dev/repos/rhtpa-release.0.4.z)
- **Source Repositories**:
  - rhtpa-backend: https://github.com/rhtpa/rhtpa-backend (local: /home/dev/repos/rhtpa-backend)
  - Deployment Context column: absent -- defaulting all repositories to `upstream`

## Step 0.8 -- Assign and Transition to Assigned

**Proposed actions** (not executed -- eval prohibits Jira calls):

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-8001 to the current user via `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`
3. Discover the "Assigned" transition via `jira.get_transitions(TC-8001)` and select the transition whose target status name is "Assigned"
4. Transition TC-8001 from New to Assigned via `jira.transition_issue(TC-8001, <assigned-transition-id>)`

The issue is currently in New status, so the transition to Assigned will proceed.

---

# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] (from summary suffix) |
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

The issue summary contains stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** stream in the Version Streams table. Triage Steps 3-8 are scoped to this stream.

### Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem.

Cargo is a source dependency ecosystem. Per the ecosystem classification table, remediation produces **2 tasks per stream**: upstream backport + downstream propagation.

### Deployment Context Lookup

The affected repository is rhtpa-backend (identified from pscomponent:org/rhtpa-server). The Source Repositories table does not have a Deployment Context column, so deployment context defaults to `upstream`. Coordination Guidance will be omitted from remediation task descriptions.
