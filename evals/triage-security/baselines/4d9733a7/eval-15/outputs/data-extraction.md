# Step 1 -- Data Extraction for TC-8001

## Step 0 -- Configuration Extraction

From `claude-md-security-config-prodsec.md`:
- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Vulnerability issue type ID: 10024
- Jira version prefix: RHTPA
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- **ProdSec contact email**: prodsec-team@example.com
- **ProdSec Jira account ID**: 557058:prodsec-mock-account-id
- Source Repositories: rhtpa-backend (no Deployment Context column -- defaults to upstream)

## Step 0.7 -- Early Assignment

1. **Retrieve current user's Jira account ID**: `jira.user_info()`
2. **Assign TC-8001 to current user**: `jira.edit_issue("TC-8001", assignee=<current-user-account-id>)`
3. **Discover transitions**: `jira.get_transitions("TC-8001")` -- select transition with target status "Assigned"
4. **Transition to Assigned**: `jira.transition_issue("TC-8001", <assigned-transition-id>)` -- issue is currently in New status

## Extracted CVE Data

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
| Upstream fix PR | quinn-rs/quinn#2048 (https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | GHSA-2026-qp73-x4mq (https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| **Reporter** | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |

### Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` which maps to the **2.2.x** stream. Triage is scoped to the 2.2.x stream.

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**.
