# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Version Streams**: 2.1.x, 2.2.x
- **Source Repositories**: rhtpa-backend (default deployment context: upstream -- no Deployment Context column present)

## Step 0.3 -- Matrix Staleness Check

Security matrix Last-Updated timestamp: 2026-06-28T10:00:00Z (11 days ago). Within the 14-day threshold. Proceeding without warning.

## Step 0.7 -- Assign and Transition to Assigned

**Proposed actions** (not executed -- eval mode):

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-8040 to the current user via `jira.edit_issue(TC-8040, assignee=<current-user-account-id>)`
3. Discover transitions via `jira.get_transitions(TC-8040)` and select the transition targeting "Assigned" status
4. Transition TC-8040 from New to Assigned via `jira.transition_issue(TC-8040, <assigned-transition-id>)`

## Step 1 -- Data Extraction

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (stream 2.2.x) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | quinn-rs/quinn#2048 |
| Advisory URL | GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| CVSS | 7.5 (High) |
| Stream scope | Scoped to 2.2.x stream |

### Ecosystem Detection

Per the eval instructions, the ecosystem detection in Step 1 resolves to **Go modules**. Checking the Ecosystem Mappings table in the security-matrix.md for stream 2.2.x:

Configured ecosystems:
- Cargo
- RPM

**Go modules** is NOT listed in the Ecosystem Mappings table.
