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
2. Assign TC-8051 to the current user via `jira.edit_issue(TC-8051, assignee=<current-user-account-id>)`
3. Discover transitions via `jira.get_transitions(TC-8051)` and select the transition targeting "Assigned" status
4. Transition TC-8051 from New to Assigned via `jira.transition_issue(TC-8051, <assigned-transition-id>)`

## Step 1 -- Data Extraction

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99002 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (stream 2.2.x) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Affected version range | < 0.23.5 |
| Fixed version | 0.23.5 |
| Upstream fix PR | rustls/rustls#2100 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 |
| Due date | 2026-08-01 |
| CVSS | 8.1 (High) |
| Stream scope | Scoped to 2.2.x stream |

### Ecosystem Detection

The library `rustls` is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem.

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`
