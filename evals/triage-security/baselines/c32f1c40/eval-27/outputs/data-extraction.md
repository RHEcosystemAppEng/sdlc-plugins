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
- **Source Repositories**: rhtpa-backend (https://github.com/rhtpa/rhtpa-backend)
- **Deployment Context column**: absent -- defaulting all repositories to `upstream`

## Step 0.8 -- Assign and Transition to Assigned

**Proposed actions** (not executed -- eval prohibits Jira calls):

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-8051 to the current user via `jira.edit_issue(TC-8051, assignee=<current-user-account-id>)`
3. Discover available transitions via `jira.get_transitions(TC-8051)` and select the transition whose target status is "Assigned"
4. Transition TC-8051 from New to Assigned via `jira.transition_issue(TC-8051, <assigned-transition-id>)`

These actions provide visibility into who is actively triaging the issue and enable Step 7 (Concurrent Triage Detection).

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99002 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Affected version range | < 0.23.5 |
| Fixed version | 0.23.5 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 |
| Due date | 2026-08-01 |
| Existing comments | None |

### Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`. Mapped to configured Version Stream **2.2.x** (Konflux release repo: rhtpa-release.0.4.z). Triage is scoped to the 2.2.x stream only.

### Ecosystem Detection

The vulnerable library `rustls` is a Rust crate. Matching against the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**.

Cargo is a source dependency ecosystem. Per the ecosystem classification table, source dependency ecosystems produce **2 tasks** per stream: upstream backport (or dependency bump) + downstream propagation.

### Deployment Context Lookup

The affected repository (rhtpa-backend, identified from component label `pscomponent:org/rhtpa-server`) is found in the Source Repositories table. The Deployment Context column is absent from the table, so the default deployment context is **upstream**.
