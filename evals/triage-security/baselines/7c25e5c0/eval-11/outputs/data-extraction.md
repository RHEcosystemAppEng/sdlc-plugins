# Step 0.7 — Early Assignment

Before data extraction, assign TC-8021 to the current user and transition to Assigned status:

1. **Retrieve current user**: `jira.user_info()` → current user account ID
2. **Assign issue**: `jira.edit_issue(TC-8021, assignee=<current-user-account-id>)`
3. **Discover transition**: `jira.get_transitions(TC-8021)` → select transition targeting "Assigned" status
4. **Transition**: `jira.transition_issue(TC-8021, <assigned-transition-id>)` — issue is currently New, so transition proceeds

# Step 1 — Data Extraction

**Issue**: TC-8021
**Summary**: CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1]

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | < 1.42.0 |
| Fixed version | 1.42.0 |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| CVSS | 8.1 (High) |
| Existing comments | (none) |
| Existing issue links | (none) |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.1]`, which maps to the `2.1.x` version stream in the Version Streams configuration. Triage is scoped to the 2.1.x stream only.

## Ecosystem Detection

The vulnerable library is `tokio`, a Rust crate. Based on the Ecosystem Mappings table in the 2.1.x stream's security-matrix.md, the ecosystem is **Cargo**. Cargo is a source dependency ecosystem, which normally produces two remediation tasks (upstream backport + downstream propagation).

## Custom Fields

- **Upstream Affected Component** (customfield_10632): tokio
- **PS Component** (customfield_10669): pscomponent:org/rhtpa-server
- **Stream** (customfield_10832): rhtpa-2.1
