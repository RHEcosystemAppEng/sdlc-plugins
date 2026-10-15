# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Version Streams**: 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z)
- **Source Repositories**: rhtpa-backend (no Deployment Context column -- defaults to upstream)

# Step 0.3 -- Matrix Staleness Check

The security-matrix.md has `Last-Updated: 2026-06-28T10:00:00Z`. The matrix is within the 14-day threshold. Proceeding without staleness warning.

# Step 0.8 -- Assign and Transition to Assigned

**Proposed actions** (not executed -- eval prohibits external calls):

1. Retrieve the current user's Jira account ID via `jira.user_info()`
2. Assign TC-8040 to the current user via `jira.edit_issue(TC-8040, assignee=<current-user-account-id>)`
3. Discover the "Assigned" transition via `jira.get_transitions(TC-8040)`
4. Transition TC-8040 from New to Assigned via `jira.transition_issue(TC-8040, <assigned-transition-id>)`

The issue is currently in New status, so the transition to Assigned would proceed.

# Step 1 -- Data Extraction

## Parsed CVE Data

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
| Existing comments | None |
| Reporter | _(from Jira issue reporter field)_ |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream.

## Ecosystem Detection

**Assumed ecosystem**: Go modules

The eval scenario specifies that ecosystem detection resolves to **Go modules** for this issue. Checking the Ecosystem Mappings tables in the loaded security-matrix.md:

- **Stream 2.1.x Ecosystem Mappings**: Cargo, RPM
- **Stream 2.2.x Ecosystem Mappings**: Cargo, RPM

**Go modules** is NOT listed in any stream's Ecosystem Mappings table. The supported ecosystems configured in the security matrix are limited to Cargo and RPM.

This triggers the unsupported ecosystem handling defined in Step 5.3 of the skill methodology. See `outputs/unsupported-ecosystem.md` for the notification.
