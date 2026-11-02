# Step 0.7 — Early Assignment

Before data extraction, the following actions are performed:

1. **Assign CVE issue TC-8001** to the current user via `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`
2. **Transition to Assigned** — retrieve available transitions via `jira.get_transitions(TC-8001)`, select the transition whose target status is "Assigned", and execute `jira.transition_issue(TC-8001, <assigned-transition-id>)`. Since TC-8001 is currently in "New" status, the transition proceeds.

# Step 1 — Data Extraction

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] → scoped to 2.2.x stream |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| Ecosystem | Cargo (Rust crate — identified from library name quinn-proto and Ecosystem Mappings table) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| CVSS | 7.5 (High) |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Existing comments | None |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` → maps to the **2.2.x** stream in Version Streams configuration. Triage is scoped to this stream. Other streams (2.1.x) will be checked in Step 8 Case A for cross-stream impact.

## Configuration Extracted (Step 0)

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Jira version prefix: RHTPA
- Vulnerability issue type ID: 10024
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- **ProdSec contact email**: prodsec-team@example.com
- **ProdSec Jira account ID**: 557058:prodsec-mock-account-id
- Product pages URL: https://access.example.com/product-life-cycle/rhtpa
