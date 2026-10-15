# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **ProdSec contact email**: prodsec-team@example.com
- **ProdSec Jira account ID**: 557058:prodsec-mock-account-id
- **Version Streams**: 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z)
- **Source Repositories**: rhtpa-backend (no Deployment Context column present -- defaulting all repositories to `upstream`)

## Step 0.7 -- Early Assignment

Before proceeding to data extraction, the following actions are proposed:

1. **Assign the CVE issue TC-8001 to the current user**: The issue is currently Unassigned. Propose calling `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)` to assign it.

2. **Transition to Assigned status**: The issue is currently in `New` status. Propose discovering the Assigned transition via `jira.get_transitions(TC-8001)` and transitioning with `jira.transition_issue(TC-8001, <assigned-transition-id>)`.

These actions provide immediate visibility into who is actively triaging TC-8001 and enable Step 7 (Concurrent Triage Detection) to reliably identify active work.

> **Note**: These are proposed actions. No Jira operations were performed -- external tool invocation is prohibited in this eval.

---

# Step 1 -- Data Extraction

## Parsed CVE Data Table

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
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |

### Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream for Steps 3 and 4.

However, per Important Rule 4, all supported versions across all streams are checked in the version impact analysis (Step 2).

### Ecosystem Detection

The vulnerable library is `quinn-proto`, a Rust crate. Based on the Ecosystem Mappings table in the security matrix, this maps to the **Cargo** ecosystem.

Cargo is a source dependency ecosystem, so remediation will produce **two tasks** per affected stream: an upstream backport (or dependency bump) task and a downstream propagation subtask.

### Deployment Context Lookup

The affected repository is `rhtpa-backend` (identified from the component label `pscomponent:org/rhtpa-server`). The Source Repositories table in the CLAUDE.md does **not** have a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. No Coordination Guidance subsection will be added to remediation task descriptions.
