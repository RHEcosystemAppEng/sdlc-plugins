# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md (claude-md-security-config-deploy-ctx.md):

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Version Streams**: 2.1.x, 2.2.x
- **Source Repositories**:

  | Repository | URL | Local Path | Deployment Context |
  |------------|-----|------------|--------------------|
  | rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | customer-shipped |

The Source Repositories table includes a **Deployment Context** column. Parsed mapping:
- `rhtpa-backend` -> `{ url: "https://github.com/rhtpa/rhtpa-backend", deployment_context: "customer-shipped" }`

## Step 0.3 -- Matrix Staleness Check

Security matrix Last-Updated timestamp: 2026-06-28T10:00:00Z
Days since last update: 11 days (within 14-day threshold).
Matrix is fresh -- proceeding without warning.

## Step 0.7 -- Early Assignment

**PROPOSED ACTIONS:**

1. **Assign TC-8001 to current user**: `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`
2. **Transition TC-8001 to Assigned**: `jira.get_transitions(TC-8001)` to discover the Assigned transition ID, then `jira.transition_issue(TC-8001, <assigned-transition-id>)`

# Step 1 -- Data Extraction

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

### Stream scope resolution

Issue summary contains stream suffix `[rhtpa-2.2]` -- mapped to stream **2.2.x** from the Version Streams table.

### Ecosystem detection

Library `quinn-proto` is a Rust crate. Ecosystem: **Cargo** (listed in the stream's Ecosystem Mappings table).

### Deployment context lookup

Affected repository identified from component label `pscomponent:org/rhtpa-server` -> repository `rhtpa-backend`.

Deployment context lookup in Source Repositories mapping:
- **rhtpa-backend** -> **customer-shipped**

Recorded `deployment_context: customer-shipped` as part of CVE metadata for use in Step 8 remediation task descriptions.
